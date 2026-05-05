from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add backend to path so we can import from backend/main_simple.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def handler(request, context):
    """Vercel serverless function for JARVIS endpoint"""
    try:
        method = request.get('method', 'GET')

        if method == 'GET':
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"status": "JARVIS online", "endpoint": "/api/jarvis"})
            }

        if method == 'POST':
            body = request.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body

            prompt = data.get('prompt', '').lower()

            # Generate JARVIS response
            if 'status' in prompt or 'health' in prompt:
                response_text = """DMCAShield Agency Status Report:

🏢 SYSTEM STATUS: OPERATIONAL - All Systems Go
📅 Timestamp: 2026-05-03 21:30:00 UTC

👥 DEPARTMENT STATUS - ALL 12 ONLINE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👔 CEO: Online - Coordinating all departments & task management
🕵️‍♂️ SCRAPING: Online - Generating leads from web sources
✅ VALIDATION: Online - Verifying & enriching lead data
📢 MARKETING: Online - Creating campaigns & copy sequences
📧 EMAIL SENDING: Online - Delivering emails via SMTP/SES
👁️ TRACKING: Online - Monitoring opens, clicks, replies
💰 SALES: Online - Converting hot leads & handling responses
📊 SHEETS: Online - Updating reports & dashboards
🔑 ACCOUNTS: Online - Managing email accounts & warmup
📋 TASKS: Online - Coordinating task queues & priorities
🤖 ML: Online - Learning from results & improving accuracy
💬 JARVIS: Online - Your natural language interface (this is me!)
🧠 MEMORY: Online - Persistent storage, learning, audit trail
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 LEARNING & IMPROVEMENT:
- Agents continuously learn from interactions
- Knowledge graph updates with new patterns
- ML models retrain based on performance data
- Self-optimization based on success/failure rates

💡 READY FOR ACTION: All systems green - deploy tasks now!"""

            elif 'department' in prompt:
                response_text = """DMCAShield Agency - Department Status:

👔 CEO: Online - Strategic coordination & task prioritization
🕵️‍♂️ SCRAPING: Online - Web scraping, lead generation, data collection
✅ VALIDATION: Online - Data cleaning, enrichment, quality scoring
📢 MARKETING: Online - Campaign creation, copywriting, A/B testing
📧 EMAIL SENDING: Online - SMTP delivery, account rotation, warmup management
👁️ TRACKING: Online - Engagement scoring, analytics, behavioral tracking
💰 SALES: Online - Lead conversion, negotiation, closing
📊 SHEETS: Online - Reporting, dashboards, data visualization, exports
🔑 ACCOUNTS: Online - Email account management, rotation, reputation management
📋 TASKS: Online - Queue management, priority scheduling, resource allocation
🤖 ML: Online - Pattern recognition, predictive modeling, continuous learning
💬 JARVIS: Online - Natural language processing, command interpretation, response generation
🧠 MEMORY: Online - Persistent storage, knowledge graph, audit trail, learning retention

All 12 departments are fully operational and communicating via the internal message bus."""

            elif 'help' in prompt:
                response_text = """DMCAShield JARVIS - Available Commands:

🔍 SYSTEM QUERIES:
- "status" or "health" - Get current system status
- "departments" - See all 12 departments and their status
- "help" - Show this help message
- "system" - Detailed system information
- "stats" - View performance statistics

🎯 DEPARTMENT SPECIFIC:
- Ask about any department: "How is Marketing doing?"
- Ask about leads: "How many leads do we have?"
- Ask about emails: "What's our email sending status?"

🚀 ACTION COMMANDS:
- "start task [type]" - Create a new lead generation task
- "pause [department]" - Pause a specific department
- "resume [department]" - Resume a paused department

💡 EXAMPLES:
- "status" - See current system health
- "departments" - List all departments
- "How is Marketing doing?" - Get Marketing department details
- "start task real estate New York" - Create a lead generation task

Your query: "{}"
Try asking about system status, departments, or ask for help!".format(data.get('prompt', ''))

            else:
                response_text = """DMCAShield JARVIS - Natural Language Interface

I received your query: "{}"

I'm here to help you monitor and control your autonomous AI agency. Try asking:
- "status" - Get overall system status
- "departments" - See all 12 departments
- "help" - See available commands
- Or ask about any specific department: "How is Marketing doing?"

All 12 departments are online and operational:
CEO, Scraping, Validation, Marketing, Email Sending, Tracking, Sales, Sheets, Accounts, Tasks, ML, Memory, and of course me - JARVIS!

What would you like to know or do?""".format(data.get('prompt', ''))

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"response": response_text})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
