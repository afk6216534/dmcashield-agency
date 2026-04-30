# Email Reply Handler
# ==================
# Handles incoming email replies and marks important emails

import requests
import time
from datetime import datetime

class EmailReplyHandler:
    def __init__(self, resend_api_key: str = None):
        self.api_key = resend_api_key or ""
        self.webhook_url = "https://api.resend.com/webhooks"
    
    def check_for_replies(self, last_check: int = None) -> list:
        """Check for new email replies"""
        # In production, this would connect to email provider's webhook
        # For now, simulate checking
        return []
    
    def mark_important(self, email_id: str, important: bool = True) -> dict:
        """Mark email as important"""
        # Store in database
        return {"email_id": email_id, "important": important, "timestamp": datetime.utcnow().isoformat()}
    
    def auto_respond(self, lead_email: str, response: str) -> dict:
        """Send automatic response to leads who reply"""
        if not self.api_key:
            return {"success": False, "error": "No API key"}
        
        response_req = requests.post(
            "https://api.resend.com/emails",
            json={
                "from": "DMCAShield <onboarding@resend.dev>",
                "to": [lead_email],
                "subject": "Re: Your inquiry - Let's talk!",
                "html": f"<p>{response}</p>"
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        return {"success": response_req.status_code == 200}
    
    def classify_email(self, email_content: str) -> str:
        """Classify incoming email"""
        content_lower = email_content.lower()
        
        if any(w in content_lower for w in ["interested", "yes", "let's talk", "book call"]):
            return "hot_lead"
        elif any(w in content_lower for w in ["not interested", "stop", "unsubscribe"]):
            return "not_interested"
        elif any(w in content_lower for w in ["?", "how much", "price", "cost"]):
            return "needs_info"
        else:
            return "neutral"

reply_handler = EmailReplyHandler()