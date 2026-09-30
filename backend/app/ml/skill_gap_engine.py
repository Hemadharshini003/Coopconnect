from typing import List, Dict, Any

class SkillGapEngine:
    PRIORITY_WEIGHTS = {
        "Critical": 1.5,
        "High": 1.2,
        "Medium": 1.0,
        "Low": 0.8
    }

    @classmethod
    def calculate_gaps(
        cls,
        member_skills: List[Dict[str, Any]],
        role_required_skills: List[Dict[str, Any]],
        available_courses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates explainable skill gaps for a member against a target role.
        """
        member_skill_map = {ms["skill_id"]: ms["current_level"] for ms in member_skills}
        gaps = []
        total_required = len(role_required_skills)
        total_met = 0

        for req in role_required_skills:
            skill_id = req["skill_id"]
            skill_name = req.get("skill_name", "Skill")
            req_level = req.get("required_level", 3)
            priority = req.get("priority", "High")
            
            curr_level = member_skill_map.get(skill_id, 0)
            raw_gap = max(0, req_level - curr_level)

            if raw_gap == 0:
                total_met += 1

            # Normalise gap to 0-100 scale
            normalized_gap = (raw_gap / max(1, req_level)) * 100
            weighted_score = min(100.0, normalized_gap * cls.PRIORITY_WEIGHTS.get(priority, 1.0))

            explanation = (
                f"Required proficiency is Level {req_level}, but current level is {curr_level}. "
                f"Gap: {raw_gap} level(s) ({priority} priority)."
            )

            # Find matching course
            recommended_courses = [
                c for c in available_courses 
                if skill_id in c.get("skills_covered", [])
            ]
            course_rec = recommended_courses[0]["title"] if recommended_courses else "General Skill Upgrade Module"

            gaps.append({
                "skill_id": skill_id,
                "skill_name": skill_name,
                "current_level": curr_level,
                "required_level": req_level,
                "gap_score": round(weighted_score, 1),
                "priority": priority,
                "explanation": explanation,
                "recommended_course": course_rec
            })

        # Sort gaps by highest gap score
        gaps.sort(key=lambda x: x["gap_score"], reverse=True)

        overall_readiness = round((total_met / max(1, total_required)) * 100, 1)

        return {
            "overall_readiness_score": overall_readiness,
            "total_skills_evaluated": total_required,
            "skills_met": total_met,
            "gaps": gaps
        }
