"""
TaskTracker Agent (9th Department) - Task Lifecycle Manager
Controls task state: queued, active, paused, complete, cancelled.
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class TaskTracker:
    """Manages all task lifecycles and progress."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def create_task(self, business_type: str, city: str,
                   state: str, country: str = "USA") -> Dict[str, Any]:
        """Create new task and return task ID."""
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        task = {
            "id": task_id,
            "business_type": business_type,
            "city": city,
            "state": state,
            "country": country,
            "status": "queued",
            "phase_scraping": "pending",
            "phase_validation": "pending",
            "phase_funnel": "pending",
            "phase_sending": "pending",
            "phase_tracking": "pending",
            "phase_sales": "pending",
            "leads_total": 0,
            "leads_scraped": 0,
            "leads_emailed": 0,
            "leads_opened": 0,
            "leads_replied": 0,
            "leads_hot": 0,
            "leads_converted": 0,
            "funnel_completion_rate": 0.0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        self.tasks[task_id] = task
        print(f"Task created: {task_id} - {business_type} in {city}, {state}")
        return task

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve task by ID."""
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update overall task status."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        valid_statuses = ["queued", "active", "paused", "complete", "cancelled"]
        if status not in valid_statuses:
            return False
        
        task["status"] = status
        task["updated_at"] = datetime.utcnow().isoformat()
        print(f"Task {task_id} status updated to: {status}")
        return True

    def update_phase(self, task_id: str, phase_name: str,
                    phase_status: str) -> bool:
        """Update a specific phase status."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        phase_key = f"phase_{phase_name}"
        if phase_key not in task:
            return False
        
        valid_phase_statuses = ["pending", "active", "complete", "failed"]
        if phase_status not in valid_phase_statuses:
            return False
        
        task[phase_key] = phase_status
        task["updated_at"] = datetime.utcnow().isoformat()
        
        # Auto-update overall status if all phases complete
        if all(task.get(f"phase_{p}", "pending") == "complete" 
               for p in ["scraping", "validation", "funnel", "sending", "tracking", "sales"]):
            self.update_task_status(task_id, "complete")
        
        return True

    def add_lead(self, task_id: str, lead_data: Dict[str, Any] = None) -> bool:
        """Increment lead counter for task."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task["leads_total"] += 1
        task["updated_at"] = datetime.utcnow().isoformat()
        return True

    def update_lead_metrics(self, task_id: str, **kwargs) -> bool:
        """Update various lead counters."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        valid_metrics = [
            "leads_scraped", "leads_emailed", "leads_opened",
            "leads_replied", "leads_hot", "leads_converted"
        ]
        
        for metric, value in kwargs.items():
            if metric in valid_metrics:
                task[metric] = value
        
        # Calculate funnel completion rate
        if task["leads_total"] > 0:
            completed = task["leads_replied"] + task["leads_hot"] + task["leads_converted"]
            task["funnel_completion_rate"] = round(completed / task["leads_total"], 3)
        
        task["updated_at"] = datetime.utcnow().isoformat()
        return True

    def list_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """List all tasks, optionally filtered by status."""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        
        # Sort by creation date (newest first)
        return sorted(tasks, key=lambda t: t["created_at"], reverse=True)

    def get_task_summary(self, task_id: str) -> Dict[str, Any]:
        """Get concise task summary."""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        
        return {
            "id": task["id"],
            "business": f"{task['business_type']} ({task['city']}, {task['state']})",
            "status": task["status"],
            "leads": {
                "total": task["leads_total"],
                "scraped": task["leads_scraped"],
                "emailed": task["leads_emailed"],
                "hot": task["leads_hot"],
                "converted": task["leads_converted"]
            },
            "funnel_completion": task["funnel_completion_rate"],
            "phases": {
                "scraping": task["phase_scraping"],
                "validation": task["phase_validation"],
                "funnel": task["phase_funnel"],
                "sending": task["phase_sending"],
                "tracking": task["phase_tracking"],
                "sales": task["phase_sales"]
            },
            "created_at": task["created_at"]
        }

# Example usage
if __name__ == "__main__":
    tracker = TaskTracker()
    
    # Create a task
    task = tracker.create_task("restaurant", "Austin", "TX")
    task_id = task["id"]
    
    # Update phases
    tracker.update_phase(task_id, "scraping", "active")
    tracker.update_phase(task_id, "scraping", "complete")
    tracker.update_phase(task_id, "validation", "active")
    
    # Add leads
    tracker.add_lead(task_id)
    tracker.add_lead(task_id)
    tracker.update_lead_metrics(task_id, leads_scraped=2)
    
    # Get summary
    summary = tracker.get_task_summary(task_id)
    print(json.dumps(summary, indent=2))
