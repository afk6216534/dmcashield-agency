# Resend Email Integration
# =====================
# Resend.com - Free email API (10,000 emails/month free)
# Sign up at: https://resend.com

import requests
from typing import Dict, List

class ResendEmail:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ""
        self.base_url = "https://api.resend.com"
    
    def send_email(self, from_email: str, to_email: str, subject: str, html: str = None, text: str = None) -> Dict:
        """Send email via Resend API"""
        if not self.api_key:
            return {"success": False, "error": "API key required"}
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
        }
        
        if html:
            data["html"] = html
        if text:
            data["text"] = text
        
        try:
            response = requests.post(f"{self.base_url}/emails", json=data, headers=headers)
            return {"success": True, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_test_email(self, to_email: str) -> Dict:
        """Send test email"""
        return self.send_email(
            from_email="DMCAShield Test <onboarding@resend.dev>",
            to_email=to_email,
            subject="✅ DMCAShield Test Email",
            html="<h1>Test Successful!</h1><p>Your email is working!</p>"
        )

resend = ResendEmail()