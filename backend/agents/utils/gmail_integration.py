import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import json
import os

class GmailIntegration:
    def __init__(self, config_file: str = "data/gmail_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_host": "imap.gmail.com",
            "sender_email": "",
            "sender_name": "DMCAShield Agency",
            "notify_email": "",
            "hot_lead_subject": "🔥 HOT LEAD ALERT"
        }
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, sender_email: str, app_password: str, notify_email: str = None):
        self.config["sender_email"] = sender_email
        self.config["app_password"] = app_password
        self.config["notify_email"] = notify_email or sender_email
        self._save_config()
    
    def send_hot_lead_alert(self, lead: Dict, credentials: Dict) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🔥 HOT LEAD: {lead.get('business_name', 'New Lead')}"
            msg["From"] = self.config.get("sender_name", "DMCAShield")
            msg["To"] = self.config.get("notify_email", credentials.get("sender_email"))
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px;">
                <h2 style="color: #e94560;">🔥 HOT LEAD DETECTED</h2>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                    <p><strong>Business:</strong> {lead.get('business_name')}</p>
                    <p><strong>Owner:</strong> {lead.get('owner_name')}</p>
                    <p><strong>Email:</strong> {lead.get('email_primary')}</p>
                    <p><strong>Phone:</strong> {lead.get('phone')}</p>
                    <p><strong>Website:</strong> {lead.get('website')}</p>
                    <p><strong>City:</strong> {lead.get('city')}, {lead.get('state')}</p>
                    <p><strong>Rating:</strong> ⭐ {lead.get('current_rating')}</p>
                    <p><strong>Negative Reviews:</strong> {lead.get('negative_review_count')}</p>
                    <p><strong>Score:</strong> {lead.get('lead_score')}</p>
                </div>
                <p style="margin-top: 20px;">
                    <a href="mailto:{lead.get('email_primary')}" style="background: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reply Now</a>
                </p>
            </body>
            </html>
            """
            
            text_body = f"""
🔥 HOT LEAD DETECTED

Business: {lead.get('business_name')}
Owner: {lead.get('owner_name')}
Email: {lead.get('email_primary')}
Phone: {lead.get('phone')}
Website: {lead.get('website')}
City: {lead.get('city')}, {lead.get('state')}
Rating: {lead.get('current_rating')}
Negative Reviews: {lead.get('negative_review_count')}
Score: {lead.get('lead_score')}
            """
            
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.config["smtp_host"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(credentials.get("sender_email"), credentials.get("app_password"))
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Hot lead alert error: {e}")
            return False
    
    def send_daily_summary(self, stats: Dict, credentials: Dict) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"📊 DMCAShield Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
            msg["From"] = self.config.get("sender_name", "DMCAShield")
            msg["To"] = self.config.get("notify_email", credentials.get("sender_email"))
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px;">
                <h2>📊 Your Daily DMCAShield Report</h2>
                <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                    <p><strong>📧 Emails Sent Today:</strong> {stats.get('emails_sent_today', 0)}</p>
                    <p><strong>🔥 Hot Leads:</strong> {stats.get('hot_leads', 0)}</p>
                    <p><strong>📁 Total Leads:</strong> {stats.get('total_leads', 0)}</p>
                    <p><strong>⚡ Active Tasks:</strong> {stats.get('active_tasks', 0)}</p>
                    <p><strong>📬 Replies Received:</strong> {stats.get('replies', 0)}</p>
                </div>
                <p style="margin-top: 20px; color: #666;">
                    The system is working 24/7 for you!
                </p>
            </body>
            </html>
            """
            
            text_body = f"""
📊 Your Daily DMCAShield Report

Emails Sent Today: {stats.get('emails_sent_today', 0)}
🔥 Hot Leads: {stats.get('hot_leads', 0)}
📁 Total Leads: {stats.get('total_leads', 0)}
⚡ Active Tasks: {stats.get('active_tasks', 0)}
📬 Replies Received: {stats.get('replies', 0)}
            """
            
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.config["smtp_host"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(credentials.get("sender_email"), credentials.get("app_password"))
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Daily summary error: {e}")
            return False
    
    def check_inbox(self, credentials: Dict, folder: str = "INBOX", unread_only: bool = True) -> List[Dict]:
        try:
            with imaplib.IMAP4_SSL(self.config["imap_host"]) as mail:
                mail.login(credentials.get("sender_email"), credentials.get("app_password"))
                mail.select(folder)
                
                search_criteria = "UNSEEN" if unread_only else "ALL"
                status, messages = mail.search(None, search_criteria)
                
                email_list = []
                for num in messages[0].split()[:20]:
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    email_list.append({
                        "subject": msg["Subject"],
                        "from": msg["From"],
                        "date": msg["Date"],
                        "snippet": str(msg)[:200]
                    })
                
                return email_list
        
        except Exception as e:
            print(f"Inbox check error: {e}")
            return []
    
    def get_config(self) -> Dict:
        return {k: v for k, v in self.config.items() if k != "app_password"}

gmail_integration = GmailIntegration()

class WebhookManager:
    def __init__(self, persist_file: str = "data/webhooks.json"):
        self.persist_file = persist_file
        self.webhooks: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    self.webhooks = json.load(f)
            except:
                pass
    
    def _save(self):
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump(self.webhooks, f, indent=2)
    
    def register(self, event: str, url: str, secret: str = None, enabled: bool = True) -> str:
        hook_id = f"wh_{uuid.uuid4().hex[:8]}"
        self.webhooks[hook_id] = {
            "id": hook_id,
            "event": event,
            "url": url,
            "secret": secret,
            "enabled": enabled,
            "created_at": datetime.utcnow().isoformat()
        }
        self._save()
        return hook_id
    
    async def trigger(self, event: str, payload: Dict):
        import httpx
        
        for hook in self.webhooks.values():
            if not hook.get("enabled") or hook.get("event") != event:
                continue
            
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(hook["url"], json=payload)
            except Exception as e:
                print(f"Webhook trigger error: {e}")
    
    def list_webhooks(self, event: str = None) -> List[Dict]:
        if event:
            return [w for w in self.webhooks.values() if w.get("event") == event]
        return list(self.webhooks.values())
    
    def delete(self, hook_id: str):
        if hook_id in self.webhooks:
            del self.webhooks[hook_id]
            self._save()
    
    def toggle(self, hook_id: str, enabled: bool):
        if hook_id in self.webhooks:
            self.webhooks[hook_id]["enabled"] = enabled
            self._save()

webhook_manager = WebhookManager()