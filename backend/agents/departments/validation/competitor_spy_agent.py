from typing import Dict, List
from agents.base_agent import BaseAgent

class CompetitorSpyAgent(BaseAgent):
    def __init__(self):
        super().__init__("CompetitorSpyAgent")

    def spy(self, lead: Dict) -> Dict:
        niche = lead.get("niche", "business")
        return {
            "competitors": [
                {"name": f"Top {niche} Co", "rating": 4.5, "reviews": 200},
                {"name": f"Best {niche} LLC", "rating": 4.3, "reviews": 150}
            ],
            "your_rating_gap": round(4.5 - lead.get("rating", 3.0), 1)
        }

    def start(self):
        return {"status": "online", "spies_active": 0}
