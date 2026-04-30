from typing import Dict, List
from agents.base_agent import BaseAgent

class CompetitorHead(BaseAgent):
    def __init__(self):
        super().__init__("CompetitorHead")

    def track_trends(self):
        return []

    def report_insights(self, insights: Dict):
        pass

    def start(self):
        return {"status": "online"}
