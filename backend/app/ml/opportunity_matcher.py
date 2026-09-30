from typing import List, Dict, Any

class OpportunityMatcher:
    """
    Explainable opportunity matching engine.
    Weights:
    - skill_match: 50%
    - location_match: 15%
    - availability_match: 10%
    - education_match: 10%
    - experience_match: 10%
    - certification_match: 5%
    
    Protected attributes (gender, religion, caste) are explicitly excluded from score computation.
    """

    @classmethod
    def match_candidate(
        cls,
        member_profile: Dict[str, Any],
        member_skills: List[Dict[str, Any]],
        member_certificates: List[Dict[str, Any]],
        opportunity: Dict[str, Any],
        opportunity_skills: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        # 1. Skill Match (50%)
        req_skill_map = {s["skill_id"]: s.get("required_level", 3) for s in opportunity_skills}
        mem_skill_map = {s["skill_id"]: s.get("current_level", 1) for s in member_skills}

        if req_skill_map:
            match_ratios = []
            for s_id, req_lvl in req_skill_map.items():
                curr_lvl = mem_skill_map.get(s_id, 0)
                match_ratios.append(min(1.0, curr_lvl / max(1, req_lvl)))
            skill_score = (sum(match_ratios) / len(req_skill_map)) * 50.0
        else:
            skill_score = 50.0

        # 2. Location Match (15%)
        opp_loc = opportunity.get("location", "").lower()
        mem_loc = member_profile.get("location", "").lower()
        remote = opportunity.get("remote_allowed", False)

        if remote or (opp_loc and mem_loc and (opp_loc in mem_loc or mem_loc in opp_loc)):
            location_score = 15.0
            loc_note = "Location match / Remote allowed"
        else:
            location_score = 7.5
            loc_note = "Partial location proximity match"

        # 3. Availability Match (10%)
        availability = member_profile.get("availability", "Immediate")
        avail_score = 10.0 if availability in ["Immediate", "Available"] else 5.0

        # 4. Education Match (10%)
        edu_score = 10.0 if member_profile.get("education_level") else 7.0

        # 5. Experience Match (10%)
        req_exp = opportunity.get("required_experience", 0)
        mem_exp = member_profile.get("years_of_experience", 0)
        exp_score = 10.0 if mem_exp >= req_exp else (mem_exp / max(1, req_exp)) * 10.0

        # 6. Certification Match (5%)
        cert_score = 5.0 if len(member_certificates) > 0 else 2.5

        total_match_score = round(
            skill_score + location_score + avail_score + edu_score + exp_score + cert_score, 1
        )

        strengths = []
        if skill_score > 35:
            strengths.append("High skill proficiency match for required role competencies.")
        if loc_note:
            strengths.append(loc_note)
        if len(member_certificates) > 0:
            strengths.append(f"Holds {len(member_certificates)} verified learning certificate(s).")

        missing = []
        for s in opportunity_skills:
            s_id = s["skill_id"]
            if mem_skill_map.get(s_id, 0) < s.get("required_level", 3):
                missing.append(s.get("skill_name", "Required Skill"))

        explanation = (
            f"Candidate match score is {total_match_score}%. "
            f"Skill match: {round(skill_score,1)}/50, Location: {location_score}/15, "
            f"Availability: {avail_score}/10, Experience: {round(exp_score,1)}/10, Certifications: {cert_score}/5."
        )

        return {
            "match_score": total_match_score,
            "matching_strengths": strengths,
            "missing_requirements": missing,
            "match_explanation": explanation,
            "recommended_training": missing[0] + " Training Module" if missing else None
        }
