"""
Soul System (12th Department)
Persistent memory and identity across all sessions and restarts.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class Soul:
    """Company soul - persistent identity and memory."""

    def __init__(self, soul_path: str = "soul.json"):
        self.soul_path = soul_path
        self.data = self._load_or_create()
        self.memory_stack = []

    def _load_or_create(self) -> Dict[str, Any]:
        """Load soul from file or create new."""
        full_path = "F:/Anti gravity projects/Dmca company/dmcashield-agency/" + self.soul_path
        
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Create new soul
        soul = {
            "creation_date": datetime.utcnow().isoformat(),
            "version": 1.0,
            "identity": {
                "company_name": "DMCAShield Agency",
                "mission": "Autonomous DMCA review removal",
                "core_values": [
                    "Persistence",
                    "Learning",
                    "Adaptability",
                    "Legal compliance",
                    "Continuous optimization"
                ]
            },
            "state": {
                "status": "operational",
                "active_tasks": 0,
                "total_leads_processed": 0,
                "total_emails_sent": 0,
                "total_clients_acquired": 0,
                "total_revenue": 0,
                "uptime_seconds": 0,
                "last_restart": datetime.utcnow().isoformat()
            },
            "memory": {
                "recent_leads": [],
                "top_patterns": {},
                "winning_strategies": [],
                "avoided_mistakes": []
            },
            "growth": {
                "learning_cycles": 0,
                "optimizations_applied": 0,
                "adaptations_made": 0
            },
            "departments": {
                "scraping": {"status": "online", "leads_found": 0},
                "validation": {"status": "online", "leads_verified": 0},
                "marketing": {"status": "online", "emails_created": 0},
                "email_sending": {"status": "online", "emails_sent": 0},
                "tracking": {"status": "online", "opens_tracked": 0},
                "sales": {"status": "online", "replies_handled": 0},
                "sheets": {"status": "online", "updates_made": 0},
                "accounts": {"status": "online", "accounts_managed": 0},
                "tasks": {"status": "online", "tasks_completed": 0},
                "ml": {"status": "online", "patterns_learned": 0},
                "jarvis": {"status": "online", "commands_processed": 0},
                "memory": {"status": "online", "memories_stored": 0}
            }
        }
        
        self._save(soul)
        return soul

    def _save(self, soul_data: Optional[Dict[str, Any]] = None) -> bool:
        """Save soul to persistent storage."""
        save_data = soul_data or self.data
        
        try:
            full_path = "F:/Anti gravity projects/Dmca company/dmcashield-agency/" + self.soul_path
            with open(full_path, 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Soul save error: {e}")
            return False

    def get_soul(self) -> Dict[str, Any]:
        """Get current soul state."""
        return self.data

    def update_state(self, updates: Dict[str, Any]) -> bool:
        """Update soul state with new data."""
        self.data["state"].update(updates)
        self.data["state"]["last_update"] = datetime.utcnow().isoformat()
        return self._save()

    def increment_metric(self, path: str, amount: int = 1) -> bool:
        """Increment a specific metric in the soul."""
        keys = path.split('.')
        target = self.data
        
        for key in keys[:-1]:
            target = target.setdefault(key, {})
        
        final_key = keys[-1]
        target[final_key] = target.get(final_key, 0) + amount
        
        return self._save()

    def add_memory(self, memory: Dict[str, Any]) -> bool:
        """Add a memory entry to the soul."""
        memory_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": memory.get("type", "general"),
            "content": memory.get("content", {}),
            "importance": memory.get("importance", 5)
        }
        
        self.memory_stack.append(memory_entry)
        
        # Keep only recent memories (last 1000)
        if len(self.memory_stack) > 1000:
            self.memory_stack = self.memory_stack[-1000:]
        
        self.data["state"]["memories_stored"] = len(self.memory_stack)
        return self._save()

    def add_growth(self, growth_type: str, description: str) -> bool:
        """Record system growth/learning."""
        growth_entry = {
            "type": growth_type,
            "description": description,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.data["growth"][f"{growth_type}s_made"] = \
            self.data["growth"].get(f"{growth_type}s_made", 0) + 1
        
        if "growth_history" not in self.data:
            self.data["growth_history"] = []
        
        self.data["growth_history"].append(growth_entry)
        self.data["growth"]["adaptations_made"] += 1
        
        return self._save()

    def backup(self) -> bool:
        """Create a backup of current soul state."""
        try:
            backup_path = "F:/Anti gravity projects/Dmca company/dmcashield-agency/soul_backup.json"
            with open(backup_path, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False

    def auto_backup(self) -> bool:
        """Perform automatic backup every 6 hours (simulated)."""
        # In production, would check time and backup periodically
        # For now, just backup
        return self.backup()

# Global soul instance
soul = Soul("soul.json")

def get_soul():
    """Get the global soul instance."""
    return soul

# Example usage
if __name__ == "__main__":
    soul = get_soul()
    
    # Update some metrics
    soul.increment_metric("state.total_leads_processed", 5)
    soul.increment_metric("departments.scraping.leads_found", 5)
    
    # Get current state
    current = soul.get_soul()
    print(f"Total leads: {current['state']['total_leads_processed']}")
    print(f"Uptime: {current['state']['uptime_seconds']}s")
