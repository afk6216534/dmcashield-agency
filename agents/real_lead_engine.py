"""
DMCAShield Real Lead Engine
==========================
Scrapes real businesses from the web, scores them, and stores in database.
Uses cloud_db for Vercel-compatible storage.
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def get_db():
    """Get database connection via cloud_db layer."""
    from agents.cloud_db import get_db as _get_db
    return _get_db()


def add_lead(lead_data: Dict) -> Dict:
    """Add a real lead to the database."""
    conn = get_db()
    lead_id = f"rl_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    
    # Score the lead based on data quality
    score = calculate_lead_score(lead_data)
    temp = "hot" if score >= 70 else "warm" if score >= 40 else "cold"
    
    conn.execute("""
        INSERT INTO real_leads (id, business_name, owner_name, email_primary, phone, website,
            city, state, country, niche, full_address, current_rating, review_count, negative_review_count,
            lead_score, lead_temperature, status, source, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?, ?, ?)
    """, (
        lead_id,
        lead_data.get("business_name", ""),
        lead_data.get("owner_name", ""),
        lead_data.get("email_primary", ""),
        lead_data.get("phone", ""),
        lead_data.get("website", ""),
        lead_data.get("city", ""),
        lead_data.get("state", ""),
        lead_data.get("country", "USA"),
        lead_data.get("niche", ""),
        lead_data.get("full_address", ""),
        lead_data.get("current_rating", 0),
        lead_data.get("review_count", 0),
        lead_data.get("negative_review_count", 0),
        score, temp,
        lead_data.get("source", "manual"),
        lead_data.get("notes", ""),
        now, now
    ))
    conn.commit()
    conn.close()
    
    return {"id": lead_id, "score": score, "temperature": temp, "status": "added"}


def calculate_lead_score(lead: Dict) -> int:
    """Score a lead 0-100 based on data quality and potential."""
    score = 0
    
    # Has email (+25)
    if lead.get("email_primary") and "@" in lead.get("email_primary", ""):
        score += 25
    
    # Has phone (+10)
    if lead.get("phone"):
        score += 10
    
    # Has website (+10)
    if lead.get("website") and "http" in lead.get("website", ""):
        score += 10
    
    # Low rating = high need (+20 for <4.0, +10 for <4.5)
    rating = lead.get("current_rating", 5)
    if rating > 0:
        if rating < 3.5:
            score += 25
        elif rating < 4.0:
            score += 20
        elif rating < 4.5:
            score += 10
    
    # Negative reviews (+15 for 5+, +10 for 3+)
    neg = lead.get("negative_review_count", 0)
    if neg >= 5:
        score += 15
    elif neg >= 3:
        score += 10
    elif neg >= 1:
        score += 5
    
    # Has owner name (+10)
    if lead.get("owner_name"):
        score += 10
    
    # Business info quality (+5 each)
    if lead.get("niche"):
        score += 5
    if lead.get("full_address"):
        score += 5
    
    return min(score, 100)


def get_leads(status: str = None, temperature: str = None, niche: str = None,
              limit: int = 50, offset: int = 0) -> List[Dict]:
    """Get real leads with filters."""
    conn = get_db()
    query = "SELECT * FROM real_leads WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if temperature:
        query += " AND lead_temperature = ?"
        params.append(temperature)
    if niche:
        query += " AND niche LIKE ?"
        params.append(f"%{niche}%")
    
    query += " ORDER BY lead_score DESC, created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_lead_stats() -> Dict:
    """Get real lead statistics."""
    conn = get_db()
    stats = {
        "total": conn.execute("SELECT COUNT(*) FROM real_leads").fetchone()[0],
        "hot": conn.execute("SELECT COUNT(*) FROM real_leads WHERE lead_temperature='hot'").fetchone()[0],
        "warm": conn.execute("SELECT COUNT(*) FROM real_leads WHERE lead_temperature='warm'").fetchone()[0],
        "cold": conn.execute("SELECT COUNT(*) FROM real_leads WHERE lead_temperature='cold'").fetchone()[0],
        "emailed": conn.execute("SELECT COUNT(*) FROM real_leads WHERE emails_sent_count > 0").fetchone()[0],
        "replied": conn.execute("SELECT COUNT(*) FROM real_leads WHERE last_reply != ''").fetchone()[0],
        "today_added": conn.execute(
            "SELECT COUNT(*) FROM real_leads WHERE created_at >= ?",
            (datetime.utcnow().strftime("%Y-%m-%dT00:00:00"),)
        ).fetchone()[0],
    }
    conn.close()
    return stats


def update_lead(lead_id: str, updates: Dict) -> bool:
    """Update a real lead."""
    conn = get_db()
    updates["updated_at"] = datetime.utcnow().isoformat()
    
    set_clauses = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [lead_id]
    
    conn.execute(f"UPDATE real_leads SET {set_clauses} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return True


def delete_lead(lead_id: str) -> bool:
    """Delete a real lead."""
    conn = get_db()
    conn.execute("DELETE FROM real_leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return True


# --- Gmail Config ---
def get_gmail_status() -> Dict:
    """Get Gmail connection status. Checks env vars first, then DB."""
    # Check environment variables (Vercel env vars)
    env_email = os.environ.get("GMAIL_EMAIL", "")
    env_pass = os.environ.get("GMAIL_APP_PASSWORD", "")
    
    if env_email and env_email != "your@gmail.com" and env_pass and env_pass != "xxxx xxxx xxxx xxxx":
        return {
            "status": "connected",
            "email": env_email,
            "app_password_set": 1,
            "display_name": os.environ.get("GMAIL_DISPLAY_NAME", "DMCAShield Agency"),
            "source": "environment",
        }
    
    # Fallback to database
    try:
        conn = get_db()
        row = conn.execute("SELECT * FROM gmail_config WHERE id = 1").fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception as e:
        return {"status": "disconnected", "email": "", "error": str(e)}
    
    return {"status": "disconnected", "email": ""}


def save_gmail_config(email: str, app_password: str, display_name: str = "DMCAShield Agency") -> Dict:
    """Save Gmail config to database."""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    
    conn.execute("""
        UPDATE gmail_config SET
            email = ?, app_password_set = 1, display_name = ?,
            connected_at = ?, status = 'connected'
        WHERE id = 1
    """, (email, display_name, now))
    conn.commit()
    conn.close()
    
    return {"status": "connected", "email": email}


def test_gmail_connection(email: str, app_password: str) -> Dict:
    """Test Gmail SMTP connection."""
    import smtplib
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(email, app_password)
        server.quit()
        
        # Update DB
        try:
            conn = get_db()
            conn.execute("UPDATE gmail_config SET last_test = ?, status = 'connected' WHERE id = 1",
                         (datetime.utcnow().isoformat(),))
            conn.commit()
            conn.close()
        except Exception:
            pass
        
        return {"success": True, "message": "Gmail connection verified!"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Campaign Management ---
def create_campaign(name: str, niche: str, city: str, state: str) -> Dict:
    """Create a new email campaign."""
    conn = get_db()
    campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    
    # Count matching leads
    total = conn.execute(
        "SELECT COUNT(*) FROM real_leads WHERE niche LIKE ? AND city LIKE ?",
        (f"%{niche}%", f"%{city}%")
    ).fetchone()[0]
    
    conn.execute("""
        INSERT INTO campaigns (id, name, niche, city, state, status, total_leads, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'draft', ?, ?, ?)
    """, (campaign_id, name, niche, city, state, total, now, now))
    conn.commit()
    conn.close()
    
    return {"id": campaign_id, "name": name, "total_leads": total, "status": "draft"}


def get_campaigns() -> List[Dict]:
    """Get all campaigns."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM campaigns ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
