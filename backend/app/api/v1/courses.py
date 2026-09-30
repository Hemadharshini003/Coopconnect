from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.course import Course, CourseLesson, Enrollment
from app.db.models.profile import MemberProfile
from app.schemas.response import success_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("")
def list_courses(category: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Course)
    if category:
        query = query.filter(Course.category == category)
    courses = query.all()

    data = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "category": c.category,
            "difficulty": c.difficulty,
            "language": c.language,
            "duration_minutes": c.duration_minutes,
            "status": c.status
        }
        for c in courses
    ]
    return success_response(data=data)

@router.post("")
def create_course(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = Course(
        title=payload["title"],
        description=payload.get("description"),
        category=payload.get("category", "Digital Basics"),
        difficulty=payload.get("difficulty", "Beginner"),
        language=payload.get("language", "en"),
        duration_minutes=payload.get("duration_minutes", 60),
        status="Published"
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return success_response(data={"id": course.id, "title": course.title}, message="Course created")

@router.get("/{id}")
def get_course(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lessons = db.query(CourseLesson).filter(CourseLesson.course_id == id).order_by(CourseLesson.sequence_number).all()

    return success_response(data={
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "difficulty": course.difficulty,
        "language": course.language,
        "duration_minutes": course.duration_minutes,
        "lessons": [
            {
                "id": l.id,
                "title": l.title,
                "content_type": l.content_type,
                "content_url": l.content_url,
                "text_content": l.text_content,
                "sequence_number": l.sequence_number,
                "duration_minutes": l.duration_minutes
            }
            for l in lessons
        ]
    })

@router.post("/{id}/enroll")
def enroll_course(id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member_id = payload.get("member_id")
    if not member_id:
        mp = db.query(MemberProfile).filter(MemberProfile.user_id == current_user.id).first()
        member_id = mp.id if mp else None

    if not member_id:
        raise HTTPException(status_code=400, detail="Member ID required for enrolment")

    existing = db.query(Enrollment).filter(Enrollment.course_id == id, Enrollment.member_id == member_id).first()
    if existing:
        return success_response(data={"enrollment_id": existing.id, "status": existing.status}, message="Already enrolled")

    enrollment = Enrollment(
        member_id=member_id,
        course_id=id,
        status="In Progress",
        progress_percentage=10.0
    )
    db.add(enrollment)
    db.commit()

    return success_response(data={"enrollment_id": enrollment.id}, message="Enrolled in course successfully")

@router.post("/{id}/complete")
def complete_course(id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member_id = payload.get("member_id")
    if not member_id:
        mp = db.query(MemberProfile).filter(MemberProfile.user_id == current_user.id).first()
        member_id = mp.id if mp else None

    enrollment = db.query(Enrollment).filter(Enrollment.course_id == id, Enrollment.member_id == member_id).first()
    if not enrollment:
        enrollment = Enrollment(member_id=member_id, course_id=id)
        db.add(enrollment)

    enrollment.status = "Completed"
    enrollment.progress_percentage = 100.0
    enrollment.completed_at = datetime.now(timezone.utc)
    db.commit()

    return success_response(data={"enrollment_id": enrollment.id, "status": "Completed"}, message="Course marked as complete")
