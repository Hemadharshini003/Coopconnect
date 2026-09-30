from app.ml.skill_gap_engine import SkillGapEngine
from app.ml.opportunity_matcher import OpportunityMatcher

def test_skill_gap_engine_calculation():
    member_skills = [
        {"skill_id": "s1", "current_level": 1},
        {"skill_id": "s2", "current_level": 4}
    ]
    role_required_skills = [
        {"skill_id": "s1", "skill_name": "ERP Operation", "required_level": 4, "priority": "Critical"},
        {"skill_id": "s2", "skill_name": "Basic Smartphone Use", "required_level": 3, "priority": "Medium"}
    ]
    available_courses = [
        {"id": "c1", "title": "ERP Fundamentals", "skills_covered": ["s1"]}
    ]

    res = SkillGapEngine.calculate_gaps(member_skills, role_required_skills, available_courses)
    assert res["overall_readiness_score"] == 50.0
    assert len(res["gaps"]) == 2
    assert res["gaps"][0]["skill_id"] == "s1"
    assert res["gaps"][0]["recommended_course"] == "ERP Fundamentals"

def test_opportunity_matcher_scoring():
    member_profile = {"location": "Nashik, Maharashtra", "availability": "Immediate", "education_level": "Higher Secondary", "years_of_experience": 3}
    member_skills = [{"skill_id": "s1", "current_level": 4}]
    certificates = [{"id": "cert1"}]
    opportunity = {"location": "Nashik, Maharashtra", "remote_allowed": False, "required_experience": 2}
    opportunity_skills = [{"skill_id": "s1", "skill_name": "ERP Operation", "required_level": 4}]

    res = OpportunityMatcher.match_candidate(member_profile, member_skills, certificates, opportunity, opportunity_skills)
    assert res["match_score"] >= 90.0
    assert len(res["matching_strengths"]) > 0
