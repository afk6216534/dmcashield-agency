"""
DMCAShield Cloud Database Layer
================================
Works on both Vercel (serverless) and local development.
- On Vercel: Uses /tmp/ ephemeral SQLite (auto-initializes on cold start)
- Locally: Uses ./data/dmcashield.db (persistent)
- Future: Can swap to Turso/Supabase via TURSO_DATABASE_URL env var

All tables are auto-created on every connection to handle cold starts.
"""

import os
import sqlite3
import logging

logger = logging.getLogger("dmcashield.db")

# Detect environment
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))


def _get_db_path() -> str:
    """Get the database file path based on environment."""
    if IS_VERCEL:
        return "/tmp/dmcashield.db"
    else:
        local_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'dmcashield.db')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        return local_path


# SQL schema — runs on every connection (CREATE IF NOT EXISTS is idempotent)
SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS real_leads (
        id TEXT PRIMARY KEY,
        business_name TEXT NOT NULL,
        owner_name TEXT DEFAULT '',
        email_primary TEXT DEFAULT '',
        phone TEXT DEFAULT '',
        website TEXT DEFAULT '',
        city TEXT DEFAULT '',
        state TEXT DEFAULT '',
        country TEXT DEFAULT 'USA',
        niche TEXT DEFAULT '',
        full_address TEXT DEFAULT '',
        current_rating REAL DEFAULT 0,
        review_count INTEGER DEFAULT 0,
        negative_review_count INTEGER DEFAULT 0,
        lead_score INTEGER DEFAULT 0,
        lead_temperature TEXT DEFAULT 'cold',
        status TEXT DEFAULT 'new',
        funnel_step INTEGER DEFAULT 0,
        emails_sent_count INTEGER DEFAULT 0,
        last_email_sent TEXT DEFAULT '',
        last_reply TEXT DEFAULT '',
        source TEXT DEFAULT 'manual',
        notes TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS email_log (
        id TEXT PRIMARY KEY,
        lead_id TEXT NOT NULL,
        subject TEXT NOT NULL,
        body_preview TEXT DEFAULT '',
        template_name TEXT DEFAULT '',
        sent_at TEXT NOT NULL,
        opened_at TEXT DEFAULT '',
        clicked_at TEXT DEFAULT '',
        replied_at TEXT DEFAULT '',
        status TEXT DEFAULT 'sent',
        FOREIGN KEY (lead_id) REFERENCES real_leads(id)
    );

    CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        niche TEXT DEFAULT '',
        city TEXT DEFAULT '',
        state TEXT DEFAULT '',
        status TEXT DEFAULT 'draft',
        total_leads INTEGER DEFAULT 0,
        emails_sent INTEGER DEFAULT 0,
        opens INTEGER DEFAULT 0,
        replies INTEGER DEFAULT 0,
        template_sequence TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS gmail_config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        email TEXT DEFAULT '',
        app_password_set INTEGER DEFAULT 0,
        display_name TEXT DEFAULT 'DMCAShield Agency',
        connected_at TEXT DEFAULT '',
        last_test TEXT DEFAULT '',
        status TEXT DEFAULT 'disconnected'
    );

    INSERT OR IGNORE INTO gmail_config (id) VALUES (1);

    CREATE TABLE IF NOT EXISTS scrape_tasks (
        id TEXT PRIMARY KEY,
        business_type TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT DEFAULT '',
        country TEXT DEFAULT 'USA',
        status TEXT DEFAULT 'pending',
        leads_found INTEGER DEFAULT 0,
        error_message TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        completed_at TEXT DEFAULT ''
    );
"""


def get_db() -> sqlite3.Connection:
    """
    Get a database connection with auto-initialized schema.
    Safe to call on every request — CREATE IF NOT EXISTS is idempotent.
    """
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except Exception:
        pass  # WAL may not work on all platforms
    
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    
    return conn


def seed_gmail_from_env(conn: sqlite3.Connection = None):
    """
    Seed Gmail config from environment variables.
    Called on startup to populate DB from Vercel env vars.
    """
    email = os.environ.get("GMAIL_EMAIL", "")
    has_password = bool(os.environ.get("GMAIL_APP_PASSWORD", ""))
    display_name = os.environ.get("GMAIL_DISPLAY_NAME", "DMCAShield Agency")
    
    if email and email != "your@gmail.com" and has_password:
        should_close = conn is None
        if conn is None:
            conn = get_db()
        
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        
        conn.execute("""
            UPDATE gmail_config SET
                email = ?, app_password_set = 1, display_name = ?,
                connected_at = COALESCE(NULLIF(connected_at, ''), ?),
                status = 'connected'
            WHERE id = 1
        """, (email, display_name, now))
        conn.commit()
        
        if should_close:
            conn.close()
        
        logger.info(f"[DB] Gmail seeded from env: {email}")
        return True
    
    return False


def get_db_info() -> dict:
    """Get database info for debugging."""
    db_path = _get_db_path()
    exists = os.path.exists(db_path)
    size = os.path.getsize(db_path) if exists else 0
    
    return {
        "path": db_path,
        "exists": exists,
        "size_bytes": size,
        "is_vercel": IS_VERCEL,
        "environment": os.environ.get("VERCEL_ENV", "local"),
    }
