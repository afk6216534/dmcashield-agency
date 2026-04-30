from typing import Dict, List
from agents.base_agent import BaseAgent

class IntelHeadAgent(BaseAgent):
    def __init__(self):
        super().__init__("IntelHead")

    def analyze_lead(self, lead: Dict) -> Dict:
        return {
            "lead_id": lead.get("lead_id", "unknown"),
            "pain_points": ["negative reviews"],
            "emotional_triggers": {"fear": 0.8},
            "strongest_trigger": "fear",
            "personalization_hooks": [],
            "competitors": [],
            "rating_gap": 1.5,
            "tone": "professional",
            "send_schedule": {"days": [1, 3, 6], "hours": [9, 10, 11]}
        }

    def start(self):
        return {"status": "online"}
