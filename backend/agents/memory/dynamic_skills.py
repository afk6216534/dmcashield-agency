"""
DYNAMIC SELF-LEARNING SKILLS SYSTEM
===================================
Skills that:
- Learn from results
- Evolve and improve
- Create new skills dynamically
- Adapt to needs
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from collections import deque
import random
import uuid

class SelfLearningSkill:
    """
    A skill that can learn and evolve
    """
    def __init__(self, skill_id: str, name: str, description: str):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        
        # Core function
        self.function = None
        self.code = ""
        
        # Learning data
        self.usage_history = deque(maxlen=100)
        self.success_rate = 0.5
        self.improvements = []
        
        # Evolution
        self.generation = 1
        self.mutations = []
        
        # Training data
        self.training_data = []
        
    def update_from_result(self, input_data: Any, result: Any, success: bool):
        """Learn from execution result"""
        self.usage_history.append({
            "input": str(input_data)[:100],
            "result": str(result)[:100],
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Calculate new success rate
        recent = list(self.usage_history)[-20:]
        if recent:
            successes = sum(1 for r in recent if r.get("success"))
            self.success_rate = successes / len(recent)
        
        # If failing, mark for improvement
        if not success and len(self.usage_history) > 5:
            self.improvements.append({
                "issue": str(result),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def evolve(self) -> "SelfLearningSkill":
        """Create improved version of skill"""
        new_gen = SelfLearningSkill(
            f"{self.skill_id}_gen{self.generation + 1}",
            self.name,
            self.description + f" (evolved v{self.generation + 1})"
        )
        new_gen.generation = self.generation + 1
        new_gen.success_rate = self.success_rate
        new_gen.training_data = self.training_data[-10:]  # Keep recent data
        
        self.mutations.append({
            "from": self.generation,
            "to": new_gen.generation,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return new_gen
    
    def to_dict(self) -> Dict:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "generation": self.generation,
            "success_rate": self.success_rate,
            "usage_count": len(self.usage_history),
            "improvements": len(self.improvements)
        }

class DynamicSkillRegistry:
    """
    Registry that can create and evolve skills dynamically
    """
    def __init__(self, registry_file: str = "data/dynamic_skills.json"):
        self.registry_file = registry_file
        self.skills = self._load()
        self.skill_templates = self._load_templates()
    
    def _load(self) -> Dict:
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    # Convert back to Skill objects
                    skills = {}
                    for k, v in data.get("skills", {}).items():
                        s = SelfLearningSkill(v["skill_id"], v["name"], v["description"])
                        s.generation = v.get("generation", 1)
                        s.success_rate = v.get("success_rate", 0.5)
                        skills[k] = s
                    return {"skills": skills}
            except:
                pass
        return {"skills": {}}
    
    def _save(self):
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        data = {
            "skills": {k: v.to_dict() for k, v in self.skills.items()}
        }
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_templates(self) -> Dict:
        """Load skill templates that can be evolved"""
        return {
            "lead_scrape": {
                "base_name": "Lead Scraper",
                "description": "Scrape business leads",
                "actions": ["scrape", "enrich", "validate"],
                "success_threshold": 0.7
            },
            "email_campaign": {
                "base_name": "Email Campaign",
                "description": "Send email campaigns",
                "actions": ["compose", "send", "track"],
                "success_threshold": 0.6
            },
            "lead_enrich": {
                "base_name": "Lead Enrichment",
                "description": "Enrich lead data",
                "actions": ["validate", "enrich", "score"],
                "success_threshold": 0.8
            },
            "response_handler": {
                "base_name": "Response Handler",
                "description": "Handle email responses",
                "actions": ["parse", "classify", "respond"],
                "success_threshold": 0.7
            }
        }
    
    def create_skill_from_template(self, template_name: str, customizations: Dict = None) -> str:
        """Create new skill from template"""
        template = self.skill_templates.get(template_name)
        if not template:
            return ""
        
        skill_id = f"skill_{template_name}_{datetime.utcnow().timestamp()}"
        skill = SelfLearningSkill(
            skill_id,
            template["base_name"],
            template["description"]
        )
        
        # Apply customizations
        if customizations:
            skill.name = customizations.get("name", skill.name)
            skill.description = customizations.get("description", skill.description)
        
        self.skills[skill_id] = skill
        self._save()
        
        return skill_id
    
    def create_skill_direct(self, name: str, description: str) -> str:
        """Create skill from scratch"""
        skill_id = f"skill_custom_{uuid.uuid4().hex[:8]}"
        skill = SelfLearningSkill(skill_id, name, description)
        
        self.skills[skill_id] = skill
        self._save()
        
        return skill_id
    
    def evolve_skill(self, skill_id: str) -> Optional[str]:
        """Evolve an existing skill"""
        skill = self.skills.get(skill_id)
        if not skill:
            return None
        
        # Evolve
        new_skill = skill.evolve()
        
        # Add to registry
        self.skills[new_skill.skill_id] = new_skill
        self._save()
        
        return new_skill.skill_id
    
    def record_result(self, skill_id: str, input_data: Any, result: Any, success: bool):
        """Record execution result for learning"""
        skill = self.skills.get(skill_id)
        if skill:
            skill.update_from_result(input_data, result, success)
            self._save()
    
    def get_best_skill(self, category: str = None) -> Optional[SelfLearningSkill]:
        """Get the best performing skill"""
        best = None
        best_rate = 0
        
        for skill in self.skills.values():
            if category and not skill.name.lower().startswith(category.lower()):
                continue
            
            if skill.success_rate > best_rate:
                best = skill
                best_rate = skill.success_rate
        
        return best
    
    def list_skills(self) -> List[Dict]:
        return [s.to_dict() for s in self.skills.values()]
    
    def get_skill(self, skill_id: str) -> Optional[Dict]:
        skill = self.skills.get(skill_id)
        return skill.to_dict() if skill else None

# Initialize
dynamic_skills = DynamicSkillRegistry()

# Create default skills from templates
for template_name in dynamic_skills.skill_templates.keys():
    dynamic_skills.create_skill_from_template(template_name)

# Skill Evolution Automator
class SkillEvolutionAutomator:
    """
    Automatically evolves skills based on performance
    """
    def __init__(self):
        self.evolution_log = []
    
    async def check_and_evolve(self) -> List[Dict]:
        """Check all skills and evolve poor performers"""
        evolutions = []
        
        for skill in dynamic_skills.skills.values():
            # Check if skill needs evolution
            if skill.success_rate < 0.5 and len(skill.usage_history) > 10:
                # Evolve it
                old_gen = skill.generation
                new_id = dynamic_skills.evolve_skill(skill.skill_id)
                
                if new_id:
                    evolutions.append({
                        "skill": skill.name,
                        "old_gen": old_gen,
                        "new_gen": old_gen + 1,
                        "reason": f"Low success rate: {skill.success_rate:.2%}",
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        return evolutions

skill_automator = SkillEvolutionAutomator()

# Auto-Create Skills from Needs
class NeedBasedSkillCreator:
    """
    Creates new skills based on needs
    """
    def __init__(self):
        self.needs = deque(maxlen=50)
    
    def register_need(self, need_description: str):
        """Register a new need"""
        self.needs.append({
            "need": need_description,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def create_skill_for_need(self, need: str) -> str:
        """Create skill to address a need"""
        skill_name = f"_auto_{need.split()[0]}_{uuid.uuid4().hex[:4]}"
        return dynamic_skills.create_skill_direct(
            skill_name,
            f"Auto-created to: {need}"
        )
    
    def get_unaddressed_needs(self) -> List[Dict]:
        """Get needs without skills"""
        # Simple check - in reality would check skill capabilities
        return list(self.needs)

need_based_creator = NeedBasedSkillCreator()