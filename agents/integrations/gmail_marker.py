import smtplib
import imaplib
import email
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional


class GmailMarker:
    def __init__(self, config_file: str = "data/gmail_marker_config.json"):
        self.config_file = config_file
        self.config = self._load()
        self.important_labels = ["DMCAShield Hot", "DMCAShield Lead"]

    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"accounts": [], "auto_mark_important": True, "label_name": "DMCAShield Hot"}

    def _save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def configure_account(self, email_address: str, app_password: str):
        existing = [a for a in self.config["accounts"] if a["email"] == email_address]
        if existing:
            existing[0]["app_password"] = app_password
        else:
            self.config["accounts"].append({
                "email": email_address,
                "app_password": app_password,
                "connected": False
            })
        self._save()

    def mark_as_important(self, email_address: str, app_password: str, target_email: str) -> Dict:
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, app_password)
            mail.select("inbox")

            status, messages = mail.search(None, f'FROM "{target_email}"')
            if status != "OK":
                mail.logout()
                return {"marked": 0, "error": "search failed"}

            msg_ids = messages[0].split()
            marked = 0
            for mid in msg_ids[-10:]:
                mail.store(mid, "+FLAGS", "\\Flagged")
                mail.store(mid, "+X-GM-LABELS", self.config.get("label_name", "DMCAShield Hot"))
                marked += 1

            mail.logout()
            return {"marked": marked, "account": email_address, "target": target_email}

        except Exception as e:
            return {"marked": 0, "error": str(e)}

    def send_important_alert(self, credentials: Dict, lead: Dict, snooze_mins: int = 30) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"IMPORTANT: {lead.get('business_name', 'Lead')} replied"
            msg["From"] = credentials.get("email")
            msg["To"] = credentials.get("notify_email", credentials.get("email"))

            html = f"""
            <h2>🔥 Hot Lead Response</h2>
            <p><b>Business:</b> {lead.get('business_name', 'Unknown')}</p>
            <p><b>Owner:</b> {lead.get('owner_name', 'Unknown')}</p>
            <p><b>Score:</b> {lead.get('lead_score', 0)}%</p>
            <p><b>Priority:</b> HIGH - Reply within {snooze_mins} min</p>
            """
            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(credentials.get("email"), credentials.get("app_password"))
                server.send_message(msg)
            return True

        except:
            return False

    def check_and_mark(self, email_address: str, app_password: str, hot_lead_emails: List[str]) -> Dict:
        results = {"checked": 0, "marked": 0}
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, app_password)
            mail.select("inbox")

            for target in hot_lead_emails:
                status, messages = mail.search(None, f'(FROM "{target}" UNSEEN)')
                if status == "OK":
                    for mid in messages[0].split()[:5]:
                        mail.store(mid, "+FLAGS", "\\Flagged")
                        results["marked"] += 1
                    results["checked"] += 1

            mail.logout()
        except:
            pass
        return results

    def get_config(self) -> Dict:
        return {
            "accounts_configured": len(self.config["accounts"]),
            "auto_mark": self.config.get("auto_mark_important", True),
            "label": self.config.get("label_name", "DMCAShield Hot")
        }


gmail_marker = GmailMarker()
