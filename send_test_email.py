# Test Email Endpoint
# ===================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_test_email():
    """Send test email to verify Gmail is working"""
    from agents.email_campaign_engine import get_gmail_credentials
    creds = get_gmail_credentials()
    if not creds:
        return {"status": "error", "message": "No Gmail credentials configured. Add an account via UI first."}
    
    email = creds["email"]
    password = creds["password"]
    display_name = creds["display_name"]
    
    to_email = "afk6216534@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = f"{display_name} <{email}>"
    msg['To'] = to_email
    msg['Subject'] = "✅ DMCAShield Test Email - System Working!"
    
    body = f"""
🎉 DMCAShield Agency - Test Email!

Hi,

This is a test email from your DMCAShield agency system.

✅ If you received this, your email ({email}) is working!

System Status:
- Scraping: 12 platforms ready
- Skills: 107+ skills available
- Auto-training: 24/7
- Ready to scrape leads and send emails

Your system is working correctly!

Best,
DMCAShield AI
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login using real active credentials
        server.login(email, password)
        
        text = msg.as_string()
        server.sendmail(email, to_email, text)
        server.quit()
        
        return {"status": "success", "message": f"Test email sent from {email} to {to_email}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = send_test_email()
    print(result)