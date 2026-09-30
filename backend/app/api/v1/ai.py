from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.skill import MemberSkill, Skill, RoleCatalog, RoleRequiredSkill
from app.db.models.assessment import SkillGap
from app.db.models.course import Course, CourseSkill
from app.ml.skill_gap_engine import SkillGapEngine
from app.ml.evaluation import MLEvaluation
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Engine"])

@router.get("/health")
def ai_health():
    return success_response(data=MLEvaluation.get_health_and_metrics())

@router.post("/skill-gap-analysis/{member_id}")
def run_skill_gap_analysis(member_id: str, target_role_id: Optional[str] = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # 1. Fetch Member Skills
    m_skills = db.query(MemberSkill).filter(MemberSkill.member_id == member_id).all()
    member_skills_data = [
        {"skill_id": ms.skill_id, "current_level": ms.current_level}
        for ms in m_skills
    ]

    # 2. Get Target Role
    if not target_role_id:
        role = db.query(RoleCatalog).filter(RoleCatalog.title == "Digital Inventory Assistant").first()
        if not role:
            role = db.query(RoleCatalog).first()
        target_role_id = role.id if role else None

    if not target_role_id:
        raise HTTPException(status_code=400, detail="Target role not found for analysis")

    # 3. Fetch Role Required Skills
    req_skills = db.query(RoleRequiredSkill, Skill).join(Skill, RoleRequiredSkill.skill_id == Skill.id).filter(RoleRequiredSkill.role_id == target_role_id).all()
    role_required_data = [
        {
            "skill_id": rrs.skill_id,
            "skill_name": s.name,
            "required_level": rrs.required_level,
            "priority": rrs.priority
        }
        for rrs, s in req_skills
    ]

    # 4. Fetch Available Courses
    courses = db.query(Course).all()
    courses_data = [
        {
            "id": c.id,
            "title": c.title,
            "skills_covered": [cs.skill_id for cs in db.query(CourseSkill).filter(CourseSkill.course_id == c.id).all()]
        }
        for c in courses
    ]

    # 5. Execute SkillGapEngine
    results = SkillGapEngine.calculate_gaps(member_skills_data, role_required_data, courses_data)

    # 6. Save or update SkillGap table records
    # Delete existing gaps for fresh calculation
    db.query(SkillGap).filter(SkillGap.member_id == member_id, SkillGap.target_role_id == target_role_id).delete()
    db.commit()

    for g in results["gaps"]:
        sg = SkillGap(
            member_id=member_id,
            target_role_id=target_role_id,
            skill_id=g["skill_id"],
            current_level=g["current_level"],
            required_level=g["required_level"],
            gap_score=g["gap_score"],
            priority=g["priority"],
            explanation=g["explanation"]
        )
        db.add(sg)
    db.commit()

    return success_response(data=results, message="Skill gap analysis executed successfully")
