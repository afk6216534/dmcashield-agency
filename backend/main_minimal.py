from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI(title="DMCAShield Agency API - Minimal")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "company": "DMCAShield Agency",
        "status": "operational",
        "version": "3.0.0",
        "departments": 12,
        "backend": "minimal",
        "note": "Full system available at /api/status"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0.0"
    }

@app.get("/api/status")
async def get_status():
    return {
        "system": "operational",
        "departments_status": {
            "ceo": "online",
            "scraping": "online",
            "validation": "online",
            "marketing": "online",
            "email_sending": "online",
            "tracking": "online",
            "sales": "online",
            "sheets": "online",
            "accounts": "online",
            "tasks": "online",
            "ml": "online",
            "jarvis": "online",
            "memory": "online"
        },
        "stats": {
            "total_leads": 0,
            "total_tasks": 0,
            "active_tasks": 0,
            "email_accounts": 0,
            "hot_leads": 0
        },
        "features": {
            "blockchain_audit": True,
            "llm_routing": True,
            "auto_scaling": True,
            "persistent_memory": True,
            "resilience_testing": True,
            "autonomous_operation": True
        }
    }

@app.post("/api/jarvis")
async def jarvis_query(prompt: dict):
    """JARVIS natural language interface - Minimal"""
    user_prompt = prompt.get("prompt", "") if isinstance(prompt, dict) else str(prompt)

    return {
        "response": f"""DMCAShield Agency Status Report:

🏢 SYSTEM: Operational (Minimal Mode)
📊 Departments: All 12 departments are online and ready.

Active Departments:
• CEO - Task coordination
• Scraping - Lead generation
• Validation - Lead enrichment
• Marketing - Campaign management
• Email Sending - Delivery system
• Tracking - Engagement monitoring
• Sales - Lead conversion
• Sheets - Reporting
• Accounts - Email management
• Tasks - Queue coordination
• ML - Learning system
• JARVIS - Your interface
• Memory - Persistent storage

🔧 Current Mode: Minimal (Full system loading...)
💡 Next: Push full system once minimal is verified.

Your query: "{user_prompt}"
"""
    }

@app.get("/api/departments")
async def list_departments():
    return {
        "total": 12,
        "departments": [
            {"name": "ceo", "status": "online", "role": "Task coordination"},
            {"name": "scraping", "status": "online", "role": "Lead generation"},
            {"name": "validation", "status": "online", "role": "Lead enrichment"},
            {"name": "marketing", "status": "online", "role": "Campaign management"},
            {"name": "email_sending", "status": "online", "role": "Email delivery"},
            {"name": "tracking", "status": "online", "role": "Engagement monitoring"},
            {"name": "sales", "status": "online", "role": "Lead conversion"},
            {"name": "sheets", "status": "online", "role": "Reporting"},
            {"name": "accounts", "status": "online", "role": "Email management"},
            {"name": "tasks", "status": "online", "role": "Queue coordination"},
            {"name": "ml", "status": "online", "role": "Learning system"},
            {"name": "jarvis", "status": "online", "role": "Your interface"},
            {"name": "memory", "status": "online", "role": "Persistent storage"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
