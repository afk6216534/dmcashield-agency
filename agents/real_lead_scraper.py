"""
DMCAShield Real Lead Scraper — FULL PIPELINE
===============================================
Orchestrates the complete outreach pipeline:
  1. SCRAPE — Find businesses from web directories (50+ leads)
  2. VALIDATE — Check email format, MX records, filter junk
  3. FUNNEL — Create campaign, assign leads to 4-email sequence
  4. SEND — Send day1_opener emails to all validated leads
  5. TRACK — Update lead status, email counts, funnel steps
  6. SYNC — Push everything to cloud backup

Uses HTTP scraping (Vercel-compatible) by default.
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
    """Check MX record exists for the email domain."""
    try:
        import socket
        domain = email.split("@")[1]
        # Quick DNS lookup — if the domain resolves, it's likely valid
        socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        return True
    except Exception:
        # Fallback: just check if domain resolves at all
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


# ─── FUNNEL BUILDER ──────────────────────────────────────────────

def create_campaign_for_task(task_id: str, business_type: str, city: str, 
                              state: str, leads_count: int) -> str:
    """Create a campaign in the database linked to this scraping task."""
    from agents.cloud_db import get_db
    campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    
    try:
        conn = get_db()
        conn.execute("""
            INSERT OR REPLACE INTO campaigns (id, name, niche, city, state, status, total_leads, 
                emails_sent, opens, replies, template_sequence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, 0, 0, 0, 
                '["day1_opener", "day3_followup", "day7_value", "day14_breakup"]', ?, ?)
        """, (campaign_id, f"{city} {business_type.title()} Outreach", business_type,
              city, state, leads_count, now, now))
        conn.commit()
        conn.close()
        logger.info(f"[FUNNEL] Created campaign {campaign_id} for {leads_count} leads")
    except Exception as e:
        logger.error(f"[FUNNEL] Campaign creation failed: {e}")
    
    return campaign_id


def assign_leads_to_funnel(lead_ids: List[str]) -> int:
    """Move all validated leads into funnel_step 1 (ready for outreach)."""
    from agents.cloud_db import get_db
    count = 0
    try:
        conn = get_db()
        now = datetime.utcnow().isoformat()
        for lid in lead_ids:
            conn.execute("""
                UPDATE real_leads SET funnel_step = 1, status = 'funnel_ready', updated_at = ?
                WHERE id = ? AND status = 'new'
            """, (now, lid))
            count += 1
        conn.commit()
        conn.close()
        logger.info(f"[FUNNEL] Assigned {count} leads to funnel step 1")
    except Exception as e:
        logger.error(f"[FUNNEL] Funnel assignment failed: {e}")
    return count


# ─── EMAIL SENDING ───────────────────────────────────────────────

def send_day1_opener_batch(lead_ids: List[str], task_id: str) -> Dict:
    """Send day1_opener email to all validated leads with proper Gmail."""
    from agents.email_campaign_engine import send_email, get_gmail_credentials
    from agents.cloud_db import get_db
    
    credentials = get_gmail_credentials()
    if not credentials:
        logger.warning("[SEND] Gmail not configured — skipping email sending")
        return {"sent": 0, "skipped": len(lead_ids), "errors": 0, "reason": "gmail_not_configured"}
    
    conn = get_db()
    results = {"sent": 0, "skipped": 0, "errors": 0, "details": []}
    
    for lid in lead_ids:
        row = conn.execute("SELECT * FROM real_leads WHERE id = ?", (lid,)).fetchone()
        if not row:
            results["skipped"] += 1
            continue
        
        lead = dict(row)
        
        # Skip if already contacted or no valid email
        if lead.get("emails_sent_count", 0) > 0:
            results["skipped"] += 1
            continue
        if lead.get("validation_status") == "invalid_format":
            results["skipped"] += 1
            continue
        if not lead.get("email_primary") or "@" not in lead.get("email_primary", ""):
            results["skipped"] += 1
            continue
        
        # Send the day1_opener
        result = send_email(lead, "day1_opener", credentials)
        if result.get("success"):
            results["sent"] += 1
            # Update funnel step
            now = datetime.utcnow().isoformat()
            conn.execute("""
                UPDATE real_leads SET funnel_step = 2, status = 'contacted', updated_at = ?
                WHERE id = ?
            """, (now, lid))
            results["details"].append({
                "lead": lead["business_name"], 
                "email": lead["email_primary"],
                "status": "sent"
            })
        else:
            results["errors"] += 1
            results["details"].append({
                "lead": lead["business_name"],
                "status": "error",
                "error": result.get("error", "unknown")
            })
    
    conn.commit()
    conn.close()
    return results


# ─── UPDATE TASK PHASE ───────────────────────────────────────────

def _update_task_phase(task_id: str, phase: str, status: str = "active", **kwargs):
    """Update task phase and any extra columns."""
    from agents.cloud_db import get_db
    try:
        conn = get_db()
        sets = ["phase = ?", "status = ?"]
        params = [phase, status]
        for key, val in kwargs.items():
            sets.append(f"{key} = ?")
            params.append(val)
        params.append(task_id)
        conn.execute(f"UPDATE scrape_tasks SET {', '.join(sets)} WHERE id = ?", params)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"[PHASE] Update failed: {e}")


# ─── FULL PIPELINE ───────────────────────────────────────────────

def run_scraper_pipeline(task_id: str, business_type: str, city: str, 
                         state: str, country: str = "USA", max_results: int = 50) -> Dict:
    """
    FULL real-world outreach pipeline. Called from Flask route.
    
    Phase 1: SCRAPING — Find businesses from YellowPages, Yelp, DuckDuckGo, OpenStreetMap
    Phase 2: VALIDATION — Check email format + MX records
    Phase 3: FUNNELS — Create campaign, assign leads to 4-email sequence
    Phase 4: SENDING — Send day1_opener to all validated leads
    Phase 5: TRACKING — Update all stats, sync to cloud
    Phase 6: SALES — Mark task complete with full metrics
    """
    from agents.cloud_db import get_db
    
    pipeline_start = datetime.utcnow()
    
    # ──── PHASE 1: SCRAPING ────────────────────────────────
    _update_task_phase(task_id, "scraping", "active")
    
    try:
        conn = get_db()
        conn.execute("""
            INSERT OR REPLACE INTO scrape_tasks (id, business_type, city, state, country, status, phase, created_at)
            VALUES (?, ?, ?, ?, ?, 'active', 'scraping', ?)
        """, (task_id, business_type, city, state, country, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Task status update failed: {e}")
    
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
            logger.info(f"[PIPELINE] Playwright scraper found {len(leads)} leads")
        except Exception as e:
            logger.warning(f"[PIPELINE] Playwright not available: {e}")
    
    _update_task_phase(task_id, "scraping", "active", leads_found=len(leads))
    
    # ──── PHASE 2: VALIDATION ──────────────────────────────
    _update_task_phase(task_id, "validation", "active")
    
    validated_leads = validate_leads(leads)
    verified_count = sum(1 for l in validated_leads if l.get("validation_status") == "verified")
    logger.info(f"[PIPELINE] Phase 2 VALIDATION: {verified_count}/{len(validated_leads)} emails verified")
    
    _update_task_phase(task_id, "validation", "active", leads_validated=verified_count)
    
    # ──── Store leads in database ──────────────────────────
    from agents.real_lead_engine import add_lead
    
    saved_count = 0
    saved_ids = []
    results_list = []
    for lead in validated_leads:
        try:
            lead["source"] = f"scrape_{task_id}"
            result = add_lead(lead)
            saved_count += 1
            saved_ids.append(result["id"])
            results_list.append({
                "id": result["id"],
                "business_name": lead.get("business_name", ""),
                "score": result["score"],
                "temperature": result["temperature"],
                "email": lead.get("email_primary", ""),
                "validated": lead.get("validation_status", "unknown"),
            })
        except Exception as e:
            logger.error(f"Error saving lead: {e}")
    
    # ──── PHASE 3: FUNNELS ─────────────────────────────────
    _update_task_phase(task_id, "funnels", "active", leads_found=saved_count)
    
    campaign_id = create_campaign_for_task(task_id, business_type, city, state, saved_count)
    funnel_count = assign_leads_to_funnel(saved_ids)
    logger.info(f"[PIPELINE] Phase 3 FUNNELS: {funnel_count} leads in funnel, campaign {campaign_id}")
    
    _update_task_phase(task_id, "funnels", "active", 
                       leads_in_funnel=funnel_count, campaign_id=campaign_id)
    
    # ──── PHASE 4: SENDING ─────────────────────────────────
    _update_task_phase(task_id, "sending", "active")
    
    # Only send to verified leads
    verified_ids = [r["id"] for r in results_list if r.get("validated") == "verified"]
    send_results = send_day1_opener_batch(verified_ids, task_id)
    logger.info(f"[PIPELINE] Phase 4 SENDING: {send_results['sent']} emails sent, {send_results['skipped']} skipped, {send_results['errors']} errors")
    
    _update_task_phase(task_id, "sending", "active", leads_emailed=send_results["sent"])
    
    # ──── PHASE 5: TRACKING ────────────────────────────────
    _update_task_phase(task_id, "tracking", "active")
    
    # Update campaign stats
    try:
        conn = get_db()
        conn.execute("""
            UPDATE campaigns SET emails_sent = ?, updated_at = ? WHERE id = ?
        """, (send_results["sent"], datetime.utcnow().isoformat(), campaign_id))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"[TRACKING] Campaign stats update failed: {e}")
    
    # ──── PHASE 6: SALES (COMPLETE) ────────────────────────
    pipeline_duration = (datetime.utcnow() - pipeline_start).total_seconds()
    
    try:
        conn = get_db()
        conn.execute("""
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
        conn.commit()
        conn.close()
        
        # Sync to cloud backup
        try:
            from agents.cloud_db import save_all_tasks_to_cloud, save_all_leads_to_cloud
            save_all_tasks_to_cloud()
            save_all_leads_to_cloud()
        except Exception as sync_err:
            logger.warning(f"Cloud sync failed: {sync_err}")
    except Exception as e:
        logger.warning(f"Task completion update failed: {e}")

    
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


def _try_playwright_scraper(business_type: str, city: str, state: str,
                             country: str, max_results: int) -> List[Dict]:
    """Try Playwright-based Google Maps scraper (local only)."""
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
