"""
DMCAShield Skills System
===================
Add skills for AI team to use - like Claude Code skills
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class SkillRegistry:
    """Registry of all skills available to the AI team"""
    
    def __init__(self, config_file: str = "data/skills.json"):
        self.config_file = config_file
        self.skills = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "skills": {},
            "active_skill": None,
            "skill_history": []
        }
    
    def _save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.skills, f, indent=2)
    
    def register_skill(self, skill_id: str, name: str, description: str, 
                 trigger: str, actions: List[str], icon: str = "⚡"):
        """Register a new skill"""
        self.skills["skills"][skill_id] = {
            "id": skill_id,
            "name": name,
            "description": description,
            "trigger": trigger,
            "actions": actions,
            "icon": icon,
            "created_at": datetime.utcnow().isoformat(),
            "usage_count": 0
        }
        self._save()
    
    def activate_skill(self, skill_id: str) -> bool:
        """Activate a skill"""
        if skill_id in self.skills["skills"]:
            self.skills["active_skill"] = skill_id
            self.skills["skills"][skill_id]["usage_count"] = \
                self.skills["skills"][skill_id].get("usage_count", 0) + 1
            self._save()
            return True
        return False
    
    def deactivate_skill(self):
        """Deactivate current skill"""
        self.skills["active_skill"] = None
        self._save()
    
    def get_skill(self, skill_id: str) -> Optional[Dict]:
        return self.skills["skills"].get(skill_id)
    
    def get_active_skill(self) -> Optional[Dict]:
        active = self.skills.get("active_skill")
        if active:
            return self.skills["skills"].get(active)
        return None
    
    def find_skill_by_trigger(self, trigger: str) -> Optional[Dict]:
        """Find skill by trigger word"""
        for skill in self.skills["skills"].values():
            if skill.get("trigger") == trigger:
                return skill
        return None
    
    def list_skills(self) -> List[Dict]:
        return list(self.skills["skills"].values())
    
    def execute_skill(self, skill_id: str, context: Dict) -> Dict:
        """Execute skill actions"""
        skill = self.skills["skills"].get(skill_id)
        if not skill:
            return {"error": "Skill not found"}
        
        results = []
        for action in skill.get("actions", []):
            result = self._execute_action(action, context)
            results.append(result)
        
        return {"skill": skill["name"], "results": results}
    
    def _execute_action(self, action: str, context: Dict) -> Dict:
        """Execute a single action"""
        parts = action.split(":")
        action_type = parts[0]
        
        if action_type == "scrape":
            return {"action": "scraping", "status": "would execute scrape"}
        elif action_type == "email":
            return {"action": "send_email", "status": "would send email"}
        elif action_type == "notify":
            return {"action": "notify", "status": "would send notification"}
        elif action_type == "track":
            return {"action": "track", "status": "would track in posthog"}
        else:
            return {"action": action_type, "status": "unknown"}

# Pre-built skills
DEFAULT_SKILLS = [
    {
        "skill_id": "lead_scrape",
        "name": "Lead Scraper",
        "description": "Automatically scrape leads for a business type and location",
        "trigger": "/scrape",
        "actions": ["scrape:google_maps", "enrich:lead_data", "save:database"],
        "icon": "🔍"
    },
    {
        "skill_id": "email_campaign",
        "name": "Email Campaign",
        "description": "Run complete email campaign sequence",
        "trigger": "/email",
        "actions": ["select:leads", "generate:email_content", "send:emails", "track:opens"],
        "icon": "📧"
    },
    {
        "skill_id": "hot_lead_alert",
        "name": "Hot Lead Alert",
        "description": "Monitor and alert on hot leads",
        "trigger": "/alert",
        "actions": ["check:hot_leads", "notify:telegram", "notify:slack", "update:database"],
        "icon": "🔥"
    },
    {
        "skill_id": "daily_report",
        "name": "Daily Report",
        "description": "Generate and send daily performance report",
        "trigger": "/report",
        "actions": ["collect:analytics", "generate:report", "send:email", "track:posthog"],
        "icon": "📊"
    },
    {
        "skill_id": "warmup_email",
        "name": "Email Warmup",
        "description": "Warm up email accounts for better deliverability",
        "trigger": "/warmup",
        "actions": ["check:account_status", "send:warmup_emails", "track:engagement", "update:score"],
        "icon": "🌡️"
    },
    {
        "skill_id": "ai_respond",
        "name": "AI Responder",
        "description": "Use AI to generate personalized responses",
        "trigger": "/ai",
        "actions": ["analyze:lead", "generate:response", "humanize:message", "queue:send"],
        "icon": "🤖"
    },
    {
        "skill_id": "autopilot",
        "name": "Autopilot",
        "description": "Run the entire agency on autopilot",
        "trigger": "/autopilot",
        "actions": ["check:tasks", "process:queue", "handle:replies", "convert:leads"],
        "icon": "✈️"
    },
    {
        "skill_id": "graphify",
        "name": "Knowledge Graph",
        "description": "Build knowledge graph for context",
        "trigger": "/graphify",
        "actions": ["extract:entities", "build:graph", "query:knowledge", "optimize:tokens"],
        "icon": "🕸️"
    }
]

def init_default_skills():
    """Initialize default skills"""
    registry = SkillRegistry()
    for skill in DEFAULT_SKILLS:
        registry.register_skill(
            skill_id=skill["skill_id"],
            name=skill["name"],
            description=skill["description"],
            trigger=skill["trigger"],
            actions=skill["actions"],
            icon=skill["icon"]
        )
    return registry

skill_registry = init_default_skills()

# AI Team Learnings System
class AIteamLearnings:
    """System for AI team to learn and improve"""
    
    def __init__(self, learnings_file: str = "data/ai_learnings.json"):
        self.learnings_file = learnings_file
        self.learnings = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.learnings_file):
            try:
                with open(self.learnings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "improvements": [],
            "patterns": {},
            "successes": [],
            "failures": [],
            "team_notes": []
        }
    
    def _save(self):
        os.makedirs(os.path.dirname(self.learnings_file), exist_ok=True)
        with open(self.learnings_file, 'w') as f:
            json.dump(self.learnings, f, indent=2)
    
    def add_improvement(self, area: str, change: str, result: str):
        """Add improvement learning"""
        self.learnings["improvements"].append({
            "area": area,
            "change": change,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()
    
    def add_pattern(self, trigger: str, success_action: str):
        """Add successful pattern"""
        if trigger not in self.learnings["patterns"]:
            self.learnings["patterns"][trigger] = []
        self.learnings["patterns"][trigger].append(success_action)
        self._save()
    
    def record_success(self, action: str, details: Dict):
        """Record successful action"""
        self.learnings["successes"].append({
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()
    
    def record_failure(self, action: str, error: str):
        """Record failed action"""
        self.learnings["failures"].append({
            "action": action,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()
    
    def add_team_note(self, note: str, author: str = "AI Team"):
        """Add team note"""
        self.learnings["team_notes"].append({
            "note": note,
            "author": author,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()
    
    def get_recommendations(self) -> List[str]:
        """Get improvement recommendations"""
        recommendations = []
        
        # Analyze failures
        for failure in self.learnings.get("failures", [])[-5:]:
            recommendations.append(f"Fix: {failure.get('error')}")
        
        # Analyze patterns
        for trigger, actions in self.learnings.get("patterns", {}).items():
            if len(actions) > 3:
                recommendations.append(f"{trigger} works well - use more!")
        
        return recommendations

ai_learnings = AIteamLearnings()