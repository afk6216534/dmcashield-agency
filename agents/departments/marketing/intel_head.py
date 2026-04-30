"""
IntelHead Agent (3A) - Psychological Profiling of Leads
Creates emotional maps and deep interest profiles.
"""

from typing import Dict, Any

class IntelHead:
    """Deep profiling for emotional triggers and interests."""

    def __init__(self):
        self.emotion_weights = {
            "fear": 1.2,
            "urgency": 1.1,
            "greed": 1.0,
            "trust": 1.3,
            "excitement": 0.9
        }

    def build_profile(self, lead_data: Dict[str, Any], 
                     review_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Build psychological profile from lead data + review emotional analysis."""
        profile = {
            "dominant_emotion": review_analysis.get("dominant_emotion", "neutral"),
            "emotional_triggers": [],
            "interests": [],
            "trust_level": "medium",
            "pain_points": review_analysis.get("found_complaint_themes", [])[:3]
        }

        # Map dominant emotion to psychological profile
        emotion_map = {
            "positive": {"emotional_triggers": ["excitement", "trust"],
                        "interests": ["reputation", "service_quality"]},
            "negative": {"emotional_triggers": ["fear", "urgency", "trust"],
                        "interests": ["recovery", "improvement", "prevention"]},
            "neutral": {"emotional_triggers": ["trust", "excitement"],
                       "interests": ["value", "reliability"]}
        }
        em = emotion_map.get(review_analysis.get("dominant_emotion", "neutral"), emotion_map["neutral"])
        profile["emotional_triggers"] = em["emotional_triggers"]
        profile["interests"] = em["interests"]

        # Assign trust level based on negative themes
        if "poor quality" in review_analysis.get("found_complaint_themes", []):
            profile["trust_level"] = "low"
        elif "excellent" in str(review_analysis).lower():
            profile["trust_level"] = "high"

        # Apply emotion weights
        weighted_profile = profile.copy()
        weighted_profile["emotional_score"] = sum(
            self.emotion_weights.get(et, 1.0) for et in profile["emotional_triggers"]
        )

        return weighted_profile

    def get_pain_points_priority(self, profile: Dict[str, Any]) -> list:
        """Return top pain points to address in copy."""
        # Simple priority based on found themes
        priority = {"service": 1, "quality": 2, "price": 3, "timing": 4, "other": 5}
        return sorted(profile.get("pain_points", []), key=lambda x: priority.get(x, 5))
