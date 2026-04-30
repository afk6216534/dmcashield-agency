# Auto-Training & Learning System 24/7
# =================================
# System trains itself continuously on real-world results

import random
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

class AutoTrainer:
    """24/7 Self-learning system that trains on real-world data"""
    
    def __init__(self):
        self.training_data = []
        self.model_performance = {}
        self.detection_evasion_score = 50
        self.last_training = None
        self.training_interval = 300
        self.always_learning = True
        
    def train_on_result(self, action: str, result: str, context: Dict):
        """Train on any action result"""
        self.training_data.append({
            "action": action,
            "result": result,
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
            "success": result in ["success", "converted", "delivered"]
        })
        
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-500:]
        
        self.last_training = datetime.utcnow().isoformat()
        
        if result == "detected_as_bot":
            self._improve_stealth()
        elif result == "blocked":
            self._improve_strategy()
        elif result == "failed":
            self._learn_from_failure(action)
    
    def _improve_stealth(self):
        """Improve detection evasion"""
        self.detection_evasion_score = max(0, self.detection_evasion_score - 5)
        self._add_training_rule("slowDown", "random_delay")
        self._add_training_rule("varyTimestamps", True)
        self._add_training_rule("rotateProfiles", True)
    
    def _improve_strategy(self):
        """Improve overall strategy"""
        self._add_training_rule("changeApproach", True)
        self._add_training_rule("retryWithDiff", True)
    
    def _learn_from_failure(self, action: str):
        """Learn from failures"""
        fail_patterns = {
            "scraping": ["slow_down", "change_ip", "wait_longer"],
            "email": ["change_template", "different_subject", "personalize_more"],
            "outreach": ["be_more_natural", "less_promotional"]
        }
        
        patterns = fail_patterns.get(action, ["try_again"])
        rule = random.choice(patterns)
        self._add_training_rule(rule, True)
    
    def _add_training_rule(self, rule: str, value):
        """Add a new training rule"""
        if "training_rules" not in self.model_performance:
            self.model_performance["training_rules"] = {}
        self.model_performance["training_rules"][rule] = value
    
    def get_stealth_level(self) -> int:
        """Get current stealth level"""
        return self.detection_evasion_score
    
    def should_learn(self) -> bool:
        """Check if should learn"""
        if not self.last_training:
            return True
        
        last = datetime.fromisoformat(self.last_training)
        elapsed = (datetime.utcnow() - last).total_seconds()
        
        return elapsed > self.training_interval
    
    def continuous_learn(self):
        """Learn continuously 24/7"""
        if self.should_learn():
            recent = self.training_data[-10:] if len(self.training_data) > 10 else self.training_data
            
            success_rate = sum(1 for t in recent if t.get("success")) / len(recent) if recent else 0
            
            if success_rate < 0.7:
                self.detection_evasion_score = max(0, self.detection_evasion_score - 3)
            else:
                self.detection_evasion_score = min(100, self.detection_evasion_score + 1)
            
            self.last_training = datetime.utcnow().isoformat()
            
            return {
                "learning": True,
                "stealth_score": self.detection_evasion_score,
                "success_rate": success_rate,
                "data_points": len(self.training_data)
            }
        
        return {"learning": False, "stealth_score": self.detection_evasion_score}
    
    def humanize_text(self, text: str) -> str:
        """Make text more human-like"""
        if self.detection_evasion_score < 70:
            return text
        
        human_patterns = [
            "Hey there",
            "Hope you're doing well",
            "Quick question",
            "I was wondering"
        ]
        
        if random.random() > 0.5:
            text = text.replace("Dear", "Hi")
            text = text.replace("Sincerely", "Best")
        
        if random.random() > 0.6:
            additions = random.choice(human_patterns)
            text = additions + ", " + text.lower()
        
        return text
    
    def get_best_practice(self, action: str) -> Dict:
        """Get best practice for action"""
        return {
            "action": action,
            "stealth_mode": self.detection_evasion_score > 60,
            "random_delays": True,
            "vary_templates": True,
            "humanize": True
        }

auto_trainer = AutoTrainer()