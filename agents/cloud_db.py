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

    INSERT OR IGNORE INTO real_leads (id, business_name, owner_name, email_primary, phone, website, city, state, country, niche, full_address, current_rating, review_count, negative_review_count, lead_score, lead_temperature, status, funnel_step, emails_sent_count, last_email_sent, last_reply, source, notes, created_at, updated_at)
    VALUES ('rl_362307dd', 'Midtown Dental', '', 'contact@midtowndental.com', '(871) 894-5445', 'https://www.midtowndental.com', 'Houston', 'Texas', 'USA', 'dentist', 'Midtown Dental, 2450, Louisiana Street, Midtown, Houston, Harris County, Texas, 77006, United States', 4.3, 112, 10, 80, 'hot', 'new', 0, 0, '', '', 'scrape_scrape_588c7131', '', '2026-06-03T09:20:30.509104', '2026-06-03T09:20:30.509104');

    INSERT OR IGNORE INTO real_leads (id, business_name, owner_name, email_primary, phone, website, city, state, country, niche, full_address, current_rating, review_count, negative_review_count, lead_score, lead_temperature, status, funnel_step, emails_sent_count, last_email_sent, last_reply, source, notes, created_at, updated_at)
    VALUES ('rl_af7025fd', 'Urban Dental', '', 'contact@urbandental.com', '(207) 623-7774', 'https://www.urbandental.com', 'Houston', 'Texas', 'USA', 'dentist', 'Urban Dental, 2511, Bagby Street, Midtown, Houston, Harris County, Texas, 77006, United States', 4.0, 83, 7, 80, 'hot', 'new', 0, 0, '', '', 'scrape_scrape_588c7131', '', '2026-06-03T09:20:30.526590', '2026-06-03T09:20:30.526590');

    INSERT OR IGNORE INTO real_leads (id, business_name, owner_name, email_primary, phone, website, city, state, country, niche, full_address, current_rating, review_count, negative_review_count, lead_score, lead_temperature, status, funnel_step, emails_sent_count, last_email_sent, last_reply, source, notes, created_at, updated_at)
    VALUES ('rl_e2215acd', 'Bayou City Smiles', '', 'contact@bayoucitysmiles.com', '(786) 564-3919', 'https://www.bayoucitysmiles.com', 'Houston', 'Texas', 'USA', 'dentist', 'Bayou City Smiles, 2313, Edwards Street, Washington Avenue Coalition / Memorial Park, Old Sixth Ward, Houston, Harris County, Texas, 77007, United States', 4.1, 65, 12, 80, 'hot', 'new', 0, 0, '', '', 'scrape_scrape_588c7131', '', '2026-06-03T09:20:30.538672', '2026-06-03T09:20:30.538672');

    INSERT OR IGNORE INTO campaigns (id, name, niche, city, state, status, total_leads, emails_sent, opens, replies, template_sequence, created_at, updated_at)
    VALUES ('c1', 'Houston Dentist Outreach', 'dentist', 'Houston', 'Texas', 'active', 3, 0, 0, 0, '["day1_opener", "day3_followup", "day7_value", "day14_breakup"]', '2026-06-03T10:00:00Z', '2026-06-03T10:00:00Z');
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
        logger.warning(f"[DB] Migration failed (real_leads): {e}")

    # Add phase-tracking columns to scrape_tasks
    try:
        cursor = conn.execute("PRAGMA table_info(scrape_tasks)")
        columns = [row[1] for row in cursor.fetchall()]
        migrations = {
            "phase": "ALTER TABLE scrape_tasks ADD COLUMN phase TEXT DEFAULT 'scraping'",
            "leads_validated": "ALTER TABLE scrape_tasks ADD COLUMN leads_validated INTEGER DEFAULT 0",
            "leads_emailed": "ALTER TABLE scrape_tasks ADD COLUMN leads_emailed INTEGER DEFAULT 0",
            "campaign_id": "ALTER TABLE scrape_tasks ADD COLUMN campaign_id TEXT DEFAULT ''",
            "leads_in_funnel": "ALTER TABLE scrape_tasks ADD COLUMN leads_in_funnel INTEGER DEFAULT 0",
        }
        for col, sql in migrations.items():
            if col not in columns:
                conn.execute(sql)
                conn.commit()
                logger.info(f"[DB] Migrated scrape_tasks: Added {col} column")
    except Exception as e:
        logger.warning(f"[DB] Migration failed (scrape_tasks): {e}")


def encrypt_val(val: str, key: str) -> str:
    import base64
    if not val:
        return ""
    key_bytes = key.encode()
    val_bytes = val.encode()
    encrypted = bytearray(len(val_bytes))
    for i in range(len(val_bytes)):
        encrypted[i] = val_bytes[i] ^ key_bytes[i % len(key_bytes)]
    return base64.b64encode(encrypted).decode()


def decrypt_val(encrypted_str: str, key: str) -> str:
    import base64
    if not encrypted_str:
        return ""
    try:
        key_bytes = key.encode()
        encrypted = base64.b64decode(encrypted_str.encode())
        decrypted = bytearray(len(encrypted))
        for i in range(len(encrypted)):
            decrypted[i] = encrypted[i] ^ key_bytes[i % len(key_bytes)]
        return decrypted.decode()
    except Exception:
        return ""


def save_accounts_to_cloud(accounts: list):
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/email_accounts"
        req = urllib.request.Request(
            url,
            data=json.dumps(accounts).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to save accounts: {e}")


def restore_accounts_from_cloud() -> list:
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/email_accounts"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception as e:
        # 404 is normal when no backup exists yet
        pass
    return []


def save_all_accounts_to_cloud():
    """Fetch all accounts from SQLite, encrypt passwords, and upload to cloud."""
    try:
        conn = sqlite3.connect(_get_db_path())
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM email_accounts").fetchall()
        conn.close()
        
        accounts = []
        key = "dmcashield-secure-key-2026"
        for r in rows:
            acc = dict(r)
            acc["encrypted_password"] = encrypt_val(acc.get("app_password", ""), key)
            if "app_password" in acc:
                del acc["app_password"]
            accounts.append(acc)
        
        save_accounts_to_cloud(accounts)
        logger.info(f"[CloudBackup] Successfully backed up {len(accounts)} accounts to cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_accounts_to_cloud failed: {e}")


def restore_and_sync_accounts(conn: sqlite3.Connection):
    """Restore email accounts from cloud backup and insert into SQLite."""
    import hashlib
    try:
        accounts = restore_accounts_from_cloud()
        if not accounts:
            return
            
        key = "dmcashield-secure-key-2026"
        for acc in accounts:
            pwd = decrypt_val(acc.get("encrypted_password", ""), key)
            conn.execute("""
                INSERT OR REPLACE INTO email_accounts (
                    id, email_address, display_name, app_password, daily_limit,
                    sent_today, total_sent, warmup_day, warmup_complete,
                    status, blacklist_status, health_score, total_opens, total_replies, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                acc["id"], acc["email_address"], acc.get("display_name", ""), pwd,
                acc.get("daily_limit", 5), acc.get("sent_today", 0), acc.get("total_sent", 0),
                acc.get("warmup_day", 1), int(acc.get("warmup_complete", 0)),
                acc.get("status", "warming_up"), acc.get("blacklist_status", "clean"),
                acc.get("health_score", 50), acc.get("total_opens", 0), acc.get("total_replies", 0),
                acc["created_at"]
            ))
        conn.commit()
        logger.info(f"[CloudBackup] Successfully restored {len(accounts)} accounts from cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore accounts: {e}")


LAST_SYNC_TIME = 0


def get_db() -> sqlite3.Connection:
    """
    Get a database connection with auto-initialized schema.
    Safe to call on every request — CREATE IF NOT EXISTS is idempotent.
    """
    global LAST_SYNC_TIME
    import time
    db_path = _get_db_path()
    is_new = not os.path.exists(db_path) or os.path.getsize(db_path) == 0
    
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=10000")
    except Exception:
        pass  # WAL may not work on all platforms
    
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    
    # Run dynamic schema migrations
    _run_migrations(conn)
    
    # Sync from cloud if the SQLite file was just created OR if 60 seconds have passed since last sync
    now = time.time()
    if is_new or (now - LAST_SYNC_TIME > 60):
        LAST_SYNC_TIME = now
        restore_and_sync_accounts(conn)
        restore_and_sync_tasks(conn)
        restore_and_sync_leads(conn)
        
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


def save_tasks_to_cloud(tasks: list):
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/scrape_tasks"
        req = urllib.request.Request(
            url,
            data=json.dumps(tasks).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to save tasks: {e}")


def restore_tasks_from_cloud() -> list:
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/scrape_tasks"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        pass
    return []


def save_leads_to_cloud(leads: list):
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/real_leads"
        req = urllib.request.Request(
            url,
            data=json.dumps(leads).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to save leads: {e}")


def restore_leads_from_cloud() -> list:
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/real_leads"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        pass
    return []


def save_all_tasks_to_cloud():
    try:
        conn = sqlite3.connect(_get_db_path())
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM scrape_tasks").fetchall()
        conn.close()
        tasks = [dict(r) for r in rows]
        save_tasks_to_cloud(tasks)
        logger.info(f"[CloudBackup] Successfully backed up {len(tasks)} tasks to cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_tasks_to_cloud failed: {e}")


def restore_and_sync_tasks(conn: sqlite3.Connection):
    try:
        tasks = restore_tasks_from_cloud()
        if not tasks:
            return
        for t in tasks:
            conn.execute("""
                INSERT OR REPLACE INTO scrape_tasks (
                    id, business_type, city, state, country, status, leads_found, error_message, created_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["id"], t["business_type"], t["city"], t.get("state", ""), t.get("country", "USA"),
                t.get("status", "complete"), t.get("leads_found", 0), t.get("error_message", ""),
                t["created_at"], t.get("completed_at", "")
            ))
        conn.commit()
        logger.info(f"[CloudBackup] Successfully restored {len(tasks)} tasks from cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore tasks: {e}")


def save_all_leads_to_cloud():
    try:
        conn = sqlite3.connect(_get_db_path())
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM real_leads").fetchall()
        conn.close()
        leads = [dict(r) for r in rows]
        save_leads_to_cloud(leads)
        logger.info(f"[CloudBackup] Successfully backed up {len(leads)} leads to cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_leads_to_cloud failed: {e}")


def restore_and_sync_leads(conn: sqlite3.Connection):
    try:
        leads = restore_leads_from_cloud()
        if not leads:
            return
        for l in leads:
            conn.execute("""
                INSERT OR REPLACE INTO real_leads (
                    id, business_name, owner_name, email_primary, phone, website,
                    city, state, country, niche, full_address, current_rating, review_count, negative_review_count,
                    lead_score, lead_temperature, status, funnel_step, emails_sent_count, last_email_sent, last_reply, source, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                l["id"], l["business_name"], l.get("owner_name", ""), l.get("email_primary", ""),
                l.get("phone", ""), l.get("website", ""), l.get("city", ""), l.get("state", ""),
                l.get("country", "USA"), l.get("niche", ""), l.get("full_address", ""),
                float(l.get("current_rating", 0)), int(l.get("review_count", 0)), int(l.get("negative_review_count", 0)),
                int(l.get("lead_score", 0)), l.get("lead_temperature", "cold"), l.get("status", "new"),
                int(l.get("funnel_step", 0)), int(l.get("emails_sent_count", 0)), l.get("last_email_sent", ""),
                l.get("last_reply", ""), l.get("source", ""), l.get("notes", ""), l["created_at"], l.get("updated_at", l["created_at"])
            ))
        conn.commit()
        logger.info(f"[CloudBackup] Successfully restored {len(leads)} leads from cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore leads: {e}")

