from typing import Dict, List
from agents.base_agent import BaseAgent

class OpenTracker(BaseAgent):
    def __init__(self):
        super().__init__("OpenTracker")
        self.tracking_data = []

    def track(self, email_id: str) -> Dict:
        self.tracking_data.append({"email_id": email_id, "opened": True})
        return {"email_id": email_id, "status": "tracked"}

    def start(self):
        return {"status": "online", "tracked": len(self.tracking_data)}
