# Quick Test Email Sender - Fixed
import requests

RESEND_API = "re_Kpy9nQk8_Hgjnt3iCMzyMZmdhfV4Q4PeW"
FROM_EMAIL = "DMCAShield Test <onboarding@resend.dev>"
TO_EMAIL = "af6216em2@gmail.com"  # Your Resend account email

def send_test():
    response = requests.post(
        "https://api.resend.com/emails",
        json={
            "from": FROM_EMAIL,
            "to": [TO_EMAIL],
            "subject": "✅ DMCAShield Test - Email Working!",
            "html": """
            <h1>🎉 Test Successful!</h1>
            <p>Your DMCAShield email system is working via Resend!</p>
            <p><strong>Next steps:</strong></p>
            <ul>
                <li>Start scraping leads from dashboard</li>
                <li>Send outreach emails</li>
                <li>Convert leads to clients</li>
            </ul>
            <p>Your system is ready! 🚀</p>
            """
        },
        headers={
            "Authorization": f"Bearer {RESEND_API}",
            "Content-Type": "application/json"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    send_test()