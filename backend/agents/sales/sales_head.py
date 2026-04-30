import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import imaplib
import email
from email.header import decode_header

from agents.memory.message_bus import MessageBus
from agents.memory.agent_brain import memory_system

class SalesHeadAgent:
    def __init__(self):
        self.name = "SalesHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["ReplyReader", "HumanVoice1", "HumanVoice2", "ConversionDetector"]

    def receive_message(self, message):
        if message.message_type == "alert" and "new_reply" in message.payload.get("alert", ""):
            self.process_new_reply(message.payload)
        elif message.message_type == "handoff":
            self.update_lead_status(message.payload)

    def classify_reply(self, reply_content: str, sender_email: str) -> str:
        reply_lower = reply_content.lower()
        
        positive_signals = ["yes", "interested", "sure", "okay", "lets", "call", "price", "cost", "how much", "book"]
        negative_signals = ["no", "not interested", "stop", "remove", "unsubscribe", "spam"]
        defer_signals = ["later", "busy", "maybe", "think about", "not now"]
        
        positive_count = sum(1 for s in positive_signals if s in reply_lower)
        negative_count = sum(1 for s in negative_signals if s in reply_lower)
        defer_count = sum(1 for s in defer_signals if s in reply_lower)
        
        if positive_count >= 2:
            return "HOT_LEAD"
        elif negative_count >= 2:
            return "HARD_NO"
        elif positive_count >= 1 and defer_count == 0:
            return "INTERESTED"
        elif defer_count >= 1 and negative_count == 0:
            return "NOT_NOW"
        else:
            return "OBJECTION"

    def generate_human_reply(self, reply_content: str, sender_name: str, classification: str) -> str:
        self.brain.remember(
            f"Generating reply for {sender_name} - Classification: {classification}",
            "reply_generation"
        )
        
        if classification == "HOT_LEAD":
            return f"""Hi {sender_name}!

Great to hear from you! I'm genuinely excited you reached out.

I'd love to jump on a quick call this week to understand your situation better and show you exactly what we can do.

What time works best for you? I'm flexible and happy to work around your schedule.

Talk soon,
Michael"""
        
        elif classification == "INTERESTED":
            return f"""Hi {sender_name}!

Thanks for getting back to me — I really appreciate it.

Happy to answer any questions you have. What specifically would you like to know more about?

Feel free to reply here or if you'd rather hop on a quick call, I'm happy to do that too.

Best,
Michael"""
        
        elif classification == "OBJECTION":
            return f"""Hi {sender_name}!

I totally get it — you want to make sure this is actually worth your time.

Here's the thing: we don't charge anything upfront. We only get paid when we successfully remove the reviews.

So there's literally no risk for you.

Worth a 5-minute call?

Best,
Michael"""
        
        elif classification == "NOT_NOW":
            return f"""Hi {sender_name}!

No worries at all — I completely understand.

I'll follow up in a couple of weeks. In the meantime, if you change your mind or have any questions, just hit reply.

Take care,
Michael"""
        
        elif classification == "HARD_NO":
            return f"""Hi {sender_name}!

Understood — I won't bother you again.

Best of luck with everything.

Michael"""
        
        else:
            return f"""Hi {sender_name}!

Thanks for your reply!

I'd love to chat more about how we can help. Let me know if you have any questions.

Best,
Michael"""

    def process_new_reply(self, payload: Dict):
        lead_email = payload.get("lead_email")
        reply_content = payload.get("reply_content", "")
        sender_name = payload.get("sender_name", "there")
        
        classification = self.classify_reply(reply_content, lead_email)
        
        from database.models import SessionLocal, Lead, EmailRecord
        db = SessionLocal()
        try:
            lead = db.query(Lead).filter(Lead.email_primary == lead_email).first()
            if not lead:
                return
            
            records = db.query(EmailRecord).filter(
                EmailRecord.lead_id == lead.id
            ).order_by(EmailRecord.created_at.desc()).all()
            
            for record in records:
                record.replied = True
                record.reply_content = reply_content
            
            lead.status = classification
            if classification == "HOT_LEAD":
                lead.temperature = "hot"
            elif classification == "INTERESTED":
                lead.temperature = "warm"
            
            db.commit()
            
            human_reply = self.generate_human_reply(reply_content, sender_name, classification)
            
            if classification in ["INTERESTED", "HOT_LEAD"]:
                self.send_reply_email(lead, human_reply)
                
                if classification == "HOT_LEAD":
                    alert = {
                        "alert": f"HOT LEAD READY: {lead_email}",
                        "details": {
                            "lead_id": lead.id,
                            "business": lead.business_name,
                            "reply": reply_content[:200],
                            "classification": classification
                        }
                    }
                    self.message_bus.send_message(
                        from_agent=self.name,
                        to_agent="CEO",
                        message_type="alert",
                        priority="critical",
                        payload=alert
                    )
                    self._save_messages()
                    
                    self.mark_important_in_gmail(lead_email)
            
            self.brain.remember(
                f"Processed reply from {lead_email}: {classification}",
                classification,
                {"lead_email": lead_email, "reply": reply_content[:100]}
            )
            
        finally:
            db.close()

    def send_reply_email(self, lead: Dict, reply_body: str):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        from database.models import SessionLocal, EmailAccount
        db = SessionLocal()
        try:
            if lead.get("assigned_account_id"):
                account = db.query(EmailAccount).filter(EmailAccount.id == lead.get("assigned_account_id")).first()
                if not account:
                    account = db.query(EmailAccount).filter(EmailAccount.status == "active").first()
            else:
                account = db.query(EmailAccount).filter(EmailAccount.status == "active").first()
            
            if not account:
                return
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Re: Quick question"
            msg["From"] = account.email_address
            msg["To"] = lead.get("email_primary")
            
            msg.attach(MIMEText(reply_body, "plain"))
            msg.attach(MIMEText(f"<html><body><p>{reply_body.replace(chr(10), '<br>')}</p></body></html>", "html"))
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(account.email_address, account.app_password_encrypted)
                server.send_message(msg)
                
        except Exception as e:
            self.brain.remember(f"Reply send failed: {str(e)}", "error")
        finally:
            db.close()

    def mark_important_in_gmail(self, email_address: str):
        pass

    def check_all_inboxes(self):
        from database.models import SessionLocal, EmailAccount
        
        db = SessionLocal()
        try:
            accounts = db.query(EmailAccount).filter(EmailAccount.status == "active").all()
            
            for account in accounts:
                try:
                    self._check_single_inbox(account)
                except Exception as e:
                    self.brain.remember(f"Inbox check failed for {account.email_address}: {str(e)}", "error")
                    
        finally:
            db.close()

    def _check_single_inbox(self, account):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(account.email_address, account.app_password_encrypted)
            mail.select('"[Gmail]/All Mail"')
            
            _, messages = mail.search(None, 'UNSEEN', 'FROM', 'MAILSEARCH')
            
            for msg_id in messages[0].split():
                _, data = mail.fetch(msg_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                sender = msg.get("From", "")
                subject = msg.get("Subject", "")
                
                if "re:" in subject.lower() or "RE:" in subject:
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    email_addr = sender.split("<")[-1].rstrip(">")
                    
                    self.process_new_reply({
                        "lead_email": email_addr,
                        "reply_content": body[:500],
                        "sender_name": sender.split("<")[0].strip(),
                        "account": account.email_address
                    })
            
            mail.logout()
            
        except Exception:
            pass

    def update_lead_status(self, payload: Dict):
        lead_id = payload.get("lead_id")
        new_status = payload.get("status")
        
        from database.models import SessionLocal, Lead
        db = SessionLocal()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                lead.status = new_status
                lead.updated_at = datetime.utcnow()
                db.commit()
        finally:
            db.close()

    def _save_messages(self):
        self.message_bus._save_messages()

    def start(self):
        return {"status": "online", "team": self.team}

sales_head = SalesHeadAgent()