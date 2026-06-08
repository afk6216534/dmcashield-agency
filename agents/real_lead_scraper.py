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

logger = logging.getLogger("scraper.real")


# ─── EMAIL VALIDATION (Format only) ─────────────────────────────

def validate_email_format(email: str) -> bool:
    if not email or "@" not in email:
        return False
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_leads(leads: List[Dict]) -> List[Dict]:
    for lead in leads:
        email = lead.get("email_primary", "")
        if validate_email_format(email):
            lead["validation_status"] = "verified"
        else:
            lead["validation_status"] = "invalid_format"
            lead["lead_score"] = max(lead.get("lead_score", 0) - 20, 10)
    return leads


# ─── FULL PIPELINE (No immediate email blast) ───────────────────

def run_scraper_pipeline(task_id: str, business_type: str, city: str, 
                         state: str, country: str = "USA", max_results: int = 20) -> Dict:
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
        from agents.http_scraper import run_scraper_sync
        leads = run_scraper_sync(business_type, city, state, country, max_results)
        logger.info(f"[PIPELINE] Phase 1 SCRAPING: Found {len(leads)} raw leads")
    except Exception as e:
        logger.error(f"[PIPELINE] HTTP scraper error: {e}")
    
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
    
    # ──── PHASE 3: FUNNELS — Create campaign + QUEUE all leads ──
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
                '["day1_opener", "day3_followup", "day7_value", "day14_social_proof", "day28_breakup"]', ?, ?)
        """, (campaign_id, f"{city} {business_type.title()} Outreach", business_type,
              city, state, verified_count, now, now))
        conn.commit()
        logger.info(f"[FUNNEL] Created campaign {campaign_id} for {verified_count} leads")
    except Exception as e:
        logger.error(f"[FUNNEL] Campaign creation failed: {e}")
    
    # Queue ALL verified leads in funnel step 0 = "queued for day1"
    funnel_count = 0
    for lid in saved_ids:
        try:
            conn.execute("""
                UPDATE real_leads SET funnel_step = 0, status = 'queued', updated_at = ?
                WHERE id = ? AND (status = 'new' OR status = 'queued')
            """, (now, lid))
            funnel_count += 1
        except Exception:
            pass
    conn.commit()
    logger.info(f"[FUNNEL] Queued {funnel_count} leads for drip sequence")
    
    try:
        conn.execute("UPDATE scrape_tasks SET leads_in_funnel = ?, campaign_id = ? WHERE id = ?",
                     (funnel_count, campaign_id, task_id))
        conn.commit()
    except Exception:
        pass
    
    # ──── PHASE 4-6: SENDING/TRACKING/SALES — Mark as "drip_active" ──
    # No immediate email blast! Leads are queued for the drip sender endpoint.
    pipeline_duration = (datetime.utcnow() - pipeline_start).total_seconds()
    
    try:
        conn.execute("""
            UPDATE scrape_tasks SET 
                status = 'drip_active',
                phase = 'sending',
                leads_found = ?,
                leads_validated = ?,
                leads_in_funnel = ?,
                leads_emailed = 0,
                campaign_id = ?,
                completed_at = ?
            WHERE id = ?
        """, (saved_count, verified_count, funnel_count,
              campaign_id, datetime.utcnow().isoformat(), task_id))
        conn.commit()
    except Exception as e:
        logger.warning(f"Task update failed: {e}")
    
    conn.close()
    
    # Sync to cloud backup
    try:
        from agents.cloud_db import save_all_tasks_to_cloud, save_all_leads_to_cloud
        save_all_tasks_to_cloud()
        save_all_leads_to_cloud()
    except Exception as sync_err:
        logger.warning(f"Cloud sync failed: {sync_err}")
    
    return {
        "task_id": task_id,
        "status": "drip_active",
        "message": f"✅ {saved_count} leads scraped, {verified_count} validated, {funnel_count} queued for drip sequence. Emails will send 3-5 per day over 28 days like a real company.",
        "pipeline_duration_seconds": round(pipeline_duration, 1),
        "phases": {
            "scraping": {"leads_found": len(leads), "status": "complete"},
            "validation": {"verified": verified_count, "total": len(validated_leads), "status": "complete"},
            "funnels": {"campaign_id": campaign_id, "leads_in_funnel": funnel_count, "status": "complete"},
            "sending": {"status": "drip_active", "message": "3-5 emails/day, Day 0→3→7→14→28 sequence"},
            "tracking": {"status": "waiting"},
            "sales": {"status": "waiting"}
        },
        "leads_scraped": len(leads),
        "leads_saved": saved_count,
        "leads_validated": verified_count,
        "leads_queued": funnel_count,
        "leads_emailed": 0,
        "campaign_id": campaign_id,
        "drip_schedule": {
            "emails_per_day": "3-5",
            "sequence": ["day1_opener (Day 0)", "day3_followup (Day 3)", "day7_value (Day 7)", "day14_social_proof (Day 14)", "day28_breakup (Day 28)"],
            "total_duration": "28 days",
            "sending_times": "9-11 AM or 1-3 PM",
            "best_days": "Tuesday-Thursday"
        },
        "source": "http_scraper",
        "results": results_list[:50],
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
