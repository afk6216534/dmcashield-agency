import uuid
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import croniter

class TriggerType(str, Enum):
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    EVENT = "event"
    CONDITION = "condition"
    MANUAL = "manual"

class ConditionOperator(str, Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"

@dataclass
class Condition:
    field: str
    operator: str
    value: Any

@dataclass
class AutomationTrigger:
    id: str
    trigger_type: TriggerType
    config: Dict[str, Any]
    conditions: List[Condition] = field(default_factory=list)
    enabled: bool = True
    last_triggered: Optional[str] = None

@dataclass
class AutomationAction:
    id: str
    name: str
    action_type: str
    config: Dict[str, Any]

@dataclass
class Automation:
    id: str
    name: str
    description: str
    trigger: AutomationTrigger
    actions: List[AutomationAction]
    enabled: bool = True
    run_count: int = 0
    last_run: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class AutomationEngine:
    def __init__(self, persist_file: str = "data/automations.json"):
        self.persist_file = persist_file
        self.automations: Dict[str, Automation] = {}
        self.scheduled_tasks: List[Dict] = []
        self.webhook_handlers: Dict[str, Callable] = {}
        self._load()
    
    def _load(self):
        import os
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    data = json.load(f)
                    for a in data.get("automations", []):
                        self.automations[a["id"]] = Automation(**a)
            except:
                pass
    
    def _save(self):
        import os
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump({
                "automations": [a.__dict__ for a in self.automations.values()]
            }, f, indent=2, default=str)
    
    def create_automation(self, name: str, description: str, trigger_type: str, 
                       trigger_config: Dict, action_configs: List[Dict]) -> Automation:
        automation_id = f"auto_{uuid.uuid4().hex[:8]}"
        
        trigger = AutomationTrigger(
            id=f"trigger_{automation_id}",
            trigger_type=TriggerType(trigger_type),
            config=trigger_config
        )
        
        actions = []
        for i, ac in enumerate(action_configs):
            action = AutomationAction(
                id=f"action_{automation_id}_{i}",
                name=ac.get("name", f"Action {i}"),
                action_type=ac.get("type", "api_call"),
                config=ac
            )
            actions.append(action)
        
        automation = Automation(
            id=automation_id,
            name=name,
            description=description,
            trigger=trigger,
            actions=actions
        )
        
        self.automations[automation_id] = automation
        self._save()
        
        return automation
    
    def create_schedule(self, name: str, cron_expr: str, action_type: str, action_config: Dict) -> str:
        schedule_id = f"sched_{uuid.uuid4().hex[:8]}"
        
        self.scheduled_tasks.append({
            "id": schedule_id,
            "name": name,
            "cron": cron_expr,
            "action_type": action_type,
            "action_config": action_config,
            "enabled": True,
            "next_run": None
        })
        
        self._save()
        return schedule_id
    
    def register_webhook(self, endpoint: str, handler: Callable):
        self.webhook_handlers[endpoint] = handler
    
    async def check_schedules(self):
        now = datetime.utcnow()
        
        for sched in self.scheduled_tasks:
            if not sched.get("enabled", True):
                continue
            
            cron_expr = sched.get("cron")
            if not cron_expr:
                continue
            
            try:
                cron = croniter.croniter(cron_expr, now)
                next_run = cron.get_next(datetime)
                
                if now >= next_run - timedelta(seconds=1):
                    await self._execute_action(sched)
                    sched["last_run"] = now.isoformat()
            except Exception as e:
                print(f"Schedule error: {e}")
    
    async def _execute_action(self, action_config: Dict):
        action_type = action_config.get("action_type")
        
        if action_type == "scrape_task":
            from agents.scraping.scrape_head import scrape_head
            config = action_config.get("config", {})
            
            msg = type('Message', (), {
                'message_type': 'instruction',
                'payload': {'action': 'start_task', 'task_id': config.get("task_id")}
            })()
            scrape_head.receive_message(msg)
        
        elif action_type == "process_queue":
            from agents.email_sending.send_head import send_head
            send_head.process_queue()
        
        elif action_type == "check_hot_leads":
            from database.models import SessionLocal, Lead
            db = SessionLocal()
            try:
                hot = db.query(Lead).filter(Lead.temperature == "hot").count()
                if hot > 0:
                    memory_system.increment_soul("total_leads_processed", hot)
            finally:
                db.close()
        
        elif action_type == "api_call":
            import httpx
            config = action_config.get("config", {})
            url = config.get("url")
            method = config.get("method", "GET")
            
            if url:
                async with httpx.AsyncClient() as client:
                    if method == "POST":
                        await client.post(url, json=config.get("body", {}))
                    else:
                        await client.get(url)
    
    def should_trigger(self, automation: Automation, context: Dict) -> bool:
        if not automation.enabled:
            return False
        
        trigger = automation.trigger
        
        if trigger.trigger_type == TriggerType.MANUAL:
            return True
        
        if trigger.trigger_type == TriggerType.CONDITION:
            for condition in trigger.conditions:
                field_value = context.get(condition.field)
                
                if condition.operator == ConditionOperator.EQUALS:
                    if field_value != condition.value:
                        return False
                elif condition.operator == ConditionOperator.NOT_EQUALS:
                    if field_value == condition.value:
                        return False
                elif condition.operator == ConditionOperator.GREATER_THAN:
                    if not (field_value and field_value > condition.value):
                        return False
                elif condition.operator == ConditionOperator.LESS_THAN:
                    if not (field_value and field_value < condition.value):
                        return False
                elif condition.operator == ConditionOperator.CONTAINS:
                    if condition.value not in str(field_value):
                        return False
            
            return True
        
        return False
    
    async def trigger_automation(self, automation_id: str, context: Dict = None):
        automation = self.automations.get(automation_id)
        if not automation or not self.should_trigger(automation, context or {}):
            return
        
        for action in automation.actions:
            await self._execute_action({
                "action_type": action.action_type,
                "config": action.config
            })
        
        automation.run_count += 1
        automation.last_run = datetime.utcnow().isoformat()
        self._save()
    
    def list_automations(self) -> List[Dict]:
        return [a.__dict__ for a in self.automations.values()]
    
    def get_automation(self, automation_id: str) -> Optional[Automation]:
        return self.automations.get(automation_id)
    
    def toggle_automation(self, automation_id: str, enabled: bool):
        if automation_id in self.automations:
            self.automations[automation_id].enabled = enabled
            self._save()
    
    def delete_automation(self, automation_id: str):
        if automation_id in self.automations:
            del self.automations[automation_id]
            self._save()

automation_engine = AutomationEngine()

DEFAULT_AUTOMATIONS = [
    {
        "name": "Morning Lead Check",
        "description": "Every morning at 8AM, check for new hot leads and send notifications",
        "trigger_type": "schedule",
        "trigger_config": {"cron": "0 8 * * *"},
        "action_configs": [
            {"name": "Check Hot Leads", "type": "check_hot_leads", "config": {}}
        ]
    },
    {
        "name": "Email Queue Processor",
        "description": "Every 15 minutes, process pending emails in queue",
        "trigger_type": "schedule", 
        "trigger_config": {"cron": "*/15 * * * *"},
        "action_configs": [
            {"name": "Process Queue", "type": "process_queue", "config": {}}
        ]
    },
    {
        "name": "Weekly Performance Report",
        "description": "Every Sunday at 6PM, generate weekly report",
        "trigger_type": "schedule",
        "trigger_config": {"cron": "0 18 * * 0"},
        "action_configs": [
            {"name": "Generate Report", "type": "api_call", "config": {"url": "/api/analytics/weekly"}}
        ]
    }
]

def init_default_automations():
    for auto in DEFAULT_AUTOMATIONS:
        automation_engine.create_automation(
            name=auto["name"],
            description=auto["description"],
            trigger_type=auto["trigger_type"],
            trigger_config=auto["trigger_config"],
            action_configs=auto["action_configs"]
        )