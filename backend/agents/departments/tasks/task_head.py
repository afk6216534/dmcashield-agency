from typing import Dict, List
from agents.base_agent import BaseAgent

class TaskTracker(BaseAgent):
    def __init__(self):
        super().__init__("TaskTracker")
        self.tasks = []

    def track_task(self, task: Dict) -> Dict:
        self.tasks.append(task)
        return {"task_id": task.get("id"), "status": "tracked"}

    def start(self):
        return {"status": "online", "tasks_tracked": len(self.tasks)}
