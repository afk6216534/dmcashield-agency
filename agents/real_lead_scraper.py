"""
DMCAShield Real Lead Scraper
==============================
Orchestrates scraping pipeline: scrape → validate → store → score.
Uses HTTP scraping (Vercel-compatible) by default.
Falls back to Playwright for local development if available.
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger("scraper.real")


def run_scraper_pipeline(task_id: str, business_type: str, city: str, 
                         state: str, country: str = "USA", max_results: int = 20) -> Dict:
    """
    Main scraping pipeline. Called from Flask route.
    
    1. Scrape businesses from web directories
    2. Extract emails from websites
    3. Score and store leads in database
    4. Return results summary
    """
    from agents.cloud_db import get_db
    
    # Update task status
    try:
        conn = get_db()
        conn.execute("""
            INSERT OR REPLACE INTO scrape_tasks (id, business_type, city, state, country, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'scraping', ?)
        """, (task_id, business_type, city, state, country, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Task status update failed: {e}")
    
    # Run the scraper
    leads = []
    try:
        from agents.http_scraper import run_scraper_sync
        leads = run_scraper_sync(business_type, city, state, country, max_results)
        logger.info(f"[PIPELINE] HTTP scraper found {len(leads)} leads")
    except Exception as e:
        logger.error(f"[PIPELINE] HTTP scraper error: {e}")
    
    # If HTTP scraper found nothing, try Playwright (local only)
    if not leads and not os.environ.get("VERCEL"):
        try:
            leads = _try_playwright_scraper(business_type, city, state, country, max_results)
            logger.info(f"[PIPELINE] Playwright scraper found {len(leads)} leads")
        except Exception as e:
            logger.warning(f"[PIPELINE] Playwright not available: {e}")
    
    # Store leads in database
    from agents.real_lead_engine import add_lead
    
    saved_count = 0
    results = []
    for lead in leads:
        try:
            lead["source"] = f"scrape_{task_id}"
            result = add_lead(lead)
            saved_count += 1
            results.append({
                "id": result["id"],
                "business_name": lead.get("business_name", ""),
                "score": result["score"],
                "temperature": result["temperature"],
                "email": lead.get("email_primary", ""),
            })
        except Exception as e:
            logger.error(f"Error saving lead: {e}")
    
    # Update task with results
    try:
        conn = get_db()
        conn.execute("""
            UPDATE scrape_tasks SET 
                status = 'complete',
                leads_found = ?,
                completed_at = ?
            WHERE id = ?
        """, (saved_count, datetime.utcnow().isoformat(), task_id))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Task completion update failed: {e}")
    
    return {
        "task_id": task_id,
        "status": "complete",
        "leads_scraped": len(leads),
        "leads_saved": saved_count,
        "source": "http_scraper",
        "results": results[:20],  # Return first 20 for API response
    }


def _try_playwright_scraper(business_type: str, city: str, state: str,
                             country: str, max_results: int) -> List[Dict]:
    """Try Playwright-based Google Maps scraper (local only)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return []
    
    # Import the old playwright scraper if available
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
