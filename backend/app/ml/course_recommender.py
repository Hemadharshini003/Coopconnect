from typing import List, Dict, Any

class CourseRecommender:
    @classmethod
    def recommend_courses(
        cls,
        member_gaps: List[Dict[str, Any]],
        all_courses: List[Dict[str, Any]],
        preferred_language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Ranks available courses based on priority of member skill gaps and user preferences.
        """
        gap_skill_ids = {g["skill_id"]: g["priority"] for g in member_gaps}
        recommendations = []

        for course in all_courses:
            score = 0.0
            reasons = []

            # Check skill overlap
            covered_skills = course.get("skills_covered", [])
            for s_id in covered_skills:
                if s_id in gap_skill_ids:
                    priority = gap_skill_ids[s_id]
                    if priority == "Critical":
                        score += 40.0
                    elif priority == "High":
                        score += 30.0
                    else:
                        score += 20.0
                    reasons.append(f"Addresses {priority} priority skill gap")

            # Language match
            if course.get("language") == preferred_language:
                score += 10.0
                reasons.append(f"Available in preferred language ({preferred_language.upper()})")

            # Offline availability
            if course.get("offline_available", True):
                score += 5.0

            if score > 0:
                recommendations.append({
                    "course_id": course["id"],
                    "title": course["title"],
                    "category": course.get("category"),
                    "difficulty": course.get("difficulty"),
                    "duration_minutes": course.get("duration_minutes"),
                    "relevance_score": min(100.0, score),
                    "recommendation_reasons": reasons
                })

        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
        return recommendations
