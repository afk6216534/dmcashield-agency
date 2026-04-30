from typing import Dict
from agents.base_agent import BaseAgent

class WarmupBot(BaseAgent):
    def __init__(self):
        super().__init__("WarmupBot")

    def warmup_account(self, email: str) -> Dict:
        return {"email": email, "warmed_up": True}

    def start(self):
        return {"status": "online", "warmup_progress": 0}
