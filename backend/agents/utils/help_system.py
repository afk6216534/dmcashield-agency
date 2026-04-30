import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import uuid

class TeamMember:
    def __init__(self, member_id: str, name: str, email: str, role: str = "member"):
        self.id = member_id
        self.name = name
        self.email = email
        self.role = role
        self.created_at = datetime.utcnow().isoformat()
        self.last_active = None
        self.permissions = []

class TeamCollaboration:
    def __init__(self, persist_file: str = "data/team.json"):
        self.persist_file = persist_file
        self.members: Dict[str, TeamMember] = {}
        self.activities: List[Dict] = []
        self._load()
    
    def _load(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    data = json.load(f)
                    for m in data.get("members", []):
                        self.members[m["id"]] = TeamMember(m["id"], m["name"], m["email"], m.get("role", "member"))
            except:
                pass
    
    def _save(self):
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump({
                "members": [m.__dict__ for m in self.members.values()]
            }, f, indent=2)
    
    def add_member(self, name: str, email: str, role: str = "member") -> str:
        member_id = f"member_{uuid.uuid4().hex[:8]}"
        member = TeamMember(member_id, name, email, role)
        self.members[member_id] = member
        self._save()
        return member_id
    
    def remove_member(self, member_id: str):
        if member_id in self.members:
            del self.members[member_id]
            self._save()
    
    def log_activity(self, member_id: str, action: str, details: Dict = None):
        self.activities.append({
            "member_id": member_id,
            "action": action,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        })
        self.activities = self.activities[-100:]
        
        if member_id in self.members:
            self.members[member_id].last_active = datetime.utcnow().isoformat()
            self._save()
    
    def get_activities(self, member_id: str = None) -> List[Dict]:
        if member_id:
            return [a for a in self.activities if a.get("member_id") == member_id]
        return self.activities
    
    def get_team_stats(self) -> Dict:
        return {
            "total_members": len(self.members),
            "active_today": sum(1 for m in self.members.values() 
                     if m.last_active and m.last_active > datetime.utcnow().isoformat()),
            "activities": len(self.activities)
        }

team_collaboration = TeamCollaboration()

class NotificationSystem:
    def __init__(self, persist_file: str = "data/notifications.json"):
        self.persist_file = persist_file
        self.notifications: List[Dict] = []
        self._load()
    
    def _load(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    self.notifications = json.load(f)
            except:
                pass
    
    def _save(self):
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump(self.notifications, f, indent=2)
    
    def send(self, title: str, message: str, notification_type: str = "info", 
          priority: str = "normal", link: str = None):
        notification = {
            "id": f"notif_{uuid.uuid4().hex[:8]}",
            "title": title,
            "message": message,
            "type": notification_type,
            "priority": priority,
            "link": link,
            "read": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.notifications.append(notification)
        self.notifications = self.notifications[-50:]
        self._save()
        return notification["id"]
    
    def mark_read(self, notification_id: str):
        for n in self.notifications:
            if n.get("id") == notification_id:
                n["read"] = True
                break
        self._save()
    
    def mark_all_read(self):
        for n in self.notifications:
            n["read"] = True
        self._save()
    
    def get_unread(self) -> List[Dict]:
        return [n for n in self.notifications if not n.get("read")]
    
    def get_all(self) -> List[Dict]:
        return self.notifications

notification_system = NotificationSystem()

class HelpGuide:
    def __init__(self):
        self.guides = {
            "getting_started": {
                "title": "Getting Started",
                "steps": [
                    {"order": 1, "title": "Add Email Account", "content": "Use /api/email-accounts to add your sender email with app password"},
                    {"order": 2, "title": "Start Warmup", "content": "Run warmup for 28 days to build sender reputation"},
                    {"order": 3, "title": "Create Task", "content": "Use /api/tasks to scrape leads for your niche"},
                    {"order": 4, "title": "Monitor Leads", "content": "Check /api/hot-leads for interested prospects"},
                    {"order": 5, "title": "Reply & Convert", "content": "Respond to leads and close deals!"}
                ]
            },
            "email_warmup": {
                "title": "Email Warmup Guide",
                "days": [
                    {"day": 1, "emails": 1, "tip": "Send to friends/family only"},
                    {"day": 7, "emails": 10, "tip": "Start professional emails"},
                    {"day": 14, "emails": 25, "tip": "Gradually increase volume"},
                    {"day": 28, "emails": 40, "tip": "Full capacity reached"}
                ]
            },
            "best_practices": {
                "title": "Best Practices",
                "tips": [
                    "Always warm up new email accounts for 28+ days",
                    "Monitor deliverability and open rates daily",
                    "Respond to leads within 1 hour",
                    "Use A/B testing for subject lines",
                    "Track all metrics in analytics dashboard",
                    "Keep lead scores above 50 for quality"
                ]
            }
        }
    
    def get_guide(self, guide_id: str) -> Dict:
        return self.guides.get(guide_id, {})
    
    def list_guides(self) -> List[Dict]:
        return [{"id": k, "title": v.get("title")} for k, v in self.guides.items()]

help_guide = HelpGuide()

class QuickStartWizard:
    def __init__(self):
        self.steps = []
    
    def get_startup_steps(self) -> List[Dict]:
        return [
            {
                "step": 1,
                "title": "Configure Email",
                "endpoint": "/api/email-accounts",
                "method": "POST",
                "body": {"email_address": "your@email.com", "app_password": "xxx"},
                "description": "Add your first email account with Gmail app password"
            },
            {
                "step": 2,
                "title": "Verify Setup",
                "endpoint": "/api/email-accounts",
                "method": "GET",
                "description": "Check your email account is active"
            },
            {
                "step": 3,
                "title": "Create First Task",
                "endpoint": "/api/tasks",
                "method": "POST",
                "body": {"business_type": "restaurant", "city": "Austin", "state": "TX"},
                "description": "Start scraping leads"
            },
            {
                "step": 4,
                "title": "Check Leads",
                "endpoint": "/api/leads",
                "method": "GET",
                "description": "View scraped leads"
            },
            {
                "step": 5,
                "title": "Send Emails",
                "endpoint": "/api/queue/process",
                "method": "POST",
                "description": "Process email queue"
            }
        ]
    
    def validate_step(self, step: int, result: Dict) -> bool:
        if step == 1:
            return bool(result.get("account_id"))
        elif step == 3:
            return bool(result.get("task_id"))
        elif step == 4:
            return len(result) > 0
        return True

quick_start = QuickStartWizard()

ERROR_MESSAGES = {
    "auth_failed": "Authentication failed. Check your API key.",
    "rate_limited": "Rate limit exceeded. Wait before retrying.",
    "email_failed": "Email send failed. Check SMTP credentials.",
    "scrape_failed": "Scraping failed. Try different sources.",
    "invalid_lead": "Lead data invalid. Check required fields.",
    "database_error": "Database error. Check connection.",
    "unauthorized": "Unauthorized. Please login first."
}

def get_error_message(error_code: str) -> str:
    return ERROR_MESSAGES.get(error_code, "An error occurred. Please try again.")

TROUBLESHOOTING = {
    "emails_not_sending": [
        "Check email account credentials",
        "Verify app password is correct",
        "Check daily limit not reached",
        "Verify account is warm enough"
    ],
    "leads_not_scraping": [
        "Check internet connection",
        "Try different business type",
        "Check city/state format",
        "Try different sources"
    ],
    "hot_leads_not_appearing": [
        "Wait for email responses",
        "Check spam folder",
        "Improve email content",
        "Lower lead score threshold"
    ]
}

def get_troubleshooting(issue: str) -> List[str]:
    return TROUBLESHOOTING.get(issue, ["Please contact support"])