from typing import Dict
from agents.base_agent import BaseAgent

class ClickTracker(BaseAgent):
    def __init__(self):
        super().__init__("ClickTracker")
        self.clicks = []

    def track_click(self, email_id: str, link: str) -> Dict:
        self.clicks.append({"email_id": email_id, "link": link})
        return {"email_id": email_id, "link": link, "tracked": True}

    def start(self):
        return {"status": "online", "clicks": len(self.clicks)}
