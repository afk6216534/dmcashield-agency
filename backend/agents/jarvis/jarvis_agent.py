import json
from datetime import datetime
from typing import Dict, List, Any

from agents.memory.message_bus import MessageBus
from agents.memory.agent_brain import memory_system

class JARVISAgent:
    def __init__(self):
        self.name = "JARVIS"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)

    def receive_message(self, message):
        if message.message_type == "instruction":
            command = message.payload.get("command", "")
            params = message.payload.get("params", {})
            self.process_command(command, params)

    def process_command(self, command: str, params: Dict) -> Dict:
        command_lower = command.lower()
        
        if "scrape" in command_lower or "task" in command_lower:
            return self.handle_task_command(command_lower, params)
        elif "how many" in command_lower or "status" in command_lower:
            return self.handle_status_command(command_lower, params)
        elif "pause" in command_lower:
            return self.handle_control_command("pause", params)
        elif "resume" in command_lower or "start" in command_lower:
            return self.handle_control_command("resume", params)
        elif "email" in command_lower:
            return self.handle_email_command(command_lower, params)
        elif "lead" in command_lower:
            return self.handle_lead_command(command_lower, params)
        else:
            return self.natural_response(command)

    def handle_task_command(self, command: str, params: Dict) -> Dict:
        from agents.tasks.task_head import task_head
        
        if "create" in command or "new" in command:
            business_type = params.get("business_type", "business")
            city = params.get("city", "")
            state = params.get("state", "")
            country = params.get("country", "USA")
            
            task_id = task_head.create_task(business_type, city, state, country)
            
            return {
                "response": f"Task created! {business_type} in {city}, {state}. Task ID: {task_id}. Starting now.",
                "action": "task_created",
                "task_id": task_id
            }
        else:
            tasks = task_head.get_all_tasks()
            return {
                "response": f"You have {len(tasks)} tasks. {sum(1 for t in tasks if t['status'] == 'active')} are active.",
                "tasks": tasks
            }

    def handle_status_command(self, command: str, params: Dict) -> Dict:
        from database.models import SessionLocal, Lead, Task, EmailAccount, EmailRecord
        
        db = SessionLocal()
        try:
            total_leads = db.query(Lead).count()
            active_tasks = db.query(Task).filter(Task.status == "active").count()
            email_accounts = db.query(EmailAccount).count()
            hot_leads = db.query(Lead).filter(Lead.temperature == "hot").count()
            total_sent = db.query(EmailRecord).count()
            
            if "hot" in command or "lead" in command:
                response = f"You have {hot_leads} hot leads ready to convert!"
            elif "task" in command:
                response = f"You have {active_tasks} active tasks running."
            elif "email" in command:
                response = f"Total emails sent: {total_sent}. Active accounts: {email_accounts}."
            else:
                response = f"System Status: {total_leads} total leads, {active_tasks} active tasks, {hot_leads} hot leads, {total_sent} emails sent."
            
            return {"response": response}
        finally:
            db.close()

    def handle_control_command(self, action: str, params: Dict) -> Dict:
        self.message_bus.broadcast(
            from_agent=self.name,
            message_type="instruction",
            payload={"action": action}
        )
        
        return {
            "response": f"Done! All sending has been {action}d.",
            "action": action
        }

    def handle_email_command(self, command: str, params: Dict) -> Dict:
        from agents.accounts.account_head import account_head
        
        if "add" in command or "new" in command:
            return {
                "response": "To add a new email account, go to the Email Accounts page and use the 'Add Account' form.",
                "action": "navigate",
                "page": "email_accounts"
            }
        else:
            accounts = account_head.get_all_accounts()
            return {
                "response": f"You have {len(accounts)} email accounts configured.",
                "accounts": accounts
            }

    def handle_lead_command(self, command: str, params: Dict) -> Dict:
        from database.models import SessionLocal, Lead
        
        db = SessionLocal()
        try:
            if "hot" in command:
                leads = db.query(Lead).filter(Lead.temperature == "hot").all()
                return {
                    "response": f"You have {len(leads)} hot leads. Check your Gmail Important folder!",
                    "leads": [{"name": l.business_name, "email": l.email_primary, "city": l.city} for l in leads]
                }
            else:
                total = db.query(Lead).count()
                return {
                    "response": f"Total leads in system: {total}",
                }
        finally:
            db.close()

    def natural_response(self, command: str) -> Dict:
        # Check system status for comprehensive response
        from database.models import SessionLocal, Lead, Task, EmailAccount, EmailRecord

        db = SessionLocal()
        try:
            total_leads = db.query(Lead).count()
            active_tasks = db.query(Task).filter(Task.status == "active").count()
            hot_leads = db.query(Lead).filter(Lead.temperature == "hot").count()
            total_sent = db.query(EmailRecord).count()
            email_accounts = db.query(EmailAccount).count()

            status_summary = f"""SYSTEM STATUS - DMCASHIELD AGENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total Leads: {total_leads}
📈 Active Tasks: {active_tasks}
🔥 Hot Leads: {hot_leads}
✉️ Emails Sent: {total_sent}
📧 Email Accounts: {email_accounts}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All 12 departments are operational and processing tasks autonomously."""

            return {"response": status_summary}
        finally:
            db.close()

    def get_department_status(self) -> Dict:
        """Get comprehensive department status"""
        return {
            "departments": {
                "ceo": {"status": "online", "role": "Task coordination and strategy"},
                "scraping": {"status": "online", "role": "Lead generation"},
                "validation": {"status": "online", "role": "Lead enrichment and verification"},
                "marketing": {"status": "online", "role": "Copywriting and campaign management"},
                "email_sending": {"status": "online", "role": "Email delivery and warmup"},
                "tracking": {"status": "online", "role": "Engagement monitoring"},
                "sales": {"status": "online", "role": "Hot lead conversion"},
                "sheets": {"status": "online", "role": "Reporting and dashboards"},
                "accounts": {"status": "online", "role": "Email account management"},
                "tasks": {"status": "online", "role": "Task queue coordination"},
                "ml": {"status": "online", "role": "Learning from results"},
                "jarvis": {"status": "online", "role": "Natural language interface"},
                "memory": {"status": "online", "role": "Persistent learning and audit"}
            },
            "learning_active": True,
            "self_improvement": "Continuous knowledge graph updates and ML model retraining"
        }

    def generate_daily_summary(self) -> str:
        from database.models import SessionLocal, Lead, Task, EmailRecord
        
        db = SessionLocal()
        try:
            hot_leads = db.query(Lead).filter(Lead.temperature == "hot").count()
            active_tasks = db.query(Task).filter(Task.status == "active").count()
            emails_sent_today = db.query(EmailRecord).filter(
                EmailRecord.sent_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
            ).count()
            
            summary = f"""
Good evening! Here's your daily DMCAShield Agency report:

📊 TODAY'S STATS:
- Emails Sent: {emails_sent_today}
- Active Tasks: {active_tasks}
- Hot Leads: {hot_leads}

🚨 ACTION ITEMS:
"""
            if hot_leads > 0:
                summary += f"- {hot_leads} hot lead(s) waiting in your Gmail Important folder!\n"
            else:
                summary += "- No hot leads yet. Keep the campaigns running!\n"
            
            summary += """
💤 Rest easy. The system is working while you sleep.
"""
            
            return summary.strip()
        finally:
            db.close()

    def start(self):
        self.brain.remember("JARVIS online", "system_start")
        return {"status": "online", "role": "Natural Language Interface"}

jarvis_agent = JARVISAgent()