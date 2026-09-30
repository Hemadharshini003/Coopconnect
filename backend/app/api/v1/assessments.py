from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.assessment import SkillAssessment, AssessmentQuestion, AssessmentAnswer, SkillGap
from app.db.models.skill import MemberSkill, Skill, RoleRequiredSkill, RoleCatalog
from app.db.models.course import Course, CourseSkill
from app.ml.skill_gap_engine import SkillGapEngine
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.post("")
def create_assessment(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    assessment = SkillAssessment(
        member_id=payload["member_id"],
        assessment_type=payload.get("assessment_type", "Initial Readiness"),
        status="In Progress"
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Seed sample assessment questions for evaluation
    questions_data = payload.get("questions", [
        {
            "question_text": "How comfortable are you using smartphone digital payment apps (UPI, NetBanking)?",
            "question_type": "MCQ",
            "options_json": '["1 - Not at all", "2 - Basic", "3 - Proficient", "4 - Advanced"]',
            "correct_answer": "3 - Proficient",
            "marks": 25
        },
        {
            "question_text": "Have you previously recorded inventory or sales in an ERP software or digital ledger?",
            "question_type": "Boolean",
            "options_json": '["Yes", "No"]',
            "correct_answer": "Yes",
            "marks": 25
        },
        {
            "question_text": "What steps do you take when reconciling daily milk or farm product collection logs?",
            "question_type": "MCQ",
            "options_json": '["Compare digital total with physical batch count", "Ignore differences", "Manually guess", "Delete record"]',
            "correct_answer": "Compare digital total with physical batch count",
            "marks": 25
        },
        {
            "question_text": "Are you able to generate and print daily summary reports for cooperative audit?",
            "question_type": "Boolean",
            "options_json": '["Yes", "No"]',
            "correct_answer": "Yes",
            "marks": 25
        }
    ])

    for qd in questions_data:
        q = AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=qd["question_text"],
            question_type=qd["question_type"],
            options_json=qd.get("options_json"),
            correct_answer=qd["correct_answer"],
            marks=qd.get("marks", 25)
        )
        db.add(q)

    db.commit()
    return success_response(data={"assessment_id": assessment.id}, message="Skill assessment created")

@router.get("/{id}")
def get_assessment(id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    assessment = db.query(SkillAssessment).filter(SkillAssessment.id == id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.assessment_id == id).all()

    return success_response(data={
        "id": assessment.id,
        "member_id": assessment.member_id,
        "assessment_type": assessment.assessment_type,
        "status": assessment.status,
        "total_score": assessment.total_score,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options_json": q.options_json,
                "marks": q.marks
            }
            for q in questions
        ]
    })

@router.post("/{id}/submit")
def submit_assessment(id: str, payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    assessment = db.query(SkillAssessment).filter(SkillAssessment.id == id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    answers = payload.get("answers", [])
    total_score = 0
    max_score = 0

    for ans in answers:
        q = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == ans["question_id"]).first()
        if q:
            max_score += q.marks
            is_correct = (ans["answer"].strip() == q.correct_answer.strip())
            marks_awarded = q.marks if is_correct else (q.marks // 2)
            total_score += marks_awarded

            user_ans = AssessmentAnswer(
                question_id=q.id,
                member_id=assessment.member_id,
                answer=ans["answer"],
                is_correct=str(is_correct),
                marks_awarded=marks_awarded
            )
            db.add(user_ans)

    assessment.status = "Evaluated"
    assessment.total_score = round((total_score / max(1, max_score)) * 100, 1)
    assessment.submitted_at = datetime.now(timezone.utc)
    db.commit()

    return success_response(
        data={"assessment_id": assessment.id, "total_score": assessment.total_score},
        message="Assessment submitted and evaluated successfully"
    )
