from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({"status": "ok", "service": "DMCAShield", "version": "3.0.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "departments": 6})

@app.route('/api/status')
def status():
    return jsonify({
        "system": {"status": "operational", "version": "3.0.0"},
        "departments": {
            "scraping": "online", "validation": "online", "marketing": "online",
            "email_sending": "online", "tracking": "online", "sales": "online"
        },
        "agents": {
            "jarvis": "active", "scraper": "running", "validator": "online"
        },
        "stats": {"total_leads": 247, "hot_leads": 38, "open_rate": 28, "tasks_active": 7}
    })

@app.route('/api/leads')
def leads():
    temp = request.args.get('temperature')
    filtered = DEMO_LEADS if temp is None else [l for l in DEMO_LEADS if l.get('lead_temperature') == temp]
    return jsonify(filtered)

@app.route('/api/tasks')
def tasks():
    return jsonify([
        {"id": "1", "title": "DMCA Scraper", "status": "active", "progress": 73},
        {"id": "2", "title": "Email Outreach", "status": "active", "progress": 45},
    ])

@app.route('/api/campaigns')
def campaigns():
    return jsonify([
        {"id": "1", "name": "DMCA Removal", "status": "active", "sent": 1247},
    ])

@app.route('/api/jarvis', methods=['POST'])
def jarvis():
    from flask import request
    data = request.get_json()
    message = data.get('message', '').lower()
    
    responses = {
        'hot leads': f'🎯 Current hot leads: 38',
        'total leads': f'📊 Total leads: 247',
        'open rate': f'📈 Open rate: 28%',
        'tasks': f'✅ Active tasks: 7',
        'status': '🟢 All systems operational',
    }
    
    for key, value in responses.items():
        if key in message:
            return jsonify({"response": value})
    
    return jsonify({
        "response": f"📡 Received: '{message}'. JARVIS active and ready! System operational. Backend version 3.0.0"
    })

@app.route('/api/hot-leads')
def hot_leads():
    return jsonify([38])

@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "system_status": "operational",
        "version": "3.0.0",
        "stats": {
            "emails_sent_today": 142,
            "emails_opened_today": 38,
            "replies_today": 12,
            "hot_leads": 38,
            "total_leads": 247,
            "open_rate": 28,
            "reply_rate": 9
        },
        "departments": {
            "scraping": {"head": {"name": "ScraperBot", "status": "working", "tasks_completed": 47}},
            "validation": {"head": {"name": "ValidatorBot", "status": "idle", "tasks_completed": 89}},
            "marketing": {"head": {"name": "MarketBot", "status": "working", "tasks_completed": 23}},
            "email_sending": {"head": {"name": "SenderBot", "status": "working", "tasks_completed": 156}},
            "tracking": {"head": {"name": "TrackerBot", "status": "idle", "tasks_completed": 34}},
            "sales": {"head": {"name": "SalesBot", "status": "idle", "tasks_completed": 12}},
            "accounts": {"head": {"name": "AccountBot", "status": "idle", "tasks_completed": 8}},
            "tasks": {"head": {"name": "TaskBot", "status": "idle", "tasks_completed": 67}},
            "analytics": {"head": {"name": "AnalystBot", "status": "idle", "tasks_completed": 45}},
            "sheets": {"head": {"name": "SheetBot", "status": "idle", "tasks_completed": 23}}
        },
        "active_tasks": [
            {"id": 1, "business_type": "Dental Practice", "city": "Los Angeles", "state": "CA", "status": "active", "leads_total": 45, "leads_emailed": 32, "leads_hot": 8},
            {"id": 2, "business_type": "Restaurant", "city": "Phoenix", "state": "AZ", "status": "active", "leads_total": 78, "leads_emailed": 45, "leads_hot": 12},
            {"id": 3, "business_type": "Law Firm", "city": "Houston", "state": "TX", "status": "active", "leads_total": 23, "leads_emailed": 18, "leads_hot": 5}
        ],
        "recent_activity": [
            {"from": "ScraperBot", "to": "ValidatorBot", "notes": "25 new leads", "message_type": "handoff", "timestamp": "2026-05-04T10:30:00Z"},
            {"from": "EmailBot", "to": "TrackerBot", "notes": "38 opens", "message_type": "alert", "timestamp": "2026-05-04T10:15:00Z"},
            {"from": "TrackerBot", "to": "SalesBot", "notes": "5 hot leads", "message_type": "alert", "timestamp": "2026-05-04T10:00:00Z"}
        ],
        "soul": {
            "total_leads_processed": 1247,
            "total_emails_sent": 8934,
            "total_clients_acquired": 47,
            "learning_cycle": 3,
            "active_since": "April 2026"
        }
    })

DEMO_LEADS = [
    {"id": "1", "business_name": "Joe's Diner", "owner_name": "Joe Smith", "email_primary": "joe@joesdiner.com", "phone": "555-0101", "city": "Los Angeles", "state": "CA", "current_rating": 4.2, "negative_review_count": 3, "lead_score": 78, "lead_temperature": "hot", "funnel_step": 4, "emails_sent_count": 12},
    {"id": "2", "business_name": "Smith Dental", "owner_name": "Dr. Sarah Smith", "email_primary": "sarah@smithdental.com", "phone": "555-0102", "city": "Phoenix", "state": "AZ", "current_rating": 4.5, "negative_review_count": 1, "lead_score": 85, "lead_temperature": "hot", "funnel_step": 5, "emails_sent_count": 18},
    {"id": "3", "business_name": "Pizza Palace", "owner_name": "Mike Johnson", "email_primary": "mike@pizzapalace.com", "phone": "555-0103", "city": "Houston", "state": "TX", "current_rating": 3.8, "negative_review_count": 7, "lead_score": 52, "lead_temperature": "warm", "funnel_step": 3, "emails_sent_count": 8},
    {"id": "4", "business_name": "Legal Eagles LLP", "owner_name": "James White", "email_primary": "james@legaleagles.com", "phone": "555-0104", "city": "Chicago", "state": "IL", "current_rating": 4.8, "negative_review_count": 0, "lead_score": 92, "lead_temperature": "hot", "funnel_step": 6, "emails_sent_count": 24},
    {"id": "5", "business_name": "Auto Fix Shop", "owner_name": "Tom Wilson", "email_primary": "tom@autofix.com", "phone": "555-0105", "city": "Denver", "state": "CO", "current_rating": 3.5, "negative_review_count": 12, "lead_score": 35, "lead_temperature": "cold", "funnel_step": 1, "emails_sent_count": 2},
]

@app.route('/api/leads/<lead_id>')
def get_lead(lead_id):
    lead = next((l for l in DEMO_LEADS if l["id"] == lead_id), None)
    if lead:
        lead["email_history"] = [
            {"email_number": 1, "subject_line": "DMCA Notice - Action Required", "opened": True, "open_count": 3, "replied": False},
            {"email_number": 2, "subject_line": "Following Up on DMCA Removal", "opened": True, "open_count": 1, "replied": True},
        ]
    return jsonify(lead or {})

@app.route('/api/tasks/<task_id>/<action>', methods=['POST'])
def task_action(task_id, action):
    return jsonify({"status": "success", "task_id": task_id, "action": action})

@app.route('/api/settings')
def settings():
    return jsonify({
        "api_keys": {"google": "****", "openai": "****"},
        "email": {"smtp_host": "smtp.gmail.com", "port": 587},
        "warmup": {"enabled": True, "daily_limit": 50},
        "scraping": {"max_concurrent": 3, "timeout": 30}
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    return jsonify({"status": "saved"})

@app.route('/api/integrations/<integration_type>/test', methods=['POST'])
def test_integration(integration_type):
    return jsonify({"status": "connected", "type": integration_type})

DEMO_ACCOUNTS = [
    {"id": "1", "email": "campaign@dmcashield.com", "status": "active", "warmup_score": 85, "emails_sent_today": 23, "daily_limit": 100},
    {"id": "2", "email": "outreach@dmcashield.com", "status": "active", "warmup_score": 72, "emails_sent_today": 45, "daily_limit": 100},
]

@app.route('/api/accounts')
def accounts():
    return jsonify(DEMO_ACCOUNTS)

@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.get_json() or {}
    new_id = str(len(DEMO_ACCOUNTS) + 1)
    DEMO_ACCOUNTS.append({"id": new_id, "email": data.get("email", "new@email.com"), "status": "active", "warmup_score": 50, "emails_sent_today": 0, "daily_limit": 100})
    return jsonify({"id": new_id, "status": "created"})

@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    global DEMO_ACCOUNTS
    DEMO_ACCOUNTS = [a for a in DEMO_ACCOUNTS if a["id"] != account_id]
    return jsonify({"status": "deleted"})

@app.route('/api/accounts/<account_id>/warmup', methods=['POST'])
def start_warmup(account_id):
    return jsonify({"status": "started", "account_id": account_id})

@app.route('/api/accounts/<account_id>/warmup', methods=['DELETE'])
def stop_warmup(account_id):
    return jsonify({"status": "stopped", "account_id": account_id})

DEMO_TEMPLATES = [
    {"id": "1", "name": "DMCA Notice", "subject": "DMCA Notice - {{business_name}}", "body": "We found copyrighted content..."},
    {"id": "2", "name": "Follow Up", "subject": "Following Up", "body": "Just checking in..."},
]

@app.route('/api/templates')
def templates():
    return jsonify(DEMO_TEMPLATES)

@app.route('/api/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    global DEMO_TEMPLATES
    DEMO_TEMPLATES = [t for t in DEMO_TEMPLATES if t["id"] != template_id]
    return jsonify({"status": "deleted"})

@app.route('/api/analytics')
def analytics():
    return jsonify({
        "sent": 1247, "opened": 349, "replied": 89, "bounced": 23,
        "open_rate": 28, "reply_rate": 7, "click_rate": 12
    })

@app.route('/api/analytics/top-subjects')
def top_subjects():
    return jsonify([
        {"subject": "DMCA Notice", "opens": 145, "replies": 34},
        {"subject": "Following Up", "opens": 89, "replies": 21},
    ])

@app.route('/api/leads/scored')
def scored_leads():
    return jsonify([{"score": 85, "count": 12}, {"score": 72, "count": 28}, {"score": 55, "count": 45}])