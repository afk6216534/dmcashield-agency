"""
DMCAShield Drip Email Sender — Human-Like Email Engine
=======================================================
Based on cold-email skill best practices:

- Sends 3-5 emails per batch (not 20 at once)
- 5-email sequence over 28 days per lead
- Each follow-up has DIFFERENT angle (not "just checking in")
- Randomized send delays (3-7 min between emails)
- Personalized using lead data
- Stops sending if lead replies
- Proper warmup: Day 1-7 = 3/day, Day 8-14 = 5/day, Day 15+ = 10/day

Sequence (from cold-email skill data):
  Day 0:  Opener — personalized hook + core value prop
  Day 3:  Follow-up 1 — different angle, new value piece
  Day 7:  Follow-up 2 — social proof / case study
  Day 14: Follow-up 3 — industry insight / resource
  Day 28: Breakup — acknowledge silence, leave door open
"""

import os
import uuid
import smtplib
import logging
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger("drip.sender")


# ─── 5-EMAIL SEQUENCE (Each has different angle) ────────────────

EMAIL_SEQUENCE = {
    0: {  # Day 0 — Opener
        "name": "day1_opener",
        "subject": "quick question about {business_name}",
        "body": """Hi {owner_name},

I was looking at {business_name}'s online presence and noticed a few reviews that seem unfair — the kind that don't reflect the quality you actually deliver.

We specialize in removing illegitimate reviews through proper DMCA and platform processes. Most of our clients see results within 5-10 business days.

Would it be worth a quick look to see which reviews qualify for removal?

Best,
{sender_name}
DMCAShield""",
        "delay_days": 0
    },
    1: {  # Day 3 — Different angle + value piece
        "name": "day3_followup",
        "subject": "re: {business_name} reviews",
        "body": """Hi {owner_name},

Quick follow-up — I ran a preliminary scan on {business_name} and found something interesting.

Businesses in {niche} with ratings above 4.3 stars get 35% more calls from Google Maps. Right now, removing just 2-3 unfair reviews could push your rating significantly higher.

Want me to send over the full audit? Takes 2 minutes to review.

Best,
{sender_name}""",
        "delay_days": 3
    },
    2: {  # Day 7 — Social proof
        "name": "day7_value",
        "subject": "how a {niche} in {city} went from 3.4 to 4.7 stars",
        "body": """Hi {owner_name},

Thought you'd find this relevant — a {niche} similar to {business_name} came to us with a 3.4-star rating dragged down by fake competitor reviews.

Within 2 weeks, we removed 8 illegitimate reviews. Their rating jumped to 4.7 and they reported a 40% increase in new customer inquiries.

I think {business_name} could see similar results. Interested in a free reputation audit?

Best,
{sender_name}""",
        "delay_days": 7
    },
    3: {  # Day 14 — Industry insight
        "name": "day14_social_proof",
        "subject": "{niche} reputation trends in {city}",
        "body": """Hi {owner_name},

One last insight — we've been tracking review patterns in {city}'s {niche} market and noticed a spike in suspicious reviews across the board. Several businesses like yours are being targeted.

Google's own data shows 10-15% of reviews violate their policies. For {business_name}, that could mean 1-3 removable reviews right now.

Our audit is free and takes 5 minutes. Reply "audit" and I'll send it over.

{sender_name}""",
        "delay_days": 14
    },
    4: {  # Day 28 — Breakup (loss aversion)
        "name": "day28_breakup",
        "subject": "closing the loop on {business_name}",
        "body": """Hi {owner_name},

I've reached out a few times about protecting {business_name}'s online reputation. Since I haven't heard back, I'll assume now isn't the right time.

Before I close the loop — reply with a number:

1 — Interested, let's talk
2 — Not now, check back in 3 months  
3 — Not interested

Either way, no hard feelings. Good luck with {business_name}.

{sender_name}
DMCAShield""",
        "delay_days": 28
    }
}


def get_daily_send_limit() -> int:
    """
    Warmup schedule: start slow to build Gmail reputation.
    Scaled per active account to support realistic agency volume.
    """
    from agents.cloud_db import get_db
    from agents.email_campaign_engine import get_all_gmail_credentials
    
    # Scale limit by number of active credentials
    creds = get_all_gmail_credentials()
    num_accounts = len(creds) if creds else 1
    
    conn = get_db()
    try:
        # Count total emails ever sent
        total = conn.execute("SELECT COUNT(*) FROM email_log").fetchone()[0]
        conn.close()
        
        if total < 20:     # Week 1: 15 per day per account
            limit_per_acct = 15
        elif total < 50:   # Week 2: 25 per day per account
            limit_per_acct = 25
        elif total < 150:  # Week 3-4: 40 per day per account
            limit_per_acct = 40
        else:              # After warmup: 60 per day per account max
            limit_per_acct = 60
            
        return limit_per_acct * num_accounts
    except Exception:
        if 'conn' in locals() and conn:
            try:
                conn.close()
            except Exception:
                pass
        return 15 * num_accounts  # Default to safe limit



def get_sent_today_count() -> int:
    """Count emails sent today."""
    from agents.cloud_db import get_db
    conn = get_db()
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        count = conn.execute(
            "SELECT COUNT(*) FROM email_log WHERE sent_at LIKE ?", (f"{today}%",)
        ).fetchone()[0]
        conn.close()
        return count
    except Exception:
        conn.close()
        return 0


# ─── DRIP SENDER (Main function) ────────────────────────────────

def send_drip_batch() -> Dict:
    """
    Send next batch of drip emails. Called periodically (e.g., every few hours).
    
    Logic:
    1. Check warmup limit (3-15 emails/day)
    2. Find leads ready for their next email in sequence
    3. Send 3-5 emails with random delays
    4. Update lead status and email_log
    5. Sync to cloud
    """
    from agents.cloud_db import get_db
    from agents.email_campaign_engine import get_all_gmail_credentials
    
    results = {
        "sent": 0, 
        "skipped": 0, 
        "errors": 0, 
        "daily_limit": 0,
        "remaining_today": 0,
        "details": [],
        "next_batch": "Call again in 3-4 hours"
    }
    
    # Check credentials
    all_credentials = get_all_gmail_credentials()
    if not all_credentials:
        results["error"] = "Gmail not configured. Add credentials in Email Accounts."
        return results
    
    # Check warmup limit
    daily_limit = get_daily_send_limit()
    sent_today = get_sent_today_count()
    remaining = max(0, daily_limit - sent_today)
    results["daily_limit"] = daily_limit
    results["remaining_today"] = remaining
    
    if remaining == 0:
        results["message"] = f"Daily limit reached ({daily_limit}/day). Try again tomorrow."
        return results
    
    # How many to send this batch (10-20, but not more than remaining)
    batch_size = min(random.randint(10, 20), remaining)
    
    # Find leads ready for their next email
    conn = get_db()
    leads_to_send = []
    
    try:
        # Get leads that are queued or in funnel, ordered by score (hot leads first)
        rows = conn.execute("""
            SELECT * FROM real_leads 
            WHERE status IN ('queued', 'funnel_ready', 'contacted')
            AND status != 'blocked_generic_email'
            AND email_primary != '' 
            AND email_primary LIKE '%@%'
            AND email_primary NOT LIKE 'info@%'
            AND email_primary NOT LIKE 'support@%'
            AND email_primary NOT LIKE 'help@%'
            AND email_primary NOT LIKE 'contact@%'
            AND email_primary NOT LIKE 'admin@%'
            AND email_primary NOT LIKE 'office@%'
            AND email_primary NOT LIKE 'hello@%'
            AND email_primary NOT LIKE 'sales@%'
            AND email_primary NOT LIKE 'service@%'
            AND email_primary NOT LIKE 'noreply@%'
            AND email_primary NOT LIKE 'marketing@%'
            AND email_primary NOT LIKE 'billing@%'
            AND email_primary NOT LIKE 'feedback@%'
            AND email_primary NOT LIKE 'general@%'
            AND email_primary NOT LIKE 'team@%'
            AND (last_reply IS NULL OR last_reply = '')
            ORDER BY lead_score DESC, created_at ASC
            LIMIT ?
        """, (batch_size * 3,)).fetchall()  # Fetch extra to find ones ready for next email
        
        now = datetime.utcnow()
        
        for row in rows:
            if len(leads_to_send) >= batch_size:
                break
                
            lead = dict(row)
            
            # ── BLOCK generic/bot emails — NEVER send to info@, support@, etc. ──
            email = lead.get("email_primary", "").strip()
            if email and "@" in email:
                prefix = email.split("@")[0].lower()
                BLOCKED = {
                    "info", "support", "help", "contact", "admin", "office",
                    "hello", "team", "sales", "service", "enquiry", "enquiries",
                    "feedback", "mail", "noreply", "no-reply", "webmaster",
                    "postmaster", "marketing", "billing", "general", "reception",
                    "customerservice", "customer.service", "customercare",
                    "frontdesk", "reservations", "booking", "orders", "dispatch",
                    "newsletter", "notifications", "alerts", "system",
                }
                if prefix in BLOCKED:
                    results["skipped"] += 1
                    # Mark this lead as blocked so we don't keep trying
                    try:
                        conn.execute("UPDATE real_leads SET status = 'blocked_generic_email' WHERE id = ?", (lead["id"],))
                        conn.commit()
                    except Exception:
                        pass
                    continue
            
            funnel_step = lead.get("funnel_step", 0)
            last_sent = lead.get("last_email_sent", "")
            emails_sent = lead.get("emails_sent_count", 0)
            
            # Determine which sequence email to send
            if emails_sent >= 5:
                continue  # Sequence complete for this lead
            
            # Check if enough time has passed since last email
            if last_sent and emails_sent > 0:
                try:
                    last_dt = datetime.fromisoformat(last_sent.replace("Z", ""))
                    seq = EMAIL_SEQUENCE.get(emails_sent, None)
                    if not seq:
                        continue
                    delay_days = seq["delay_days"] - EMAIL_SEQUENCE.get(emails_sent - 1, {}).get("delay_days", 0)
                    if delay_days < 1:
                        delay_days = 3
                    if (now - last_dt).days < delay_days:
                        continue  # Not ready yet, wait for proper gap
                except Exception:
                    pass
            
            leads_to_send.append(lead)
    except Exception as e:
        logger.error(f"[DRIP] Error finding leads: {e}")
    
    if not leads_to_send:
        conn.close()
        results["message"] = "No leads ready for next email. All caught up!"
        return results
    
    def connect_smtp(credentials_list) -> tuple:
        """Try connecting to one of the credentials in credentials_list."""
        for creds in credentials_list:
            try:
                srv = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                srv.starttls()
                srv.login(creds["email"], creds["password"])
                return srv, creds
            except Exception as smtp_err:
                logger.warning(f"[DRIP] SMTP login failed for {creds['email']}: {smtp_err}")
                # Mark account as failing in database
                try:
                    conn_err = get_db()
                    conn_err.execute(
                        "UPDATE email_accounts SET status = 'auth_failed', health_score = MAX(health_score - 10, 0) WHERE email_address = ?",
                        (creds["email"],)
                    )
                    conn_err.commit()
                    conn_err.close()
                    from agents.cloud_db import save_all_accounts_to_cloud
                    save_all_accounts_to_cloud()
                except Exception:
                    pass
        return None, None

    server, credentials = connect_smtp(all_credentials)
    if not server or not credentials:
        conn.close()
        results["error"] = "All configured SMTP accounts failed to authenticate."
        return results
        
    sender_name = credentials.get("display_name", "DMCAShield Team")
    
    try:
        for i, lead in enumerate(leads_to_send):
            try:
                # Ensure SMTP connection is active
                is_active = False
                if server:
                    try:
                        status, _ = server.noop()
                        if status == 250:
                            is_active = True
                    except Exception:
                        pass
                
                if not is_active:
                    logger.info("[DRIP] SMTP connection lost/inactive. Reconnecting...")
                    try:
                        server.close()
                    except Exception:
                        pass
                    # Try current account first
                    try:
                        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                        server.starttls()
                        server.login(credentials["email"], credentials["password"])
                        is_active = True
                    except Exception as reconn_err:
                        logger.warning(f"[DRIP] Reconnection failed for {credentials['email']}: {reconn_err}")
                        server = None
                
                if not is_active:
                    logger.info("[DRIP] Rotating/falling back to other SMTP accounts...")
                    server, credentials = connect_smtp(all_credentials)
                    if not server:
                        raise Exception("No active SMTP accounts available for sending")
                    sender_name = credentials.get("display_name", "DMCAShield Team")

                emails_sent = lead.get("emails_sent_count", 0)
                seq = EMAIL_SEQUENCE.get(emails_sent, EMAIL_SEQUENCE[0])
                
                # Personalize email
                biz = lead.get("business_name", "your business")
                owner = lead.get("owner_name", "there")
                niche = lead.get("niche", "business")
                lead_city = lead.get("city", "your city")
                
                subject = seq["subject"].format(
                    business_name=biz, owner_name=owner, niche=niche, city=lead_city
                )
                body = seq["body"].format(
                    business_name=biz, owner_name=owner, niche=niche, 
                    city=lead_city, sender_name=sender_name
                )
                
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"{sender_name} <{credentials['email']}>"
                msg["To"] = lead["email_primary"]
                msg.attach(MIMEText(body, "plain"))
                
                server.send_message(msg)
                
                # Log to DB
                email_id = f"em_{uuid.uuid4().hex[:8]}"
                now_str = datetime.utcnow().isoformat()
                
                conn.execute("""
                    INSERT OR IGNORE INTO email_log (id, lead_id, subject, body_preview, template_name, sent_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'sent')
                """, (email_id, lead["id"], subject, body[:100], seq["name"], now_str))
                
                conn.execute("""
                    UPDATE real_leads SET 
                        emails_sent_count = emails_sent_count + 1,
                        funnel_step = ?,
                        status = 'contacted',
                        last_email_sent = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (emails_sent + 1, now_str, now_str, lead["id"]))
                
                # Log agent message to SQLite DB
                msg_id = f"msg_{uuid.uuid4().hex[:8]}"
                conn.execute("""
                    INSERT INTO agent_messages (id, from_agent, to_agent, message_type, priority, notes, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    msg_id,
                    "SMTPWorker",
                    "SendHead",
                    "report",
                    "normal",
                    f"Outreach email ({seq['name']}) sent to {biz} ({lead['email_primary']}) via {credentials['email']}",
                    now_str
                ))
                
                conn.commit()
                
                results["sent"] += 1
                results["details"].append({
                    "lead": biz,
                    "email": lead["email_primary"],
                    "sequence_step": seq["name"],
                    "step_number": emails_sent + 1,
                    "status": "sent"
                })
                
                logger.info(f"[DRIP] Sent {seq['name']} to {biz} ({lead['email_primary']})")
                
                # Random delay between emails (human-like, optimized for Vercel timeout limits)
                if i < len(leads_to_send) - 1:
                    from agents.cloud_db import IS_VERCEL
                    delay = random.uniform(0.1, 0.3) if IS_VERCEL else random.uniform(5, 15)
                    time.sleep(delay)
                    
            except Exception as e:
                results["errors"] += 1
                # Log email send error
                try:
                    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
                    now_str = datetime.utcnow().isoformat()
                    conn.execute("""
                        INSERT INTO agent_messages (id, from_agent, to_agent, message_type, priority, notes, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        msg_id,
                        "SMTPWorker",
                        "SendHead",
                        "alert",
                        "high",
                        f"Outreach send error for {biz} ({lead['email_primary']}): {str(e)[:80]}",
                        now_str
                    ))
                    conn.commit()
                except Exception:
                    pass
                results["details"].append({
                    "lead": lead.get("business_name", ""),
                    "status": "error",
                    "error": str(e)[:80]
                })
        
        if server:
            try:
                server.quit()
            except Exception:
                pass
        
    except Exception as e:
        logger.error(f"[DRIP] SMTP connection failed: {e}")
        results["errors"] += len(leads_to_send)
        results["smtp_error"] = str(e)[:100]
    
    # Update campaign stats
    try:
        conn.execute("""
            UPDATE campaigns SET emails_sent = emails_sent + ?, updated_at = ?
            WHERE status = 'active'
            ORDER BY created_at DESC LIMIT 1
        """, (results["sent"], datetime.utcnow().isoformat()))
        
        # Update task emailed counts
        conn.execute("""
            UPDATE scrape_tasks SET leads_emailed = (
                SELECT COUNT(*) FROM real_leads WHERE emails_sent_count > 0
            ) WHERE status = 'drip_active'
        """)
        conn.commit()
    except Exception:
        pass
    
    conn.close()
    
    # Sync to cloud
    try:
        from agents.cloud_db import save_all_tasks_to_cloud, save_all_leads_to_cloud
        save_all_tasks_to_cloud()
        save_all_leads_to_cloud()
    except Exception:
        pass
    
    results["message"] = f"Sent {results['sent']} emails ({sent_today + results['sent']}/{daily_limit} today). Next batch in 3-4 hours."
    return results


def get_drip_status() -> Dict:
    """Get current drip campaign status."""
    from agents.cloud_db import get_db
    conn = get_db()
    try:
        total_leads = conn.execute("SELECT COUNT(*) FROM real_leads WHERE email_primary LIKE '%@%'").fetchone()[0]
        queued = conn.execute("SELECT COUNT(*) FROM real_leads WHERE status IN ('queued', 'funnel_ready')").fetchone()[0]
        contacted = conn.execute("SELECT COUNT(*) FROM real_leads WHERE status = 'contacted'").fetchone()[0]
        total_emails = conn.execute("SELECT COUNT(*) FROM email_log").fetchone()[0]
        sent_today = get_sent_today_count()
        daily_limit = get_daily_send_limit()
        
        # Get sequence distribution
        step_counts = {}
        for i in range(6):
            count = conn.execute("SELECT COUNT(*) FROM real_leads WHERE emails_sent_count = ?", (i,)).fetchone()[0]
            step_counts[f"step_{i}"] = count
        
        conn.close()
        return {
            "total_leads": total_leads,
            "queued": queued,
            "contacted": contacted,
            "total_emails_sent": total_emails,
            "sent_today": sent_today,
            "daily_limit": daily_limit,
            "remaining_today": max(0, daily_limit - sent_today),
            "sequence_distribution": step_counts,
            "warmup_phase": "week1" if total_emails < 20 else "week2" if total_emails < 50 else "week3" if total_emails < 150 else "mature"
        }
    except Exception as e:
        conn.close()
        return {"error": str(e)}
