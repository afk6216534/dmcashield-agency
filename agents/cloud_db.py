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

    CREATE TABLE IF NOT EXISTS email_accounts (
        id TEXT PRIMARY KEY,
        email_address TEXT UNIQUE NOT NULL,
        display_name TEXT DEFAULT '',
        app_password TEXT DEFAULT '',
        daily_limit INTEGER DEFAULT 5,
        sent_today INTEGER DEFAULT 0,
        total_sent INTEGER DEFAULT 0,
        warmup_day INTEGER DEFAULT 1,
        warmup_complete INTEGER DEFAULT 0,
        status TEXT DEFAULT 'warming_up',
        blacklist_status TEXT DEFAULT 'clean',
        health_score INTEGER DEFAULT 50,
        total_opens INTEGER DEFAULT 0,
        total_replies INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );

    INSERT OR IGNORE INTO email_accounts (id, email_address, display_name, daily_limit, sent_today, total_sent, warmup_day, warmup_complete, status, blacklist_status, health_score, total_opens, total_replies, created_at)
    VALUES ('a1', 'outreach@dmcashield.com', 'DMCA Support', 30, 15, 234, 14, 0, 'warming_up', 'clean', 82, 90, 22, '2026-04-15T00:00:00Z');

    INSERT OR IGNORE INTO email_accounts (id, email_address, display_name, app_password, daily_limit, sent_today, total_sent, warmup_day, warmup_complete, status, blacklist_status, health_score, total_opens, total_replies, created_at)
    VALUES ('ce972985-b30e-4420-90ff-c1c9ed99b741', 'af6216em2@gmail.com', 'John', 'Ahmad12345@', 40, 0, 0, 1, 0, 'warming_up', 'clean', 100, 0, 0, '2026-04-29T13:13:27Z');
"""


def _run_migrations(conn: sqlite3.Connection):
    """Run table migrations to add missing columns if upgrading from old DB versions."""
    try:
        cursor = conn.execute("PRAGMA table_info(real_leads)")
        columns = [row[1] for row in cursor.fetchall()]
        if "country" not in columns:
            conn.execute("ALTER TABLE real_leads ADD COLUMN country TEXT DEFAULT 'USA'")
            conn.commit()
            logger.info("[DB] Migrated real_leads: Added country column")
    except Exception as e:
        logger.warning(f"[DB] Migration failed: {e}")


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
    
    # Run dynamic schema migrations
    _run_migrations(conn)
    
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
