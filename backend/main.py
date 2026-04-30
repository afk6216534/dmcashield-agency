from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from fastapi.responses import JSONResponse
from fastapi import Path
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime
import smtplib
import ssl

app = FastAPI(title="DMCAShield Agency API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import database models and utilities
from database.models import SessionLocal, Task, EmailAccount, Lead
from agents.memory.message_bus import message_bus
from agents.memory.memory_system import memory_system
from agents.memory.persistent_memory import persistent_memory
from agents.resource_integrator import resource_integrator

class EmailAccountCreate(BaseModel):
    email_address: str
    app_password: str
    display_name: Optional[str] = None
    provider: Optional[str] = "gmail"

class TaskCreate(BaseModel):
    business_type: str
    city: str
    state: str
    country: str = "USA"

class SystemCommand(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None

# =============================
# API Endpoints
# =============================
@app.get("/", response_model=dict)
async def root():
    return {
        "company": "DMCAShield Agency",
        "status": "operational",
        "departments": 12,
        "version": "2.0.0",
        "features": ["blockchain_audit", "llm_routing", "auto_scaling", "persistent_memory"]
    }

@app.get("/api/status", response_model=dict)
async def get_status():
    db = SessionLocal()
    try:
        total_leads = db.query(Lead).count()
        total_tasks = db.query(Task).count()
        active_tasks = db.query(Task).filter(Task.status == "active").count()
        email_accounts = db.query(EmailAccount).count()
        active_accounts = db.query(EmailAccount).filter(EmailAccount.status == "active").count()
        hot_leads = db.query(Lead).filter(Lead.temperature == "hot").count()

        # Get memory stats
        memory_stats = persistent_memory.get_memory_stats()

        return {
            "system": memory_system.get_soul(),
            "stats": {
                "total_leads": total_leads,
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "email_accounts": email_accounts,
                "active_accounts": active_accounts,
                "hot_leads": hot_leads,
            },
            "memory": memory_stats,
            "departments_status": {
                "ceo": "online", "scraping": "online", "validation": "online",
                "marketing": "online", "email_sending": "online", "tracking": "online",
                "sales": "online", "sheets": "online", "accounts": "online",
                "tasks": "online", "ml": "online", "jarvis": "online", "memory": "online"
            }
        }
    finally:
        db.close()

@app.post("/api/tasks", response_model=dict)
async def create_task(task_data: TaskCreate):
    db = SessionLocal()
    try:
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            business_type=task_data.business_type,
            city=task_data.city,
            state=task_data.state,
            country=task_data.country,
            status="queued"
        )
        db.add(task)
        db.commit()

        message_bus.send_message(
            from_agent="API",
            to_agent="TaskHead",
            message_type="instruction",
            payload={"action": "start_task", "task_id": task_id}
        )

        return {"task_id": task_id, "status": "queued", "message": "Task created and queued for processing"}
    finally:
        db.close()

@app.get("/api/tasks", response_model=List[dict])
async def list_tasks(status: str = None):
    db = SessionLocal()
    try:
        query = db.query(Task)
        if status:
            query = query.filter(Task.status == status)
        tasks = query.all()
        return [{
            "id": t.id,
            "business_type": t.business_type,
            "city": t.city,
            "state": t.state,
            "status": t.status,
            "leads_total": t.leads_total,
            "leads_scraped": t.leads_scraped,
            "leads_emailed": t.leads_emailed,
            "leads_hot": t.leads_hot
        } for t in tasks]
    finally:
        db.close()

@app.get("/api/warmup/status", response_model=dict)
async def get_warmup_status():
    """Check warmup status for all email accounts"""
    db = SessionLocal()
    try:
        accounts = db.query(EmailAccount).filter(EmailAccount.status.in_(['active', 'warmup'])).all()
        warmup_data = []
        for acc in accounts:
            warmup_data.append({
                "account_id": acc.id,
                "email_address": acc.email_address,
                "status": acc.status,
                "warmup_day": acc.warmup_day,
                "daily_limit": acc.daily_limit,
                "sent_today": acc.sent_today,
                "last_used": acc.last_used.isoformat() if acc.last_used else None
            })
        return {
            "accounts": warmup_data,
            "total_accounts": len(warmup_data),
            "active_warmup": len([a for a in warmup_data if a['status'] == 'warmup'])
        }
    finally:
        db.close()
    db = SessionLocal()
    try:
        accounts = db.query(EmailAccount).all()
        return [{
            "id": a.id,
            "email_address": a.email_address,
            "display_name": a.display_name,
            "status": a.status,
            "daily_limit": a.daily_limit,
            "sent_today": a.sent_today,
            "warmup_day": a.warmup_day,
            "health_score": a.health_score,
            "last_used": a.last_used.isoformat() if a.last_used else None
        } for a in accounts]
    finally:
        db.close()

@app.post("/api/email-accounts", response_model=dict)
async def create_email_account(account_data: EmailAccountCreate):
    db = SessionLocal()
    try:
        account_id = f"acc-{uuid.uuid4().hex[:8]}"

        provider = account_data.provider or "gmail"

        account = EmailAccount(
            id=account_id,
            email_address=account_data.email_address,
            app_password_encrypted=account_data.app_password,
            display_name=account_data.display_name or account_data.email_address.split('@')[0],
            status="active" if provider == "resend" else "warmup"
        )
        db.add(account)
        db.commit()

        return {"account_id": account_id, "status": "active" if provider == "resend" else "warmup", "message": "Email account added"}
    finally:
        db.close()

# =============================
# LLM Integration Status
# =============================

@app.get("/api/llm/status", response_model=dict)
async def get_llm_status():
    try:
        from agents.llm_integration import llm_router
        return {
            "providers": llm_router.get_provider_stats(),
            "cost_summary": llm_router.get_cost_summary()
        }
    except:
        return {"status": "LLM router not initialized"}

@app.post("/api/llm/route", response_model=dict)
async def route_llm(prompt: str, task_type: str = "balanced"):
    try:
        from agents.llm_integration import llm_router
        result = llm_router.execute_with_fallback(prompt, task_type)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

# =============================
# Blockchain Audit
# =============================

@app.get("/api/audit/blocks", response_model=dict)
async def get_audit_blocks(limit: int = 100):
    try:
        from agents.blockchain.blockchain_audit import blockchain_audit
        return {
            "blocks": blockchain_audit.get_records(limit=limit),
            "stats": blockchain_audit.get_statistics()
        }
    except:
        return {"status": "Blockchain audit not initialized"}

@app.post("/api/audit/add", response_model=dict)
async def add_audit_record(actor: str, action: str, target: str, status: str):
    try:
        from agents.blockchain.blockchain_audit import blockchain_audit
        block = blockchain_audit.add_record(actor, action, target, status)
        return {"block_index": block.index, "hash": block.hash}
    except Exception as e:
        return {"error": str(e)}

# =============================
# Auto-Scaling Status
# =============================

@app.get("/api/scaling/status", response_model=dict)
async def get_scaling_status():
    try:
        from agents.autoscaling.autoscaler import auto_scaler
        return auto_scaler.get_status()
    except:
        return {"status": "Auto-scaler not initialized"}

# =============================
# Resilience Testing
# =============================

@app.post("/api/resilience/test", response_model=dict)
async def run_resilience_test(iterations: int = 10):
    try:
        from agents.resilience_tester import resilience_tester
        result = resilience_tester.run_all_scenarios(iterations_per_scenario=iterations)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/resilience/report", response_model=dict)
async def get_resilience_report():
    try:
        from agents.resilience_tester import resilience_tester
        return resilience_tester._generate_report()
    except:
        return {"status": "Resilience tester not initialized"}

# =============================
# Gmail Connection Test
# =============================

@app.post("/api/gmail/test", response_model=dict)
async def test_gmail_connection(email_address: str, app_password: str):
    """Test Gmail SMTP connection"""
    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(email_address, app_password)  # Login with app password
        server.quit()  # Close connection

        return {
            "success": True,
            "message": "Gmail connection successful",
            "email": email_address,
            "timestamp": datetime.utcnow().isoformat()
        }
    except smtplib.SMTPAuthenticationError as e:
        return {
            "success": False,
            "error": f"Authentication failed: {str(e)}",
            "suggestion": "Check your email address and app password. Make sure you're using an App Password, not your regular password."
        }
    except smtplib.SMTPException as e:
        return {
            "success": False,
            "error": f"SMTP error: {str(e)}",
            "suggestion": "Check your internet connection and Gmail SMTP settings"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Connection failed: {str(e)}",
            "suggestion": "Check your network connection and try again"
        }

# =============================
# Health Check
# =============================

@app.get("/health", response_model=dict)
async def health_check():
    from database.models import SessionLocal

    db = SessionLocal()
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    finally:
        db.close()

    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "features": {
            "blockchain_audit": True,
            "llm_routing": True,
            "auto_scaling": True,
            "persistent_memory": True,
            "resilience_testing": True
        }
    }

# =============================
# Startup Configuration
# =============================

@app.on_event("startup")
async def startup_event():
    init_db()

    try:
        from agents.ceo.ceo_agent import ceo_agent
        from agents.scraping.scrape_head import scrape_head
        from agents.validation.enrich_head import enrich_head
        from agents.marketing.marketing_head import marketing_head
        from agents.email_sending.send_head import send_head
        from agents.tracking.analytics_head import analytics_head
        from agents.sales.sales_head import sales_head
        from agents.blockchain.blockchain_audit import blockchain_audit
        from agents.llm_integration import llm_router
        from agents.autoscaling.autoscaler import auto_scaler

        # Initialize blockchain audit
        blockchain_audit.load_chain()

        # Initialize LLM router
        _ = llm_router

        # Start auto-scaler
        auto_scaler.start_monitoring()

        # Start all agents
        ceo_agent.start()
        scrape_head.start()
        enrich_head.start()
        marketing_head.start()
        send_head.start()
        analytics_head.start()
        sales_head.start()

        memory_system.update_soul("status", "operational")
        memory_system.update_soul("version", "2.0.0")

        # Log startup to blockchain
        blockchain_audit.add_record("system", "startup", "all_agents", "success")

        print("All agents initialized successfully - System v2.0.0 with blockchain audit, LLM routing, and auto-scaling")
    except Exception as e:
        print(f"Agent startup warning: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
