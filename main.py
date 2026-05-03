from flask import Flask, jsonify
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
    return jsonify([
        {"id": "1", "business_name": "Joe's Diner", "lead_score": 78, "temperature": "hot"},
        {"id": "2", "business_name": "Smith Dental", "lead_score": 85, "temperature": "hot"},
    ])

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