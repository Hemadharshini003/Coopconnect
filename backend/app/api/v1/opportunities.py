from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.opportunity import Opportunity, OpportunityRequiredSkill, Application
from app.db.models.profile import MemberProfile
from app.db.models.skill import MemberSkill, Skill
from app.db.models.quiz import Certificate
from app.db.models.user import User
from app.ml.opportunity_matcher import OpportunityMatcher
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.get("")
def list_opportunities(cooperative_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Opportunity)
    if cooperative_id:
        query = query.filter(Opportunity.cooperative_id == cooperative_id)
    opps = query.all()

    data = [
        {
            "id": o.id,
            "cooperative_id": o.cooperative_id,
            "title": o.title,
            "description": o.description,
            "opportunity_type": o.opportunity_type,
            "location": o.location,
            "remote_allowed": o.remote_allowed,
            "stipend_or_salary": o.stipend_or_salary,
            "duration": o.duration,
            "number_of_positions": o.number_of_positions,
            "status": o.status
        }
        for o in opps
    ]
    return success_response(data=data)

@router.post("")
def create_opportunity(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    opp = Opportunity(
        cooperative_id=payload.get("cooperative_id", current_user.cooperative_id or "c1111111-1111-1111-1111-111111111111"),
        created_by=current_user.id,
        title=payload["title"],
        description=payload.get("description"),
        opportunity_type=payload.get("opportunity_type", "Job"),
        location=payload.get("location", "Nashik, Maharashtra"),
        remote_allowed=payload.get("remote_allowed", False),
        stipend_or_salary=payload.get("stipend_or_salary", "₹18,000 / month"),
        duration=payload.get("duration", "Full-time"),
        number_of_positions=payload.get("number_of_positions", 2)
    )
    db.add(opp)
    db.commit()
    db.refresh(opp)

    # Attach required skills if passed
    for s_id in payload.get("required_skill_ids", []):
        ors = OpportunityRequiredSkill(opportunity_id=opp.id, skill_id=s_id, required_level=3)
        db.add(ors)
    db.commit()

    return success_response(data={"id": opp.id, "title": opp.title}, message="Opportunity created")

@router.get("/{id}")
def get_opportunity(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    opp = db.query(Opportunity).filter(Opportunity.id == id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    skills = db.query(OpportunityRequiredSkill, Skill).join(Skill, OpportunityRequiredSkill.skill_id == Skill.id).filter(OpportunityRequiredSkill.opportunity_id == id).all()

    return success_response(data={
        "id": opp.id,
        "title": opp.title,
        "description": opp.description,
        "opportunity_type": opp.opportunity_type,
        "location": opp.location,
        "remote_allowed": opp.remote_allowed,
        "stipend_or_salary": opp.stipend_or_salary,
        "duration": opp.duration,
        "number_of_positions": opp.number_of_positions,
        "status": opp.status,
        "required_skills": [
            {"skill_id": s.id, "name": s.name, "required_level": ors.required_level}
            for ors, s in skills
        ]
    })

@router.get("/{id}/matches")
def get_opportunity_candidate_matches(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    opp = db.query(Opportunity).filter(Opportunity.id == id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opp_skills = db.query(OpportunityRequiredSkill, Skill).join(Skill, OpportunityRequiredSkill.skill_id == Skill.id).filter(OpportunityRequiredSkill.opportunity_id == id).all()
    opp_skills_data = [
        {"skill_id": s.id, "skill_name": s.name, "required_level": ors.required_level}
        for ors, s in opp_skills
    ]

    members = db.query(MemberProfile, User).join(User, MemberProfile.user_id == User.id).all()
    matches = []

    for mp, u in members:
        m_skills = db.query(MemberSkill).filter(MemberSkill.member_id == mp.id).all()
        m_skills_data = [{"skill_id": ms.skill_id, "current_level": ms.current_level} for ms in m_skills]
        certs = db.query(Certificate).filter(Certificate.member_id == mp.id).all()
        certs_data = [{"id": c.id} for c in certs]

        prof_data = {
            "location": mp.location,
            "availability": mp.availability,
            "education_level": mp.education_level,
            "years_of_experience": mp.years_of_experience
        }

        match_res = OpportunityMatcher.match_candidate(
            prof_data, m_skills_data, certs_data,
            {"location": opp.location, "remote_allowed": opp.remote_allowed},
            opp_skills_data
        )

        matches.append({
            "member_id": mp.id,
            "full_name": u.full_name,
            "membership_number": mp.membership_number,
            "match_score": match_res["match_score"],
            "matching_strengths": match_res["matching_strengths"],
            "missing_requirements": match_res["missing_requirements"],
            "match_explanation": match_res["match_explanation"]
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return success_response(data=matches)

@router.post("/{id}/apply")
def apply_opportunity(id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member_id = payload.get("member_id")
    if not member_id:
        mp = db.query(MemberProfile).filter(MemberProfile.user_id == current_user.id).first()
        member_id = mp.id if mp else None

    if not member_id:
        raise HTTPException(status_code=400, detail="Member profile ID required")

    existing = db.query(Application).filter(Application.opportunity_id == id, Application.member_id == member_id).first()
    if existing:
        return success_response(data={"application_id": existing.id, "status": existing.status}, message="Application already submitted")

    app = Application(
        opportunity_id=id,
        member_id=member_id,
        match_score=payload.get("match_score", 92.5),
        match_explanation=payload.get("match_explanation", "Verified high compatibility match"),
        status="Submitted"
    )
    db.add(app)
    db.commit()

    return success_response(data={"application_id": app.id, "status": app.status}, message="Application submitted successfully")
