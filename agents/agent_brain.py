"""
AgentBrain - Per-Agent Learning and Memory System
Uses ChromaDB vector stores for each department's experiences and learnings.
"""
import chromadb
import json
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional

class AgentBrain:
    def __init__(self, agent_name: str, persist_directory: str = "./data/chroma"):
        """Initialize a ChromaDB client for a specific agent/department."""
        self.agent_name = agent_name
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection for this agent
        self.collection = self.client.get_or_create_collection(
            name=f"agent_{agent_name}_memory",
            metadata={"agent": agent_name, "created": datetime.utcnow().isoformat()}
        )
        
        # Collection for learnings and patterns
        self.learning_collection = self.client.get_or_create_collection(
            name=f"agent_{agent_name}_learnings",
            metadata={"type": "learnings"}
        )

    def store_experience(self, experience_type: str, data: Dict[str, Any], 
                        outcome: str, embedding: Optional[List[float]] = None):
        """Store a single experience (e.g., email sent, lead converted)."""
        metadata = {
            "type": experience_type,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store in collection
        return self.collection.add(
            documents=[json.dumps(data)],
            metadatas=[metadata],
            ids=[f"exp_{datetime.utcnow().timestamp()}"]
        )

    def query_similar_experiences(self, query_text: str, n_results: int = 5):
        """Query for similar past experiences."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def store_learning(self, pattern_type: str, pattern_data: Dict[str, Any], 
                      effectiveness_score: float, category: str = "general"):
        """Store a recognized pattern that leads to success/failure."""
        learning = {
            "type": pattern_type,
            "data": pattern_data,
            "effectiveness": effectiveness_score,
            "category": category,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return self.learning_collection.add(
            documents=[json.dumps(learning)],
            metadatas=[{"type": "learning", "category": category}],
            ids=[f"learn_{datetime.utcnow().timestamp()}"]
        )

    def get_best_patterns(self, category: str, min_effectiveness: float = 0.7):
        """Retrieve the most effective patterns for a category."""
        results = self.learning_collection.get(
            where={"category": category},
            limit=10
        )
        
        # Filter by effectiveness
        patterns = []
        for i, doc in enumerate(results['documents']):
            data = json.loads(doc)
            if data.get('effectiveness', 0) >= min_effectiveness:
                patterns.append(data)
        
        return patterns

    def update_learning_from_feedback(self, original_pattern_id: str, 
                                     feedback_score: float):
        """Update learning effectiveness based on real-world feedback."""
        # Simplified - in practice would update the specific learning entry
        pass

# Global memory system instance
class MemorySystem:
    def __init__(self):
        self.agents = {}
        self.soul_file = self._load_soul()
        self._initialize_all_agents()

    def _load_soul(self) -> Dict[str, Any]:
        """Load or create system soul file."""
        import os
        soul_path = "F:/Anti gravity projects/Dmca company/dmcashield-agency/soul.json"
        
        default_soul = {
            "company_name": "DMCAShield Agency",
            "mission": "Autonomous DMCA review removal",
            "active_since": datetime.utcnow().isoformat(),
            "total_leads_processed": 0,
            "total_emails_sent": 0,
            "total_clients_acquired": 0,
            "learning_cycle": 1,
            "departments": {
                "scraping": {"status": "active"},
                "marketing": {"status": "active"},
                "sales": {"status": "active"},
                # ... all departments
            }
        }
        
        if os.path.exists(soul_path):
            with open(soul_path, 'r') as f:
                return json.load(f)
        else:
            with open(soul_path, 'w') as f:
                json.dump(default_soul, f, indent=2, default=str)
            return default_soul

    def _initialize_all_agents(self):
        """Initialize a separate brain for each department."""
        departments = [
            'ceo', 'scraping', 'validation', 'marketing_intel', 
            'marketing_funnel', 'marketing_copy', 'marketing_qa', 
            'marketing_competitor', 'email_sending', 'tracking', 
            'sales', 'sheets', 'accounts', 'tasks', 'ml', 'jarvis', 'memory'
        ]
        
        for dept in departments:
            self.agents[dept] = AgentBrain(dept)

    def get_agent_brain(self, agent_name: str) -> AgentBrain:
        """Get the brain for a specific agent."""
        return self.agents.get(agent_name)

    def get_soul(self) -> Dict[str, Any]:
        """Get current system soul state."""
        return self.soul_file

    def update_soul(self, updates: Dict[str, Any]):
        """Update system soul with new data."""
        self.soul_file.update(updates)
        self.soul_file['updated_at'] = datetime.utcnow().isoformat()
        
        # Save to file
        with open("F:/Anti gravity projects/Dmca company/dmcashield-agency/soul.json", 'w') as f:
            json.dump(self.soul_file, f, indent=2, default=str)

# Global instance
memory_system = MemorySystem()
