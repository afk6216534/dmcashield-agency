import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

from agents.memory.message_bus import MessageBus, create_handoff_message, create_alert_message
from agents.memory.agent_brain import memory_system

class TaskHeadAgent:
    def __init__(self):
        self.name = "TaskHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["TaskTracker", "ProgressMonitor", "QueueManager", "LimitEnforcer"]

    def receive_message(self, message):
        if message.message_type == "instruction":
            action = message.payload.get("action")
            if action == "start_task":
                self.start_task(message.payload.get("task_id"))
            elif action == "resume_task":
                self.resume_task(message.payload.get("task_id"))
            elif action == "pause_task":
                self.pause_task(message.payload.get("task_id"))

    def create_task(self, business_type: str, city: str, state: str, country: str = "USA") -> str:
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        from database.models import Task, SessionLocal
        db = SessionLocal()
        try:
            task = Task(
                id=task_id,
                business_type=business_type,
                city=city,
                state=state,
                country=country,
                status="queued"
            )
            db.add(task)
            db.commit()
            
            self.brain.remember(
                f"Task created: {task_id} - {business_type} in {city}, {state}",
                "task_created"
            )
            
            return task_id
        finally:
            db.close()

    def start_task(self, task_id: str):
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "active"
                task.phase_scraping = "in_progress"
                db.commit()
                
                self.message_bus.send_message(
                    from_agent=self.name,
                    to_agent="ScrapeHead",
                    message_type="instruction",
                    payload={"action": "start_task", "task_id": task_id}
                )
                
                self.brain.remember(f"Task started: {task_id}", "task_started")
        finally:
            db.close()

    def pause_task(self, task_id: str):
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "paused"
                db.commit()
                self.brain.remember(f"Task paused: {task_id}", "task_paused")
        finally:
            db.close()

    def resume_task(self, task_id: str):
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "active"
                db.commit()
                self.brain.remember(f"Task resumed: {task_id}", "task_resumed")
        finally:
            db.close()

    def update_task_progress(self, task_id: str, phase: str, value: Any):
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                if phase == "leads_scraped":
                    task.leads_scraped = value
                elif phase == "leads_emailed":
                    task.leads_emailed = value
                elif phase == "leads_opened":
                    task.leads_opened = value
                elif phase == "leads_replied":
                    task.leads_replied = value
                elif phase == "leads_hot":
                    task.leads_hot = value
                elif phase == "leads_converted":
                    task.leads_converted = value
                elif phase.startswith("phase_"):
                    setattr(task, phase, value)
                
                total = task.leads_total if task.leads_total > 0 else 1
                completed = task.leads_scraped + task.leads_emailed + task.leads_opened
                task.funnel_completion_rate = min((completed / (total * 3)) * 100, 100)
                
                task.updated_at = datetime.utcnow()
                db.commit()
        finally:
            db.close()

    def get_all_tasks(self) -> List[Dict]:
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            tasks = db.query(Task).order_by(Task.created_at.desc()).all()
            return [
                {
                    "id": t.id,
                    "business_type": t.business_type,
                    "city": t.city,
                    "state": t.state,
                    "country": t.country,
                    "status": t.status,
                    "leads_total": t.leads_total,
                    "leads_scraped": t.leads_scraped,
                    "leads_emailed": t.leads_emailed,
                    "leads_opened": t.leads_opened,
                    "leads_replied": t.leads_replied,
                    "leads_hot": t.leads_hot,
                    "funnel_completion_rate": t.funnel_completion_rate,
                    "phases": {
                        "scraping": t.phase_scraping,
                        "validation": t.phase_validation,
                        "funnel": t.phase_funnel,
                        "sending": t.phase_sending,
                        "tracking": t.phase_tracking,
                        "sales": t.phase_sales
                    }
                }
                for t in tasks
            ]
        finally:
            db.close()

    def start(self):
        return {"status": "online", "team": self.team}

task_head = TaskHeadAgent()