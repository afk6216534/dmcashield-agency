from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class JARVISCore(BaseAgent):
    def __init__(self):
        super().__init__("JARVISCore")
        self.message_bus = MessageBus()
        self.commands_processed = 0
        self.active = True

    def process_command(self, command: str) -> Dict:
        self.commands_processed += 1
        return {
            "command": command,
            "processed": True,
            "response": f"Processed: {command}"
        }

    def start(self):
        return {
            "status": "online",
            "commands_processed": self.commands_processed,
            "active": self.active
        }
