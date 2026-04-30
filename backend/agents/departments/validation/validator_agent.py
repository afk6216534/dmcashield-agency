from typing import Dict, List
from agents.base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ValidatorAgent")

    def validate(self, leads: List[Dict]) -> List[Dict]:
        validated = []
        for lead in leads:
            if lead.get("rating", 5.0) < 4.0 and lead.get("reviews_count", 0) > 5:
                lead["valid_for_campaign"] = True
                lead["priority"] = "high" if lead.get("rating", 5.0) < 2.5 else "medium"
                validated.append(lead)
        return validated

    def start(self):
        return {"status": "online", "validated": 0}
