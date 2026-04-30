import uuid
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from agents.memory.message_bus import MessageBus, create_handoff_message, create_alert_message
from agents.memory.agent_brain import memory_system

class CEOAgent:
    def __init__(self):
        self.name = "CEO"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.departments = {
            "scraping": "ScrapeHead",
            "validation": "EnrichHead",
            "marketing": "MarketingHead",
            "email_sending": "SendHead",
            "tracking": "AnalyticsHead",
            "sales": "SalesHead",
            "sheets": "SheetsHead",
            "accounts": "AccountHead",
            "tasks": "TaskHead",
            "ml": "MLHead",
            "jarvis": "JARVIS",
            "memory": "MemorySystem"
        }

    def receive_message(self, message):
        self.brain.remember(
            f"Received {message.message_type} from {message.from_agent}",
            context={"message": message.payload}
        )
        self.process_message(message)

    def process_message(self, message):
        if message.message_type == "alert":
            self.handle_alert(message.payload)
        elif message.message_type == "report":
            self.handle_report(message.payload, message.from_agent)
        elif message.message_type == "handoff":
            self.route_to_next_department(message)

    def handle_alert(self, payload: Dict):
        alert = payload.get("alert", "Unknown alert")
        details = payload.get("details", {})
        
        if "hot_lead" in alert.lower():
            memory_system.increment_soul("total_leads_processed")
            self.notify_department("sales", "escalate", {"priority": "critical", "alert": alert})
        elif "blacklist" in alert.lower():
            self.notify_department("accounts", "blacklist_recovery", details)
        elif "email_failed" in alert.lower():
            self.notify_department("email_sending", "retry", details)

    def handle_report(self, payload: Dict, from_agent: str):
        report_type = payload.get("type", "unknown")
        
        if report_type == "weekly_performance":
            insights = payload.get("insights", {})
            self.brain.learn(
                f"Weekly report from {from_agent}: {insights.get('summary', 'No summary')}",
                category="performance"
            )
            
            for dept, status in payload.get("departments", {}).items():
                self.brain.set_preference(f"dept_{dept}_health", status)
        
        elif report_type == "lead_conversion":
            conversion_data = payload.get("data", {})
            self.brain.learn(
                f"Lead conversion rate: {conversion_data.get('rate', 0)}%",
                category="conversion"
            )

    def route_to_next_department(self, message):
        current_dept = message.from_agent
        payload = message.payload
        task_id = payload.get("task_id")
        
        department_flow = [
            "ScrapeHead", "EnrichHead", "MarketingHead",
            "SendHead", "AnalyticsHead", "SalesHead"
        ]
        
        try:
            current_idx = department_flow.index(current_dept)
            next_dept = department_flow[current_idx + 1] if current_idx + 1 < len(department_flow) else "SheetsHead"
            
            self.message_bus.send_message(
                from_agent=self.name,
                to_agent=next_dept,
                message_type="handoff",
                priority="normal",
                payload=payload
            )
        except ValueError:
            pass

    def notify_department(self, dept_key: str, action: str, details: Dict):
        dept_name = self.departments.get(dept_key, dept_key)
        self.message_bus.send_message(
            from_agent=self.name,
            to_agent=dept_name,
            message_type="instruction",
            priority="high",
            payload={"action": action, "details": details}
        )

    def check_system_health(self) -> Dict:
        soul = memory_system.get_soul()
        return {
            "status": "operational",
            "soul": soul,
            "all_departments_online": True,
            "last_check": datetime.utcnow().isoformat()
        }

    def start(self):
        self.brain.remember("CEO Agent initialized", "System startup")
        return {"status": "online", "departments": len(self.departments)}

    def get_directives(self) -> List[Dict]:
        return [
            {
                "priority": "critical",
                "directive": "Monitor all hot leads and escalate immediately",
                "reason": "Revenue depends on converting hot leads"
            },
            {
                "priority": "high",
                "directive": "Ensure no email account gets blacklisted",
                "reason": "Email deliverability is the lifeblood of the system"
            },
            {
                "priority": "high",
                "directive": "Keep all departments communicating",
                "reason": "Pipeline must flow smoothly from scrape to conversion"
            },
            {
                "priority": "normal",
                "directive": "Learn from every campaign",
                "reason": "ML system must improve over time"
            }
        ]

ceo_agent = CEOAgent()