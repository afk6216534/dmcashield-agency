from typing import Dict, List
from agents.base_agent import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__("VerifierAgent")

    def verify(self, leads: List[Dict]) -> List[Dict]:
        verified = []
        for lead in leads:
            if lead.get("phone") and lead.get("address"):
                lead["verified"] = True
                lead["quality_score"] = 0.5 + (lead.get("rating", 3.0) / 5.0) * 0.5
                verified.append(lead)
        return verified

    def start(self):
        return {"status": "online", "verified_count": 0}
