import uuid
import random
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailWarmupManager:
    def __init__(self, warmup_file: str = "data/email_warmup.json"):
        self.warmup_file = warmup_file
        self.warmup_campaigns: Dict[str, Dict] = {}
        self._load()
        
        self.warmup_templates = [
            {"subject": "Quick question about your", "body": "Hi {name},\n\nHope you're having a great week! I had a quick question about your business...\n\nBest,\n{sender}"},
            {"subject": "Thought you'd want to see this", "body": "Hey {name},\n\nFound something you might like...\n\nCheers,\n{sender}"},
            {"subject": "Following up on our chat", "body": "Hi {name},\n\nJust following up on a previous conversation...\n\nBest,\n{sender}"},
            {"subject": "Quick favor - can you help?", "body": "Hey {name},\n\nGot a quick favor to ask - would you mind taking a look?\n\nThanks!\n{sender}"},
            {"subject": "Interesting article I found", "body": "Hi {name},\n\nFound this interesting and thought of you...\n\nBest,\n{sender}"},
            {"subject": "Your thoughts on this?", "body": "Hey {name},\n\nWould love to get your thoughts on this...\n\nThanks,\n{sender}"},
            {"subject": "Quick observation", "body": "Hi {name},\n\nQuick observation I wanted to share...\n\nBest,\n{sender}"},
            {"subject": "Following up", "body": "Hey {name},\n\nJust checking in - any thoughts?\n\n{sender}"}
        ]
        
        self.reply_templates = [
            "Thanks for the response! Let me think about this...",
            "Appreciate you getting back to me!",
            "That's interesting - tell me more.",
            "Got it! I'll follow up shortly.",
            "Thanks! I'll be in touch soon.",
            "Great hearing from you! Let's chat more."
        ]
    
    def _load(self):
        import os
        if os.path.exists(self.warmup_file):
            try:
                import json
                with open(self.warmup_file, 'r') as f:
                    self.warmup_campaigns = json.load(f)
            except:
                pass
    
    def _save(self):
        import os
        os.makedirs(os.path.dirname(self.warmup_file), exist_ok=True)
        import json
        with open(self.warmup_file, 'w') as f:
            json.dump(self.warmup_campaigns, f, indent=2)
    
    def start_warmup(self, account_id: str, credentials: Dict, warmup_days: int = 28) -> str:
        campaign_id = f"warmup_{account_id}"
        
        self.warmup_campaigns[campaign_id] = {
            "id": campaign_id,
            "account_id": account_id,
            "email": credentials.get("email"),
            "start_date": datetime.utcnow().isoformat(),
            "target_days": warmup_days,
            "current_day": 1,
            "emails_sent": 0,
            "replies_received": 0,
            "status": "active",
            "daily_schedule": self._generate_schedule(warmup_days)
        }
        
        self._save()
        return campaign_id
    
    def _generate_schedule(self, days: int) -> List[Dict]:
        schedule = []
        
        daily_limits = {
            1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
            6: 7, 7: 10, 8: 12, 9: 14, 10: 16,
            11: 18, 12: 20, 13: 22, 14: 25,
            15: 25, 16: 25, 17: 25, 18: 25, 19: 25,
            20: 25, 21: 28, 22: 30, 23: 32, 24: 35,
            25: 35, 26: 35, 27: 40, 28: 40
        }
        
        for day in range(1, days + 1):
            limit = daily_limits.get(day, 40)
            
            hours = list(range(8, 20))
            random.shuffle(hours)
            send_times = []
            
            for _ in range(min(limit, 5)):
                hour = random.choice(hours)
                send_times.append(f"{hour}:{random.choice([0, 15, 30, 45])}")
                hours.remove(hour)
            
            schedule.append({
                "day": day,
                "emails_to_send": min(limit, 5),
                "send_times": send_times
            })
        
        return schedule
    
    def send_warmup_email(self, campaign_id: str, to_email: str, credentials: Dict) -> bool:
        campaign = self.warmup_campaigns.get(campaign_id)
        if not campaign or campaign.get("status") != "active":
            return False
        
        template = random.choice(self.warmup_templates)
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = template["subject"].format(name="there")
        msg["From"] = credentials.get("email")
        msg["To"] = to_email
        
        body = template["body"].format(
            name="there",
            sender=credentials.get("display_name", "Friend")
        )
        
        msg.attach(MIMEText(body, "plain"))
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(credentials.get("email"), credentials.get("app_password"))
                server.send_message(msg)
            
            campaign["emails_sent"] += 1
            self._save()
            return True
            
        except Exception as e:
            print(f"Warmup email error: {e}")
            return False
    
    def get_campaign_status(self, campaign_id: str) -> Optional[Dict]:
        campaign = self.warmup_campaigns.get(campaign_id)
        if not campaign:
            return None
        
        day = campaign.get("current_day", 1)
        target = campaign.get("daily_schedule", [])[day - 1] if day <= len(campaign.get("daily_schedule", [])) else {}
        
        return {
            "campaign_id": campaign_id,
            "email": campaign.get("email"),
            "day": day,
            "target_day_emails": target.get("emails_to_send", 0),
            "total_sent": campaign.get("emails_sent", 0),
            "replies": campaign.get("replies_received", 0),
            "status": campaign.get("status"),
            "progress": f"{(day / campaign.get('target_days', 28)) * 100:.1f}%"
        }
    
    def check_daily_warmup(self):
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            for campaign in self.warmup_campaigns.values():
                if campaign.get("status") != "active":
                    continue
                
                account = db.query(EmailAccount).filter(
                    EmailAccount.id == campaign.get("account_id")
                ).first()
                
                if not account or account.status != "warmup":
                    continue
                
                current_day = current_day = campaign.get("current_day", 1)
                target = campaign.get("daily_schedule", [])[current_day - 1] if current_day <= len(campaign.get("daily_schedule", [])) else {}
                
                if campaign.get("emails_sent", 0) >= target.get("emails_to_send", 0):
                    campaign["current_day"] += 1
                    self._save()
        
        finally:
            db.close()
    
    def stop_warmup(self, campaign_id: str):
        if campaign_id in self.warmup_campaigns:
            self.warmup_campaigns[campaign_id]["status"] = "stopped"
            self._save()
    
    def list_campaigns(self) -> List[Dict]:
        return [self.get_campaign_status(c_id) for c_id in self.warmup_campaigns.keys()]

email_warmup = EmailWarmupManager()