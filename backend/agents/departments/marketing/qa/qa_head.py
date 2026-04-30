from typing import Dict, List
from agents.base_agent import BaseAgent

class QAHeadAgent(BaseAgent):
    def __init__(self):
        super().__init__("QAHeadAgent")
        self.spam_words = ["free", "guarantee"]

    def check_emails(self, emails: List[Dict]) -> List[Dict]:
        return emails

    def start(self):
        return {"status": "online"}
