import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from .learning_persistence import SQLiteMemoryBank, SQLiteMistakeTracker, SQLiteLearningEngine

MEMORY_FILE = "ai_brain_memory.json"


class MemoryBank:
    @staticmethod
    def save(memory: Dict) -> bool:
        return SQLiteMemoryBank("default").save(memory)

    @staticmethod
    def load() -> Dict:
        return SQLiteMemoryBank("default").load()


class AIBrainMemory:
    def __init__(self, dept_name: str):
        self.dept_name = dept_name
        self.db = SQLiteMemoryBank(f"brain_{dept_name}")

    def save(self, data: Dict) -> bool:
        return self.db.save(data)

    def load(self) -> Dict:
        return self.db.load()

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
    def __init__(self):
        self.db = SQLiteMistakeTracker()
        self._local_mistakes = []
        self._local_patterns = {}

    def record_mistake(self, category: str, context: Dict, failure_reason: str) -> Dict:
        result = self.db.record_mistake(category, context, failure_reason)
        self._local_mistakes.append(result)
        if category not in self._local_patterns:
            self._local_patterns[category] = {"count": 0, "reasons": []}
        self._local_patterns[category]["count"] += 1
        if failure_reason not in self._local_patterns[category]["reasons"]:
            self._local_patterns[category]["reasons"].append(failure_reason)
        return result

    def get_failure_patterns(self) -> List[Dict]:
        return self.db.get_failure_patterns()

    def mark_improvement(self, category: str) -> Dict:
        return self.db.mark_improvement(category)

    def mark_fixed_by_id(self, mistake_id: int) -> Dict:
        return self.db.mark_fixed_by_id(mistake_id)

    def get_mistake_count(self) -> int:
        return self.db.get_mistake_count()


class LearningEngine:
    def __init__(self):
        self.db = SQLiteLearningEngine()
        self._local_successes = []
        self._local_failures = []
        self._local_patterns = {}

    def learn(self, action: str, outcome: str, context: Dict) -> Dict:
        result = self.db.learn(action, outcome, context)
        if outcome in ["success", "won", "gained", "profit"]:
            self._local_successes.append(result)
            self._local_patterns[action] = {"wins": self._local_patterns.get(action, {"wins": 0, "losses": 0})["wins"] + 1,
                                             "losses": self._local_patterns.get(action, {"wins": 0, "losses": 0})["losses"]}
        else:
            self._local_failures.append(result)
            self._local_patterns[action] = {"wins": self._local_patterns.get(action, {"wins": 0, "losses": 0})["wins"],
                                             "losses": self._local_patterns.get(action, {"wins": 0, "losses": 0})["losses"] + 1}
        return result

    def get_best_actions(self) -> List[Dict]:
        return self.db.get_best_actions()

    def get_improvement_suggestions(self) -> List[str]:
        return self.db.get_improvement_suggestions()


class KnowledgeBaseQuery:
    _kb_data = None

    @classmethod
    def init(cls, kb_dict: Dict = None):
        if kb_dict:
            cls._kb_data = kb_dict

    @classmethod
    def query(cls, query: str) -> List[str]:
        if not cls._kb_data:
            return []
        q = query.lower()
        results = []

        sources = cls._kb_data.get("sources", {})
        for key, src in sources.items():
            if q in key.lower() or q in src.get("repo", "").lower():
                results.append(f"[{key}] {src['repo']}: {src.get('status', 'available')}")

        cold_email = cls._kb_data.get("cold_email_knowledge", {})
        for p in cold_email.get("principles", []):
            if q in p.lower():
                results.append(f"[cold_email] {p}")

        psychology = cls._kb_data.get("psychology_knowledge", {})
        for pp in psychology.get("persuasion_principles", []):
            if q in pp["name"].lower() or q in pp["rule"].lower():
                results.append(f"[psychology] {pp['name']}: {pp['rule']}")

        lead_magnets = cls._kb_data.get("lead_magnet_knowledge", {})
        for lm in lead_magnets.get("dmca_lead_magnets", []):
            if q in lm["name"].lower():
                results.append(f"[lead_magnet] {lm['name']} ({lm['conversion']})")

        return results[:5]

    @classmethod
    def get_context_for_decision(cls, options: List[str], context: Dict) -> str:
        context_str = " ".join(context.get(k, "") for k in context if isinstance(context[k], str))
        context_str += " " + " ".join(options)
        return context_str


def caveman_compress(text: str, mode: str = "lite") -> str:
    if not text:
        return text
    if mode == "ultra":
        lines = text.strip().split("\n")
        compressed = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("I'm") or line.startswith("Let me") or line.startswith("Here's"):
                continue
            line = line.replace("Here is ", "").replace("Here are ", "").replace("I think ", "")
            line = line.replace("Based on my experience", "Per exp")
            line = line.replace("Considering current", "Per")
            line = line.replace("After analyzing", "Post-analyze")
            line = line.replace("Following best practices", "Per best practice")
            if len(line) > 200:
                line = line[:197] + "..."
            compressed.append(line)
        return "\n".join(compressed)
    elif mode == "medium":
        lines = text.strip().split("\n")
        compressed = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line.replace("Based on my experience as", "Per")
            line = line.replace("Considering current mood", "Mood")
            line = line.replace("After analyzing the situation", "Analyzed")
            if len(line) > 300:
                line = line[:297] + "..."
            compressed.append(line)
        return "\n".join(compressed)
    else:
        if len(text) > 500:
            text = text[:497] + "..."
        return text


class HumanLikeAI:
    def __init__(self, agent_name: str):
        self.name = agent_name
        self.mood = "neutral"
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
        kb_insights = KnowledgeBaseQuery.query(
            KnowledgeBaseQuery.get_context_for_decision(options, context)
        )

        best_actions = self.learning_engine.get_best_actions()
        chosen = random.choice(options)

        if best_actions:
            top_action = best_actions[0]["action"]
            action_opts = [o for o in options if top_action in o.lower()]
            if action_opts:
                chosen = action_opts[0]

        kb_context = ""
        if kb_insights:
            kb_context = f"KB says: {kb_insights[0]}"

        decision = {
            "chosen": chosen,
            "reasoning": self._generate_reasoning(options, context),
            "confidence": self.confidence,
            "mood": self.mood,
            "kb_used": len(kb_insights) > 0,
            "kb_insights": kb_insights[:2] if kb_insights else [],
            "timestamp": datetime.utcnow().isoformat()
        }
        self.decision_history.append(decision)
        return decision

    def _generate_reasoning(self, options: List[str], context: Dict) -> str:
        kb_insights = KnowledgeBaseQuery.query(
            KnowledgeBaseQuery.get_context_for_decision(options, context)
        )
        if kb_insights:
            return f"Per KB + {self.experience_level} {self.name}: {kb_insights[0][:80]}"
        reasonings = [
            f"Per {self.experience_level} {self.name} exp",
            f"Mood: {self.mood}",
            f"{int(self.confidence*100)}% confidence",
            "Analyzed situation",
            "Per best practices"
        ]
        return random.choice(reasonings)

    def learn(self, skill: str, quality: float):
        if skill not in self.skills:
            self.skills[skill] = {"level": 0.1, "experiences": 0}
        self.skills[skill]["level"] = (
            self.skills[skill]["level"] * 0.9 + quality * 0.1
        )
        self.skills[skill]["experiences"] += 1
        self.skills[skill]["last_practiced"] = datetime.utcnow().isoformat()
        self.mood = "curious" if random.random() > 0.5 else "happy"

    def get_skill_level(self, skill: str) -> float:
        return self.skills.get(skill, {}).get("level", 0.0)


class SalesDepartment:
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
        quality = 1.0 if result == "success" else 0.3
        self.brain.learn(tactic, quality)
        self.learned_tactics.append({
            "tactic": tactic,
            "result": result,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        if result == "success":
            return self.brain.feel("happy", f"{tactic} worked!")
        else:
            return self.brain.feel("concerned", f"Need to improve {tactic}")

    def get_best_tactic(self, situation: str) -> str:
        best = max(self.sales_skills.items(), key=lambda x: x[1])
        return f"Use {best[0]} (skill level: {int(best[1]*100)}%)"

    def make_decision(self, lead_context: Dict) -> Dict:
        options = ["call_now", "email_first", "wait", "qualify_more"]
        decision = self.brain.decide(options, lead_context)
        decision["skill_considered"] = self.get_best_tactic(lead_context.get("situation", "general"))
        return decision


class MarketingDepartment:
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
        open_rate = metrics.get("open_rate", 0)
        reply_rate = metrics.get("reply_rate", 0)
        quality = (open_rate * 0.6 + reply_rate * 0.4)
        skill_map = {
            "subject": "subject_lines",
            "body": "email_copy",
            "timing": "timing",
            "personalization": "personalization",
        }
        skill = skill_map.get(email_type, "email_copy")
        self.brain.learn(skill, quality)
        self.funnel_patterns.append({
            "email_type": email_type,
            "metrics": metrics,
            "quality": quality,
            "timestamp": datetime.utcnow().isoformat()
        })
        if quality > 0.5:
            self.best_performers.append({
                "type": email_type,
                "metrics": metrics,
                "timestamp": datetime.utcnow().isoformat()
            })
        return self.brain.feel("focused", f"Learning from {email_type} performance")

    def generate_subject_line(self, context: Dict) -> str:
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
        best_times = {
            "dentist": "Tuesday 9AM",
            "lawyer": "Wednesday 10AM",
            "clinic": "Monday 8AM",
            "default": "Tuesday 10AM"
        }
        return best_times.get(audience, best_times["default"])


class ScrapingDepartment:
    def __init__(self):
        self.brain = HumanLikeAI("Scraping")
        self.scraping_skills = {
            "source_selection": 0.5,
            "data_validation": 0.6,
            "contact_extraction": 0.5,
            "business_identification": 0.5,
        }

    def learn_from_scrape(self, source: str, quality: float, contacts_found: int):
        self.brain.learn("source_selection", quality)
        return self.brain.feel(
            "happy" if contacts_found > 10 else "curious",
            f"Found {contacts_found} contacts from {source}"
        )

    def get_best_sources(self, niche: str) -> List[str]:
        source_map = {
            "dentist": ["Google Maps", "Yelp", "Healthgrades"],
            "lawyer": ["Google Maps", "Avvo", "Martindale"],
            "default": ["Google Maps", "Yelp", "Bing"]
        }
        return source_map.get(niche, source_map["default"])


class CEOAgent:
    def __init__(self):
        self.brain = HumanLikeAI("CEO")
        self.strategic_decisions = []
        self.company_mood = "excited"

    def make_strategic_decision(self, options: List[Dict]) -> Dict:
        decision = {
            "decision": random.choice(options),
            "confidence": self.brain.confidence,
            "mood": self.company_mood,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.strategic_decisions.append(decision)
        return decision

    def assess_situation(self, metrics: Dict) -> Dict:
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


sales_ai = SalesDepartment()
marketing_ai = MarketingDepartment()
scraping_ai = ScrapingDepartment()
ceo_ai = CEOAgent()

def get_ai_department(dept: str):
    departments = {
        "sales": sales_ai,
        "marketing": marketing_ai,
        "scraping": scraping_ai,
        "ceo": ceo_ai,
    }
    return departments.get(dept)
