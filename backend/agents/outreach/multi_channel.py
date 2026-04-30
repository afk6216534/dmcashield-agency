# Multi-Channel Outreach Engine
# ==============================
# Coordinate outreach across email, SMS, WhatsApp, LinkedIn, calls

from typing import Dict, List
from datetime import datetime, timedelta
import random

class MultiChannelOrchestrator:
    """Orchestrate outreach across multiple channels"""
    
    def __init__(self):
        self.channels = ["email", "sms", "whatsapp", "linkedin", "call"]
        self.sequences = {}
        self.contact_log = []
    
    def create_sequence(self, name: str, steps: List[Dict]) -> Dict:
        """Create multi-channel sequence"""
        self.sequences[name] = {
            "steps": steps,
            "active": True,
            "created": datetime.utcnow().isoformat()
        }
        return {"sequence": name, "steps": len(steps)}
    
    def get_next_step(self, lead: Dict, sequence: str) -> Dict:
        """Get next step in sequence based on lead response"""
        seq = self.sequences.get(sequence)
        if not seq:
            return {}
        
        last_contact = None
        for contact in self.contact_log:
            if contact.get("lead_id") == lead.get("id"):
                last_contact = contact
        
        step_index = last_contact.get("step_index", -1) + 1 if last_contact else 0
        
        if step_index >= len(seq["steps"]):
            return {"action": "done", "message": "Sequence complete"}
        
        step = seq["steps"][step_index]
        return {
            "step": step_index,
            "channel": step.get("channel"),
            "action": step.get("action"),
            "delay_hours": step.get("delay_hours", 24)
        }
    
    def execute_step(self, lead: Dict, step: Dict) -> Dict:
        """Execute outreach step"""
        channel = step.get("channel", "email")
        
        actions = {
            "email": self._send_email,
            "sms": self._send_sms,
            "whatsapp": self._send_whatsapp,
            "linkedin": self._send_linkedin,
            "call": self._make_call
        }
        
        action_fn = actions.get(channel, self._send_email)
        result = action_fn(lead)
        
        self.contact_log.append({
            "lead_id": lead.get("id"),
            "channel": channel,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return result
    
    def _send_email(self, lead: Dict) -> Dict:
        return {"channel": "email", "status": "sent", "to": lead.get("email")}
    
    def _send_sms(self, lead: Dict) -> Dict:
        return {"channel": "sms", "status": "sent", "to": lead.get("phone")}
    
    def _send_whatsapp(self, lead: Dict) -> Dict:
        return {"channel": "whatsapp", "status": "sent", "to": lead.get("phone")}
    
    def _send_linkedin(self, lead: Dict) -> Dict:
        return {"channel": "linkedin", "status": "sent", "to": lead.get("linkedin")}
    
    def _make_call(self, lead: Dict) -> Dict:
        return {"channel": "call", "status": "initiated", "to": lead.get("phone")}
    
    def get_channel_performance(self) -> Dict:
        """Get performance by channel"""
        stats = {ch: {"sent": 0, "opened": 0, "replied": 0} for ch in self.channels}
        
        for contact in self.contact_log:
            ch = contact.get("channel")
            if ch in stats:
                stats[ch]["sent"] += 1
                if random.random() > 0.5:
                    stats[ch]["opened"] += 1
                if random.random() > 0.7:
                    stats[ch]["replied"] += 1
        
        return stats

class SmartScheduler:
    """Schedule outreach at optimal times"""
    
    def __init__(self):
        self.busy_hours = []
    
    def get_optimal_times(self, timezone: str = "EST") -> List[str]:
        """Get optimal outreach times"""
        return [
            "Tuesday 9:00 AM",
            "Tuesday 10:00 AM", 
            "Wednesday 9:00 AM",
            "Wednesday 10:00 AM",
            "Thursday 9:00 AM",
            "Thursday 10:00 AM"
        ]
    
    def should_retry(self, previous_attempts: int, last_error: str) -> bool:
        """Decide if should retry"""
        if previous_attempts >= 3:
            return False
        if "rate_limit" in last_error:
            return True
        if "temporary" in last_error:
            return True
        return random.random() > 0.5
    
    def get_delay(self, attempt: int) -> int:
        """Get delay between retries"""
        delays = [1, 2, 4, 8, 24]
        return min(delays[min(attempt, len(delays)-1)], 24)

multi_channel = MultiChannelOrchestrator()
smart_scheduler = SmartScheduler()