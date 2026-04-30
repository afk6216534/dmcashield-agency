from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class SheetBot(BaseAgent):
    def __init__(self):
        super().__init__("SheetBot")
        self.message_bus = MessageBus()
        self.sheet_data = []

    def update_sheet(self, leads: List[Dict]) -> Dict:
        for lead in leads:
            self.sheet_data.append({
                "lead_id": lead.get("lead_id", "unknown"),
                "status": "updated",
                "timestamp": "now"
            })
        return {"status": "updated", "count": len(self.sheet_data)}

    def start(self):
        return {"status": "online", "entries": len(self.sheet_data)}
