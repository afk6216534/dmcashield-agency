from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

class Soul:
    def __init__(self, version: str = "1.0.0"):
        self.version = version
        self.creation_date = datetime.utcnow().isoformat() + "Z"
        self.mission = "Autonomous DMCA review removal for businesses"
        self.core_principles = [
            "Zero human intervention after launch",
            "Continuous learning and optimization",
            "Ethical compliance with DMCA processes",
            "Persistent memory across restarts",
            "Self-healing via DeepSleep integration"
        ]
        self.departments = self._init_departments()
        self.learning_cycle = 1
        self.total_autonomous_hours = 0
        self.status = "operational"

    def _init_departments(self) -> Dict:
        depts = {}
        dept_names = [
            "scraping", "validation", "marketing", "email_sending",
            "tracking", "sales", "sheets", "accounts",
            "tasks", "ml", "jarvis", "memory"
        ]
        for name in dept_names:
            depts[name] = {"status": "online", "last_active": None}
        return depts

    def update_department(self, name: str, updates: Dict):
        if name in self.departments:
            self.departments[name].update(updates)

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "creation_date": self.creation_date,
            "mission": self.mission,
            "core_principles": self.core_principles,
            "departments": self.departments,
            "learning_cycle": self.learning_cycle,
            "total_autonomous_hours": self.total_autonomous_hours,
            "status": self.status
        }

    def save(self, path: str = "soul.json"):
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    def load(self, path: str = "soul.json"):
        if Path(path).exists():
            data = json.loads(Path(path).read_text())
            self.__dict__.update(data)

def get_soul() -> Soul:
    return Soul()
