from typing import Dict, List, Optional
from datetime import datetime

class AgentBrain:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory = []
        self.long_term = {}

    def remember(self, content: str, category: str = "general"):
        self.memory.append({
            "content": content,
            "category": category,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    def recall(self, category: str, limit: int = 10) -> List[Dict]:
        return [m for m in self.memory if m["category"] == category][-limit:]

    def learn(self, content: str, category: str = "general"):
        self.long_term[category] = self.long_term.get(category, []) + [{
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]

class MemorySystem:
    def __init__(self):
        self.brains = {}

    def get_brain(self, agent_name: str) -> AgentBrain:
        if agent_name not in self.brains:
            self.brains[agent_name] = AgentBrain(agent_name)
        return self.brains[agent_name]

memory_system = MemorySystem()
