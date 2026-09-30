from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.profile import MemberProfile
from app.db.models.user import User
from app.db.models.skill import MemberSkill, Skill, RoleRequiredSkill, RoleCatalog
from app.db.models.assessment import SkillGap
from app.db.models.course import Course, CourseSkill
from app.ml.skill_gap_engine import SkillGapEngine
from app.ml.course_recommender import CourseRecommender
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/members", tags=["Members"])

@router.get("")
def list_members(cooperative_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(MemberProfile, User).join(User, MemberProfile.user_id == User.id)
    if cooperative_id:
        query = query.filter(MemberProfile.cooperative_id == cooperative_id)
    elif current_user.role == "COOPERATIVE_ADMIN" and current_user.cooperative_id:
        query = query.filter(MemberProfile.cooperative_id == current_user.cooperative_id)

    results = query.all()
    data = []
    for mp, u in results:
        data.append({
            "id": mp.id,
            "user_id": u.id,
            "membership_number": mp.membership_number,
            "full_name": u.full_name,
            "email": u.email,
            "phone": u.phone,
            "cooperative_id": mp.cooperative_id,
            "education_level": mp.education_level,
            "occupation": mp.occupation,
            "years_of_experience": mp.years_of_experience,
            "profile_completion_percentage": mp.profile_completion_percentage
        })
    return success_response(data=data)

@router.post("")
def create_member(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check email
    existing_user = db.query(User).filter(User.email == payload["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User email already exists")

    # Create User account
    user = User(
        email=payload["email"],
        phone=payload.get("phone"),
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # ChangeMe123!
        full_name=payload["full_name"],
        role="MEMBER",
        preferred_language=payload.get("preferred_language", "en"),
        cooperative_id=payload["cooperative_id"]
    )
    db.add(user)
    db.flush()

    # Create Member profile
    mp = MemberProfile(
        user_id=user.id,
        cooperative_id=payload["cooperative_id"],
        membership_number=payload["membership_number"],
        education_level=payload.get("education_level", "Higher Secondary"),
        occupation=payload.get("occupation", "Farming / Dairy"),
        years_of_experience=payload.get("years_of_experience", 2),
        preferred_language=payload.get("preferred_language", "en"),
        location=payload.get("location", "Nashik, Maharashtra"),
        profile_completion_percentage=85.0
    )
    db.add(mp)
    db.commit()

    return success_response(
        data={"member_id": mp.id, "user_id": user.id, "membership_number": mp.membership_number},
        message="Member created successfully"
    )

@router.get("/{id}")
def get_member(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mp = db.query(MemberProfile).filter(MemberProfile.id == id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="Member profile not found")

    user = db.query(User).filter(User.id == mp.user_id).first()

    return success_response(data={
        "id": mp.id,
        "user_id": mp.user_id,
        "membership_number": mp.membership_number,
        "full_name": user.full_name if user else "Member",
        "email": user.email if user else "",
        "phone": user.phone if user else "",
        "cooperative_id": mp.cooperative_id,
        "education_level": mp.education_level,
        "occupation": mp.occupation,
        "years_of_experience": mp.years_of_experience,
        "preferred_language": mp.preferred_language,
        "location": mp.location,
        "availability": mp.availability,
        "profile_completion_percentage": mp.profile_completion_percentage
    })

@router.get("/{id}/skills")
def get_member_skills(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    skills = db.query(MemberSkill, Skill).join(Skill, MemberSkill.skill_id == Skill.id).filter(MemberSkill.member_id == id).all()
    data = [
        {
            "id": ms.id,
            "skill_id": s.id,
            "name": s.name,
            "code": s.code,
            "category": s.category,
            "current_level": ms.current_level,
            "evidence_source": ms.evidence_source,
            "confidence_score": ms.confidence_score
        }
        for ms, s in skills
    ]
    return success_response(data=data)

@router.get("/{id}/skill-gaps")
def get_member_skill_gaps(id: str, target_role_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    gaps = db.query(SkillGap, Skill).join(Skill, SkillGap.skill_id == Skill.id).filter(SkillGap.member_id == id).all()
    
    data = [
        {
            "id": sg.id,
            "skill_id": s.id,
            "skill_name": s.name,
            "category": s.category,
            "current_level": sg.current_level,
            "required_level": sg.required_level,
            "gap_score": sg.gap_score,
            "priority": sg.priority,
            "explanation": sg.explanation
        }
        for sg, s in gaps
    ]
    return success_response(data=data)

@router.get("/{id}/recommendations")
def get_member_recommendations(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mp = db.query(MemberProfile).filter(MemberProfile.id == id).first()
    gaps = db.query(SkillGap).filter(SkillGap.member_id == id).all()
    courses = db.query(Course).all()

    gap_data = [{"skill_id": g.skill_id, "priority": g.priority} for g in gaps]
    course_data = [
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "difficulty": c.difficulty,
            "duration_minutes": c.duration_minutes,
            "language": c.language,
            "skills_covered": [cs.skill_id for cs in db.query(CourseSkill).filter(CourseSkill.course_id == c.id).all()]
        }
        for c in courses
    ]

    recs = CourseRecommender.recommend_courses(gap_data, course_data, preferred_language=mp.preferred_language if mp else "en")
    return success_response(data=recs)
