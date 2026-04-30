# Enhanced Automation Engine
# =======================
# Advanced automation with more intelligence

import asyncio
import random
from typing import Dict, List, Callable
from datetime import datetime, timedelta

class SmartAutomation:
    """Intelligent automation that learns"""
    
    def __init__(self):
        self.workflows = {}
        self.learned_patterns = {}
        self.automations_running = []
    
    def register_workflow(self, name: str, steps: List[Callable], conditions: Dict = None):
        """Register a workflow"""
        self.workflows[name] = {
            "steps": steps,
            "conditions": conditions or {},
            "run_count": 0,
            "success_count": 0,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def run_workflow(self, name: str, context: Dict) -> Dict:
        """Run workflow with learning"""
        workflow = self.workflows.get(name)
        if not workflow:
            return {"error": "Workflow not found"}
        
        workflow["run_count"] += 1
        results = []
        
        for step in workflow["steps"]:
            try:
                result = await step(context)
                results.append({"step": step.__name__, "result": result, "success": True})
            except Exception as e:
                results.append({"step": step.__name__, "error": str(e), "success": False})
                workflow["success_count"] += 1
                break
        
        if results[-1].get("success"):
            workflow["success_count"] += 1
        
        return {"workflow": name, "results": results}
    
    def learn_from_result(self, workflow: str, result: Dict):
        """Learn from workflow result"""
        if workflow not in self.learned_patterns:
            self.learned_patterns[workflow] = []
        
        self.learned_patterns[workflow].append({
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if len(self.learned_patterns[workflow]) > 10:
            self.learned_patterns[workflow] = self.learned_patterns[workflow][-10:]

class AdaptiveScheduler:
    """Scheduler that adapts to performance"""
    
    def __init__(self):
        self.schedules = {}
        self.performance_history = []
    
    def add_schedule(self, name: str, interval_minutes: int, action: Callable):
        """Add adaptive schedule"""
        self.schedules[name] = {
            "interval": interval_minutes,
            "action": action,
            "last_run": None,
            "avg_duration": 0,
            "success_rate": 1.0
        }
    
    def get_optimal_interval(self, name: str) -> int:
        """Get optimal interval based on performance"""
        schedule = self.schedules.get(name)
        if not schedule:
            return 60
        
        perf = schedule["success_rate"]
        base = schedule["interval"]
        
        if perf > 0.9:
            return int(base * 0.8)
        elif perf > 0.7:
            return base
        else:
            return int(base * 1.5)
    
    def record_performance(self, name: str, duration: float, success: bool):
        """Record performance for learning"""
        schedule = self.schedules.get(name)
        if not schedule:
            return
        
        history = self.performance_history
        history.append({
            "schedule": name,
            "duration": duration,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if len(history) > 50:
            history = history[-50:]
        
        schedule["success_rate"] = sum(1 for h in history if h["success"]) / len(history)
        schedule["avg_duration"] = sum(h["duration"] for h in history) / len(history)

class SelfHealing:
    """System that heals itself"""
    
    def __init__(self):
        self.error_patterns = {}
        self.fixes_applied = []
    
    def record_error(self, error: str, context: Dict):
        """Record error for pattern matching"""
        if error not in self.error_patterns:
            self.error_patterns[error] = []
        self.error_patterns[error].append({
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_fix(self, error: str) -> str:
        """Get fix for error"""
        fixes = {
            "connection_timeout": "increase_timeout",
            "rate_limit": "add_delay",
            "invalid_email": "skip_lead",
            "auth_failed": "refresh_token",
            "parse_error": "fallback_parser"
        }
        return fixes.get(error, "retry")
    
    def apply_fix(self, error: str) -> Dict:
        """Apply automatic fix"""
        fix = self.get_fix(error)
        self.fixes_applied.append({
            "error": error,
            "fix": fix,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {"error": error, "fix_applied": fix}

smart_automation = SmartAutomation()
adaptive_scheduler = AdaptiveScheduler()
self_healing = SelfHealing()