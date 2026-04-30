from typing import Dict, List
from agents.base_agent import BaseAgent
import uuid

class FunnelHeadAgent(BaseAgent):
    def __init__(self):
        super().__init__("FunnelHead")

    def design_funnel(self, lead: Dict, intel: Dict) -> Dict:
        funnel = {
            "funnel_id": str(uuid.uuid4()),
            "lead_id": intel.get("lead_id", "unknown"),
            "total_steps": 6,
            "steps": [
                self._step(1, 1, "curiosity", "cold_intro", intel.get("strongest_trigger", "fear"), "curious about their situation"),
                self._step(2, 3, "social_proof", "case_study", "trust", "see how we helped similar businesses"),
                self._step(3, 6, "fear_trigger", "what_happens_if_ignored", "fear", "realize the cost of inaction"),
                self._step(4, 10, "value_offer", "free_audit", "greed", "get a free reputation audit"),
                self._step(5, 15, "scarcity", "last_chance", "urgency", "limited time offer"),
                self._step(6, 21, "breakup", "reverse_psychology", "fear", "final goodbye")
            ]
        }
        return funnel

    def _step(self, step: int, day: int, subject_angle: str, body_angle: str, emotional_focus: str, cta: str) -> Dict:
        return {"step": step, "day": day, "subject_angle": subject_angle, "body_angle": body_angle, "emotional_focus": emotional_focus, "cta": cta}

    def start(self):
        return {"status": "online", "funnels_created": 0}
