import uuid
from datetime import datetime
from typing import Dict, List, Any

from agents.memory.message_bus import MessageBus
from agents.memory.agent_brain import memory_system

class AccountHeadAgent:
    def __init__(self):
        self.name = "AccountHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["WarmupBot", "HealthMonitor", "CapacityPlanner", "UISync"]

    def receive_message(self, message):
        if message.message_type == "instruction":
            action = message.payload.get("action")
            if action == "add_account":
                self.add_account(message.payload)
            elif action == "check_health":
                self.check_account_health(message.payload.get("account_id"))

    def add_account(self, payload: Dict):
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            account_id = f"acc-{uuid.uuid4().hex[:8]}"
            
            warmup_schedule = {
                "day_1_7": 5,
                "day_8_14": 10,
                "day_15_21": 20,
                "day_22_plus": 40
            }
            
            account = EmailAccount(
                id=account_id,
                email_address=payload.get("email_address"),
                app_password_encrypted=payload.get("app_password"),
                display_name=payload.get("display_name", payload.get("email_address").split("@")[0]),
                status="warmup",
                warmup_day=0,
                warmup_schedule=warmup_schedule
            )
            
            db.add(account)
            db.commit()
            
            self.brain.remember(
                f"Email account added: {payload.get('email_address')}",
                "account_added"
            )
            
            self.message_bus.send_message(
                from_agent=self.name,
                to_agent="WarmupBot",
                message_type="instruction",
                payload={"action": "start_warmup", "account_id": account_id}
            )
            
            return account_id
        finally:
            db.close()

    def check_account_health(self, account_id: str):
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            account = db.query(EmailAccount).filter(EmailAccount.id == account_id).first()
            if not account:
                return
            
            health_score = 100.0
            
            if account.sent_today >= account.daily_limit:
                health_score -= 30
            elif account.sent_today >= account.daily_limit * 0.8:
                health_score -= 15
            
            if account.blacklist_status != "clean":
                health_score -= 50
            
            if account.warmup_day < 14:
                health_score -= (14 - account.warmup_day) * 2
            
            account.health_score = max(health_score, 0)
            
            if account.health_score < 30:
                account.status = "paused"
                
                alert = {
                    "alert": f"Account health critical: {account.email_address}",
                    "details": {"account_id": account_id, "health_score": account.health_score}
                }
                self.message_bus.send_message(
                    from_agent=self.name,
                    to_agent="CEO",
                    message_type="alert",
                    payload=alert
                )
            
            db.commit()
            
        finally:
            db.close()

    def get_all_accounts(self) -> List[Dict]:
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            accounts = db.query(EmailAccount).order_by(EmailAccount.created_at.desc()).all()
            return [
                {
                    "id": a.id,
                    "email_address": a.email_address,
                    "display_name": a.display_name,
                    "status": a.status,
                    "daily_limit": a.daily_limit,
                    "sent_today": a.sent_today,
                    "warmup_day": a.warmup_day,
                    "health_score": a.health_score,
                    "blacklist_status": a.blacklist_status,
                    "total_sent": a.total_sent,
                    "last_used": a.last_used.isoformat() if a.last_used else None
                }
                for a in accounts
            ]
        finally:
            db.close()

    def reset_daily_counts(self):
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            accounts = db.query(EmailAccount).filter(EmailAccount.status == "active").all()
            for account in accounts:
                account.sent_today = 0
            db.commit()
        finally:
            db.close()

    def start(self):
        return {"status": "online", "team": self.team}

account_head = AccountHeadAgent()