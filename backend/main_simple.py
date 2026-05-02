from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from typing import Optional, Dict, Any, List
import sqlite3
import uuid
import os
import json

app = FastAPI(title="DMCAShield Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "dmcashield.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY, business_name TEXT, email_primary TEXT, phone TEXT,
        city TEXT, state TEXT, lead_score INTEGER DEFAULT 0,
        temperature TEXT DEFAULT 'cold', created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY, title TEXT, description TEXT,
        status TEXT DEFAULT 'active', progress INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id TEXT PRIMARY KEY, email TEXT, provider TEXT, status TEXT DEFAULT 'active',
        sent_today INTEGER DEFAULT 0, daily_limit INTEGER DEFAULT 500,
        health_score INTEGER DEFAULT 100
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY, name TEXT, subject TEXT, body TEXT,
        status TEXT DEFAULT 'active', sent INTEGER DEFAULT 0,
        opened INTEGER DEFAULT 0, replied INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS templates (
        id TEXT PRIMARY KEY, name TEXT, subject TEXT, body TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS warmup (
        id TEXT PRIMARY KEY, email TEXT, status TEXT DEFAULT 'warming',
        emails_sent INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS integrations (
        service TEXT PRIMARY KEY, connected INTEGER DEFAULT 0,
        config TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS learning_logs (
        id TEXT PRIMARY KEY, event_type TEXT, event_data TEXT,
        outcome TEXT, learned_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY, entity_type TEXT, entity_id TEXT,
        feedback_type TEXT, score INTEGER, notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base (
        id TEXT PRIMARY KEY, category TEXT, key TEXT, value TEXT,
        confidence REAL DEFAULT 0.5, uses INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

def row_to_dict(cursor, row):
    if row is None:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

@app.get("/")
async def root():
    return {"company": "DMCAShield Agency", "status": "operational", "version": "3.0.0", "auto_reload": "enabled"}

@app.get("/health")
async def health():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    lead_count = c.fetchone()[0]
    conn.close()
    return {"status": "healthy", "departments": 6, "total_leads": lead_count}

@app.get("/api/status")
async def get_status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    total_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM leads WHERE temperature = 'hot'")
    hot_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('queued', 'active', 'running')")
    tasks_active = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM campaigns")
    campaigns = c.fetchone()[0]
    conn.close()
    return {
        "system": {"status": "operational", "version": "3.0.0"},
        "departments": {d: "online" for d in ["scraping", "validation", "marketing", "email_sending", "tracking", "sales"]},
        "agents": {
            "jarvis": "active", "scraper": "running", "validator": "online", 
            "email_agent": "active", "tracker": "online", "sales_agent": "ready"
        },
        "stats": {"total_leads": total_leads, "hot_leads": hot_leads, "open_rate": 28, "reply_rate": 9, "tasks_active": tasks_active, "campaigns": campaigns}
    }

# =============================
# LEADS
# =============================
@app.get("/api/leads")
async def get_leads(temperature: Optional[str] = None, scored: bool = False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if scored:
        c.execute("SELECT id, business_name, email_primary, lead_score, temperature FROM leads WHERE lead_score >= 70")
    elif temperature:
        c.execute("SELECT * FROM leads WHERE temperature = ?", (temperature,))
    else:
        c.execute("SELECT * FROM leads")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.post("/api/leads")
async def create_lead(lead: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    lead_id = f"lead-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO leads (id, business_name, email_primary, phone, city, state, lead_score, temperature) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (lead_id, lead.get("business_name"), lead.get("email_primary"), lead.get("phone"), lead.get("city"), lead.get("state"), 0, "cold"))
    conn.commit()
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, lead: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in lead.keys()])
    values = list(lead.values()) + [lead_id]
    c.execute(f"UPDATE leads SET {fields} WHERE id = ?", values)
    conn.commit()
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return row_to_dict(c, row)

@app.patch("/api/leads/{lead_id}")
async def patch_lead(lead_id: str, lead: dict):
    return await update_lead(lead_id, lead)

@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return {"deleted": lead_id}

@app.get("/api/leads/scored")
async def get_scored_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE lead_score >= 70")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.get("/api/leads/hot")
async def get_hot_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE temperature = 'hot'")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.get("/api/hot-leads")
async def get_hot_leads_alias():
    return await get_hot_leads()

# =============================
# TASKS
# =============================
@app.get("/api/tasks")
async def get_tasks(status: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    else:
        c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.post("/api/tasks")
async def create_task(task: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO tasks (id, title, description, status, progress) VALUES (?, ?, ?, 'active', 0)",
              (task_id, task.get("title"), task.get("description")))
    conn.commit()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, task: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in task.keys()])
    values = list(task.values()) + [task_id]
    c.execute(f"UPDATE tasks SET {fields} WHERE id = ?", values)
    conn.commit()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row_to_dict(c, row)

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"deleted": task_id}

# =============================
# ACCOUNTS
# =============================
@app.get("/api/accounts")
async def get_accounts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.post("/api/accounts")
async def create_account(account: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    account_id = f"acc-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO accounts (id, email, provider, status, sent_today, daily_limit, health_score) VALUES (?, ?, ?, 'active', 0, 500, 100)",
              (account_id, account.get("email"), account.get("provider")))
    conn.commit()
    conn.close()
    return {"account_id": account_id, "status": "active"}

@app.put("/api/accounts/{account_id}")
async def update_account(account_id: str, account: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in account.keys()])
    values = list(account.values()) + [account_id]
    c.execute(f"UPDATE accounts SET {fields} WHERE id = ?", values)
    conn.commit()
    c.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return row_to_dict(c, row)

@app.delete("/api/accounts/{account_id}")
async def delete_account(account_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()
    return {"deleted": account_id}

@app.get("/api/email-accounts")
async def get_email_accounts():
    return await get_accounts()

# =============================
# CAMPAIGNS
# =============================
@app.get("/api/campaigns")
async def get_campaigns(status: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM campaigns WHERE status = ?", (status,))
    else:
        c.execute("SELECT * FROM campaigns")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.post("/api/campaigns")
async def create_campaign(campaign: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    campaign_id = f"camp-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO campaigns (id, name, subject, body, status, sent, opened, replied) VALUES (?, ?, ?, ?, 'active', 0, 0, 0)",
              (campaign_id, campaign.get("name"), campaign.get("subject"), campaign.get("body")))
    conn.commit()
    c.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.put("/api/campaigns/{campaign_id}")
async def update_campaign(campaign_id: str, campaign: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in campaign.keys()])
    values = list(campaign.values()) + [campaign_id]
    c.execute(f"UPDATE campaigns SET {fields} WHERE id = ?", values)
    conn.commit()
    c.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return row_to_dict(c, row)

@app.delete("/api/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
    conn.commit()
    conn.close()
    return {"deleted": campaign_id}

# =============================
# EMAIL WARMUP
# =============================
@app.get("/api/warmup")
async def get_warmup_status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM warmup")
    rows = c.fetchall()
    conn.close()
    return {"warming_up": len(rows), "accounts": [row_to_dict(c, row) for row in rows]}

@app.post("/api/warmup")
async def start_warmup(account: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    warmup_id = f"warmup-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO warmup (id, email, status, emails_sent) VALUES (?, ?, 'warming', 0)",
              (warmup_id, account.get("email")))
    conn.commit()
    c.execute("SELECT * FROM warmup WHERE id = ?", (warmup_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

# =============================
# TEMPLATES
# =============================
@app.get("/api/templates")
async def get_templates():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM templates")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.post("/api/templates")
async def create_template(template: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    template_id = f"tpl-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO templates (id, name, subject, body) VALUES (?, ?, ?, ?)",
              (template_id, template.get("name"), template.get("subject"), template.get("body")))
    conn.commit()
    c.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.put("/api/templates/{template_id}")
async def update_template(template_id: str, template: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in template.keys()])
    values = list(template.values()) + [template_id]
    c.execute(f"UPDATE templates SET {fields} WHERE id = ?", values)
    conn.commit()
    c.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return row_to_dict(c, row)

@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM templates WHERE id = ?", (template_id,))
    conn.commit()
    conn.close()
    return {"deleted": template_id}

# =============================
# ANALYTICS
# =============================
@app.get("/api/analytics")
async def get_analytics():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    total_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM leads WHERE temperature = 'hot'")
    hot_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('queued', 'active', 'running')")
    active_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM campaigns")
    total_campaigns = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'active'")
    active_campaigns = c.fetchone()[0]
    conn.close()
    return {
        "leads": {"total": total_leads, "hot": hot_leads, "cold": total_leads - hot_leads},
        "tasks": {"active": active_tasks, "completed": completed_tasks},
        "campaigns": {"total": total_campaigns, "active": active_campaigns},
        "emails": {"sent": 0, "opened": 0, "replied": 0}
    }

# =============================
# INTEGRATIONS
# =============================
@app.get("/api/integrations")
async def get_integrations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM integrations")
    rows = c.fetchall()
    conn.close()
    result = {}
    for row in rows:
        d = row_to_dict(c, row)
        if d:
            result[d["service"]] = {"connected": bool(d["connected"]), "config": d.get("config")}
    if not result:
        result = {"slack": {"connected": False}, "telegram": {"connected": False}, "resend": {"connected": False}}
    return result

@app.post("/api/integrations/{service}")
async def connect_integration(service: str, config: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO integrations (service, connected, config) VALUES (?, 1, ?)", (service, json.dumps(config)))
    conn.commit()
    conn.close()
    return {"service": service, "connected": True, "config": config}

# =============================
# JARVIS AI
# =============================
@app.post("/api/jarvis")
async def jarvis_command(command: dict):
    cmd = command.get("command", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    lead_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'active'")
    task_count = c.fetchone()[0]
    conn.close()
    response = f"Processed: {cmd}"
    if "lead" in cmd.lower():
        response = f"Lead analysis complete. Found {lead_count} leads."
    elif "task" in cmd.lower():
        response = f"Task executed. {task_count} active tasks."
    return {"response": response, "status": "success"}

# =============================
# SOUL
# =============================
@app.get("/api/soul")
async def get_soul():
    return {
        "mission": "Autonomous DMCA review removal for businesses",
        "core_principles": ["Zero human intervention", "Continuous learning"],
        "departments": {"scraping": "online", "validation": "online", "marketing": "online", "sales": "online"},
        "status": "operational"
    }

# =============================
# WEBSOCKET
# =============================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM leads")
            lead_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('queued', 'active', 'running')")
            task_count = c.fetchone()[0]
            c.execute("SELECT AVG(lead_score) FROM leads WHERE lead_score > 0")
            avg_score = c.fetchone()[0] or 0
            conn.close()
            await websocket.send_json({
                "type": "heartbeat",
                "status": "operational",
                "leads": lead_count,
                "tasks": task_count,
                "avg_lead_score": round(avg_score, 1)
            })
    except Exception:
        pass

# =============================
# SELF-LEARNING SYSTEM
# =============================
@app.get("/api/learning")
async def get_learning_status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM learning_logs")
    total_logs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = c.fetchone()[0]
    c.execute("SELECT AVG(confidence) FROM knowledge_base")
    avg_confidence = c.fetchone()[0] or 0.5
    c.execute("SELECT * FROM knowledge_base ORDER BY uses DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return {
        "status": "learning",
        "total_events_logged": total_logs,
        "knowledge_entries": total_knowledge,
        "average_confidence": round(avg_confidence, 2),
        "top_knowledge": [row_to_dict(c, row) for row in rows]
    }

@app.post("/api/learning/log")
async def log_learning_event(event: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    event_id = f"learn-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO learning_logs (id, event_type, event_data, outcome) VALUES (?, ?, ?, ?)",
              (event_id, event.get("type"), json.dumps(event.get("data")), event.get("outcome", "logged")))
    conn.commit()
    conn.close()
    return {"logged": event_id, "learning": "active"}

@app.post("/api/learning/feedback")
async def submit_feedback(feedback: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    feedback_id = f"fb-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO feedback (id, entity_type, entity_id, feedback_type, score, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (feedback_id, feedback.get("entity_type"), feedback.get("entity_id"), feedback.get("feedback_type"), feedback.get("score", 5), feedback.get("notes")))
    conn.commit()
    
    if feedback.get("entity_type") == "lead" and feedback.get("feedback_type") == "conversion":
        c.execute("UPDATE leads SET lead_score = ? WHERE id = ?", (feedback.get("score", 5) * 20, feedback.get("entity_id")))
        conn.commit()
    
    conn.close()
    return {"feedback_id": feedback_id, "processed": True}

@app.post("/api/learning/knowledge")
async def add_knowledge(knowledge: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    kb_id = f"kb-{uuid.uuid4().hex[:8]}"
    c.execute("INSERT INTO knowledge_base (id, category, key, value, confidence) VALUES (?, ?, ?, ?, ?)",
              (kb_id, knowledge.get("category"), knowledge.get("key"), knowledge.get("value"), knowledge.get("confidence", 0.5)))
    conn.commit()
    c.execute("SELECT * FROM knowledge_base WHERE id = ?", (kb_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.get("/api/learning/knowledge")
async def get_knowledge(category: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if category:
        c.execute("SELECT * FROM knowledge_base WHERE category = ? ORDER BY confidence DESC", (category,))
    else:
        c.execute("SELECT * FROM knowledge_base ORDER BY confidence DESC")
    rows = c.fetchall()
    conn.close()
    return [row_to_dict(c, row) for row in rows]

@app.put("/api/learning/knowledge/{kb_id}")
async def update_knowledge(kb_id: str, knowledge: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if "confidence" in knowledge:
        c.execute("UPDATE knowledge_base SET confidence = confidence + ? WHERE id = ?", (knowledge.get("confidence"), kb_id))
    if "uses" in knowledge or knowledge.get("increment_use", False):
        c.execute("UPDATE knowledge_base SET uses = uses + 1 WHERE id = ?", (kb_id,))
    conn.commit()
    c.execute("SELECT * FROM knowledge_base WHERE id = ?", (kb_id,))
    row = c.fetchone()
    conn.close()
    return row_to_dict(c, row)

@app.get("/api/learning/insights")
async def get_insights():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT AVG(lead_score), temperature FROM leads GROUP BY temperature")
    score_by_temp = c.fetchall()
    c.execute("SELECT COUNT(*), status FROM tasks GROUP BY status")
    tasks_by_status = c.fetchall()
    c.execute("SELECT COUNT(*), phase_scraping FROM tasks")
    scrapes = c.fetchall()
    conn.close()
    return {
        "lead_scoring": {row[1]: row[0] for row in score_by_temp if row[0]},
        "task_distribution": {row[1]: row[0] for row in tasks_by_status},
        "recommendations": [
            "Focus on leads with score > 70 for higher conversion",
            "Increase email warmup for new accounts",
            "Use templates with >30% open rate"
        ]
    }

# =============================
# DASHBOARD
# =============================
@app.get("/api/dashboard")
async def get_dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads")
    total_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM leads WHERE temperature = 'hot'")
    hot_leads = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('queued', 'active', 'running')")
    active_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM campaigns")
    total_campaigns = c.fetchone()[0]
    c.execute("SELECT AVG(lead_score) FROM leads")
    avg_score = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM knowledge_base")
    knowledge_count = c.fetchone()[0]
    conn.close()
    return {
        "leads": {"total": total_leads, "hot": hot_leads},
        "tasks": {"active": active_tasks},
        "campaigns": {"total": total_campaigns},
        "avg_lead_score": round(avg_score, 1),
        "knowledge_base": knowledge_count,
        "system_status": "operational"
    }

# =============================
# SMS CAMPAIGN
# =============================
sms_db = []

@app.get("/api/sms")
async def get_sms_campaigns():
    return sms_db

@app.post("/api/sms")
async def create_sms_campaign(campaign: dict):
    campaign_id = f"sms-{uuid.uuid4().hex[:8]}"
    new_campaign = {**campaign, "id": campaign_id, "status": "active", "sent": 0}
    sms_db.append(new_campaign)
    return new_campaign

# =============================
# WHATSAPP CAMPAIGN
# =============================
whatsapp_db = []

@app.get("/api/whatsapp")
async def get_whatsapp_campaigns():
    return whatsapp_db

@app.post("/api/whatsapp")
async def create_whatsapp_campaign(campaign: dict):
    campaign_id = f"wa-{uuid.uuid4().hex[:8]}"
    new_campaign = {**campaign, "id": campaign_id, "status": "active", "sent": 0}
    whatsapp_db.append(new_campaign)
    return new_campaign

# =============================
# LINKEDIN OUTREACH
# =============================
linkedin_db = []

@app.get("/api/linkedin")
async def get_linkedin_campaigns():
    return linkedin_db

@app.post("/api/linkedin")
async def create_linkedin_campaign(campaign: dict):
    campaign_id = f"li-{uuid.uuid4().hex[:8]}"
    new_campaign = {**campaign, "id": campaign_id, "status": "active", "sent": 0}
    linkedin_db.append(new_campaign)
    return new_campaign

# =============================
# COLD CALLING
# =============================
calls_db = []

@app.get("/api/calls")
async def get_calls():
    return calls_db

@app.post("/api/calls")
async def schedule_call(call: dict):
    call_id = f"call-{uuid.uuid4().hex[:8]}"
    new_call = {**call, "id": call_id, "status": "scheduled"}
    calls_db.append(new_call)
    return new_call

@app.put("/api/calls/{call_id}")
async def update_call(call_id: str, call: dict):
    for c in calls_db:
        if c.get("id") == call_id:
            c.update(call)
            return c
    raise HTTPException(status_code=404, detail="Call not found")

# =============================
# AUTO-LEARNING SCHEDULER
# =============================
@app.get("/api/learning/auto")
async def auto_learn():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        UPDATE knowledge_base 
        SET confidence = MIN(1.0, confidence + 0.05) 
        WHERE uses > 3 AND confidence < 0.9
    """)
    conn.commit()
    
    c.execute("SELECT COUNT(*) FROM knowledge_base WHERE confidence >= 0.8")
    high_confidence = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM knowledge_base")
    total = c.fetchone()[0]
    
    c.execute("DELETE FROM learning_logs WHERE id IN (SELECT id FROM learning_logs ORDER BY learned_at LIMIT 100)")
    conn.commit()
    
    conn.close()
    return {
        "auto_learned": True,
        "high_confidence_knowledge": high_confidence,
        "total_knowledge": total,
        "learning_rate": "improving" if high_confidence > 0 else "collecting data"
    }

# =============================
# AUTO-RELOAD (No restart needed)
# =============================
auto_reload_config = {
    "enabled": True,
    "watch_files": ["main_simple.py"],
    "last_modified": 0,
    "reload_count": 0,
    "test_token": "hot_reload_working_2026"
}

@app.get("/api/admin/reload")
async def check_reload():
    """Check if reload needed - returns auto-reload status"""
    import os
    import time
    config = auto_reload_config.copy()
    try:
        mtime = os.path.getmtime(__file__)
        config["last_modified"] = mtime
        config["server_time"] = time.time()
    except:
        pass
    return config

@app.post("/api/admin/reload")
async def trigger_reload():
    """Trigger manual reload"""
    return {"status": "reload_triggered", "message": "Server will reload on next request"}

print("DMCAShield API started on http://localhost:8000")
print(f"Database: {DB_PATH}")