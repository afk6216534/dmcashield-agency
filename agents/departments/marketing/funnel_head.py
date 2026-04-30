"""
FunnelHead Agent (3B) - Email Funnel Sequence Builder
Creates time-spaced funnels for cold → warm → hot progression.
"""

from typing import Dict, Any, List

class FunnelHead:
    """Designs optimal email sequences and timing."""

    def __init__(self):
        # Standard funnel stages
        self.funnel_stages = {
            "cold": ["intro", "pain", "proof"],
            "warm": ["case_study", "offer", "testimonial"],
            "hot": ["urgency", "direct_request", "close"]
        }
        
        # Email spacing per niche (days)
        self.spacing_rules = {
            "restaurant": [1, 3, 7, 14, 21],
            "dentist": [2, 5, 10, 15, 25],
            "salon": [1, 2, 5, 14, 30],
            "clinic": [2, 4, 10, 20, 30],
            "hotel": [2, 5, 12, 20, 35]
        }

    def design_funnel(self, lead_profile: Dict[str, Any], 
                     niche: str) -> Dict[str, Any]:
        """Create a personalized funnel strategy."""
        # Default 6-email sequence
        stage_progression = [0, 1, 2, 1, 3, 4]
        
        # Get spacing
        spacing = self.spacing_rules.get(niche, [2, 4, 8, 15, 25, 35])
        
        emails = []
        current_day = 0
        for i, stage_idx in enumerate(stage_progression):
            current_day += spacing[min(i, len(spacing)-1)]
            email = {
                "email_number": i + 1,
                "stage": list(self.funnel_stages.keys())[stage_idx],
                "send_day": current_day,
                "angle": self._get_angle(i, stage_idx, niche)
            }
            emails.append(email)
        
        # Set warmup period
        warmup_days = max(14, 30 - len(spacing) * 2)
        
        return {
            "funnel_length": len(emails),
            "warmup_required": warmup_days,
            "total_campaign_days": max(spacing) * len(emails),
            "emails": emails,
            "conversion_target": self._estimate_conversion_rate(niche, lead_profile)
        }

    def _get_angle(self, email_idx: int, stage_idx: int, niche: str) -> str:
        """Get messaging angle for this email."""
        angles = {
            "restaurant": ["reputation", "competitor", "review_impact", "offer", "case_study", "urgency"],
            "dentist": ["trust", "family", "health", "offer", "testimonial", "book_now"],
            "salon": ["beauty", "competitor", "before_after", "booking", "happy_client", "limited"],
            "clinic": ["health", "comfort", "safety", "special", "success", "appointment"],
            "hotel": ["comfort", "rating", "comparison", "deal", "experience", "book_direct"]
        }
        niche_angles = angles.get(niche, ["reputation", "improvement", "proof", "offer", "success", "action"])
        return niche_angles[stage_idx] if stage_idx < len(niche_angles) else "general"

    def _estimate_conversion_rate(self, niche: str, profile: Dict[str, Any]) -> float:
        """Estimate funnel conversion rate based on niche and profile."""
        base_rates = {
            "restaurant": 0.15, "dentist": 0.18, "salon": 0.20,
            "clinic": 0.12, "hotel": 0.10, "other": 0.14
        }
        base = base_rates.get(niche, base_rates["other"])
        trust_boost = {"high": 1.1, "medium": 1.0, "low": 0.8}
        boost = trust_boost.get(profile.get("trust_level", "medium"), 1.0)
        return round(base * boost, 3)
