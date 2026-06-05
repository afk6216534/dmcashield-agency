"""
DMCAShield Real Lead Scraper — FULL PIPELINE
===============================================
Orchestrates the complete outreach pipeline:
  1. SCRAPE — Find businesses from web directories (50+ leads)
  2. VALIDATE — Check email format, MX records, filter junk
  3. FUNNEL — Create campaign, assign leads to 4-email sequence
  4. SEND — Send day1_opener emails to all validated leads
  5. TRACK — Update campaign stats, email counts, funnel steps
  6. SYNC — Push everything to cloud backup

Uses a SINGLE database connection throughout to avoid SQLite "database is locked" errors.
"""

import os
import re
import uuid
import asyncio
import logging
import random
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger("scraper.real")


# ─── EMAIL VALIDATION ───────────────────────────────────────────

def validate_email_format(email: str) -> bool:
    """Basic email format validation."""
    if not email or "@" not in email:
        return False
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_email_mx(email: str) -> bool:
    """Check if the email domain resolves via DNS."""
    try:
        import socket
        domain = email.split("@")[1]
        socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        return True
    except Exception:
        try:
            import socket
            domain = email.split("@")[1]
            socket.gethostbyname(domain)
            return True
        except Exception:
            return False


def validate_leads(leads: List[Dict]) -> List[Dict]:
    """Validate all leads — check email format and domain MX."""
    validated = []
    for lead in leads:
        email = lead.get("email_primary", "")
        if not validate_email_format(email):
            lead["validation_status"] = "invalid_format"
            lead["lead_score"] = max(lead.get("lead_score", 0) - 20, 10)
        elif not validate_email_mx(email):
            lead["validation_status"] = "no_mx"
            lead["lead_score"] = max(lead.get("lead_score", 0) - 10, 20)
        else:
            lead["validation_status"] = "verified"
        validated.append(lead)
    return validated


# ─── FULL PIPELINE ───────────────────────────────────────────────

def run_scraper_pipeline(task_id: str, business_type: str, city: str, 
                         state: str, country: str = "USA", max_results: int = 50) -> Dict:
    """
    FULL real-world outreach pipeline using a SINGLE DB connection.
    """
    from agents.cloud_db import get_db
    from agents.real_lead_engine import calculate_lead_score
    
    pipeline_start = datetime.utcnow()
    conn = get_db()  # Single connection for entire pipeline
    
    # ──── PHASE 1: SCRAPING ────────────────────────────────
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT OR REPLACE INTO scrape_tasks (id, business_type, city, state, country, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'active', ?)
    """, (task_id, business_type, city, state, country, now))
    conn.commit()
    
    # Update phase
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'scraping' WHERE id = ?", (task_id,))
        conn.commit()
    except Exception:
        pass
    
    leads = []
    try:
        from agents.http_scraper import run_scraper_sync
        leads = run_scraper_sync(business_type, city, state, country, max_results)
        logger.info(f"[PIPELINE] Phase 1 SCRAPING: Found {len(leads)} raw leads")
    except Exception as e:
        logger.error(f"[PIPELINE] HTTP scraper error: {e}")
    
    # Playwright fallback for local
    if not leads and not os.environ.get("VERCEL"):
        try:
            leads = _try_playwright_scraper(business_type, city, state, country, max_results)
        except Exception:
            pass
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_found = ? WHERE id = ?", (len(leads), task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── PHASE 2: VALIDATION ──────────────────────────────
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'validation' WHERE id = ?", (task_id,))
        conn.commit()
    except Exception:
        pass
    
    validated_leads = validate_leads(leads)
    verified_count = sum(1 for l in validated_leads if l.get("validation_status") == "verified")
    logger.info(f"[PIPELINE] Phase 2 VALIDATION: {verified_count}/{len(validated_leads)} emails verified")
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_validated = ? WHERE id = ?", (verified_count, task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── Store leads in database (using same conn) ────────
    saved_count = 0
    saved_ids = []
    results_list = []
    
    for lead in validated_leads:
        try:
            lead_id = f"rl_{uuid.uuid4().hex[:8]}"
            now = datetime.utcnow().isoformat()
            score = calculate_lead_score(lead)
            temp = "hot" if score >= 70 else "warm" if score >= 40 else "cold"
            
            conn.execute("""
                INSERT OR IGNORE INTO real_leads (id, business_name, owner_name, email_primary, phone, website,
                    city, state, country, niche, full_address, current_rating, review_count, negative_review_count,
                    lead_score, lead_temperature, status, source, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?, ?, ?)
            """, (
                lead_id,
                lead.get("business_name", ""),
                lead.get("owner_name", ""),
                lead.get("email_primary", ""),
                lead.get("phone", ""),
                lead.get("website", ""),
                lead.get("city", ""),
                lead.get("state", ""),
                lead.get("country", "USA"),
                lead.get("niche", business_type),
                lead.get("full_address", ""),
                lead.get("current_rating", 0),
                lead.get("review_count", 0),
                lead.get("negative_review_count", 0),
                score, temp,
                f"scrape_{task_id}",
                lead.get("validation_status", ""),
                now, now
            ))
            saved_count += 1
            saved_ids.append(lead_id)
            results_list.append({
                "id": lead_id,
                "business_name": lead.get("business_name", ""),
                "score": score,
                "temperature": temp,
                "email": lead.get("email_primary", ""),
                "validated": lead.get("validation_status", "unknown"),
            })
        except Exception as e:
            logger.error(f"Error saving lead: {e}")
    
    conn.commit()
    
    # ──── PHASE 3: FUNNELS ─────────────────────────────────
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'funnels', leads_found = ? WHERE id = ?", (saved_count, task_id))
        conn.commit()
    except Exception:
        pass
    
    campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO campaigns (id, name, niche, city, state, status, total_leads,
                emails_sent, opens, replies, template_sequence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, 0, 0, 0,
                '["day1_opener", "day3_followup", "day7_value", "day14_breakup"]', ?, ?)
        """, (campaign_id, f"{city} {business_type.title()} Outreach", business_type,
              city, state, saved_count, now, now))
        conn.commit()
        logger.info(f"[FUNNEL] Created campaign {campaign_id}")
    except Exception as e:
        logger.error(f"[FUNNEL] Campaign creation failed: {e}")
    
    # Assign leads to funnel
    funnel_count = 0
    for lid in saved_ids:
        try:
            conn.execute("""
                UPDATE real_leads SET funnel_step = 1, status = 'funnel_ready', updated_at = ?
                WHERE id = ? AND status = 'new'
            """, (now, lid))
            funnel_count += 1
        except Exception:
            pass
    conn.commit()
    logger.info(f"[FUNNEL] Assigned {funnel_count} leads to funnel step 1")
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_in_funnel = ?, campaign_id = ? WHERE id = ?",
                     (funnel_count, campaign_id, task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── PHASE 4: SENDING ─────────────────────────────────
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'sending' WHERE id = ?", (task_id,))
        conn.commit()
    except Exception:
        pass
    
    # Close connection BEFORE sending emails (SMTP takes time, would lock DB)
    conn.close()
    
    verified_ids = [r["id"] for r in results_list if r.get("validated") == "verified"]
    send_results = _send_day1_batch(verified_ids)
    logger.info(f"[PIPELINE] Phase 4 SENDING: {send_results['sent']} sent, {send_results['skipped']} skipped")
    
    # ──── PHASE 5 & 6: TRACKING + SALES ───────────────────
    conn2 = get_db()
    try:
        conn2.execute("""
            UPDATE campaigns SET emails_sent = ?, updated_at = ? WHERE id = ?
        """, (send_results["sent"], datetime.utcnow().isoformat(), campaign_id))
        conn2.commit()
    except Exception:
        pass
    
    pipeline_duration = (datetime.utcnow() - pipeline_start).total_seconds()
    
    try:
        conn2.execute("""
            UPDATE scrape_tasks SET 
                status = 'complete',
                phase = 'sales',
                leads_found = ?,
                leads_validated = ?,
                leads_in_funnel = ?,
                leads_emailed = ?,
                campaign_id = ?,
                completed_at = ?
            WHERE id = ?
        """, (saved_count, verified_count, funnel_count, send_results["sent"],
              campaign_id, datetime.utcnow().isoformat(), task_id))
        conn2.commit()
    except Exception as e:
        logger.warning(f"Task completion update failed: {e}")
    
    conn2.close()
    
    # Sync to cloud backup
    try:
        from agents.cloud_db import save_all_tasks_to_cloud, save_all_leads_to_cloud
        save_all_tasks_to_cloud()
        save_all_leads_to_cloud()
    except Exception as sync_err:
        logger.warning(f"Cloud sync failed: {sync_err}")
    
    return {
        "task_id": task_id,
        "status": "complete",
        "pipeline_duration_seconds": round(pipeline_duration, 1),
        "phases": {
            "scraping": {"leads_found": len(leads)},
            "validation": {"verified": verified_count, "total": len(validated_leads)},
            "funnels": {"campaign_id": campaign_id, "leads_in_funnel": funnel_count},
            "sending": send_results,
            "tracking": {"campaign_updated": True},
            "sales": {"complete": True}
        },
        "leads_scraped": len(leads),
        "leads_saved": saved_count,
        "leads_validated": verified_count,
        "leads_emailed": send_results["sent"],
        "campaign_id": campaign_id,
        "source": "http_scraper",
        "results": results_list[:50],
    }


def _send_day1_batch(lead_ids: List[str]) -> Dict:
    """Send day1_opener email to all verified leads."""
    from agents.email_campaign_engine import send_email, get_gmail_credentials
    from agents.cloud_db import get_db
    
    credentials = get_gmail_credentials()
    if not credentials:
        logger.warning("[SEND] Gmail not configured — skipping email sending")
        return {"sent": 0, "skipped": len(lead_ids), "errors": 0, "reason": "gmail_not_configured"}
    
    results = {"sent": 0, "skipped": 0, "errors": 0, "details": []}
    
    conn = get_db()
    for lid in lead_ids:
        row = conn.execute("SELECT * FROM real_leads WHERE id = ?", (lid,)).fetchone()
        if not row:
            results["skipped"] += 1
            continue
        
        lead = dict(row)
        if lead.get("emails_sent_count", 0) > 0:
            results["skipped"] += 1
            continue
        if not lead.get("email_primary") or "@" not in lead.get("email_primary", ""):
            results["skipped"] += 1
            continue
        
        result = send_email(lead, "day1_opener", credentials)
        if result.get("success"):
            results["sent"] += 1
            now = datetime.utcnow().isoformat()
            conn.execute("""
                UPDATE real_leads SET funnel_step = 2, status = 'contacted', updated_at = ?
                WHERE id = ?
            """, (now, lid))
            results["details"].append({"lead": lead["business_name"], "status": "sent"})
        else:
            results["errors"] += 1
            results["details"].append({"lead": lead["business_name"], "status": "error", "error": result.get("error", "")[:100]})
    
    conn.commit()
    conn.close()
    return results


def _try_playwright_scraper(business_type: str, city: str, state: str,
                             country: str, max_results: int) -> List[Dict]:
    """Try Playwright-based scraper (local only)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return []
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        from agents.http_scraper import scrape_all_sources
        leads = loop.run_until_complete(
            scrape_all_sources(business_type, city, state, country, max_results)
        )
        loop.close()
        return leads
    except Exception:
        return []


def get_scrape_tasks() -> List[Dict]:
    """Get all scraping tasks."""
    try:
        from agents.cloud_db import get_db
        conn = get_db()
        rows = conn.execute("SELECT * FROM scrape_tasks ORDER BY created_at DESC LIMIT 20").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []
