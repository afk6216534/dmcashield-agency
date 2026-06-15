"""
DMCAShield Real Lead Scraper — HUMAN-LIKE PIPELINE
====================================================
Based on cold-email skill best practices:

TASK LAUNCH (instant):
  1. SCRAPE — Find 20 businesses
  2. VALIDATE — Format check
  3. FUNNEL — Create campaign, queue ALL leads for drip sequence
  4. NO IMMEDIATE BLAST — leads are queued, not emailed all at once

DRIP SENDING (separate endpoint, called periodically):
  - Sends 3-5 emails per call with 3-7 min random gaps
  - Follows 5-email sequence over 28 days
  - Each follow-up has different angle
  - Stops if lead replies
  - Tuesday-Thursday, 9-11 AM or 1-3 PM preferred
  - Proper warmup: start with 3/day, increase gradually

Based on cold-email skill data:
  - 55% of replies come from follow-ups
  - 4-7 email campaigns achieve 27% reply rates vs 9% for 1-3
  - Optimal cadence: Day 0, Day 3, Day 7, Day 14, Day 28
  - Best days: Tue-Thu, Best times: 9-11 AM, 1-3 PM
"""

import os
import re
import uuid
import asyncio
import logging
from typing import List, Dict
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor
import socket

logger = logging.getLogger("scraper.real")


# ─── EMAIL VALIDATION (Format & DNS Resolution) ─────────────────

def validate_email_format(email: str) -> bool:
    if not email or "@" not in email:
        return False
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def check_domain_exists(domain: str) -> bool:
    """Check if a domain has active DNS records (socket.getaddrinfo)."""
    try:
        socket.getaddrinfo(domain, None)
        return True
    except Exception:
        return False


def validate_leads(leads: List[Dict]) -> List[Dict]:
    # Extract unique domains to avoid redundant lookups
    domains_to_check = set()
    for lead in leads:
        email = lead.get("email_primary", "")
        if validate_email_format(email):
            try:
                domain = email.split("@")[1].strip()
                domains_to_check.add(domain)
            except Exception:
                pass
                
    # Check domains concurrently (max 20 workers to prevent thread overhead)
    domain_status = {}
    if domains_to_check:
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_domain = {executor.submit(check_domain_exists, d): d for d in domains_to_check}
            for future in future_to_domain:
                d = future_to_domain[future]
                try:
                    domain_status[d] = future.result()
                except Exception:
                    domain_status[d] = False
                    
    # Assign validation status to leads
    for lead in leads:
        email = lead.get("email_primary", "")
        if validate_email_format(email):
            try:
                domain = email.split("@")[1].strip()
                if domain_status.get(domain, False):
                    lead["validation_status"] = "verified"
                else:
                    # Email format is ok but domain has no MX records – treat as format_ok
                    lead["validation_status"] = "format_ok"
                    lead["lead_score"] = max(lead.get("lead_score", 0) - 30, 10)
            except Exception:
                lead["validation_status"] = "invalid_domain"
                lead["lead_score"] = max(lead.get("lead_score", 0) - 30, 10)
        else:
            lead["validation_status"] = "invalid_format"
            lead["lead_score"] = max(lead.get("lead_score", 0) - 20, 10)
            
    return leads


# ─── FULL PIPELINE (No immediate email blast) ───────────────────

def run_scraper_pipeline(task_id: str, business_type: str, city: str, 
                         state: str, country: str = "USA", max_results: int = 100) -> Dict:
    """
    HUMAN-LIKE pipeline: scrape → validate → create funnel → QUEUE for drip.
    Does NOT send emails immediately. Leads are queued for the drip sender.
    """
    from agents.cloud_db import get_db
    from agents.real_lead_engine import calculate_lead_score
    
    pipeline_start = datetime.utcnow()
    conn = get_db()
    
    # ──── PHASE 1: SCRAPING ────────────────────────────────
    now = datetime.utcnow().isoformat()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO scrape_tasks (id, business_type, city, state, country, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?)
        """, (task_id, business_type, city, state, country, now))
        conn.commit()
    except Exception:
        pass
    
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'scraping' WHERE id = ?", (task_id,))
        conn.commit()
    except Exception:
        pass
    
    leads = []
    try:
        from agents.google_maps_scraper import run_google_maps_scraper_sync
        leads = run_google_maps_scraper_sync(business_type, city, state, country, max_results)
        logger.info(f"[PIPELINE] Phase 1 SCRAPING: Found {len(leads)} raw leads")
    except Exception as e:
        logger.error(f"[PIPELINE] Google Maps scraper error: {e}")
    
    # Fallback to old HTTP scraper if Google Maps finds nothing
    if not leads:
        try:
            from agents.http_scraper import run_scraper_sync
            leads = run_scraper_sync(business_type, city, state, country, max_results)
            logger.info(f"[PIPELINE] Fallback HTTP scraper: Found {len(leads)} raw leads")
        except Exception:
            pass
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_found = ? WHERE id = ?", (len(leads), task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── PHASE 2: VALIDATION (format only — fast) ─────────
    try:
        conn.execute("UPDATE scrape_tasks SET phase = 'validation' WHERE id = ?", (task_id,))
        conn.commit()
    except Exception:
        pass
    
    validated_leads = validate_leads(leads)
    verified_count = sum(1 for l in validated_leads if l.get("validation_status") == "verified")
    logger.info(f"[PIPELINE] Phase 2 VALIDATION: {verified_count}/{len(validated_leads)} format-valid")
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_validated = ? WHERE id = ?", (verified_count, task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── Store leads in database ──────────────────────────
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
                lead.get("city", city),
                lead.get("state", state),
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
    
    # ──── STOP HERE — Wait for user approval ──────────────────
    # Pipeline PAUSES after scraping + validation + saving.
    # User reviews leads in the dashboard, then clicks "Approve" to proceed.
    pipeline_duration = (datetime.utcnow() - pipeline_start).total_seconds()
    
    # Count leads with real emails
    email_count = sum(1 for item in results_list if item.get("email") and "@" in item.get("email", ""))
    
    try:
        conn.execute("""
            UPDATE scrape_tasks SET 
                status = 'awaiting_approval',
                phase = 'validation',
                leads_found = ?,
                leads_validated = ?,
                leads_in_funnel = 0,
                leads_emailed = 0,
                completed_at = ?
            WHERE id = ?
        """, (saved_count, verified_count, datetime.utcnow().isoformat(), task_id))
        conn.commit()
    except Exception as e:
        logger.warning(f"Task update failed: {e}")
    
    # Also update the simple tasks table
    try:
        conn.execute("""
            UPDATE tasks SET 
                status = 'awaiting_approval',
                leads_total = ?,
                phase_scraping = 'complete',
                phase_validation = 'complete',
                phase_funnel_creation = 'pending',
                phase_email_sending = 'pending',
                phase_tracking = 'pending',
                phase_sales = 'pending'
            WHERE id = ?
        """, (saved_count, task_id))
        conn.commit()
    except Exception:
        pass
    
    conn.close()
    
    # Sync to cloud backup
    try:
        from agents.cloud_db import save_all_tasks_to_cloud, save_all_leads_to_cloud
        save_all_tasks_to_cloud()
        save_all_leads_to_cloud()
    except Exception as sync_err:
        logger.warning(f"Cloud sync failed: {sync_err}")
    
    logger.info(f"[PIPELINE] ✅ Scraped {saved_count} leads ({email_count} with email). AWAITING USER APPROVAL.")
    
    return {
        "task_id": task_id,
        "status": "awaiting_approval",
        "message": f"✅ {saved_count} leads scraped, {email_count} with real emails. Review leads and click Approve to start outreach.",
        "pipeline_duration_seconds": round(pipeline_duration, 1),
        "phases": {
            "scraping": {"leads_found": len(leads), "status": "complete"},
            "validation": {"verified": verified_count, "total": len(validated_leads), "status": "complete"},
            "funnels": {"status": "awaiting_approval"},
            "sending": {"status": "awaiting_approval"},
            "tracking": {"status": "waiting"},
            "sales": {"status": "waiting"}
        },
        "leads_scraped": len(leads),
        "leads_saved": saved_count,
        "leads_with_email": email_count,
        "leads_validated": verified_count,
        "source": "google_maps_scraper",
        "results": results_list[:50],
    }


# ─── PHASE 2: APPROVE + START OUTREACH (called after user review) ──

def approve_and_start_outreach(task_id: str) -> Dict:
    """
    Called AFTER user reviews scraped leads and clicks Approve.
    Creates funnels, queues leads for drip sequence, and starts sending.
    """
    from agents.cloud_db import get_db
    
    conn = get_db()
    now = datetime.utcnow().isoformat()
    
    # Get task info
    try:
        task_row = conn.execute("SELECT * FROM scrape_tasks WHERE id = ?", (task_id,)).fetchone()
        if not task_row:
            # Try simple tasks table
            task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task_row:
            return {"error": f"Task {task_id} not found"}
        task = dict(task_row)
    except Exception as e:
        return {"error": str(e)}
    
    # Get all leads for this task that have a real email
    try:
        leads_rows = conn.execute("""
            SELECT id, business_name, email_primary, phone, website, city, state, niche,
                   lead_score, lead_temperature, status
            FROM real_leads 
            WHERE source = ? AND email_primary != '' AND email_primary IS NOT NULL
        """, (f"scrape_{task_id}",)).fetchall()
        leads_with_email = [dict(r) for r in leads_rows]
    except Exception as e:
        logger.error(f"Error fetching leads: {e}")
        leads_with_email = []
    
    if not leads_with_email:
        conn.close()
        return {"error": "No leads with valid email found for this task", "task_id": task_id}
    
    # ── Create campaign ──
    business_type = task.get("business_type", "business")
    city = task.get("city", "")
    state = task.get("state", "")
    
    campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
    try:
        conn.execute("""
            INSERT OR REPLACE INTO campaigns (id, name, niche, city, state, status, total_leads,
                emails_sent, opens, replies, template_sequence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, 0, 0, 0,
                '["day1_opener", "day3_followup", "day7_value", "day14_social_proof", "day28_breakup"]', ?, ?)
        """, (campaign_id, f"{city} {business_type.title()} Outreach", business_type,
              city, state, len(leads_with_email), now, now))
        conn.commit()
        logger.info(f"[APPROVE] Created campaign {campaign_id} for {len(leads_with_email)} leads")
    except Exception as e:
        logger.error(f"[APPROVE] Campaign creation failed: {e}")
    
    # ── Queue leads for drip ──
    funnel_count = 0
    for lead in leads_with_email:
        try:
            conn.execute("""
                UPDATE real_leads SET funnel_step = 0, status = 'queued', updated_at = ?
                WHERE id = ? AND (status = 'new' OR status = 'queued')
            """, (now, lead["id"]))
            funnel_count += 1
        except Exception:
            pass
    conn.commit()
    logger.info(f"[APPROVE] Queued {funnel_count} leads for drip sequence")
    
    # ── Update task status to drip_active ──
    try:
        conn.execute("""
            UPDATE scrape_tasks SET 
                status = 'drip_active',
                phase = 'sending',
                leads_in_funnel = ?,
                campaign_id = ?
            WHERE id = ?
        """, (funnel_count, campaign_id, task_id))
        conn.commit()
    except Exception:
        pass
    
    try:
        conn.execute("""
            UPDATE tasks SET 
                status = 'drip_active',
                phase_funnel_creation = 'complete',
                phase_email_sending = 'in_progress',
                phase_tracking = 'pending',
                phase_sales = 'pending'
            WHERE id = ?
        """, (task_id,))
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
    
    # Auto-trigger first drip batch
    drip_result = None
    if funnel_count > 0:
        try:
            from agents.drip_sender import send_drip_batch
            logger.info(f"[APPROVE] Triggering drip sender for {funnel_count} queued leads...")
            drip_result = send_drip_batch()
            logger.info(f"[APPROVE] Drip result: {drip_result.get('sent', 0)} emails sent")
        except Exception as drip_err:
            logger.warning(f"[APPROVE] Drip send failed: {drip_err}")
            drip_result = {"error": str(drip_err)}
    
    emails_sent = drip_result.get("sent", 0) if drip_result else 0
    
    return {
        "task_id": task_id,
        "status": "drip_active",
        "message": f"✅ Approved! {funnel_count} leads queued for drip. {emails_sent} emails sent.",
        "campaign_id": campaign_id,
        "leads_queued": funnel_count,
        "emails_sent": emails_sent,
        "drip_result": drip_result,
    }


def _try_playwright_scraper(business_type: str, city: str, state: str,
                             country: str, max_results: int) -> List[Dict]:
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
    try:
        from agents.cloud_db import get_db
        conn = get_db()
        rows = conn.execute("SELECT * FROM scrape_tasks ORDER BY created_at DESC LIMIT 20").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []
