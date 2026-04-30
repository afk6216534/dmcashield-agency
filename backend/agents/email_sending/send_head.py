import uuid
import json
import smtplib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

from agents.memory.message_bus import MessageBus, create_alert_message
from agents.memory.persistent_memory import persistent_memory
from backend.database.models import EmailAccount
from agents.memory.agent_brain import memory_system
from agents.blockchain.blockchain_audit import blockchain_audit

class SendHeadAgent:
    def __init__(self):
        self.name = "SendHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["AccountBalancer", "ThrottleGuard", "SchedulerBot", "IPGuardian"]
        self.send_queue = []
        self.min_gap_seconds = 180
        self.max_gap_seconds = 420

    def receive_message(self, message):
        if message.message_type == "handoff":
            leads = message.payload.get("leads", [])
            task_id = message.payload.get("task_id")
            self.queue_leads_for_sending(leads, task_id)
        elif message.message_type == "instruction":
            action = message.payload.get("action")
            if action == "pause_all":
                self.pause_all_sending()
            elif action == "resume":
                self.resume_sending()

    def get_available_account(self, db) -> Optional[Dict]:
        from database.models import EmailAccount
        
        accounts = db.query(EmailAccount).filter(
            EmailAccount.status.in_(["active", "warmup"])
        ).all()
        
        available = []
        for acc in accounts:
            if acc.sent_today < acc.daily_limit:
                if acc.blacklist_status == "clean":
                    available.append({
                        "id": acc.id,
                        "email": acc.email_address,
                        "remaining": acc.daily_limit - acc.sent_today,
                        "warmup_day": acc.warmup_day
                    })
        
        if not available:
            return None
        
        available.sort(key=lambda x: (x["remaining"], -x["warmup_day"]))
        return available[0] if available else None

    def schedule_email(self, lead: Dict, email: Dict, account: Dict, send_time: datetime, db):
        from database.models import EmailRecord, Lead, Task
        
        record_id = str(uuid.uuid4())
        
        record = EmailRecord(
            id=record_id,
            lead_id=lead.get("lead_id"),
            task_id=lead.get("task_id"),
            account_id=account["id"],
            email_number=email["step"],
            subject_line=email["subjects"][0],
            email_body=email["body"],
            status="pending",
            sent_at=send_time
        )
        
        db.add(record)
        
        lead_db = db.query(Lead).filter(Lead.id == lead.get("lead_id")).first()
        if lead_db:
            lead_db.assigned_account_id = account["id"]
            lead_db.updated_at = datetime.utcnow()
        
        task_db = db.query(Task).filter(Task.id == lead.get("task_id")).first()
        if task_db:
            task_db.leads_emailed += 1
        
        db.commit()
        
        self.send_queue.append({
            "record_id": record_id,
            "send_time": send_time,
            "lead": lead,
            "email": email,
            "account": account
        })
        
        self.send_queue.sort(key=lambda x: x["send_time"])
        
        return record_id


    def _create_html_email(self, body: str, lead: Dict) -> str:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; border-radius: 10px; color: white;">
                <h2 style="color: #e94560; margin-bottom: 20px;">DMCAShield</h2>
                <div style="background: white; color: #333; padding: 25px; border-radius: 8px; font-size: 16px; line-height: 1.6;">
                    {body.replace('\n\n', '</p><p style="margin: 15px 0;">').replace('\n', '<br>')}
                    <hr style="margin: 25px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 12px;">
                        P.S. If you're not interested, no worries — just hit delete. But if you are, 
                        I'd love to show you exactly how we can help your {lead.get('business_name', 'business')}.
                    </p>
                </div>
                <div style="margin-top: 20px; text-align: center; color: #888; font-size: 12px;">
                    © 2026 DMCAShield Agency | Remove negative reviews legally
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def queue_leads_for_sending(self, leads: List[Dict], task_id: str):
        from database.models import SessionLocal, EmailAccount, Task
        
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "active"
                task.phase_sending = "in_progress"
                db.commit()
            
            current_time = datetime.utcnow()
            accounts = db.query(EmailAccount).filter(EmailAccount.status == "active").all()
            
            if not accounts:
                alert = create_alert_message(
                    from_agent=self.name,
                    to_agent="CEO",
                    alert_text="No email accounts available for sending",
                    details={"task_id": task_id}
                )
                self.message_bus.messages.append(alert)
                self._save_messages()
                return
            
            account_map = {acc.id: acc for acc in accounts}
            
            for lead in leads:
                if not lead.get("email_primary"):
                    continue
                
                email_sequence = lead.get("email_sequence", [])
                assigned_account = None
                
                for email in email_sequence:
                    day_offset = email.get("day", 1)
                    send_time = current_time + timedelta(days=day_offset)
                    send_time = send_time.replace(
                        hour=random.randint(9, 11),
                        minute=random.randint(0, 59)
                    )
                    
                    if not assigned_account:
                        for acc_id, acc in account_map.items():
                            if acc.sent_today < acc.daily_limit:
                                assigned_account = {"id": acc_id, "email": acc.email_address}
                                break
                    
                    if assigned_account:
                        self.schedule_email(lead, email, assigned_account, send_time, db)
            
            self.brain.remember(
                f"Queued emails for {len(leads)} leads in task {task_id}",
                "emails_queued"
            )
            
        finally:
            db.close()

    def process_queue(self):
        from database.models import SessionLocal, EmailRecord, EmailAccount
        
        db = SessionLocal()
        try:
            current_time = datetime.utcnow()
            pending = [item for item in self.send_queue 
                      if item["send_time"] <= current_time and item["email"].get("status") == "pending"]
            
            for item in pending[:10]:
                account = {
                    "id": item["account"]["id"],
                    "email": item["account"]["email"],
                    "app_password": "xxxx"
                }
                
                acc = db.query(EmailAccount).filter(EmailAccount.id == account["id"]).first()
                if acc and acc.sent_today < acc.daily_limit:
                    success = self.send_email(
                        item["record_id"],
                        item["lead"],
                        item["email"],
                        account
                    )
                    
                    if success:
                        acc.sent_today += 1
                        acc.total_sent += 1
                        acc.last_used = datetime.utcnow()
                        
                        record = db.query(EmailRecord).filter(EmailRecord.id == item["record_id"]).first()
                        if record:
                            record.status = "sent"
                        
                        db.commit()
                        
                        item["email"]["status"] = "sent"
                
                time.sleep(random.randint(self.min_gap_seconds, self.max_gap_seconds))
                
        finally:
            db.close()

    def pause_all_sending(self):
        self.send_queue = []
        self.brain.remember("All sending paused", "system_control")

    def resume_sending(self):
        self.brain.remember("Sending resumed", "system_control")

    def _save_messages(self):
        self.message_bus._save_messages()

    def start(self):
        return {"status": "online", "team": self.team, "queue_size": len(self.send_queue)}

send_head = SendHeadAgent()