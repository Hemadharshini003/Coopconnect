from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.quiz import Quiz, QuizQuestion, QuizAttempt, Certificate
from app.db.models.course import Course, CourseLesson, Enrollment
from app.ml.quiz_generator import QuizGenerator
from app.schemas.response import success_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/generate")
def generate_quiz(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course_id = payload["course_id"]
    lesson_id = payload.get("lesson_id")
    lesson = db.query(CourseLesson).filter(CourseLesson.id == lesson_id).first() if lesson_id else None

    title = lesson.title if lesson else "ERP & Digital Fundamentals"
    text = lesson.text_content if lesson else "Operational guidelines for inventory and ERP digital entry."

    generated = QuizGenerator.generate_quiz_from_lesson(course_id, lesson_id, title, text)

    quiz = Quiz(
        course_id=course_id,
        lesson_id=lesson_id,
        title=generated["title"],
        generated_by_ai=True,
        status="Pending Trainer Approval"
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for qd in generated["questions"]:
        qq = QuizQuestion(
            quiz_id=quiz.id,
            question_text=qd["question_text"],
            question_type=qd["question_type"],
            options_json=qd["options_json"],
            correct_answer=qd["correct_answer"],
            explanation=qd["explanation"],
            marks=qd["marks"]
        )
        db.add(qq)

    db.commit()
    return success_response(data={"quiz_id": quiz.id, "status": quiz.status}, message="AI Quiz generated and sent for Trainer review")

@router.post("/{id}/approve")
def approve_quiz(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.status = "Approved"
    db.commit()
    return success_response(data={"quiz_id": quiz.id, "status": "Approved"}, message="Quiz approved by Trainer and published")

@router.post("/{id}/attempt")
def submit_quiz_attempt(id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    member_id = payload["member_id"]
    answers = payload.get("answers", [])

    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == id).all()
    correct_count = 0
    total_questions = len(questions)

    q_map = {q.id: q for q in questions}
    for ans in answers:
        q_id = ans.get("question_id")
        user_ans = ans.get("answer", "").strip()
        if q_id in q_map:
            if user_ans == q_map[q_id].correct_answer.strip():
                correct_count += 1

    score = round((correct_count / max(1, total_questions)) * 100, 1)
    passed = score >= 60.0

    attempt = QuizAttempt(
        quiz_id=id,
        member_id=member_id,
        score=score,
        passed=passed,
        completed_at=datetime.now(timezone.utc)
    )
    db.add(attempt)

    # Issue Certificate if passed
    if passed:
        cert_num = f"CERT-SIH-{quiz.course_id[:6].upper()}-{member_id[:6].upper()}"
        existing_cert = db.query(Certificate).filter(Certificate.course_id == quiz.course_id, Certificate.member_id == member_id).first()
        if not existing_cert:
            cert = Certificate(
                member_id=member_id,
                course_id=quiz.course_id,
                certificate_number=cert_num,
                certificate_url=f"/certificates/{cert_num}.pdf"
            )
            db.add(cert)

    db.commit()
    return success_response(
        data={"attempt_id": attempt.id, "score": score, "passed": passed},
        message="Quiz attempt recorded successfully"
    )

@router.get("/{id}/results")
def get_quiz_results(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    attempts = db.query(QuizAttempt).filter(QuizAttempt.quiz_id == id).all()
    return success_response(data={
        "quiz_id": id,
        "title": quiz.title if quiz else "Quiz",
        "total_attempts": len(attempts),
        "attempts": [
            {"id": a.id, "member_id": a.member_id, "score": a.score, "passed": a.passed}
            for a in attempts
        ]
    })
