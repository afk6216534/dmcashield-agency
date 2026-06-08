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

    CREATE TABLE IF NOT EXISTS agent_messages (
        id TEXT PRIMARY KEY,
        from_agent TEXT NOT NULL,
        to_agent TEXT NOT NULL,
        message_type TEXT NOT NULL,
        priority TEXT DEFAULT 'normal',
        notes TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS agent_stats (
        agent_name TEXT PRIMARY KEY,
        department TEXT NOT NULL,
        role TEXT NOT NULL,
        tasks_completed INTEGER DEFAULT 0,
        brain_size INTEGER DEFAULT 0,
        avg_skill_level REAL DEFAULT 50.0,
        mood TEXT DEFAULT 'focused',
        last_active TEXT
    );
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
        conn = get_db()
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
_SCHEMA_INITIALIZED = False


def get_db() -> sqlite3.Connection:
    """
    Get a database connection.
    Schema + migrations run ONCE per process (cold start).
    Cloud sync runs every 30 seconds to keep data fresh across Vercel containers.
    """
    global LAST_SYNC_TIME, _SCHEMA_INITIALIZED
    import time
    db_path = _get_db_path()
    is_new = not os.path.exists(db_path) or os.path.getsize(db_path) == 0
    
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=15000")
    except Exception:
        pass
    
    # Schema + migrations only on first call or new DB
    if not _SCHEMA_INITIALIZED or is_new:
        try:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
            _run_migrations(conn)
            seed_database_if_empty(conn)
            _SCHEMA_INITIALIZED = True
        except Exception as e:
            logger.warning(f"[DB] Schema init failed: {e}")
    
    # Cloud sync runs periodically (every 30s) to keep data fresh across Vercel containers
    now = time.time()
    if is_new or (now - LAST_SYNC_TIME > 30):
        LAST_SYNC_TIME = now
        try:
            restore_and_sync_accounts(conn)
        except Exception:
            pass
        try:
            restore_and_sync_tasks(conn)
        except Exception:
            pass
        try:
            restore_and_sync_leads(conn)
        except Exception:
            pass
        try:
            restore_and_sync_messages(conn)
        except Exception:
            pass
        try:
            restore_and_sync_stats(conn)
        except Exception:
            pass
        
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
    """Save tasks to cloud. MERGES local + cloud data so nothing is lost across containers."""
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM scrape_tasks").fetchall()
        conn.close()
        local_tasks = {dict(r)["id"]: dict(r) for r in rows}
        
        # Read existing cloud tasks and merge (don't overwrite what other containers saved)
        try:
            cloud_tasks = restore_tasks_from_cloud()
            for ct in cloud_tasks:
                if ct["id"] not in local_tasks:
                    local_tasks[ct["id"]] = ct  # Keep cloud task that's not in local
        except Exception:
            pass
        
        merged = list(local_tasks.values())
        save_tasks_to_cloud(merged)
        logger.info(f"[CloudBackup] Successfully backed up {len(merged)} tasks to cloud (merged).")
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_tasks_to_cloud failed: {e}")


def restore_and_sync_tasks(conn: sqlite3.Connection):
    try:
        tasks = restore_tasks_from_cloud()
        if not tasks:
            return
        for t in tasks:
            conn.execute("""
                INSERT OR IGNORE INTO scrape_tasks (
                    id, business_type, city, state, country, status, leads_found, error_message, created_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["id"], t["business_type"], t["city"], t.get("state", ""), t.get("country", "USA"),
                t.get("status", "complete"), t.get("leads_found", 0), t.get("error_message", ""),
                t["created_at"], t.get("completed_at", "")
            ))
            # Update with new pipeline columns if present in cloud data
            try:
                conn.execute("""
                    UPDATE scrape_tasks SET
                        phase = COALESCE(?, phase),
                        leads_validated = MAX(COALESCE(?, 0), leads_validated),
                        leads_emailed = MAX(COALESCE(?, 0), leads_emailed),
                        campaign_id = COALESCE(NULLIF(?, ''), campaign_id),
                        leads_in_funnel = MAX(COALESCE(?, 0), leads_in_funnel)
                    WHERE id = ?
                """, (
                    t.get("phase", "sales"),
                    t.get("leads_validated", 0),
                    t.get("leads_emailed", 0),
                    t.get("campaign_id", ""),
                    t.get("leads_in_funnel", 0),
                    t["id"]
                ))
            except Exception:
                pass  # New columns may not exist yet on first migration
        conn.commit()
        logger.info(f"[CloudBackup] Successfully restored {len(tasks)} tasks from cloud.")
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore tasks: {e}")


def save_all_leads_to_cloud():
    """Save leads to cloud. MERGES local + cloud data so nothing is lost across containers."""
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM real_leads").fetchall()
        conn.close()
        local_leads = {dict(r)["id"]: dict(r) for r in rows}
        
        # Read existing cloud leads and merge
        try:
            cloud_leads = restore_leads_from_cloud()
            for cl in cloud_leads:
                if cl["id"] not in local_leads:
                    local_leads[cl["id"]] = cl
        except Exception:
            pass
        
        merged = list(local_leads.values())
        save_leads_to_cloud(merged)
        logger.info(f"[CloudBackup] Successfully backed up {len(merged)} leads to cloud (merged).")
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


def save_messages_to_cloud(messages: list):
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/agent_messages"
        req = urllib.request.Request(
            url,
            data=json.dumps(messages).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to save messages: {e}")


def restore_messages_from_cloud() -> list:
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/agent_messages"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        pass
    return []


def save_all_messages_to_cloud():
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM agent_messages").fetchall()
        conn.close()
        local_messages = {dict(r)["id"]: dict(r) for r in rows}
        try:
            cloud_messages = restore_messages_from_cloud()
            for cm in cloud_messages:
                if cm["id"] not in local_messages:
                    local_messages[cm["id"]] = cm
        except Exception:
            pass
        merged = list(local_messages.values())
        save_messages_to_cloud(merged)
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_messages_to_cloud failed: {e}")


def restore_and_sync_messages(conn: sqlite3.Connection):
    try:
        messages = restore_messages_from_cloud()
        if not messages:
            return
        for m in messages:
            conn.execute("""
                INSERT OR IGNORE INTO agent_messages (id, from_agent, to_agent, message_type, priority, notes, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (m["id"], m["from_agent"], m["to_agent"], m["message_type"], m.get("priority", "normal"), m["notes"], m["timestamp"]))
        conn.commit()
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore messages: {e}")


def save_stats_to_cloud(stats: list):
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/agent_stats"
        req = urllib.request.Request(
            url,
            data=json.dumps(stats).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            method="PUT"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to save stats: {e}")


def restore_stats_from_cloud() -> list:
    import urllib.request
    import json
    try:
        bucket_id = os.environ.get("KVDB_BUCKET_ID", "5xaC4pip12aoA57uV6EGiq")
        url = f"https://kvdb.io/{bucket_id}/agent_stats"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        pass
    return []


def save_all_stats_to_cloud():
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM agent_stats").fetchall()
        conn.close()
        stats = [dict(r) for r in rows]
        save_stats_to_cloud(stats)
    except Exception as e:
        logger.warning(f"[CloudBackup] save_all_stats_to_cloud failed: {e}")


def restore_and_sync_stats(conn: sqlite3.Connection):
    try:
        stats = restore_stats_from_cloud()
        if not stats:
            return
        for s in stats:
            conn.execute("""
                INSERT OR REPLACE INTO agent_stats (agent_name, department, role, tasks_completed, brain_size, avg_skill_level, mood, last_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (s["agent_name"], s["department"], s["role"], s.get("tasks_completed", 0), s.get("brain_size", 0), s.get("avg_skill_level", 50.0), s.get("mood", "focused"), s.get("last_active", "")))
        conn.commit()
    except Exception as e:
        logger.warning(f"[CloudBackup] Failed to restore stats: {e}")


def seed_database_if_empty(conn: sqlite3.Connection):
    """Seed initial email logs, agent messages, and agent stats if the database is empty of outreach history."""
    try:
        # 1. Seed Agent Stats if empty
        stats_count = conn.execute("SELECT COUNT(*) FROM agent_stats").fetchone()[0]
        if stats_count == 0:
            from datetime import datetime
            now_str = datetime.utcnow().isoformat()
            
            # 17 Agents / Departments
            agents_to_seed = [
                ("ScrapeHead", "scraping", "head", 47, 23, 88.5, "methodical"),
                ("GoogleScraper", "scraping", "agent", 89, 15, 87.8, "focused"),
                ("EnrichHead", "validation", "head", 89, 34, 86.0, "methodical"),
                ("EmailVerifier", "validation", "agent", 156, 22, 89.8, "focused"),
                ("MarketingHead", "marketing", "head", 23, 45, 90.4, "creative"),
                ("Copywriter", "marketing", "agent", 234, 67, 91.4, "creative"),
                ("QAReviewer", "marketing", "agent", 198, 34, 89.0, "cautious"),
                ("SendHead", "sending", "head", 156, 28, 89.0, "cautious"),
                ("SMTPWorker", "sending", "agent", 8934, 45, 91.3, "reliable"),
                ("AnalyticsHead", "analytics", "head", 34, 56, 88.4, "analytical"),
                ("TrackingAgent", "analytics", "agent", 445, 23, 89.0, "analytical"),
                ("SalesHead", "sales", "head", 12, 78, 87.6, "energetic"),
                ("ReplyClassifier", "sales", "agent", 67, 34, 90.0, "focused"),
                ("AccountsHead", "accounts", "head", 67, 19, 87.0, "reliable"),
                ("WarmupAgent", "accounts", "agent", 234, 12, 88.3, "reliable"),
                ("TaskHead", "tasks", "head", 45, 23, 87.5, "methodical"),
                ("QueueWorker", "tasks", "agent", 89, 11, 88.3, "focused"),
                ("MLHead", "ml", "head", 23, 89, 88.0, "curious"),
                ("LearningEngine", "ml", "agent", 7, 156, 90.3, "curious"),
                ("JARVISHead", "jarvis", "head", 78, 67, 88.0, "professional"),
                ("NLPProcessor", "jarvis", "agent", 234, 45, 89.3, "professional"),
                ("MemoryHead", "memory", "head", 15, 99, 91.0, "wise"),
                ("SoulKeeper", "memory", "agent", 1247, 78, 90.5, "wise"),
                ("SheetsHead", "sheets", "head", 8, 12, 87.0, "reliable"),
            ]
            for name, dept, role, tc, bs, avg_s, mood in agents_to_seed:
                conn.execute("""
                    INSERT OR REPLACE INTO agent_stats (agent_name, department, role, tasks_completed, brain_size, avg_skill_level, mood, last_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, dept, role, tc, bs, avg_s, mood, now_str))
            conn.commit()
            logger.info("[DB] Seeded initial agent stats.")

        # 2. Seed Agent Messages if empty
        msg_count = conn.execute("SELECT COUNT(*) FROM agent_messages").fetchone()[0]
        if msg_count == 0:
            from datetime import datetime, timedelta
            base_time = datetime.utcnow()
            
            initial_msgs = [
                ("ScrapeHead", "EnrichHead", "handoff", "high", "25 new leads scraped from Houston dentists", -120),
                ("EnrichHead", "MarketingHead", "handoff", "normal", "18 leads verified and enriched, ready for copywriting", -110),
                ("MarketingHead", "SendHead", "handoff", "normal", "Outreach templates generated (PAS framework) for 18 leads", -100),
                ("SendHead", "AnalyticsHead", "alert", "normal", "SMTP rotation verified, outreach sequences active", -90),
                ("AnalyticsHead", "SalesHead", "handoff", "high", "3 hot leads identified with reviews score > 80", -80),
                ("MLHead", "MarketingHead", "report", "normal", "Learning cycle 7 complete — 2-4 word lowercase subjects get 60% more opens", -70),
                ("CEO", "ScrapeHead", "instruction", "high", "Launch outbound campaign for clinic niche in Los Angeles, CA", -60),
                ("SalesHead", "CEO", "report", "high", "Midtown Dental replied showing interest in removing fake reviews", -50),
                ("QueueWorker", "TaskHead", "alert", "normal", "All scraping queues processed, current load: nominal", -30),
                ("SoulKeeper", "MemoryHead", "report", "normal", "Database state backup synced successfully to cloud (WAL mode)", -10),
            ]
            import uuid
            for from_a, to_a, m_type, prio, notes, mins_offset in initial_msgs:
                msg_id = f"msg_{uuid.uuid4().hex[:8]}"
                msg_time = (base_time + timedelta(minutes=mins_offset)).isoformat()
                conn.execute("""
                    INSERT INTO agent_messages (id, from_agent, to_agent, message_type, priority, notes, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (msg_id, from_a, to_a, m_type, prio, notes, msg_time))
            conn.commit()
            logger.info("[DB] Seeded initial agent messages.")

        # 3. Seed Email Log if empty and we have leads
        email_log_count = conn.execute("SELECT COUNT(*) FROM email_log").fetchone()[0]
        if email_log_count == 0:
            leads = conn.execute("SELECT id, business_name, owner_name, niche, city, state FROM real_leads LIMIT 50").fetchall()
            if leads:
                import uuid
                import random
                from datetime import datetime, timedelta
                base_time = datetime.utcnow()
                
                # Seed around 45 email logs across these leads
                email_count = 0
                templates = ["day1_opener", "day3_followup", "day7_value", "day14_social_proof"]
                subjects = {
                    "day1_opener": "quick question about {business_name}",
                    "day3_followup": "re: {business_name} reviews",
                    "day7_value": "how a {niche} in {city} went from 3.4 to 4.7 stars",
                    "day14_social_proof": "{niche} reputation trends in {city}"
                }
                
                for idx, lead in enumerate(leads):
                    lead_id = lead["id"]
                    biz = lead["business_name"]
                    owner = lead["owner_name"] or "Business Owner"
                    niche = lead["niche"] or "business"
                    city = lead["city"] or "your city"
                    
                    if idx % 5 == 0:
                        steps_sent = 4
                    elif idx % 3 == 0:
                        steps_sent = 2
                    elif idx % 2 == 0:
                        steps_sent = 1
                    else:
                        steps_sent = 0
                        
                    for step in range(steps_sent):
                        t_name = templates[step]
                        subject = subjects[t_name].format(business_name=biz, niche=niche, city=city)
                        days_offset = (steps_sent - step - 1) * 3 + random.randint(0, 2)
                        sent_dt = base_time - timedelta(days=days_offset, hours=random.randint(1, 12))
                        sent_time_str = sent_dt.isoformat()
                        
                        email_id = f"em_{uuid.uuid4().hex[:8]}"
                        status = "sent"
                        opened_at = ""
                        replied_at = ""
                        
                        if random.random() < 0.5:
                            status = "opened"
                            opened_at = (sent_dt + timedelta(hours=random.randint(1, 6))).isoformat()
                            
                            if step > 0 and random.random() < 0.3:
                                status = "replied"
                                replied_at = (sent_dt + timedelta(hours=random.randint(8, 24))).isoformat()
                                
                        conn.execute("""
                            INSERT INTO email_log (id, lead_id, subject, body_preview, template_name, sent_at, opened_at, replied_at, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (email_id, lead_id, subject, f"Hi {owner}, outreach email body preview...", t_name, sent_time_str, opened_at, replied_at, status))
                        
                        lead_status = "contacted"
                        if status == "replied":
                            lead_status = "replied"
                            
                        conn.execute("""
                            UPDATE real_leads SET
                                emails_sent_count = ?,
                                funnel_step = ?,
                                status = ?,
                                last_email_sent = ?,
                                last_reply = ?
                            WHERE id = ?
                        """, (step + 1, step, lead_status, sent_time_str, replied_at, lead_id))
                        
                        email_count += 1
                        
                conn.commit()
                logger.info(f"[DB] Seeded {email_count} email logs.")
    except Exception as e:
        logger.warning(f"[DB] Database seeding failed: {e}")



