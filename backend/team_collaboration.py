# Team Collaboration Hub
# ===================
# Coordinate between OpenCode, Claude Code, and Antigravity

import os
import json
from typing import Dict, List
from datetime import datetime, timedelta

class AICollaboration:
    """Team collaboration across AI systems"""
    
    def __init__(self, team_file: str = "data/team_collaboration.json"):
        self.team_file = team_file
        self.team = self._load_team()
    
    def _load_team(self) -> Dict:
        if os.path.exists(self.team_file):
            try:
                with open(self.team_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "opencode": {
                "name": "OpenCode",
                "status": "ready",
                "strengths": ["file operations", "glob/search", "API creation"],
                "current_task": None,
                "last_active": None
            },
            "claude_code": {
                "name": "Claude Code",
                "status": "ready",
                "strengths": ["React/Frontend", "complex debugging", "testing"],
                "current_task": None,
                "last_active": None
            },
            "antigravity": {
                "name": "Antigravity",
                "status": "ready",
                "strengths": ["orchestration", "team coordination"],
                "current_task": None,
                "last_active": None
            }
        }
    
    def _save_team(self):
        os.makedirs("data", exist_ok=True)
        with open(self.team_file, 'w') as f:
            json.dump(self.team, f, indent=2)
    
    def assign_task(self, ai: str, task: str):
        """Assign task to AI team member"""
        if ai in self.team:
            self.team[ai]["current_task"] = task
            self.team[ai]["last_active"] = datetime.utcnow().isoformat()
            self._save_team()
            return {"assigned": task, "to": ai}
        return {"error": f"AI {ai} not found"}
    
    def get_available_ai(self) -> str:
        """Get available AI"""
        for ai, info in self.team.items():
            if info.get("status") == "ready":
                return ai
        return "opencode"
    
    def get_status(self) -> Dict:
        """Get all AI statuses"""
        return {ai: {
            "status": info.get("status"),
            "task": info.get("current_task"),
            "last_active": info.get("last_active")
        } for ai, info in self.team.items()}
    
    def complete_task(self, ai: str):
        """Mark task complete"""
        if ai in self.team:
            self.team[ai]["current_task"] = None
            self.team[ai]["status"] = "ready"
            self._save_team()
            return {"status": "complete", "ai": ai}
        return {"error": f"AI {ai} not found"}
    
    def delegate(self, task: str) -> Dict:
        """Delegate task to best available AI"""
        available = self.get_available_ai()
        
        priorities = {
            "frontend": "claude_code",
            "react": "claude_code",
            "debug": "claude_code",
            "api": "opencode",
            "file": "opencode",
            "database": "opencode",
            "orchestrate": "antigravity",
            "coordinate": "antigravity"
        }
        
        for keyword, ai in priorities.items():
            if keyword in task.lower():
                if self.team[ai].get("status") == "ready":
                    available = ai
                    break
        
        return self.assign_task(available, task)

class Handoffs:
    """Handle handoffs between AIs"""
    
    def __init__(self, handoff_file: str = "data/handoffs.json"):
        self.handoff_file = handoff_file
        self.handoffs = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.handoff_file):
            try:
                with open(self.handoff_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"handoffs": [], "pending": []}
    
    def create_handoff(self, from_ai: str, to_ai: str, context: Dict) -> Dict:
        """Create handoff"""
        handoff = {
            "id": len(self.handoffs["handoffs"]) + 1,
            "from": from_ai,
            "to": to_ai,
            "context": context,
            "status": "pending",
            "created": datetime.utcnow().isoformat()
        }
        self.handoffs["handoffs"].append(handoff)
        self.handoffs["pending"].append(handoff["id"])
        self._save()
        return handoff
    
    def complete_handoff(self, handoff_id: int) -> Dict:
        """Complete handoff"""
        if handoff_id in self.handoffs["pending"]:
            self.handoffs["pending"].remove(handoff_id)
            for h in self.handoffs["handoffs"]:
                if h["id"] == handoff_id:
                    h["status"] = "complete"
                    h["completed"] = datetime.utcnow().isoformat()
            self._save()
            return {"status": "complete", "id": handoff_id}
        return {"error": "Handoff not found"}
    
    def _save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.handoff_file, 'w') as f:
            json.dump(self.handoffs, f, indent=2)
    
    def get_pending(self) -> List[Dict]:
        """Get pending handoffs"""
        return [h for h in self.handoffs["handoffs"] if h.get("status") == "pending"]

Collaboration = AICollaboration()
handoffs = Handoffs()