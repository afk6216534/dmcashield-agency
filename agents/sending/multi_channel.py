import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class MultiChannelOrchestrator:
    def __init__(self):
        self.channels = ["email", "sms", "whatsapp", "linkedin", "call"]
        self.sequences: Dict[str, Dict] = {}
        self.contact_log: List[Dict] = []

    def create_sequence(self, name: str, steps: List[Dict]) -> Dict:
        self.sequences[name] = {
            "steps": steps,
            "active": True,
            "created": datetime.utcnow().isoformat()
        }
        return {"sequence": name, "steps": len(steps)}

    def get_next_step(self, lead_id: str, lead_data: Dict, sequence: str) -> Dict:
        seq = self.sequences.get(sequence)
        if not seq:
            return {"error": f"sequence '{sequence}' not found"}

        contacts = [c for c in self.contact_log if c.get("lead_id") == lead_id]
        step_index = contacts[-1].get("step_index", -1) + 1 if contacts else 0

        if step_index >= len(seq["steps"]):
            return {"action": "done", "message": "Sequence complete"}

        step = seq["steps"][step_index]
        return {
            "step": step_index,
            "channel": step.get("channel"),
            "action": step.get("action"),
            "delay_hours": step.get("delay_hours", 24)
        }

    def execute_step(self, lead_id: str, lead_data: Dict, step: Dict) -> Dict:
        channel = step.get("channel", "email")
        action = step.get("action", "send_message")

        result = {
            "lead_id": lead_id,
            "channel": channel,
            "action": action,
            "status": "sent" if random.random() > 0.1 else "failed",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.contact_log.append({
            "lead_id": lead_id,
            "step_index": step.get("step", 0),
            "channel": channel,
            "action": action,
            "status": result["status"],
            "timestamp": result["timestamp"]
        })

        result["next_step"] = self._suggest_next(lead_id, channel, result["status"])
        return result

    def _suggest_next(self, lead_id: str, last_channel: str, status: str) -> str:
        if status == "failed":
            alt_channels = [c for c in self.channels if c != last_channel]
            return f"Try {random.choice(alt_channels)} instead"
        return f"Continue with next channel in sequence"

    def get_lead_history(self, lead_id: str) -> List[Dict]:
        return [c for c in self.contact_log if c.get("lead_id") == lead_id]

    def get_channel_stats(self) -> Dict:
        stats = {c: {"total": 0, "sent": 0, "failed": 0} for c in self.channels}
        for c in self.contact_log:
            ch = c.get("channel", "email")
            if ch in stats:
                stats[ch]["total"] += 1
                if c.get("status") == "sent":
                    stats[ch]["sent"] += 1
                else:
                    stats[ch]["failed"] += 1
        for ch in stats:
            t = stats[ch]["total"]
            stats[ch]["success_rate"] = round((stats[ch]["sent"] / max(1, t)) * 100, 1) if t > 0 else 0
        return stats

    def get_dmca_sequence(self) -> List[Dict]:
        return [
            {"step": 0, "channel": "email", "action": "cold_intro", "delay_hours": 0, "msg": "First touch via email"},
            {"step": 1, "channel": "email", "action": "social_proof", "delay_hours": 48, "msg": "Case studies"},
            {"step": 2, "channel": "linkedin", "action": "connect_request", "delay_hours": 72, "msg": "LinkedIn connect with note"},
            {"step": 3, "channel": "email", "action": "fear_trigger", "delay_hours": 96, "msg": "Competitor alert"},
            {"step": 4, "channel": "sms", "action": "text_followup", "delay_hours": 120, "msg": "Quick SMS nudge"},
            {"step": 5, "channel": "call", "action": "cold_call", "delay_hours": 168, "msg": "Phone call attempt"},
        ]


multi_channel = MultiChannelOrchestrator()
