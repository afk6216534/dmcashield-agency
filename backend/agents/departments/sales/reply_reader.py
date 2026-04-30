from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class ReplyReader(BaseAgent):
    def __init__(self):
        super().__init__("ReplyReader")
        self.message_bus = MessageBus()
        self.incoming_replies = []

    def process_replies(self, emails: List[Dict]) -> Dict:
        for email in emails:
            if email.get("replies"):
                self.incoming_replies.extend(email["replies"])
        return {"processed": len(self.incoming_replies)}

    def start(self):
        return {"status": "online", "subscribed": True}