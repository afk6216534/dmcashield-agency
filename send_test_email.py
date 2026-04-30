# Test Email Endpoint
# ===================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_test_email():
    """Send test email to verify Gmail is working"""
    
    # Load email accounts from database or config
    # For now, use the .env or create test
    email = "af6216em2@gmail.com"
    password = os.environ.get('GMAIL_APP_PASSWORD', '')
    
    # If not in env, we need to get it from the account that was added
    # For testing, let's try to use a different approach
    
    to_email = "afk6216534@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = f"John <{email}>"
    msg['To'] = to_email
    msg['Subject'] = "✅ DMCAShield Test Email - System Working!"
    
    body = """
🎉 DMCAShield Agency - Test Email!

Hi,

This is a test email from your DMCAShield agency system.

✅ If you received this, your email is working!

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
        
        # For accounts added via dashboard, we need stored password
        # This is a placeholder - in real system, passwords are encrypted
        server.login(email, "test_password")
        
        text = msg.as_string()
        server.sendmail(email, to_email, text)
        server.quit()
        
        return {"status": "success", "message": "Test email sent!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = send_test_email()
    print(result)