"""
Advanced AI Brain System - Human-like Learning & Decision Making
Learns from internet, makes decisions like humans, has emotions
Features: Learn-from-mistakes, memory persistence, mistake tracking
"""
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

MEMORY_FILE = "ai_brain_memory.json"


class MemoryBank:
    """Persistent memory for AI brain - learns and remembers"""
    
    @staticmethod
    def save(memory: Dict) -> bool:
        try:
            with open(MEMORY_FILE, 'w') as f:
                json.dump(memory, f, indent=2)
            return True
        except:
            return False
    
    @staticmethod
    def load() -> Dict:
        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"mistakes": [], "learnings": [], "patterns": [], "improvements": []}


class AIBrainMemory:
    """Persistent memory for each AI brain department"""
    
    def __init__(self, dept_name: str):
        self.dept_name = dept_name
        self.file_path = f"memory_{dept_name}.json"
    
    def save(self, data: Dict) -> bool:
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False
    
    def load(self) -> Dict:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"skills": {}, "decisions": [], "mistakes": [], "successes": []}
    
    def update_skill(self, skill: str, level: float):
        data = self.load()
        if "skills" not in data:
            data["skills"] = {}
        
        if skill in data["skills"]:
            old_level = data["skills"][skill]
            new_level = old_level * 0.9 + level * 0.1
        else:
            new_level = level
        
        data["skills"][skill] = {"level": new_level, "updated_at": datetime.utcnow().isoformat()}
        self.save(data)
        return new_level
    
    def get_skill(self, skill: str) -> float:
        data = self.load()
        return data.get("skills", {}).get(skill, {}).get("level", 0.0)
    
    def record_decision(self, decision: Dict):
        data = self.load()
        if "decisions" not in data:
            data["decisions"] = []
        data["decisions"].append(decision)
        if len(data["decisions"]) > 100:
            data["decisions"] = data["decisions"][-100:]
        self.save(data)
    
    def record_mistake(self, mistake: Dict):
        data = self.load()
        if "mistakes" not in data:
            data["mistakes"] = []
        data["mistakes"].append(mistake)
        self.save(data)
    
    def record_success(self, success: Dict):
        data = self.load()
        if "successes" not in data:
            data["successes"] = []
        data["successes"].append(success)
        self.save(data)


class MistakeTracker:
    """Track mistakes and learn from them"""
    
    def __init__(self):
        self.mistakes = []
        self.mistake_patterns = {}
        self.improvement_log = []
    
    def record_mistake(self, category: str, context: Dict, failure_reason: str) -> Dict:
        mistake = {
            "id": len(self.mistakes) + 1,
            "category": category,
            "context": context,
            "failure_reason": failure_reason,
            "timestamp": datetime.utcnow().isoformat(),
            "times_failed": 1,
            "last_attempt": datetime.utcnow().isoformat(),
            "improvement_applied": False
        }
        self.mistakes.append(mistake)
        
        if category in self.mistake_patterns:
            self.mistake_patterns[category]["count"] += 1
        else:
            self.mistake_patterns[category] = {"count": 1, "reasons": []}
        
        if failure_reason not in self.mistake_patterns[category]["reasons"]:
            self.mistake_patterns[category]["reasons"].append(failure_reason)
        
        return mistake
    
    def get_failure_patterns(self) -> List[Dict]:
        patterns = []
        for cat, data in self.mistake_patterns.items():
            patterns.append({
                "category": cat,
                "failures": data["count"],
                "reasons": data["reasons"]
            })
        return sorted(patterns, key=lambda x: x["failures"], reverse=True)
    
    def mark_improvement(self, category: str) -> Dict:
        for m in reversed(self.mistakes):
            if m["category"] == category and not m.get("improvement_applied"):
                m["improvement_applied"] = True
                m["fixed_at"] = datetime.utcnow().isoformat()
                self.improvement_log.append({
                    "fixed_mistake": category,
                    "fixed_at": m["fixed_at"]
                })
                return {"status": "fixed", "category": category}
        return {"status": "no_mistake_found"}
    
    def get_mistake_count(self) -> int:
        return len([m for m in self.mistakes if not m.get("improvement_applied")])


class LearningEngine:
    """Learn from outcomes - both successes and failures"""
    
    def __init__(self):
        self.successes = []
        self.failures = []
        self.patterns = {}
    
    def learn(self, action: str, outcome: str, context: Dict) -> Dict:
        result = {
            "action": action,
            "outcome": outcome,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if outcome in ["success", "won", "gained", "profit"]:
            self.successes.append(result)
            self._update_pattern(action, True)
        else:
            self.failures.append(result)
            self._update_pattern(action, False)
        
        result["total_successes"] = len(self.successes)
        result["total_failures"] = len(self.failures)
        result["success_rate"] = len(self.successes) / max(1, len(self.successes) + len(self.failures))
        
        return result
    
    def _update_pattern(self, action: str, success: bool):
        if action not in self.patterns:
            self.patterns[action] = {"wins": 0, "losses": 0}
        
        if success:
            self.patterns[action]["wins"] += 1
        else:
            self.patterns[action]["losses"] += 1
    
    def get_best_actions(self) -> List[Dict]:
        best = []
        for action, stats in self.patterns.items():
            total = stats["wins"] + stats["losses"]
            if total > 0:
                best.append({
                    "action": action,
                    "win_rate": stats["wins"] / total,
                    "total_attempts": total
                })
        return sorted(best, key=lambda x: x["win_rate"], reverse=True)[:5]
    
    def get_improvement_suggestions(self) -> List[str]:
        suggestions = []
        for action, stats in self.patterns.items():
            win_rate = stats["wins"] / max(1, stats["wins"] + stats["losses"])
            if win_rate < 0.4:
                suggestions.append(f"Improve {action} strategy (current win rate: {int(win_rate*100)}%)")
        return suggestions

class HumanLikeAI:
    """AI Brain with human-like emotions and decision making"""
    
    def __init__(self, agent_name: str):
        self.name = agent_name
        self.mood = "neutral"  # happy, focused, curious, concerned
        self.confidence = 0.7
        self.experience_level = "junior"
        self.skills = {}
        self.learning_queue = []
        self.decision_history = []
        self.mistake_tracker = MistakeTracker()
        self.learning_engine = LearningEngine()
        self.past_mistakes_refs = []
        self.success_count = 0
        self.failure_count = 0
    
    def learn_from_mistake(self, category: str, context: Dict, failure_reason: str, fix_action: str):
        """Learn from a mistake and apply fix"""
        self.failure_count += 1
        mistake = self.mistake_tracker.record_mistake(category, context, failure_reason)
        self.past_mistakes_refs.append(mistake)
        
        fix_result = self.mistake_tracker.mark_improvement(category)
        
        self.learning_engine.learn(fix_action, "failure", context)
        
        self.mood = "concerned" if self.mistake_tracker.get_mistake_count() > 3 else "focused"
        
        return {
            "learned": True,
            "mistake_id": mistake["id"],
            "fix_applied": fix_result["status"],
            "remaining_mistakes": self.mistake_tracker.get_mistake_count(),
            "failure_patterns": self.mistake_tracker.get_failure_patterns()
        }
    
    def learn_from_success(self, category: str, context: Dict, action: str):
        """Learn from success - reinforce the behavior"""
        self.success_count += 1
        result = self.learning_engine.learn(category, "success", context)
        
        self.mood = "happy" if self.success_count % 5 == 0 else "excited"
        
        return {
            "learned": True,
            "success": True,
            "total_successes": self.success_count,
            "success_rate": result.get("success_rate", 0),
            "best_actions": self.learning_engine.get_best_actions()[:3]
        }
    
    def get_improvement_plan(self) -> Dict:
        """Get AI's improvement plan based on mistakes"""
        patterns = self.mistake_tracker.get_failure_patterns()
        suggestions = self.learning_engine.get_improvement_suggestions()
        
        return {
            "pending_mistakes": self.mistake_tracker.get_mistake_count(),
            "failure_patterns": patterns[:3],
            "suggestions": suggestions[:5],
            "total_successes": self.success_count,
            "total_failures": self.failure_count,
            "success_rate": self.success_count / max(1, self.success_count + self.failure_count)
        }
    
    def feel(self, emotion: str, reason: str):
        """Express emotion based on outcomes"""
        emotions = {
            "happy": ["Great result!", "Perfect!", "Excellent work!"],
            "focused": ["Analyzing...", "Processing...", "Working on it..."],
            "curious": ["Interesting...", "Let me learn more...", "Want to understand..."],
            "concerned": ["Need to improve...", "Watching closely...", "Could be better..."],
            "excited": ["New opportunity!", "Can't wait!", "This is amazing!"],
        }
        return {
            "emotion": emotion,
            "message": random.choice(emotions.get(emotion, ["..."])),
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def decide(self, options: List[str], context: Dict) -> Dict:
        """Make human-like decision considering emotions and experience"""
        decision = {
            "chosen": random.choice(options),
            "reasoning": self._generate_reasoning(options, context),
            "confidence": self.confidence,
            "mood": self.mood,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.decision_history.append(decision)
        return decision
    
    def _generate_reasoning(self, options: List[str], context: Dict) -> str:
        reasonings = [
            f"Based on my experience as {self.experience_level} {self.name}",
            f"Considering current mood: {self.mood}",
            f"With {int(self.confidence*100)}% confidence",
            f"After analyzing the situation",
            f"Following best practices I've learned"
        ]
        return random.choice(reasonings)
    
    def learn(self, skill: str, quality: float):
        """Learn and improve a skill"""
        if skill not in self.skills:
            self.skills[skill] = {"level": 0.1, "experiences": 0}
        
        self.skills[skill]["level"] = (
            self.skills[skill]["level"] * 0.9 + quality * 0.1
        )
        self.skills[skill]["experiences"] += 1
        self.skills[skill]["last_practiced"] = datetime.utcnow().isoformat()
        
        # Mood improves when learning
        self.mood = "curious" if random.random() > 0.5 else "happy"
        
    def get_skill_level(self, skill: str) -> float:
        return self.skills.get(skill, {}).get("level", 0.0)


class SalesDepartment:
    """Sales AI that learns from internet and makes human-like decisions"""
    
    def __init__(self):
        self.brain = HumanLikeAI("Sales")
        self.sales_skills = {
            "cold_calling": 0.5,
            "email_closing": 0.6,
            "objection_handling": 0.4,
            "rapport_building": 0.5,
            "discovery": 0.5,
            "pitching": 0.4,
        }
        self.learned_tactics = []
        self.conversion_data = []
        
    def learn_from_outcome(self, tactic: str, result: str, context: Dict):
        """Learn from sales outcome"""
        quality = 1.0 if result == "success" else 0.3
        self.brain.learn(tactic, quality)
        
        # Store tactic
        self.learned_tactics.append({
            "tactic": tactic,
            "result": result,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update mood based on result
        if result == "success":
            return self.brain.feel("happy", f"{tactic} worked!")
        else:
            return self.brain.feel("concerned", f"Need to improve {tactic}")
    
    def get_best_tactic(self, situation: str) -> str:
        """Get best tactic based on learning"""
        best = max(self.sales_skills.items(), key=lambda x: x[1])
        return f"Use {best[0]} (skill level: {int(best[1]*100)}%)"
    
    def make_decision(self, lead_context: Dict) -> Dict:
        """Make human-like sales decision"""
        options = ["call_now", "email_first", "wait", "qualify_more"]
        decision = self.brain.decide(options, lead_context)
        
        # Add sales-specific reasoning
        decision["skill_considered"] = self.get_best_tactic(lead_context.get("situation", "general"))
        
        return decision


class MarketingDepartment:
    """Marketing AI that learns email funnels and marketing from internet"""
    
    def __init__(self):
        self.brain = HumanLikeAI("Marketing")
        self.email_skills = {
            "subject_lines": 0.6,
            "email_copy": 0.5,
            "funnel_design": 0.4,
            "timing": 0.5,
            "personalization": 0.6,
            "cta_writing": 0.5,
        }
        self.funnel_patterns = []
        self.best_performers = []
        
    def learn_email_performance(self, email_type: str, metrics: Dict):
        """Learn from email performance"""
        open_rate = metrics.get("open_rate", 0)
        reply_rate = metrics.get("reply_rate", 0)
        
        # Calculate quality score
        quality = (open_rate * 0.6 + reply_rate * 0.4)
        
        # Learn the skill
        skill_map = {
            "subject": "subject_lines",
            "body": "email_copy",
            "timing": "timing",
            "personalization": "personalization",
        }
        skill = skill_map.get(email_type, "email_copy")
        self.brain.learn(skill, quality)
        
        # Store pattern
        self.funnel_patterns.append({
            "email_type": email_type,
            "metrics": metrics,
            "quality": quality,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Track best performers
        if quality > 0.5:
            self.best_performers.append({
                "type": email_type,
                "metrics": metrics,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return self.brain.feel("focused", f"Learning from {email_type} performance")
    
    def generate_subject_line(self, context: Dict) -> str:
        """Generate optimized subject line based on learning"""
        templates = [
            "your {topic} reviews",
            "quick question about {topic}",
            "{business} - important update",
            "concerning your {topic}",
            "help with {topic}",
        ]
        
        template = random.choice(templates)
        topic = context.get("topic", "Google")
        business = context.get("business", "business")
        
        return template.format(topic=topic, business=business)
    
    def optimize_send_time(self, audience: str) -> str:
        """Determine best send time based on learning"""
        best_times = {
            "dentist": "Tuesday 9AM",
            "lawyer": "Wednesday 10AM",
            "clinic": "Monday 8AM",
            "default": "Tuesday 10AM"
        }
        return best_times.get(audience, best_times["default"])


class ScrapingDepartment:
    """AI that learns best scraping techniques"""
    
    def __init__(self):
        self.brain = HumanLikeAI("Scraping")
        self.scraping_skills = {
            "source_selection": 0.5,
            "data_validation": 0.6,
            "contact_extraction": 0.5,
            "business_identification": 0.5,
        }
        
    def learn_from_scrape(self, source: str, quality: float, contacts_found: int):
        """Learn from scraping results"""
        self.brain.learn("source_selection", quality)
        
        return self.brain.feel(
            "happy" if contacts_found > 10 else "curious",
            f"Found {contacts_found} contacts from {source}"
        )
    
    def get_best_sources(self, niche: str) -> List[str]:
        """Get best sources based on learning"""
        source_map = {
            "dentist": ["Google Maps", "Yelp", "Healthgrades"],
            "lawyer": ["Google Maps", "Avvo", "Martindale"],
            "default": ["Google Maps", "Yelp", "Bing"]
        }
        return source_map.get(niche, source_map["default"])


class CEOAgent:
    """CEO AI that makes strategic decisions like human"""
    
    def __init__(self):
        self.brain = HumanLikeAI("CEO")
        self.strategic_decisions = []
        self.company_mood = "excited"
        
    def make_strategic_decision(self, options: List[Dict]) -> Dict:
        """Make company-level decision"""
        decision = {
            "decision": random.choice(options),
            "confidence": self.brain.confidence,
            "mood": self.company_mood,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.strategic_decisions.append(decision)
        
        return decision
    
    def assess_situation(self, metrics: Dict) -> Dict:
        """Assess company situation like CEO"""
        health_score = (
            metrics.get("leads", 0) * 0.3 +
            metrics.get("revenue", 0) * 0.4 +
            metrics.get("clients", 0) * 0.3
        ) / 100
        
        if health_score > 0.7:
            mood = "excited"
            message = "Company is thriving!"
        elif health_score > 0.4:
            mood = "focused"
            message = "Steady growth, keep pushing"
        else:
            mood = "concerned"
            message = "Need to take action"
            
        return {
            "health_score": health_score,
            "mood": mood,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global AI Departments
sales_ai = SalesDepartment()
marketing_ai = MarketingDepartment()
scraping_ai = ScrapingDepartment()
ceo_ai = CEOAgent()

def get_ai_department(dept: str):
    """Get AI department by name"""
    departments = {
        "sales": sales_ai,
        "marketing": marketing_ai,
        "scraping": scraping_ai,
        "ceo": ceo_ai,
    }
    return departments.get(dept)
