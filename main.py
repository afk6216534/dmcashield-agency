from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DMCAShield Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "service": "DMCAShield Agency", "version": "3.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "departments": 6}

@app.get("/api/status")
def status():
    return {
        "system": {"status": "operational", "version": "3.0.0"},
        "departments": {
            "scraping": "online", "validation": "online", "marketing": "online",
            "email_sending": "online", "tracking": "online", "sales": "online"
        },
        "agents": {
            "jarvis": "active", "scraper": "running", "validator": "online",
            "email_agent": "active", "tracker": "online", "sales_agent": "ready"
        },
        "stats": {"total_leads": 247, "hot_leads": 38, "open_rate": 28, "reply_rate": 9, "tasks_active": 7, "campaigns": 4}
    }

@app.get("/api/leads")
def leads():
    return [
        {"id": "1", "business_name": "Joe's Diner", "lead_score": 78, "temperature": "hot"},
        {"id": "2", "business_name": "Smith Dental", "lead_score": 85, "temperature": "hot"},
    ]

@app.get("/api/tasks")
def tasks():
    return [
        {"id": "1", "title": "DMCA Scraper", "status": "active", "progress": 73},
        {"id": "2", "title": "Email Outreach", "status": "active", "progress": 45},
    ]

@app.get("/api/campaigns")
def campaigns():
    return [
        {"id": "1", "name": "DMCA Removal", "status": "active", "sent": 1247},
    ]