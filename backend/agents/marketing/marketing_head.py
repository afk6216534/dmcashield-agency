import uuid
import json
from datetime import datetime
from typing import Dict, List, Any
import re

from agents.memory.message_bus import MessageBus, create_handoff_message
from agents.memory.agent_brain import memory_system

class MarketingHeadAgent:
    def __init__(self):
        self.name = "MarketingHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.sub_departments = {
            "intelligence": IntelHeadAgent(),
            "funnel": FunnelHeadAgent(),
            "copywriting": CopyHeadAgent(),
            "qa": QAHeadAgent(),
            "competitive": CompetitorHeadAgent()
        }

    def receive_message(self, message):
        if message.message_type == "handoff":
            leads = message.payload.get("leads", [])
            task_id = message.payload.get("task_id")
            self.process_leads(leads, task_id)

    def process_leads(self, leads: List[Dict], task_id: str):
        self.brain.remember(f"Marketing processing {len(leads)} leads", "marketing_start")
        
        for lead in leads:
            intel = self.sub_departments["intelligence"].analyze_lead(lead)
            funnel = self.sub_departments["funnel"].design_funnel(lead, intel)
            emails = self.sub_departments["copywriting"].write_emails(lead, intel, funnel)
            validated_emails = self.sub_departments["qa"].check_emails(emails)
            lead["email_sequence"] = validated_emails
            lead["funnel"] = funnel
        
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.phase_funnel = "complete"
                db.commit()
        finally:
            db.close()
        
        handoff = create_handoff_message(
            from_agent=self.name,
            to_agent="SendHead",
            leads=leads,
            task_id=task_id,
            notes=f"{len(leads)} leads with personalized email sequences ready"
        )
        self.message_bus.messages.append(handoff)
        self._save_messages()

    def _save_messages(self):
        self.message_bus._save_messages()

    def start(self):
        return {"status": "online", "sub_departments": list(self.sub_departments.keys())}

class IntelHeadAgent:
    def __init__(self):
        self.name = "IntelHead"
        self.brain = memory_system.get_brain(self.name)

    def analyze_lead(self, lead: Dict) -> Dict:
        intel = {
            "lead_id": lead.get("lead_id", str(uuid.uuid4())),
            "pain_points": lead.get("enrichment_data", {}).get("pain_points", []),
            "emotional_triggers": lead.get("enrichment_data", {}).get("emotional_triggers", {}),
            "strongest_trigger": "fear",
            "personalization_hooks": lead.get("enrichment_data", {}).get("personalization_hooks", []),
            "competitors": lead.get("competitor_info", {}).get("competitors", []),
            "rating_gap": lead.get("competitor_info", {}).get("your_rating_gap", 0),
            "tone": lead.get("enrichment_data", {}).get("tone", "professional"),
            "send_schedule": lead.get("enrichment_data", {}).get("send_schedule", {"days": [1, 2, 3], "hours": [9, 10, 11]})
        }
        
        if lead.get("worst_reviews"):
            intel["pain_points"].append(f"Reviews like: '{lead['worst_reviews'][0][:100]}...'")
        
        if intel["rating_gap"] > 1.5:
            intel["strongest_trigger"] = "fear"
        elif len(intel["competitors"]) > 2:
            intel["strongest_trigger"] = "urgency"
        else:
            intel["strongest_trigger"] = "greed"
        
        self.brain.remember(
            f"Analyzed lead {intel['lead_id']}: strongest trigger = {intel['strongest_trigger']}",
            "intel_analysis"
        )
        
        return intel

class FunnelHeadAgent:
    def __init__(self):
        self.name = "FunnelHead"
        self.brain = memory_system.get_brain(self.name)
        self.learned_patterns = self.brain.recall("funnel patterns", limit=10)

    def design_funnel(self, lead: Dict, intel: Dict) -> Dict:
        funnel = {
            "funnel_id": str(uuid.uuid4()),
            "lead_id": intel["lead_id"],
            "total_steps": 6,
            "steps": [
                {
                    "step": 1,
                    "day": 1,
                    "subject_angle": "curiosity",
                    "body_angle": "cold_intro",
                    "emotional_focus": intel.get("strongest_trigger", "fear"),
                    "cta": "curious about their situation"
                },
                {
                    "step": 2,
                    "day": 3,
                    "subject_angle": "social_proof",
                    "body_angle": "case_study",
                    "emotional_focus": "trust",
                    "cta": "see how we helped similar businesses"
                },
                {
                    "step": 3,
                    "day": 6,
                    "subject_angle": "fear_trigger",
                    "body_angle": "what_happens_if_ignored",
                    "emotional_focus": "fear",
                    "cta": "realize the cost of inaction"
                },
                {
                    "step": 4,
                    "day": 10,
                    "subject_angle": "value_offer",
                    "body_angle": "free_audit",
                    "emotional_focus": "greed",
                    "cta": "get a free reputation audit"
                },
                {
                    "step": 5,
                    "day": 15,
                    "subject_angle": "scarcity",
                    "body_angle": "last_chance",
                    "emotional_focus": "urgency",
                    "cta": "limited time offer"
                },
                {
                    "step": 6,
                    "day": 21,
                    "subject_angle": "breakup",
                    "body_angle": "reverse_psychology",
                    "emotional_focus": "fear",
                    "cta": "final goodbye"
                }
            ]
        }
        
        self.brain.remember(f"Designed funnel for lead {intel['lead_id']}", "funnel_created")
        return funnel

class CopyHeadAgent:
    def __init__(self):
        self.name = "CopyHead"
        self.brain = memory_system.get_brain(self.name)

    def write_emails(self, lead: Dict, intel: Dict, funnel: Dict) -> List[Dict]:
        emails = []
        
        for step in funnel["steps"]:
            email = self._write_single_email(lead, intel, step)
            if email:
                emails.append(email)
        
        return emails

    def _write_single_email(self, lead: Dict, intel: Dict, step: Dict) -> Dict:
        business_name = lead.get("business_name", "your business")
        owner_name = lead.get("owner_name", "there")
        rating_gap = intel.get("rating_gap", 1.5)
        competitor = intel.get("competitors", [{}])[0].get("name", "competitors")
        
        templates = {
            "cold_intro": {
                "subjects": [
                    f"Quick question about {business_name}",
                    f"{business_name} - one question",
                    f"Saw something interesting about {business_name}"
                ],
                "body": f"""Hi {owner_name},

I came across {business_name} while researching local businesses, and I noticed something that might interest you.

Most businesses like yours are losing customers every single month due to a handful of negative reviews online. The worst part? Most of them don't even know it's happening.

A quick question: have you ever tried to remove a fake or unfair Google review before?

I'd love to chat for 5 minutes if you're open to it.

Best,
Michael"""
            },
            "social_proof": {
                "subjects": [
                    f"Re: Quick question about {business_name}",
                    f"How we helped {competitor}",
                    f"Similar business, different result"
                ],
                "body": f"""Hi {owner_name},

Following up on my last email.

We recently helped a {lead.get('niche', 'business')} in {lead.get('city', 'your area')} remove 12 negative reviews in 3 weeks.

Result? Their Google rating went from {lead.get('current_rating', 3.0):.1f} to 4.6 stars.

Want to see how we did it?

Best,
Michael"""
            },
            "what_happens_if_ignored": {
                "subjects": [
                    f"What happens if negative reviews keep piling up?",
                    f"Don't ignore this about {business_name}",
                    f"The snowball effect of bad reviews"
                ],
                "body": f"""Hi {owner_name},

Here's what I see happening with businesses that don't address their negative reviews:

Month 1: 3 negative reviews → 15 potential customers click away
Month 3: 7 negative reviews → 40 potential customers lost
Month 6: 12 negative reviews → Business is bleeding

Your competitors at {competitor}? They've already figured this out.

The longer you wait, the harder it gets.

Best,
Michael"""
            },
            "free_audit": {
                "subjects": [
                    f"Free reputation audit for {business_name}",
                    f"{business_name} - complimentary review analysis",
                    f"Can I show you something about your Google listing?"
                ],
                "body": f"""Hi {owner_name},

I'll cut to the chase.

I want to give you a FREE reputation audit for {business_name}. 

I'll show you:
- Which reviews can be legally removed
- What your competitors are doing differently
- A clear action plan to get to 4.5+ stars

No obligation. Just valuable information.

Ready to see what's possible?

Best,
Michael"""
            },
            "last_chance": {
                "subjects": [
                    f"Last chance - {business_name}",
                    f"One more thing before I move on",
                    f"Saving this for {business_name} only"
                ],
                "body": f"""Hi {owner_name},

I don't usually do this, but I'm closing out this campaign.

If you're still interested in improving {business_name}'s reputation, this is your last chance to claim a free audit.

After this email, I'll be focusing on other businesses in {lead.get('city', 'your area')}.

But I genuinely believe I can help you.

Best,
Michael"""
            },
            "reverse_psychology": {
                "subjects": [
                    f"You know what? Forget {business_name}",
                    f"Okay, I'm done",
                    f"Last email about {business_name}, I promise"
                ],
                "body": f"""Hi {owner_name},

You know what? I get it. You're busy. You have better things to do than respond to cold emails.

You're right to be skeptical. Most "reputation management" services are garbage.

But if you're ever sitting around wondering "what if I had fixed those reviews"...

You know where to find me.

Best,
Michael"""
            }
        }
        
        angle = step.get("body_angle", "cold_intro")
        template = templates.get(angle, templates["cold_intro"])
        
        return {
            "step": step["step"],
            "day": step["day"],
            "subjects": template["subjects"],
            "body": template["body"],
            "angle": angle,
            "emotional_focus": step.get("emotional_focus"),
            "cta": step.get("cta"),
            "status": "ready"
        }

class QAHeadAgent:
    def __init__(self):
        self.name = "QAHead"
        self.brain = memory_system.get_brain(self.name)
        self.spam_words = ["free", "guarantee", "winner", "congratulations", "urgent", "act now", "limited time"]

    def check_emails(self, emails: List[Dict]) -> List[Dict]:
        validated = []
        seen_subjects = set()
        
        for email in emails:
            issues = []
            
            body_lower = email["body"].lower()
            for word in self.spam_words:
                if word in body_lower:
                    issues.append(f"Spam word found: {word}")
            
            for subj in email["subjects"]:
                if subj.lower() in seen_subjects:
                    issues.append(f"Duplicate subject: {subj}")
                seen_subjects.add(subj.lower())
            
            if len(email["body"].split()) > 250:
                issues.append("Email too long (over 250 words)")
            
            if "{{" in email["body"] or "}}" in email["body"]:
                issues.append("Contains unfilled personalization tokens")
            
            email["issues"] = issues
            email["status"] = "approved" if not issues else "needs_review"
            validated.append(email)
        
        return validated

class CompetitorHeadAgent:
    def __init__(self):
        self.name = "CompetitorHead"
        self.brain = memory_system.get_brain(self.name)

    def track_trends(self):
        trends = self.brain.recall("email trends", limit=20)
        return trends

    def report_insights(self, insights: Dict):
        self.brain.learn(
            f"Market insight: {insights.get('summary', 'New insight')}",
            category="market_trends"
        )

marketing_head = MarketingHeadAgent()