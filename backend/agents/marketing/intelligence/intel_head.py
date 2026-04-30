from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class IntelHeadAgent(BaseAgent):
    def __init__(self):
        super().__init__("IntelHead")
        self.message_bus = MessageBus()
        self.brain = None  # Would connect to memory system

    def analyze_lead(self, lead: Dict) -> Dict:
        intel = {
            "lead_id": lead.get("lead_id", "unknown"),
            "pain_points": self._extract_pain_points(lead),
            "emotional_triggers": self._analyze_emotional_triggers(lead),
            "personalization_hooks": self._get_personalization_hooks(lead),
            "competitors": self._identify_competitors(lead),
            "rating_gap": self._calculate_rating_gap(lead)
        }
        return intel

    def _extract_pain_points(self, lead: Dict) -> List[str]:
        # Extract pain points from worst reviews
        pain_points = []
        reviews = lead.get("worst_reviews", [])
        if reviews:
            pain_points.append(f"Reviews like: '{reviews[0][:100]}...'")
        return pain_points

    def _analyze_emotional_triggers(self, lead: Dict) -> Dict:
        # Analyze emotional triggers based on lead data
        return {"fear": 0.8, "greed": 0.6, "urgency": 0.7}

    def _get_personalization_hooks(self, lead: Dict) -> List[str]:
        hooks = []
        if lead.get("business_name"):
            hooks.append(lead["business_name"])
        if lead.get("city"):
            hooks.append(lead["city"])
        return hooks

    def _identify_competitors(self, lead: Dict) -> List[Dict]:
        # Identify competitors based on niche and location
        return [
            {"name": f"Top {lead.get('niche', 'business')} Co", "rating": 4.5},
            {"name": f"Best {lead.get('niche', 'business')} LLC", "rating": 4.3}
        ]

    def _calculate_rating_gap(self, lead: Dict) -> float:
        # Calculate gap between lead's rating and competitors
        competitor_ratings = [comp["rating"] for comp in self._identify_competitors(lead)]
        avg_competitor = sum(competitor_ratings) / len(competitor_ratings) if competitor_ratings else 0
        return round(avg_competitor - lead.get("current_rating", 3.0), 1)

    def start(self):
        return {"status": "online", "analyzed": 0}