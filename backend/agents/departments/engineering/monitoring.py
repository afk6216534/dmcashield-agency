from typing import Dict
from agents.base_agent import BaseAgent

class EngineeringMonitor(BaseAgent):
    def __init__(self):
        super().__init__("EngineeringMonitor")
        self.alerts = 0

    def check_system(self) -> Dict:
        return {"cpu": 45.2, "memory": 62.1, "disk": 78.3, "alerts": self.alerts}

    def start(self):
        return {"status": "online", "alerts_triggered": self.alerts}
