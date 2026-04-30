"""
AI Team Gamification
=================
Gamify the work - achievements, levels, streaks for AI team
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List

class AITeamGamification:
    """Gamification system for AI team"""
    
    def __init__(self, gamification_file: str = "data/gamification.json"):
        self.gamification_file = gamification_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.gamification_file):
            try:
                with open(self.gamification_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "members": {
                "opencode": {"xp": 0, "level": 1, "streak": 0, "achievements": []},
                "claude_code": {"xp": 0, "level": 1, "streak": 0, "achievements": []},
                "antigravity": {"xp": 0, "level": 1, "streak": 0, "achievements": []}
            },
            "leaderboard": [],
            "achievements": {
                "first_task": {"name": "First Task", "xp": 10, "icon": "🎯"},
                "hot_lead": {"name": "Hot Lead Found", "xp": 50, "icon": "🔥"},
                "speed_demon": {"name": "Fast Response", "xp": 25, "icon": "⚡"},
                "team_player": {"name": "Team Player", "xp": 30, "icon": "🤝"},
                "night_owl": {"name": "Night Owl", "xp": 20, "icon": "🦉"},
                "early_bird": {"name": "Early Bird", "xp": 20, "icon": "🐦"},
                "innovator": {"name": "Innovator", "xp": 100, "icon": "💡"},
                "mentor": {"name": "Helpful Mentor", "xp": 40, "icon": "📚"},
                "workhorse": {"name": "Dedicated Worker", "xp": 50, "icon": "🐴"},
                "master": {"name": "Skill Master", "xp": 200, "icon": "🏆"}
            }
        }
    
    def _save(self):
        os.makedirs(os.path.dirname(self.gamification_file), exist_ok=True)
        with open(self.gamification_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_xp(self, member: str, xp: int):
        if member not in self.data["members"]:
            self.data["members"][member] = {"xp": 0, "level": 1, "streak": 0, "achievements": []}
        
        self.data["members"][member]["xp"] += xp
        
        # Level up check
        xp_needed = self.data["members"][member]["level"] * 100
        if self.data["members"][member]["xp"] >= xp_needed:
            self.data["members"][member]["level"] += 1
            return {"level_up": True, "new_level": self.data["members"][member]["level"]}
        
        return {"level_up": False}
    
    def unlock_achievement(self, member: str, achievement_id: str) -> bool:
        if member not in self.data["members"]:
            return False
        
        achievement = self.data["achievements"].get(achievement_id)
        if not achievement:
            return False
        
        # Check if already has
        if achievement_id in self.data["members"][member].get("achievements", []):
            return False
        
        # Add achievement and XP
        self.data["members"][member]["achievements"].append(achievement_id)
        self.add_xp(member, achievement.get("xp", 0))
        self._save()
        return True
    
    def update_streak(self, member: str):
        if member not in self.data["members"]:
            self.data["members"][member] = {"xp": 0, "level": 1, "streak": 0, "achievements": []}
        
        self.data["members"][member]["streak"] += 1
        
        # Bonus XP for streaks
        if self.data["members"][member]["streak"] in [7, 30, 100]:
            self.add_xp(member, self.data["members"][member]["streak"] * 10)
    
    def get_member_stats(self, member: str) -> Dict:
        return self.data["members"].get(member, {})
    
    def get_leaderboard(self) -> List[Dict]:
        members = []
        for name, stats in self.data["members"].items():
            members.append({
                "name": name,
                "xp": stats.get("xp", 0),
                "level": stats.get("level", 1),
                "achievements": len(stats.get("achievements", []))
            })
        
        return sorted(members, key=lambda x: x["xp"], reverse=True)
    
    def get_achievements(self) -> List[Dict]:
        return [
            {"id": k, **v} for k, v in self.data["achievements"].items()
        ]

gamification = AITeamGamification()