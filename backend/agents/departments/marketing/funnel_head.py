from typing import Dict, List
import uuid
from agents.base_agent import BaseAgent

class FunnelHead(BaseAgent):
    def __init__(self):
        super().__init__("FunnelHead")

    def design_funnel(self, lead: Dict, intel: Dict) -> Dict:
        return {
            "funnel_id": str(uuid.uuid4()),
            "lead_id": intel.get("lead_id", "unknown"),
            "total_steps": 6,
            "steps": []
        }

    def start(self):
        return {"status": "online"}
