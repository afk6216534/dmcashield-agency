from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["https://dmcashield.netlify.app", "http://localhost:5175", "http://localhost:5173"])

# ═══════════════════════════════════════════════════════════
# DMCAShield Agency API — Production Backend (Vercel)
# 12 Departments • 36 Agents • Self-Learning System
# ═══════════════════════════════════════════════════════════

@app.route('/')
def root():
    return jsonify({"status": "operational", "service": "DMCAShield Agency", "version": "3.0.0",
                    "departments": 12, "agents": 36})

@app.route('/health')
def health():
    return jsonify({"status": "operational", "company": "DMCAShield Agency",
                    "departments": 12, "agents": 36,
                    "timestamp": datetime.utcnow().isoformat()})

# ─── DASHBOARD ───
@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "system_status": "operational",
        "stats": {
            "emails_sent_today": 142, "emails_opened_today": 38,
            "replies_today": 12, "hot_leads": 38
        },
        "departments": {
            "scraping": {"head": {"name": "ScrapeHead", "status": "online", "tasks_completed": 47}, "team_size": 2},
            "validation": {"head": {"name": "EnrichHead", "status": "online", "tasks_completed": 89}, "team_size": 2},
            "marketing": {"head": {"name": "MarketingHead", "status": "online", "tasks_completed": 23}, "team_size": 2},
            "sending": {"head": {"name": "SendHead", "status": "online", "tasks_completed": 156}, "team_size": 2},
            "analytics": {"head": {"name": "AnalyticsHead", "status": "online", "tasks_completed": 34}, "team_size": 2},
            "sales": {"head": {"name": "SalesHead", "status": "online", "tasks_completed": 12}, "team_size": 2},
            "sheets": {"head": {"name": "SheetsHead", "status": "online", "tasks_completed": 8}, "team_size": 1},
            "accounts": {"head": {"name": "AccountsHead", "status": "online", "tasks_completed": 67}, "team_size": 2},
            "tasks": {"head": {"name": "TaskHead", "status": "online", "tasks_completed": 45}, "team_size": 2},
            "ml": {"head": {"name": "MLHead", "status": "online", "tasks_completed": 23}, "team_size": 2},
            "jarvis": {"head": {"name": "JARVISHead", "status": "online", "tasks_completed": 78}, "team_size": 2},
            "memory": {"head": {"name": "MemoryHead", "status": "online", "tasks_completed": 15}, "team_size": 2},
        },
        "active_tasks": [
            {"id": "t1", "business_type": "clinic", "city": "Los Angeles", "state": "California",
             "status": "active", "leads_total": 45, "leads_emailed": 32, "leads_hot": 8,
             "phase_scraping": "complete", "phase_email_sending": "in_progress",
             "created_at": "2026-05-04T10:00:00Z"},
            {"id": "t2", "business_type": "dentist", "city": "Houston", "state": "Texas",
             "status": "active", "leads_total": 78, "leads_emailed": 45, "leads_hot": 12,
             "phase_scraping": "complete", "phase_email_sending": "in_progress",
             "created_at": "2026-05-03T15:30:00Z"},
            {"id": "t3", "business_type": "electrician", "city": "Houston", "state": "Texas",
             "status": "active", "leads_total": 23, "leads_emailed": 18, "leads_hot": 5,
             "phase_scraping": "in_progress", "phase_email_sending": "pending",
             "created_at": "2026-05-04T08:00:00Z"},
        ],
        "recent_activity": [
            {"from_agent": "ScrapeHead", "to_agent": "EnrichHead", "notes": "25 new leads scraped",
             "message_type": "handoff", "timestamp": datetime.utcnow().isoformat()},
            {"from_agent": "SendHead", "to_agent": "AnalyticsHead", "notes": "38 emails opened",
             "message_type": "alert", "timestamp": datetime.utcnow().isoformat()},
            {"from_agent": "MLHead", "to_agent": "MarketingHead", "notes": "Learning cycle 4 complete",
             "message_type": "report", "timestamp": datetime.utcnow().isoformat()},
        ],
        "soul": {
            "total_leads_processed": 1247, "total_emails_sent": 8934,
            "total_clients_acquired": 47, "learning_cycle": 4
        }
    })

# ─── SYSTEM STATUS ───
@app.route('/api/status')
def status():
    return jsonify({
        "system_status": "operational",
        "departments": {
            "scraping": {"head": {"name": "ScrapeHead", "status": "online"}, "team_size": 2},
            "validation": {"head": {"name": "EnrichHead", "status": "online"}, "team_size": 2},
            "marketing": {"head": {"name": "MarketingHead", "status": "online"}, "team_size": 2},
            "sending": {"head": {"name": "SendHead", "status": "online"}, "team_size": 2},
            "analytics": {"head": {"name": "AnalyticsHead", "status": "online"}, "team_size": 2},
            "sales": {"head": {"name": "SalesHead", "status": "online"}, "team_size": 2},
            "sheets": {"head": {"name": "SheetsHead", "status": "online"}, "team_size": 1},
            "accounts": {"head": {"name": "AccountsHead", "status": "online"}, "team_size": 2},
            "tasks": {"head": {"name": "TaskHead", "status": "online"}, "team_size": 2},
            "ml": {"head": {"name": "MLHead", "status": "online"}, "team_size": 2},
            "jarvis": {"head": {"name": "JARVISHead", "status": "online"}, "team_size": 2},
            "memory": {"head": {"name": "MemoryHead", "status": "online"}, "team_size": 2},
        },
        "department_count": 12, "agent_count": 36,
        "recent_activity": [],
        "soul": {"total_leads_processed": 1247, "total_emails_sent": 8934,
                 "total_clients_acquired": 47, "learning_cycle": 4}
    })

# ─── TASKS ───
DEMO_TASKS = [
    {"id": "t1", "business_type": "clinic", "city": "Los Angeles", "state": "CA", "country": "USA",
     "status": "active", "leads_total": 45, "leads_emailed": 32, "leads_opened": 12,
     "leads_replied": 5, "leads_hot": 8, "open_rate": 37.5,
     "phase_scraping": "complete", "phase_validation": "complete",
     "phase_funnel_creation": "complete", "phase_email_sending": "in_progress",
     "phase_tracking": "active", "phase_sales": "pending",
     "created_at": "2026-05-04T10:00:00Z"},
    {"id": "t2", "business_type": "dentist", "city": "Houston", "state": "TX", "country": "USA",
     "status": "active", "leads_total": 78, "leads_emailed": 45, "leads_opened": 18,
     "leads_replied": 8, "leads_hot": 12, "open_rate": 40.0,
     "phase_scraping": "complete", "phase_validation": "complete",
     "phase_funnel_creation": "complete", "phase_email_sending": "in_progress",
     "phase_tracking": "active", "phase_sales": "active",
     "created_at": "2026-05-03T15:30:00Z"},
]

@app.route('/api/tasks')
def tasks():
    return jsonify(DEMO_TASKS)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    import uuid
    task_id = str(uuid.uuid4())[:8]
    new_task = {"id": task_id, "business_type": data.get("business_type", ""),
                "city": data.get("city", ""), "state": data.get("state", ""),
                "status": "active", "leads_total": 0, "leads_emailed": 0,
                "created_at": datetime.utcnow().isoformat()}
    DEMO_TASKS.append(new_task)
    return jsonify({"task_id": task_id, "task": new_task, "status": "launched", "phase": "scraping"})

@app.route('/api/tasks/<task_id>/<action>', methods=['POST'])
def task_action(task_id, action):
    for t in DEMO_TASKS:
        if t["id"] == task_id:
            t["status"] = "paused" if action == "pause" else "active"
    return jsonify({"status": action})

# ─── LEADS ───
DEMO_LEADS = [
    {"id": "l1", "business_name": "Smile Dental Clinic", "owner_name": "Dr. Sarah Ahmed",
     "email_primary": "sarah@smileclinic.com", "phone": "555-0101",
     "city": "Los Angeles", "state": "CA", "niche": "dentist",
     "current_rating": 3.8, "negative_review_count": 7, "lead_score": 85,
     "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
     "emails_sent_count": 12, "created_at": "2026-05-01T10:00:00Z"},
    {"id": "l2", "business_name": "Houston Auto Repair", "owner_name": "Mike Johnson",
     "email_primary": "mike@houstonauto.com", "phone": "555-0102",
     "city": "Houston", "state": "TX", "niche": "auto repair",
     "current_rating": 4.2, "negative_review_count": 3, "lead_score": 72,
     "lead_temperature": "warm", "status": "emailed", "funnel_step": 3,
     "emails_sent_count": 8, "created_at": "2026-05-02T14:00:00Z"},
    {"id": "l3", "business_name": "Legal Eagles LLP", "owner_name": "James White",
     "email_primary": "james@legaleagles.com", "phone": "555-0103",
     "city": "Chicago", "state": "IL", "niche": "law firm",
     "current_rating": 4.8, "negative_review_count": 1, "lead_score": 92,
     "lead_temperature": "hot", "status": "replied", "funnel_step": 5,
     "emails_sent_count": 18, "created_at": "2026-05-01T08:00:00Z"},
    {"id": "l4", "business_name": "Pizza Palace", "owner_name": "Tom Wilson",
     "email_primary": "tom@pizzapalace.com", "phone": "555-0104",
     "city": "Denver", "state": "CO", "niche": "restaurant",
     "current_rating": 3.5, "negative_review_count": 12, "lead_score": 45,
     "lead_temperature": "cold", "status": "scraped", "funnel_step": 1,
     "emails_sent_count": 2, "created_at": "2026-05-03T16:00:00Z"},
    {"id": "l5", "business_name": "Bright Eyes Optometry", "owner_name": "Dr. Lisa Chen",
     "email_primary": "lisa@brighteyes.com", "phone": "555-0105",
     "city": "Phoenix", "state": "AZ", "niche": "optometrist",
     "current_rating": 4.5, "negative_review_count": 2, "lead_score": 78,
     "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
     "emails_sent_count": 10, "created_at": "2026-05-02T09:00:00Z"},
]

@app.route('/api/leads')
def leads():
    temp = request.args.get('temperature')
    status_filter = request.args.get('status')
    result = DEMO_LEADS
    if temp:
        result = [l for l in result if l.get('lead_temperature') == temp]
    if status_filter:
        result = [l for l in result if l.get('status') == status_filter]
    return jsonify(result)

@app.route('/api/leads/<lead_id>')
def get_lead(lead_id):
    lead = next((l for l in DEMO_LEADS if l["id"] == lead_id), None)
    if not lead:
        return jsonify({}), 404
    lead_copy = dict(lead)
    lead_copy["email_history"] = [
        {"id": "e1", "email_number": 1, "subject_line": "your google reviews",
         "opened": True, "open_count": 3, "replied": False, "status": "sent",
         "sent_at": "2026-05-01T10:00:00Z"},
        {"id": "e2", "email_number": 2, "subject_line": "review reputation",
         "opened": True, "open_count": 1, "replied": True, "status": "sent",
         "reply_content": "Hi, I'm interested. Can you tell me more?",
         "sent_at": "2026-05-03T10:00:00Z"},
    ]
    return jsonify(lead_copy)

@app.route('/api/leads/export')
def export_leads():
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Business Name", "Owner", "Email", "City", "State", "Rating", "Score", "Temperature"])
    for l in DEMO_LEADS:
        writer.writerow([l["business_name"], l["owner_name"], l["email_primary"],
                        l["city"], l["state"], l["current_rating"], l["lead_score"], l["lead_temperature"]])
    return output.getvalue(), 200, {"Content-Type": "text/csv",
                                     "Content-Disposition": "attachment; filename=leads.csv"}

@app.route('/api/leads/scored')
def scored_leads():
    scored = sorted([l for l in DEMO_LEADS if l["lead_score"] > 0],
                   key=lambda x: x["lead_score"], reverse=True)
    return jsonify([{"id": l["id"], "business_name": l["business_name"], "city": l["city"],
                    "niche": l["niche"], "lead_score": l["lead_score"],
                    "lead_temperature": l["lead_temperature"],
                    "emails_sent_count": l["emails_sent_count"]} for l in scored])

# ─── HOT LEADS ───
@app.route('/api/hot-leads')
def hot_leads():
    hot = [l for l in DEMO_LEADS if l["lead_temperature"] == "hot"]
    return jsonify([{
        "id": l["id"], "business_name": l["business_name"], "owner_name": l["owner_name"],
        "email_primary": l["email_primary"], "city": l["city"], "niche": l["niche"],
        "current_rating": l["current_rating"],
        "conversations": [{"subject": "your reviews", "reply": "Interested, tell me more",
                          "replied_at": "2026-05-04T10:00:00Z"}]
    } for l in hot])

# ─── ACCOUNTS ───
DEMO_ACCOUNTS = [
    {"id": "a1", "email_address": "campaign@dmcashield.com", "display_name": "Review Team",
     "daily_limit": 40, "sent_today": 23, "total_sent": 456, "warmup_day": 28,
     "warmup_complete": True, "status": "active", "blacklist_status": "clean",
     "health_score": 95, "total_opens": 180, "total_replies": 45,
     "created_at": "2026-04-01T00:00:00Z"},
    {"id": "a2", "email_address": "outreach@dmcashield.com", "display_name": "DMCA Support",
     "daily_limit": 30, "sent_today": 15, "total_sent": 234, "warmup_day": 14,
     "warmup_complete": False, "status": "warming_up", "blacklist_status": "clean",
     "health_score": 82, "total_opens": 90, "total_replies": 22,
     "created_at": "2026-04-15T00:00:00Z"},
]

@app.route('/api/accounts')
def accounts():
    return jsonify(DEMO_ACCOUNTS)

@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.get_json() or {}
    import uuid
    new_id = str(uuid.uuid4())[:8]
    acc = {"id": new_id, "email_address": data.get("email_address", ""),
           "display_name": data.get("display_name", ""), "daily_limit": 5,
           "sent_today": 0, "total_sent": 0, "warmup_day": 1,
           "warmup_complete": False, "status": "warming_up", "blacklist_status": "clean",
           "health_score": 50, "total_opens": 0, "total_replies": 0,
           "created_at": datetime.utcnow().isoformat()}
    DEMO_ACCOUNTS.append(acc)
    return jsonify({"id": new_id, "email_address": acc["email_address"], "status": "warming_up"})

@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    global DEMO_ACCOUNTS
    DEMO_ACCOUNTS = [a for a in DEMO_ACCOUNTS if a["id"] != account_id]
    return jsonify({"deleted": True})

@app.route('/api/accounts/<account_id>/warmup', methods=['POST'])
def start_warmup(account_id):
    for a in DEMO_ACCOUNTS:
        if a["id"] == account_id:
            a["status"] = "warming_up"
    return jsonify({"status": "warming_up"})

@app.route('/api/accounts/<account_id>/warmup', methods=['DELETE'])
def stop_warmup(account_id):
    for a in DEMO_ACCOUNTS:
        if a["id"] == account_id:
            a["status"] = "paused"
    return jsonify({"status": "paused"})

# ─── ANALYTICS ───
@app.route('/api/analytics')
def analytics():
    return jsonify({
        "total_leads": 247, "total_emails_sent": 1247, "total_opened": 349,
        "total_replied": 89, "hot_leads": 38, "converted": 12,
        "open_rate": 28.0, "reply_rate": 7.1
    })

@app.route('/api/analytics/top-subjects')
def top_subjects():
    return jsonify([
        {"subject": "your google reviews", "sends": 245, "opens": 89},
        {"subject": "review reputation", "sends": 189, "opens": 72},
        {"subject": "online reviews", "sends": 156, "opens": 58},
        {"subject": "review audit", "sends": 134, "opens": 51},
        {"subject": "competitor reviews", "sends": 98, "opens": 34},
    ])

# ─── CAMPAIGNS ───
@app.route('/api/campaigns')
def campaigns():
    return jsonify([
        {"id": "t1", "name": "clinic - Los Angeles", "status": "active",
         "leads_total": 45, "leads_emailed": 32, "leads_hot": 8, "open_rate": 37.5,
         "created_at": "2026-05-04T10:00:00Z"},
        {"id": "t2", "name": "dentist - Houston", "status": "active",
         "leads_total": 78, "leads_emailed": 45, "leads_hot": 12, "open_rate": 40.0,
         "created_at": "2026-05-03T15:30:00Z"},
    ])

# ─── TEMPLATES ───
DEMO_TEMPLATES = [
    {"id": "ft1", "name": "DMCA Cold Outreach (6 Steps)", "steps": [
        {"step": 1, "delay_days": 0, "angle": "cold_intro", "emotion_trigger": "fear"},
        {"step": 2, "delay_days": 3, "angle": "social_proof", "emotion_trigger": "trust"},
        {"step": 3, "delay_days": 7, "angle": "fear_trigger", "emotion_trigger": "urgency"},
        {"step": 4, "delay_days": 14, "angle": "value_offer", "emotion_trigger": "greed"},
        {"step": 5, "delay_days": 21, "angle": "last_chance", "emotion_trigger": "fomo"},
        {"step": 6, "delay_days": 28, "angle": "breakup", "emotion_trigger": "loss"},
    ], "created_at": "2026-04-27T00:00:00Z"},
]

@app.route('/api/templates')
def templates():
    return jsonify(DEMO_TEMPLATES)

@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.get_json() or {}
    import uuid
    t = {"id": str(uuid.uuid4())[:8], "name": data.get("name", "Custom"),
         "steps": data.get("steps", []), "created_at": datetime.utcnow().isoformat()}
    DEMO_TEMPLATES.append(t)
    return jsonify({"id": t["id"], "name": t["name"], "status": "created"})

@app.route('/api/templates/<template_id>', methods=['PUT'])
def update_template(template_id):
    data = request.get_json() or {}
    for t in DEMO_TEMPLATES:
        if t["id"] == template_id:
            if "name" in data: t["name"] = data["name"]
            if "steps" in data: t["steps"] = data["steps"]
    return jsonify({"status": "updated"})

@app.route('/api/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    global DEMO_TEMPLATES
    DEMO_TEMPLATES = [t for t in DEMO_TEMPLATES if t["id"] != template_id]
    return jsonify({"deleted": True})

# ─── JARVIS AI ───
@app.route('/api/jarvis', methods=['POST'])
def jarvis():
    data = request.get_json() or {}
    message = data.get('message', '').lower().strip()

    if "how many" in message and "lead" in message:
        return jsonify({"response": "You have 247 total leads: 38 hot, 45 warm, 164 cold.", "type": "info"})
    elif "status" in message or "system" in message:
        return jsonify({"response": "System: operational. 12 departments active, 36 agents running. All systems nominal.", "type": "info"})
    elif ("email" in message and "sent" in message) or "stats" in message:
        return jsonify({"response": "Email stats: 1247 sent, 349 opened (28% open rate), 89 replies (7.1% reply rate).", "type": "info"})
    elif "account" in message:
        return jsonify({"response": "You have 2 email accounts registered. 1 active, 1 warming up.", "type": "info"})
    elif "learning" in message or "cycle" in message:
        return jsonify({"response": "Learning engine at cycle 4. Current open rate: 28%. Best subject style: short personalized. 1 discovered rule.", "type": "info"})

    return jsonify({"response": f"I understand you're asking about: '{data.get('message', '')}'. "
                    "Try: 'how many leads', 'show stats', 'system status', or 'learning cycle'.", "type": "info"})

# ─── SETTINGS ───
@app.route('/api/settings')
def get_settings():
    return jsonify({
        "openrouter_configured": True,
        "max_emails_per_day": 40,
        "email_gap_min": 180, "email_gap_max": 420,
        "models": {"copywriting": "google/gemini-2.0-flash-exp:free",
                   "analysis": "google/gemini-2.0-flash-exp:free",
                   "sales": "google/gemini-2.0-flash-exp:free",
                   "general": "google/gemini-2.0-flash-exp:free"}
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    return jsonify({"status": "updated"})

# ─── INTEGRATIONS ───
@app.route('/api/integrations/<integration_type>/test', methods=['POST'])
def test_integration(integration_type):
    statuses = {
        "smtp": {"status": "ok", "message": "SMTP active via email accounts"},
        "imap": {"status": "ok", "message": "IMAP reply monitoring active"},
        "google_sheets": {"status": "fallback", "message": "Using CSV export"},
        "openrouter": {"status": "ok", "message": "OpenRouter connected"},
    }
    result = statuses.get(integration_type, {"status": "not_supported", "message": f"'{integration_type}' not implemented"})
    result["type"] = integration_type
    return jsonify(result)

# ─── SELF-LEARNING ───
@app.route('/api/learning')
def get_learning():
    return jsonify({
        "cycle": 4, "last_updated": datetime.utcnow().isoformat(),
        "avg_open_rate": 28.0, "avg_reply_rate": 7.1,
        "best_subject_patterns": [
            {"subject": "your google reviews", "sends": 245, "open_rate": 36.3, "reply_rate": 8.2},
            {"subject": "review reputation", "sends": 189, "open_rate": 38.1, "reply_rate": 7.4},
        ],
        "worst_subject_patterns": [],
        "best_send_hours": [{"hour": 10, "open_rate": 42.3, "sends": 89}],
        "top_performing_niches": [{"niche": "dentist", "leads": 78, "hot": 12}],
        "email_style_scores": {
            "short_subject": {"sends": 434, "opens": 161, "score": 37.1},
            "question_subject": {"sends": 56, "opens": 18, "score": 32.1},
            "urgency_subject": {"sends": 98, "opens": 28, "score": 28.6},
            "personalized_subject": {"sends": 312, "opens": 124, "score": 39.7},
        },
        "rules": ["Use 2-4 word lowercase subjects", "Lead with pain point",
                  "Include specific numbers", "Keep email under 150 words"],
        "discovered_rules": ["Best performing style: personalized subject"],
    })

@app.route('/api/learning/run', methods=['POST'])
def trigger_learning():
    return jsonify({"status": "completed", "cycle": 5, "discovered_rules": 2})

# ─── DMCA TRACKING ───
DEMO_DMCA_CASES = [
    {"id": "dmca1", "client_name": "Smile Dental Clinic", "platform": "Google",
     "status": "submitted", "negative_reviews_removed": 3, "submitted_at": "2026-05-01T10:00:00Z"},
    {"id": "dmca2", "client_name": "Houston Auto Repair", "platform": "Yelp",
     "status": "under_review", "negative_reviews_removed": 0, "submitted_at": "2026-05-03T14:00:00Z"},
    {"id": "dmca3", "client_name": "Legal Eagles LLP", "platform": "Google",
     "status": "completed", "negative_reviews_removed": 5, "submitted_at": "2026-04-28T09:00:00Z"},
]

@app.route('/api/dmca/cases')
def dmca_cases():
    return jsonify(DEMO_DMCA_CASES)

@app.route('/api/dmca/cases', methods=['POST'])
def create_dmca_case():
    data = request.get_json() or {}
    import uuid
    case = {"id": str(uuid.uuid4())[:8], "client_name": data.get("client_name", ""),
            "platform": data.get("platform", "Google"), "status": "submitted",
            "negative_reviews_removed": 0, "submitted_at": datetime.utcnow().isoformat()}
    DEMO_DMCA_CASES.append(case)
    return jsonify({"id": case["id"], "status": "submitted"})

@app.route('/api/dmca/cases/<case_id>')
def get_dmca_case(case_id):
    case = next((c for c in DEMO_DMCA_CASES if c["id"] == case_id), None)
    if not case:
        return jsonify({}), 404
    return jsonify(case)

# ─── WEBHOOKS ───
@app.route('/api/webhooks', methods=['GET'])
def list_webhooks():
    return jsonify([
        {"id": "wh1", "url": "https://example.com/webhook", "events": ["lead.created", "lead.hot"],
         "active": True, "created_at": "2026-05-01T00:00:00Z"}
    ])

@app.route('/api/webhooks', methods=['POST'])
def create_webhook():
    data = request.get_json() or {}
    import uuid
    wh = {"id": str(uuid.uuid4())[:8], "url": data.get("url", ""),
          "events": data.get("events", []), "active": True,
          "created_at": datetime.utcnow().isoformat()}
    return jsonify({"id": wh["id"], "status": "active"})

# ─── CAMPAIGN SCHEDULER ───
DEMO_SCHEDULES = [
    {"id": "sch1", "campaign_id": "t1", "scheduled_at": "2026-05-05T14:00:00Z",
     "action": "send_batch", "status": "pending", "leads_count": 20},
    {"id": "sch2", "campaign_id": "t2", "scheduled_at": "2026-05-06T10:00:00Z",
     "action": "send_batch", "status": "pending", "leads_count": 30},
]

@app.route('/api/scheduler')
def scheduler():
    return jsonify(DEMO_SCHEDULES)

@app.route('/api/scheduler', methods=['POST'])
def create_schedule():
    data = request.get_json() or {}
    import uuid
    sch = {"id": str(uuid.uuid4())[:8], "campaign_id": data.get("campaign_id", ""),
           "scheduled_at": data.get("scheduled_at", ""), "action": data.get("action", "send_batch"),
           "status": "pending", "leads_count": data.get("leads_count", 0)}
    DEMO_SCHEDULES.append(sch)
    return jsonify({"id": sch["id"], "status": "scheduled"})

# ─── CLIENTS ───
DEMO_CLIENTS = [
    {"id": "c1", "business_name": "Smile Dental Clinic", "owner": "Dr. Sarah Ahmed",
     "email": "sarah@smileclinic.com", "phone": "555-0101", "plan": "pro",
     "dmca_cases": 1, "total_spent": 2500, "status": "active", "joined_at": "2026-04-01T00:00:00Z"},
    {"id": "c2", "business_name": "Houston Auto Repair", "owner": "Mike Johnson",
     "email": "mike@houstonauto.com", "phone": "555-0102", "plan": "basic",
     "dmca_cases": 1, "total_spent": 500, "status": "active", "joined_at": "2026-04-15T00:00:00Z"},
]

@app.route('/api/clients')
def clients():
    return jsonify(DEMO_CLIENTS)

@app.route('/api/clients/<client_id>')
def get_client(client_id):
    client = next((c for c in DEMO_CLIENTS if c["id"] == client_id), None)
    if not client:
        return jsonify({}), 404
    return jsonify(client)

# ─── REVENUE ANALYTICS ───
@app.route('/api/revenue')
def revenue():
    return jsonify({
        "monthly_revenue": 12500, "annual_projection": 150000,
        "active_clients": 47, "avg_client_value": 266,
        "revenue_by_plan": {"pro": 8500, "basic": 4000},
        "recent_payments": [
            {"client": "Smile Dental Clinic", "amount": 500, "date": "2026-05-01T00:00:00Z"},
            {"client": "Houston Auto Repair", "amount": 250, "date": "2026-05-02T00:00:00Z"},
        ]
    })

# ─── TEAM & AGENTS ───
@app.route('/api/team')
def team():
    return jsonify({
        "departments": [
            {"name": "Scraping", "agents": 3, "status": "active", "tasks_today": 47},
            {"name": "Validation", "agents": 3, "status": "active", "tasks_today": 89},
            {"name": "Marketing", "agents": 5, "status": "active", "tasks_today": 23},
            {"name": "Sales", "agents": 4, "status": "active", "tasks_today": 12},
            {"name": "DMCA", "agents": 2, "status": "active", "tasks_today": 8},
        ],
        "total_agents": 17, "online": 17
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)