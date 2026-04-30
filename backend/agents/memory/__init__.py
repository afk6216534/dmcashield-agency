from .message_bus import MessageBus
from .persistent_memory import XII_PersistentMemory

message_bus = MessageBus()

class MemorySystem:
    def __init__(self):
        self.soul = {
            "version": "1.0.0",
            "mission": "Autonomous DMCA review removal for businesses",
            "core_principles": [
                "Zero human intervention after launch",
                "Continuous learning and optimization",
                "Ethical compliance with DMCA processes",
                "Persistent memory across restarts"
            ],
            "departments": {
                "scraping": {"status": "online", "lead_count": 0},
                "validation": {"status": "online", "verified_count": 0},
                "marketing": {"status": "online", "campaigns_ran": 0},
                "email_sending": {"status": "online", "accounts_active": 0},
                "tracking": {"status": "online", "metrics_collected": "daily"},
                "sales": {"status": "online", "hot_leads": 0}
            },
            "learning_cycle": 1,
            "total_autonomous_hours": 0,
            "status": "operational"
        }
    
    def get_soul(self):
        return self.soul
    
    def update_soul(self, key, value):
        if "departments" in self.soul and key in self.soul["departments"]:
            self.soul["departments"][key] = value
        else:
            self.soul[key] = value

memory_system = MemorySystem()
persistent_memory = XII_PersistentMemory()