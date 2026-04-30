from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uuid
import os

app = FastAPI(title="DMCAShield Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.getenv("DB_PATH", "dmcashield.db")

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY, business_name TEXT, email_primary TEXT, phone TEXT,
            city TEXT, state TEXT, lead_score INTEGER DEFAULT 0,
            temperature TEXT DEFAULT 'cold', created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
    except:
        pass

init_db()

@app.get("/")
async def root():
    return {"company": "DMCAShield Agency", "status": "operational", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "departments": 6}

@app.get("/api/status")
async def get_status():
    return {
        "status": "operational",
        "leads": 0,
        "tasks": 0,
        "accounts": 0,
        "campaigns": 0
    }

@app.get("/api/leads")
async def get_leads():
    return {"leads": []}

@app.post("/api/leads")
async def create_lead(lead: dict):
    return {"id": str(uuid.uuid4()), "status": "created"}