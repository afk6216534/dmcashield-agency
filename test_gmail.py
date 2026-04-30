# Gmail Test Script
# =============
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_config():
    """Test if Gmail is configured correctly"""
    
    # Load from .env
    env_file = "backend/.env"
    config = {}
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    config[key] = val
    
    email = config.get('GMAIL_EMAIL', '')
    password = config.get('GMAIL_APP_PASSWORD', '')
    display_name = config.get('GMAIL_DISPLAY_NAME', '')
    
    print("=" * 50)
    print("GMAIL CONFIG TEST")
    print("=" * 50)
    
    # Check if set
    if email in ['', 'your@gmail.com', None]:
        print("❌ GMAIL_EMAIL: NOT SET!")
        return False
    else:
        print(f"✓ GMAIL_EMAIL: {email}")
    
    if password in ['', 'xxxx xxxx xxxx xxxx', None]:
        print("❌ GMAIL_APP_PASSWORD: NOT SET!")
        print("   Need 16-char app password from:")
        print("   https://myaccount.google.com/apppasswords")
        return False
    else:
        # Check format
        if len(password.replace(' ', '')) == 16:
            print(f"✓ GMAIL_APP_PASSWORD: Set ({len(password.replace(' ', ''))} chars)")
        else:
            print(f"❌ GMAIL_APP_PASSWORD: Wrong length!")
            print(f"   Expected: 16 chars, Got: {len(password.replace(' ', ''))}")
            return False
    
    print(f"✓ GMAIL_DISPLAY_NAME: {display_name}")
    
    # Try to connect
    print("\nTesting connection...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.quit()
        print("✓ CONNECTION SUCCESS! Gmail is working!")
        return True
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return False

if __name__ == "__main__":
    test_gmail_config()