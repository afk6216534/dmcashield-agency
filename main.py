from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

api = FastAPI(title="DMCAShield API")
api.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@api.get("/")
async def root():
    return {"status": "ok", "service": "DMCAShield"}

@api.get("/health") 
async def health():
    return {"status": "healthy"}

@api.get("/api/status")
async def status():
    return {
        "system": {"status": "operational", "version": "3.0.0"},
        "departments": {"scraping": "online", "validation": "online", "marketing": "online", "email_sending": "online", "tracking": "online", "sales": "online"},
        "agents": {"jarvis": "active", "scraper": "running"},
        "stats": {"total_leads": 247, "hot_leads": 38}
    }

@api.get("/api/leads")
async def leads():
    return [{"id": "1", "business_name": "Test", "lead_score": 78}]

@api.get("/api/tasks")
async def tasks():
    return [{"id": "1", "title": "Test Task", "status": "active"}]

app = api

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)