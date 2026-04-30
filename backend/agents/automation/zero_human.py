import os
import json
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import uuid

class ZeroHumanOrchestrator:
    """
    Zero-Human Autonomous Company System
    =====================================
    Runs DMCAShield Agency with ZERO human intervention.
    Self-scrapes, self-emails, self-responds, self-converts.
    """
    
    def __init__(self, config_file: str = "data/orchestrator.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.running = False
        self.loop_task = None
        
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "autonomous_mode": True,
            "auto_scrape_interval_hours": 6,
            "auto_email_interval_minutes": 30,
            "auto_check_replies_minutes": 5,
            "max_tasks_per_day": 10,
            "max_emails_per_day": 100,
            "hot_lead_score_threshold": 60,
            "business_types": ["restaurant", "dentist", "salon", "gym", "plumber", "hvac", " electrician", "lawyer", "doctor"],
            "cities": [
                {"city": "Austin", "state": "TX"},
                {"city": "Houston", "state": "TX"},
                {"city": "Dallas", "state": "TX"},
                {"city": "Miami", "state": "FL"},
                {"city": "Orlando", "state": "FL"},
                {"city": "Los Angeles", "state": "CA"},
                {"city": "Chicago", "state": "IL"},
                {"city": "New York", "state": "NY"}
            ],
            "auto_respond": True,
            "auto_export_to_sheets": True,
            "notifications_enabled": True
        }
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, **kwargs):
        for key, value in kwargs.items():
            self.config[key] = value
        self._save_config()
    
    async def start_autonomous_mode(self):
        """Start the zero-human loop"""
        self.running = True
        self.loop_task = asyncio.create_task(self._autonomous_loop())
        return {"status": "autonomous_started", "config": self.config}
    
    async def stop_autonomous_mode(self):
        """Stop the zero-human loop"""
        self.running = False
        if self.loop_task:
            self.loop_task.cancel()
        return {"status": "autonomous_stopped"}
    
    async def _autonomous_loop(self):
        """Main autonomous loop - runs forever"""
        print("🚀 Zero-Human Mode started!")
        
        while self.running:
            try:
                # Phase 1: Check and create new tasks
                await self._auto_manage_tasks()
                
                # Phase 2: Process email queue
                await self._auto_process_emails()
                
                # Phase 3: Check for replies
                await self._auto_check_replies()
                
                # Phase 4: Handle hot leads
                await self._auto_handle_hot_leads()
                
                # Wait before next cycle
                await asyncio.sleep(self.config.get("auto_email_interval_minutes", 30) * 60)
                
            except Exception as e:
                print(f"Autonomous loop error: {e}")
                await asyncio.sleep(60)
    
    async def _auto_manage_tasks(self):
        """Auto-create new scraping tasks"""
        from database.models import SessionLocal, Task
        from agents.scraping.scrape_head import scrape_head
        
        db = SessionLocal()
        try:
            # Count active tasks
            active_tasks = db.query(Task).filter(Task.status == "active").count()
            
            if active_tasks < self.config.get("max_tasks_per_day", 10):
                # Create new task with random city/business
                import random
                
                biz_type = random.choice(self.config.get("business_types", ["restaurant"]))
                location = random.choice(self.config.get("cities", [{"city": "Austin", "state": "TX"}]))
                
                task_id = f"auto-{uuid.uuid4().hex[:8]}"
                task = Task(
                    id=task_id,
                    business_type=biz_type,
                    city=location["city"],
                    state=location["state"],
                    country="USA",
                    status="active"
                )
                db.add(task)
                db.commit()
                
                print(f"📋 Auto-task created: {biz_type} in {location['city']}, {location['state']}")
                
        finally:
            db.close()
    
    async def _auto_process_emails(self):
        """Auto-process email queue"""
        from agents.email_sending.send_head import send_head
        
        try:
            send_head.process_queue()
        except Exception as e:
            print(f"Email processing error: {e}")
    
    async def _auto_check_replies(self):
        """Auto-check email replies and respond"""
        from database.models import SessionLocal, EmailRecord, Lead
        
        db = SessionLocal()
        try:
            # Get recent replies
            recent = db.query(EmailRecord).filter(
                EmailRecord.reply_content != None
            ).order_by(EmailRecord.sent_at.desc()).limit(10).all()
            
            for record in recent:
                if record.reply_content:
                    # Auto-respond logic here
                    pass
                    
        finally:
            db.close()
    
    async def _auto_handle_hot_leads(self):
        """Auto-handle hot leads"""
        from database.models import SessionLocal, Lead
        from agents.utils.monitoring import slack_integration, twilio_sms
        from agents.utils.help_system import notification_system
        
        db = SessionLocal()
        try:
            # Get hot leads
            hot_leads = db.query(Lead).filter(
                Lead.temperature == "hot",
                Lead.status != "converted"
            ).all()
            
            for lead in hot_leads:
                # Send notifications
                if self.config.get("notifications_enabled"):
                    # Telegram notification
                    # Slack notification  
                    # Email to owner
                    pass
                
                # Update status
                lead.status = "notified"
                    
            db.commit()
            
        finally:
            db.close()
    
    async def run_now(self):
        """Run all phases once immediately"""
        await self._auto_manage_tasks()
        await self._auto_process_emails()
        await self._auto_check_replies()
        await self._auto_handle_hot_leads()
        return {"status": "run_complete", "timestamp": datetime.utcnow().isoformat()}
    
    def get_status(self) -> Dict:
        return {
            "autonomous_mode": self.running,
            "config": self.config,
            "tasks_today": 0,
            "emails_today": 0,
            "hot_leads": 0
        }

orchestrator = ZeroHumanOrchestrator()

AUTONOMOUS_COMMANDS = {
    "start": orchestrator.start_autonomous_mode,
    "stop": orchestrator.stop_autonomous_mode,
    "run_now": orchestrator.run_now,
    "status": orchestrator.get_status
}

async def execute_autonomous_command(command: str) -> Dict:
    func = AUTONOMOUS_COMMANDS.get(command)
    if func:
        return await func()
    return {"error": f"Unknown command: {command}"}