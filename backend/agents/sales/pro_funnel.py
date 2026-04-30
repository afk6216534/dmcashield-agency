"""
PROFESSIONAL SALES FUNNEL SYSTEM
================================
Complete automated funnel with stages, automation, and tracking
"""

import uuid
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class FunnelStage(str, Enum):
    """Professional funnel stages"""
    AWARENESS = "awareness"           # Lead becomes aware
    INTEREST = "interest"               # Lead shows interest
    CONSIDERATION = "consideration"    # Lead considers offer
    INTENT = "intent"                   # Lead intends to buy
    EVALUATION = "evaluation"           # Lead evaluates
    PURCHASE = "purchase"              # Lead converts
    RETENTION = "retention"             # Keep customer
    ADVOCACY = "advocacy"              # Customer refers others

class FunnelAction(str, Enum):
    """Actions that can happen in funnel"""
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    WAIT = "wait"
    CONDITION = "condition"
    WEBHOOK = "webhook"
    UPDATE_SCORE = "update_score"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    CREATE_TASK = "create_task"
    NOTIFY = "notify"

@dataclass
class FunnelStep:
    """Individual step in funnel"""
    step_id: str
    name: str
    stage: FunnelStage
    action: FunnelAction
    config: Dict[str, Any]
    delay_days: int = 0
    delay_hours: int = 0

@dataclass 
class Funnel:
    """Complete funnel definition"""
    funnel_id: str
    name: str
    description: str
    industry: str
    steps: List[FunnelStep]
    entry_score: int = 50
    exit_score: int = 90
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    stats: Dict[str, Any] = field(default_factory=dict)

class ProfessionalFunnelEngine:
    """
    Professional funnel engine with automation
    """
    
    def __init__(self, persist_file: str = "data/pro_funnel.json"):
        self.persist_file = persist_file
        self.funnels = self._load()
        self.active_leads = {}  # lead_id -> funnel progress
        
    def _load(self) -> Dict:
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"funnels": {}, "active_leads": {}}
    
    def _save(self):
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump(self.funnels, f, indent=2)
    
    def create_funnel(self, name: str, description: str, industry: str) -> str:
        """Create new professional funnel"""
        funnel_id = f"funnel_{uuid.uuid4().hex[:8]}"
        
        # Create default professional steps
        steps = self._create_default_steps(industry)
        
        funnel = Funnel(
            funnel_id=funnel_id,
            name=name,
            description=description,
            industry=industry,
            steps=steps,
            stats={
                "total_entered": 0,
                "completed": 0,
                "converted": 0,
                "dropped": 0
            }
        )
        
        self.funnels["funnels"][funnel_id] = {
            "funnel_id": funnel_id,
            "name": name,
            "description": description,
            "industry": industry,
            "steps": [{"step_id": s.step_id, "name": s.name, "stage": s.stage, "action": s.action, "config": s.config} for s in steps],
            "is_active": True,
            "stats": funnel.stats
        }
        
        self._save()
        return funnel_id
    
    def _create_default_steps(self, industry: str) -> List[FunnelStep]:
        """Create professional default steps"""
        
        if industry == "dmca":
            steps = [
                # AWARENESS
                FunnelStep(
                    step_id="step_1",
                    name="Welcome Email - Problem Awareness",
                    stage=FunnelStage.AWARENESS,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "Did you know you can remove those negative reviews?",
                        "template": "awareness_1"
                    },
                    delay_hours=0
                ),
                # INTEREST  
                FunnelStep(
                    step_id="step_2",
                    name="Case Study - Proof",
                    stage=FunnelStage.INTEREST,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "How we helped [business] remove 15 fake reviews",
                        "template": "case_study"
                    },
                    delay_days=2
                ),
                # CONSIDERATION
                FunnelStep(
                    step_id="step_3",
                    name="Free Consultation Offer",
                    stage=FunnelStage.CONSIDERATION,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "Free review analysis - worth $197",
                        "template": "free_consultation"
                    },
                    delay_days=3
                ),
                # INTENT
                FunnelStep(
                    step_id="step_4",
                    name="Social Proof - Testimonials",
                    stage=FunnelStage.INTENT,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "See what other business owners say",
                        "template": "testimonials"
                    },
                    delay_days=2
                ),
                # EVALUATION
                FunnelStep(
                    step_id="step_5",
                    name="Special Offer - Limited Time",
                    stage=FunnelStage.EVALUATION,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "50% off - 24 hours only",
                        "template": "special_offer"
                    },
                    delay_days=3
                ),
                # PURCHASE
                FunnelStep(
                    step_id="step_6",
                    name="Final Call - Urgency",
                    stage=FunnelStage.PURCHASE,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "Your offer expires tonight",
                        "template": "final_call"
                    },
                    delay_days=1
                ),
                # RETENTION
                FunnelStep(
                    step_id="step_7",
                    name="Welcome & Onboarding",
                    stage=FunnelStage.RETENTION,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "Welcome to DMCAShield!",
                        "template": "welcome"
                    },
                    delay_days=1
                ),
                # ADVOCACY
                FunnelStep(
                    step_id="step_8",
                    name="Referral Program",
                    stage=FunnelStage.ADVOCACY,
                    action=FunnelAction.SEND_EMAIL,
                    config={
                        "subject": "Invite friends, earn rewards",
                        "template": "referral"
                    },
                    delay_days=7
                )
            ]
        else:
            # Generic business funnel
            steps = [
                FunnelStep("step_1", "Welcome", FunnelStage.AWARENESS, FunnelAction.SEND_EMAIL, {"subject": "Welcome!"}, 0),
                FunnelStep("step_2", "Value", FunnelStage.INTEREST, FunnelAction.SEND_EMAIL, {"subject": "Here's value for you"}, 2),
                FunnelStep("step_3", "Offer", FunnelStage.CONSIDERATION, FunnelAction.SEND_EMAIL, {"subject": "Special offer"}, 3),
                FunnelStep("step_4", "Close", FunnelStage.PURCHASE, FunnelAction.SEND_EMAIL, {"subject": "Last chance"}, 2),
            ]
        
        return steps
    
    def enroll_lead(self, funnel_id: str, lead_id: str, lead_data: Dict) -> Dict:
        """Enroll lead in funnel"""
        funnel = self.funnels["funnels"].get(funnel_id)
        if not funnel:
            return {"error": "Funnel not found"}
        
        # Initialize lead progress
        self.active_leads[lead_id] = {
            "funnel_id": funnel_id,
            "current_step": 0,
            "started_at": datetime.utcnow().isoformat(),
            "lead_data": lead_data,
            "stage": FunnelStage.AWARENESS.value,
            "completed_steps": [],
            "emails_sent": []
        }
        
        # Update stats
        funnel["stats"]["total_entered"] = funnel["stats"].get("total_entered", 0) + 1
        
        self._save()
        
        return {
            "enrolled": True,
            "lead_id": lead_id,
            "funnel_id": funnel_id,
            "first_step": funnel["steps"][0]["name"] if funnel["steps"] else None
        }
    
    def process_lead_step(self, lead_id: str) -> Optional[Dict]:
        """Process next step for lead"""
        if lead_id not in self.active_leads:
            return None
        
        lead_progress = self.active_leads[lead_id]
        funnel_id = lead_progress["funnel_id"]
        funnel = self.funnels["funnels"].get(funnel_id)
        
        if not funnel:
            return None
        
        current_step_index = lead_progress["current_step"]
        steps = funnel["steps"]
        
        if current_step_index >= len(steps):
            return {"status": "completed"}
        
        # Get current step
        step = steps[current_step_index]
        
        # Simulate sending email
        result = {
            "lead_id": lead_id,
            "step": step["name"],
            "stage": step["stage"],
            "action": step["action"],
            "sent_at": datetime.utcnow().isoformat()
        }
        
        # Record email sent
        lead_progress["emails_sent"].append(result)
        lead_progress["completed_steps"].append(step["step_id"])
        
        # Move to next step
        lead_progress["current_step"] += 1
        lead_progress["stage"] = step["stage"]
        
        # Check if converted
        if step["stage"] == FunnelStage.PURCHASE.value:
            funnel["stats"]["converted"] = funnel["stats"].get("converted", 0) + 1
        
        self._save()
        
        return result
    
    def get_lead_progress(self, lead_id: str) -> Optional[Dict]:
        """Get lead's progress in funnel"""
        if lead_id not in self.active_leads:
            return None
        
        return self.active_leads[lead_id]
    
    def get_funnel_stats(self, funnel_id: str) -> Optional[Dict]:
        """Get funnel statistics"""
        funnel = self.funnels["funnels"].get(funnel_id)
        if not funnel:
            return None
        
        stats = funnel.get("stats", {})
        total = stats.get("total_entered", 1)
        
        # Calculate conversion rate
        if total > 0:
            conversion_rate = (stats.get("converted", 0) / total) * 100
        else:
            conversion_rate = 0
        
        return {
            "funnel_id": funnel_id,
            "name": funnel["name"],
            "total_entered": total,
            "converted": stats.get("converted", 0),
            "conversion_rate": f"{conversion_rate:.1f}%",
            "active_leads": sum(1 for lp in self.active_leads.values() if lp["funnel_id"] == funnel_id),
            "steps": len(funnel.get("steps", []))
        }
    
    def list_funnels(self) -> List[Dict]:
        """List all funnels"""
        return [
            {"funnel_id": k, **v} 
            for k, v in self.funnels["funnels"].items()
        ]
    
    def get_funnel_leads(self, funnel_id: str) -> List[Dict]:
        """Get all leads in funnel"""
        return [
            {"lead_id": k, **v}
            for k, v in self.active_leads.items()
            if v.get("funnel_id") == funnel_id
        ]
    
    def move_to_stage(self, lead_id: str, stage: str) -> bool:
        """Manually move lead to specific stage"""
        if lead_id in self.active_leads:
            self.active_leads[lead_id]["stage"] = stage
            self._save()
            return True
        return False
    
    def remove_lead(self, lead_id: str) -> bool:
        """Remove lead from funnel"""
        if lead_id in self.active_leads:
            funnel_id = self.active_leads[lead_id]["funnel_id"]
            funnel = self.funnels["funnels"].get(funnel_id)
            
            if funnel:
                funnel["stats"]["dropped"] = funnel["stats"].get("dropped", 0) + 1
            
            del self.active_leads[lead_id]
            self._save()
            return True
        return False

# Initialize
funnel_engine = ProfessionalFunnelEngine()

# Create default DMCA funnel
DEFAULT_FUNNELS = [
    {
        "name": "DMCA Removal Service",
        "description": "Complete funnel for DMCA negative review removal service",
        "industry": "dmca"
    },
    {
        "name": "Lead Magnet - Free Report", 
        "description": "Lead generation funnel with free report",
        "industry": "lead_gen"
    },
    {
        "name": "Consultation Booking",
        "description": "Book a consultation call",
        "industry": "consulting"
    }
]

def init_default_funnels():
    """Initialize default funnels"""
    for f in DEFAULT_FUNNELS:
        funnel_engine.create_funnel(f["name"], f["description"], f["industry"])

init_default_funnels()