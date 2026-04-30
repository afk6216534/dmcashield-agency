from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class SendHead(BaseAgent):
    def __init__(self):
        super().__init__("SendHead")
        self.message_bus = MessageBus()
        self.accounts = []  # Would load from Gmail integration
        self.daily_limit = 40

    def send_emails(self, leads: List[Dict]) -> Dict:
        sent = []
        for lead in leads[:self.daily_limit]:
            # Simulate sending
            sent.append({
                "lead_id": lead.get("lead_id"),
                "status": "sent",
                "timestamp": "now"
            })
        return {"sent": sent, "count": len(sent)}

    def start(self):
        return {"status": "online", "accounts_active": len(self.accounts), "daily_limit": self.daily_limit}
