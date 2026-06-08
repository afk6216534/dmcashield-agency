"""
DMCAShield Email Campaign Engine
=================================
Sends real emails via Gmail SMTP with rate limiting, tracking, and auto-follow-up.
Uses cloud_db for Vercel-compatible storage.
"""

import smtplib
import os
import json
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import random


# Rate limiting config
MAX_EMAILS_PER_DAY = int(os.environ.get("MAX_EMAILS_PER_ACCOUNT_PER_DAY", 40))
MIN_GAP_SECONDS = int(os.environ.get("EMAIL_SEND_GAP_MIN_SECONDS", 180))
MAX_GAP_SECONDS = int(os.environ.get("EMAIL_SEND_GAP_MAX_SECONDS", 420))


def get_db():
    """Get database connection via cloud_db layer."""
    from agents.cloud_db import get_db as _get_db
    return _get_db()


# ─── EMAIL TEMPLATES (from cold-email KB) ───

COLD_EMAIL_TEMPLATES = {
    "day1_opener": {
        "subject": "Quick question about {business_name}",
        "body": """Hi {owner_name},

I noticed {business_name} has some reviews online that might not reflect your actual quality of service.

We help businesses like yours remove unfair and fake reviews through legitimate DMCA processes — typically getting results within 5-10 business days.

Would it be worth a quick 5-minute chat to see if we can help?

Best,
DMCAShield Team"""
    },
    "day3_followup": {
        "subject": "Re: Quick question about {business_name}",
        "body": """Hi {owner_name},

Just following up on my note about protecting {business_name}'s online reputation.

Here's what one of our clients said after we removed 12 unfair reviews:

"Our rating went from 3.2 to 4.6 in two weeks. We've seen a 40% increase in new patient bookings." — Dr. Martinez, LA Dental

Want me to run a free reputation audit for {business_name}? Takes 2 minutes and shows exactly which reviews qualify for removal.

Best,
DMCAShield Team"""
    },
    "day7_value": {
        "subject": "{owner_name}, your competitors are doing this",
        "body": """Hi {owner_name},

Did you know that 94% of consumers avoid businesses with negative reviews?

For {business_name} in {city}, that could mean you're losing customers to competitors every single day those reviews stay up.

We've helped 200+ businesses in the {niche} industry remove unfair reviews and recover their ratings. Here's what we can do:

✅ Free Reputation Audit (2 minutes)
✅ Identify removable reviews
✅ No-risk guarantee — you only pay if reviews come down

Want me to send over the free audit?

Best,
DMCAShield Team"""
    },
    "day14_breakup": {
        "subject": "Should I close your file?",
        "body": """Hi {owner_name},

I've reached out a few times about protecting {business_name}'s online reputation but haven't heard back.

I totally understand — you're busy running a business. I'll close your file for now, but if unfair reviews ever become a problem, just reply to this email and I'll pick things right back up.

Wishing you all the best with {business_name}!

Best,
DMCAShield Team

P.S. — Our free reputation audit is always available if you change your mind."""
    }
}

SEQUENCE_ORDER = ["day1_opener", "day3_followup", "day7_value", "day14_breakup"]
SEQUENCE_DELAYS = [0, 3, 7, 14]  # Days between emails


def get_all_gmail_credentials() -> List[Dict]:
    """Load all valid Gmail credentials from database, filtering out placeholder accounts."""
    creds = []
    
    # Check env variables first if they contain a valid 16-char app password
    env_email = os.environ.get("GMAIL_EMAIL", "")
    env_pwd = os.environ.get("GMAIL_APP_PASSWORD", "")
    env_display = os.environ.get("GMAIL_DISPLAY_NAME", "DMCAShield Agency")
    
    if env_email and env_pwd and len(env_pwd.replace(" ", "")) == 16:
        creds.append({
            "email": env_email,
            "password": env_pwd.replace(" ", ""),
            "display_name": env_display
        })

    # Try loading from the database (accounts added via UI)
    try:
        conn = get_db()
        rows = conn.execute("""
            SELECT email_address, app_password, display_name 
            FROM email_accounts 
            WHERE status IN ('active', 'warming_up') 
            AND app_password != ''
            AND email_address NOT LIKE 'test%'
            AND app_password NOT LIKE 'test%'
            AND app_password NOT LIKE 'xxxx%'
            ORDER BY sent_today ASC
        """).fetchall()
        conn.close()
        for row in rows:
            if not any(c["email"] == row["email_address"] for c in creds):
                creds.append({
                    "email": row["email_address"],
                    "password": row["app_password"],
                    "display_name": row["display_name"] or "DMCAShield Agency"
                })
    except Exception:
        pass

    # Fallback to environment variables if no db entries
    if not creds:
        email = os.environ.get("GMAIL_EMAIL", "")
        password = os.environ.get("GMAIL_APP_PASSWORD", "")
        display = os.environ.get("GMAIL_DISPLAY_NAME", "DMCAShield Agency")
        if email and email != "your@gmail.com" and password and password != "xxxx xxxx xxxx xxxx":
            creds.append({
                "email": email,
                "password": password.replace(" ", ""),
                "display_name": display
            })
            
    return creds


def get_gmail_credentials() -> Optional[Dict]:
    """Load Gmail credentials from database or environment variables."""
    creds = get_all_gmail_credentials()
    return creds[0] if creds else None


def can_send_today() -> Dict:
    """Check if we can send more emails today."""
    conn = get_db()
    today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00")
    
    sent_today = conn.execute(
        "SELECT COUNT(*) FROM email_log WHERE sent_at >= ?", (today,)
    ).fetchone()[0]
    
    last_sent = conn.execute(
        "SELECT sent_at FROM email_log ORDER BY sent_at DESC LIMIT 1"
    ).fetchone()
    
    conn.close()
    
    can_send = sent_today < MAX_EMAILS_PER_DAY
    remaining = MAX_EMAILS_PER_DAY - sent_today
    
    # Check time gap
    seconds_since_last = 999
    if last_sent:
        last_time = datetime.fromisoformat(last_sent[0])
        seconds_since_last = (datetime.utcnow() - last_time).total_seconds()
    
    gap_ok = seconds_since_last >= MIN_GAP_SECONDS
    
    return {
        "can_send": can_send and gap_ok,
        "sent_today": sent_today,
        "remaining": remaining,
        "max_per_day": MAX_EMAILS_PER_DAY,
        "seconds_since_last": int(seconds_since_last),
        "min_gap": MIN_GAP_SECONDS,
        "gap_ok": gap_ok
    }


def send_email(lead: Dict, template_name: str, credentials: Dict = None) -> Dict:
    """Send a single email to a lead."""
    if not credentials:
        credentials = get_gmail_credentials()
    
    if not credentials:
        return {"success": False, "error": "Gmail not configured. Set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables."}
    
    # Check rate limits
    rate = can_send_today()
    if not rate["can_send"]:
        return {"success": False, "error": f"Rate limited. Sent {rate['sent_today']}/{rate['max_per_day']} today.",
                "rate_info": rate}
    
    # Get template
    template = COLD_EMAIL_TEMPLATES.get(template_name)
    if not template:
        return {"success": False, "error": f"Template '{template_name}' not found"}
    
    # Fill template
    subject = template["subject"].format(
        business_name=lead.get("business_name", "your business"),
        owner_name=lead.get("owner_name", "there"),
        city=lead.get("city", ""),
        niche=lead.get("niche", "")
    )
    
    body = template["body"].format(
        business_name=lead.get("business_name", "your business"),
        owner_name=lead.get("owner_name", "there"),
        city=lead.get("city", ""),
        niche=lead.get("niche", "")
    )
    
    to_email = lead.get("email_primary", "")
    if not to_email or "@" not in to_email:
        return {"success": False, "error": "Lead has no valid email address"}
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{credentials['display_name']} <{credentials['email']}>"
        msg["To"] = to_email
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(credentials["email"], credentials["password"])
            server.send_message(msg)
        
        # Log to DB
        email_id = f"em_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow().isoformat()
        conn = get_db()
        conn.execute("""
            INSERT INTO email_log (id, lead_id, subject, body_preview, template_name, sent_at, status)
            VALUES (?, ?, ?, ?, ?, ?, 'sent')
        """, (email_id, lead.get("id", ""), subject, body[:200], template_name, now))
        
        # Update lead
        conn.execute("""
            UPDATE real_leads SET emails_sent_count = emails_sent_count + 1,
                last_email_sent = ?, status = 'contacted', updated_at = ?
            WHERE id = ?
        """, (now, now, lead.get("id", "")))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "email_id": email_id,
            "to": to_email,
            "subject": subject,
            "template": template_name,
            "sent_at": now
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_next_template_for_lead(lead_id: str) -> Optional[str]:
    """Determine next email template in sequence for a lead."""
    conn = get_db()
    
    # Get emails already sent to this lead
    sent = conn.execute(
        "SELECT template_name, sent_at FROM email_log WHERE lead_id = ? ORDER BY sent_at DESC",
        (lead_id,)
    ).fetchall()
    conn.close()
    
    if not sent:
        return "day1_opener"
    
    last_template = sent[0]["template_name"]
    last_sent = datetime.fromisoformat(sent[0]["sent_at"])
    
    # Find next in sequence
    if last_template in SEQUENCE_ORDER:
        idx = SEQUENCE_ORDER.index(last_template)
        if idx < len(SEQUENCE_ORDER) - 1:
            next_idx = idx + 1
            days_required = SEQUENCE_DELAYS[next_idx] - SEQUENCE_DELAYS[idx]
            days_passed = (datetime.utcnow() - last_sent).days
            
            if days_passed >= days_required:
                return SEQUENCE_ORDER[next_idx]
    
    return None  # Sequence complete or not ready


def run_campaign_batch(campaign_id: str, batch_size: int = 10) -> Dict:
    """Send a batch of emails for a campaign."""
    credentials = get_gmail_credentials()
    if not credentials:
        return {"success": False, "error": "Gmail not configured. Set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables."}
    
    conn = get_db()
    campaign = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    if not campaign:
        conn.close()
        return {"success": False, "error": "Campaign not found"}
    
    campaign = dict(campaign)
    
    # Get leads for this campaign's niche/city that haven't completed the sequence
    leads = conn.execute("""
        SELECT * FROM real_leads
        WHERE niche LIKE ? AND city LIKE ?
        AND (status = 'new' OR status = 'contacted')
        ORDER BY lead_score DESC
        LIMIT ?
    """, (f"%{campaign['niche']}%", f"%{campaign['city']}%", batch_size)).fetchall()
    conn.close()
    
    results = {"sent": 0, "skipped": 0, "errors": 0, "details": []}
    
    for lead in leads:
        lead = dict(lead)
        
        # Check rate limit
        rate = can_send_today()
        if not rate["can_send"]:
            results["details"].append({"lead": lead["business_name"], "status": "rate_limited"})
            break
        
        # Get next template
        next_template = get_next_template_for_lead(lead["id"])
        if not next_template:
            results["skipped"] += 1
            continue
        
        # Send
        result = send_email(lead, next_template, credentials)
        if result["success"]:
            results["sent"] += 1
            results["details"].append({"lead": lead["business_name"], "status": "sent", "template": next_template})
        else:
            results["errors"] += 1
            results["details"].append({"lead": lead["business_name"], "status": "error", "error": result.get("error")})
        
        # Random gap between sends
        gap = random.randint(MIN_GAP_SECONDS, MAX_GAP_SECONDS)
        results["next_send_in"] = f"{gap} seconds"
    
    # Update campaign stats
    conn = get_db()
    conn.execute("""
        UPDATE campaigns SET emails_sent = emails_sent + ?, updated_at = ? WHERE id = ?
    """, (results["sent"], datetime.utcnow().isoformat(), campaign_id))
    conn.commit()
    conn.close()
    
    return results


def get_email_stats() -> Dict:
    """Get email sending statistics."""
    conn = get_db()
    today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00")
    
    stats = {
        "total_sent": conn.execute("SELECT COUNT(*) FROM email_log").fetchone()[0],
        "sent_today": conn.execute("SELECT COUNT(*) FROM email_log WHERE sent_at >= ?", (today,)).fetchone()[0],
        "opens": conn.execute("SELECT COUNT(*) FROM email_log WHERE opened_at != ''").fetchone()[0],
        "replies": conn.execute("SELECT COUNT(*) FROM email_log WHERE replied_at != ''").fetchone()[0],
        "remaining_today": MAX_EMAILS_PER_DAY - conn.execute(
            "SELECT COUNT(*) FROM email_log WHERE sent_at >= ?", (today,)
        ).fetchone()[0],
    }
    
    if stats["total_sent"] > 0:
        stats["open_rate"] = f"{(stats['opens'] / stats['total_sent'] * 100):.1f}%"
        stats["reply_rate"] = f"{(stats['replies'] / stats['total_sent'] * 100):.1f}%"
    else:
        stats["open_rate"] = "0%"
        stats["reply_rate"] = "0%"
    
    conn.close()
    return stats
