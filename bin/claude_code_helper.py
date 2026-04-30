# Claude Code Helper for DMCAShield
# ===========================
# Functions Claude Code can use to work with DMCAShield

import requests
import json
from typing import Dict, List, Optional

BASE_URL = "http://localhost:8000"

def get_tasks() -> List[Dict]:
    """Get all tasks"""
    r = requests.get(f"{BASE_URL}/api/tasks/")
    return r.json()

def get_task(task_id: int) -> Dict:
    """Get single task"""
    r = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    return r.json()

def create_task(business_type: str, city: str, state: str) -> Dict:
    """Create new scraping task"""
    data = {
        "business_type": business_type,
        "city": city,
        "state": state,
        "country": "USA"
    }
    r = requests.post(f"{BASE_URL}/api/tasks/", json=data)
    return r.json()

def get_leads(status: str = "all", limit: int = 50) -> List[Dict]:
    """Get leads with status filter"""
    r = requests.get(f"{BASE_URL}/api/leads/", params={"status": status, "limit": limit})
    return r.json()

def get_hot_leads() -> List[Dict]:
    """Get hot leads ready for sales"""
    r = requests.get(f"{BASE_URL}/api/sales/hot-leads")
    return r.json()

def send_email(lead_id: int, subject: str, body: str) -> Dict:
    """Send email to lead"""
    data = {"subject": subject, "body": body}
    r = requests.post(f"{BASE_URL}/api/email/send/{lead_id}", json=data)
    return r.json()

def get_analytics() -> Dict:
    """Get dashboard analytics"""
    r = requests.get(f"{BASE_URL}/api/analytics/dashboard")
    return r.json()

def run_autonomous() -> Dict:
    """Start autonomous mode"""
    r = requests.post(f"{BASE_URL}/api/autonomous/full_start")
    return r.json()

def chat_with_jarvis(message: str) -> str:
    """Chat with JARVIS"""
    r = requests.post(f"{BASE_URL}/api/jarvis/chat", json={"message": message})
    return r.json().get("response", "")

def get_agent_status() -> Dict:
    """Get all agent statuses"""
    r = requests.get(f"{BASE_URL}/api/agents/status")
    return r.json()

def trigger_skill(skill_trigger: str, context: Dict = None) -> Dict:
    """Trigger a skill"""
    data = {"trigger": skill_trigger, "context": context or {}}
    r = requests.post(f"{BASE_URL}/api/skills/execute", json=data)
    return r.json()

def get_resource(resource_name: str) -> Dict:
    """Get resource info"""
    r = requests.get(f"{BASE_URL}/api/resources/{resource_name}")
    return r.json()

__all__ = [
    "get_tasks", "get_task", "create_task", "get_leads", "get_hot_leads",
    "send_email", "get_analytics", "run_autonomous", "chat_with_jarvis",
    "get_agent_status", "trigger_skill", "get_resource"
]