from typing import Dict, List
from agents.base_agent import BaseAgent

class AudienceAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("AudienceAnalystAgent")

    def analyze(self, lead: Dict) -> Dict:
        return {
            "pain_points": ["negative reviews", "losing customers", "bad online reputation"],
            "emotional_triggers": {"fear": 0.8, "greed": 0.6, "urgency": 0.7},
            "personalization_hooks": [lead.get("business_name", ""), lead.get("city", "")],
            "tone": "professional",
            "send_schedule": {"days": [1, 3, 6, 10, 15, 21], "hours": [9, 10, 11, 14, 15]}
        }

    def start(self):
        return {"status": "online", "analyzed": 0}
