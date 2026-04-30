from typing import Dict, List
from agents.base_agent import BaseAgent

class ModelTrainer(BaseAgent):
    def __init__(self):
        super().__init__("ModelTrainer")
        self.model_trained = False

    def train(self, data: List[Dict]) -> Dict:
        self.model_trained = True
        return {"status": "trained", "samples": len(data)}

    def start(self):
        return {"status": "online", "trained": self.model_trained}
