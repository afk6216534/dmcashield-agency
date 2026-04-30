import uuid
import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

class AgentState:
    """Base class for all agents - inspired by Devika's agent architecture"""
    def __init__(self, name: str, role: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.status = "idle"
        self.memory = []
        self.tools = []
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "memory": self.memory,
            "tools": self.tools,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }

@dataclass
class Department:
    id: str
    name: str
    head_agent: str
    sub_agents: List[str]
    status: str
    tasks_completed: int
    current_load: int
    
    def to_dict(self) -> dict:
        return asdict(self)

class DepartmentManager:
    """Manages all 12 departments - inspired by CrewAI crew management"""
    
    def __init__(self):
        self.departments: Dict[str, Department] = {}
        self.agents: Dict[str, AgentState] = {}
        self._init_departments()
    
    def _init_departments(self):
        departments_config = [
            {"id": "dept_1", "name": "Lead Scraping", "head": "ScrapeHead", "subs": ["DataHunter1", "DataHunter2", "DataHunter3", "VerifierAgent"]},
            {"id": "dept_2", "name": "Validation & Enrichment", "head": "EnrichHead", "subs": ["ValidatorAgent", "CompetitorSpyAgent", "AudienceAnalystAgent", "StructureBotAgent"]},
            {"id": "dept_3", "name": "Marketing", "head": "MarketingHead", "subs": ["IntelHead", "FunnelHead", "CopyHead", "QAHead", "CompetitorHead"]},
            {"id": "dept_4", "name": "Email Sending", "head": "SendHead", "subs": ["AccountBalancer", "ThrottleGuard", "SchedulerBot", "IPGuardian"]},
            {"id": "dept_5", "name": "Tracking & Analytics", "head": "AnalyticsHead", "subs": ["OpenTracker", "ClickTracker", "ReplyDetector", "InsightBot"]},
            {"id": "dept_6", "name": "Sales & Replies", "head": "SalesHead", "subs": ["ReplyReader", "HumanVoice1", "HumanVoice2", "ConversionDetector"]},
            {"id": "dept_7", "name": "Sheets & Reporting", "head": "SheetsHead", "subs": ["SheetBot1", "SheetBot2", "DataFormatter", "ExportBot"]},
            {"id": "dept_8", "name": "Email Accounts", "head": "AccountHead", "subs": ["WarmupBot", "HealthMonitor", "CapacityPlanner", "UISync"]},
            {"id": "dept_9", "name": "Task Management", "head": "TaskHead", "subs": ["TaskTracker", "ProgressMonitor", "QueueManager", "LimitEnforcer"]},
            {"id": "dept_10", "name": "ML Learning", "head": "MLHead", "subs": ["PatternFinder", "ModelTrainer", "StrategyUpdater", "PerformanceScorer"]},
            {"id": "dept_11", "name": "JARVIS Interface", "head": "JARVIS", "subs": ["CommandParser", "ResponseGenerator", "NotificationBot"]},
            {"id": "dept_12", "name": "Memory & Soul", "head": "MemorySystem", "subs": ["SoulKeeper", "BrainManager", "BackupAgent"]},
        ]
        
        for dept in departments_config:
            self.departments[dept["id"]] = Department(
                id=dept["id"],
                name=dept["name"],
                head_agent=dept["head"],
                sub_agents=dept["subs"],
                status="online",
                tasks_completed=0,
                current_load=0
            )
            
            for agent_name in [dept["head"]] + dept["subs"]:
                self.agents[agent_name] = AgentState(agent_name, f"{dept['name']} - {agent_name}")
    
    def get_department(self, dept_id: str) -> Optional[Department]:
        return self.departments.get(dept_id)
    
    def get_agent(self, agent_name: str) -> Optional[AgentState]:
        return self.agents.get(agent_name)
    
    def update_agent_status(self, agent_name: str, status: str):
        if agent_name in self.agents:
            self.agents[agent_name].status = status
            self.agents[agent_name].last_active = datetime.utcnow()
    
    def assign_task(self, dept_id: str, task_data: Dict) -> bool:
        dept = self.departments.get(dept_id)
        if dept and dept.current_load < 10:
            dept.current_load += 1
            return True
        return False
    
    def complete_task(self, dept_id: str):
        dept = self.departments.get(dept_id)
        if dept:
            dept.current_load = max(0, dept.current_load - 1)
            dept.tasks_completed += 1
    
    def get_system_status(self) -> Dict:
        return {
            "total_departments": len(self.departments),
            "total_agents": len(self.agents),
            "departments": {k: v.to_dict() for k, v in self.departments.items()},
            "online_agents": sum(1 for a in self.agents.values() if a.status == "online"),
            "system_health": self._calculate_health()
        }
    
    def _calculate_health(self) -> str:
        online_count = sum(1 for d in self.departments.values() if d.status == "online")
        if online_count == len(self.departments):
            return "excellent"
        elif online_count >= len(self.departments) * 0.8:
            return "good"
        elif online_count >= len(self.departments) * 0.5:
            return "fair"
        return "critical"
    
    def save_state(self, filepath: str = "data/department_state.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                "departments": {k: v.to_dict() for k, v in self.departments.items()},
                "agents": {k: v.to_dict() for k, v in self.agents.items()},
                "saved_at": datetime.utcnow().isoformat()
            }, f, indent=2)
    
    def load_state(self, filepath: str = "data/department_state.json"):
        if not os.path.exists(filepath):
            return
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for dept_id, dept_data in data.get("departments", {}).items():
                    if dept_id in self.departments:
                        self.departments[dept_id].status = dept_data.get("status", "online")
                        self.departments[dept_id].tasks_completed = dept_data.get("tasks_completed", 0)
        except Exception:
            pass

department_manager = DepartmentManager()