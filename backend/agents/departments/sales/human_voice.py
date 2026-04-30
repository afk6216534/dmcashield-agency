from typing import Dict
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class HumanVoice(BaseAgent):
    def __init__(self):
        super().__init__("HumanVoice")
        self.message_bus = MessageBus()
        self.voice_records = []

    def convert_to_voice(self, message: str) -> Dict:
        self.voice_records.append(message)
        return {"audio": message, "format": "WAV"}

    def start(self):
        return {"status": "online", "voice_records": len(self.voice_records)}
