from typing import Dict, List
from agents.base_agent import BaseAgent

class QAHead(BaseAgent):
    def __init__(self):
        super().__init__("QAHead")
        self.spam_words = ["free", "guarantee", "winner"]

    def check_emails(self, emails: List[Dict]) -> List[Dict]:
        return emails

    def start(self):
        return {"status": "online"}
