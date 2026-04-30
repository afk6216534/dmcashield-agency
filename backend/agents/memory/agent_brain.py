import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import os

# ChromaDB is optional - system works without it
CHROMADB_AVAILABLE = False
chromadb = None

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    pass

class AgentBrain:
    def __init__(self, agent_name: str, persist_dir: str = "data/chromadb"):
        self.agent_name = agent_name
        self.persist_dir = os.path.join(persist_dir, agent_name)
        os.makedirs(self.persist_dir, exist_ok=True)
        
        self.client = None
        self.collection = None
        
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=self.persist_dir)
                self.collection = self.client.get_or_create_collection(
                    name=f"{agent_name}_memory",
                    metadata={"description": f"Memory for {agent_name} agent"}
                )
            except Exception as e:
                print(f"ChromaDB init failed for {agent_name}: {e}")
        
        self.memory_file = os.path.join(self.persist_dir, "memory.json")
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
            except:
                self.memory = {"experiences": [], "learnings": [], "preferences": {}}
        else:
            self.memory = {"experiences": [], "learnings": [], "preferences": {}}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def remember(self, experience: str, outcome: str = "", context: Dict[str, Any] = None):
        entry = {
            "id": str(uuid.uuid4()),
            "experience": experience,
            "outcome": outcome,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.memory["experiences"].append(entry)
        
        if self.collection:
            try:
                self.collection.add(
                    documents=[experience],
                    metadatas=[{"outcome": outcome, "timestamp": entry["timestamp"]}],
                    ids=[entry["id"]]
                )
            except:
                pass
        
        self._save_memory()
        return entry

    def learn(self, lesson: str, category: str = "general"):
        entry = {
            "id": str(uuid.uuid4()),
            "lesson": lesson,
            "category": category,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.memory["learnings"].append(entry)
        self._save_memory()
        return entry

    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        if not self.collection:
            experiences = self.memory["experiences"]
            return experiences[-limit:] if experiences else []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            return results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        except:
            return self.memory["experiences"][-limit:]

    def set_preference(self, key: str, value: Any):
        self.memory["preferences"][key] = value
        self._save_memory()

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self.memory["preferences"].get(key, default)

class MemorySystem:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self.agents: Dict[str, AgentBrain] = {}
        os.makedirs(base_dir, exist_ok=True)
        
        self.soul_file = os.path.join(base_dir, "soul.json")
        self._load_soul()

    def _load_soul(self):
        if os.path.exists(self.soul_file):
            try:
                with open(self.soul_file, 'r') as f:
                    self.soul = json.load(f)
            except:
                self.soul = self._default_soul()
        else:
            self.soul = self._default_soul()
            self._save_soul()

    def _default_soul(self) -> dict:
        return {
            "company_name": "DMCAShield Agency",
            "mission": "Remove negative reviews for businesses through legal DMCA process",
            "active_since": "2026-04-27",
            "total_leads_processed": 0,
            "total_emails_sent": 0,
            "total_clients_acquired": 0,
            "learning_cycle": 1,
            "last_active": None,
            "departments_active": 12,
            "status": "initializing",
            "version": "1.0.0"
        }

    def _save_soul(self):
        self.soul["last_active"] = datetime.utcnow().isoformat()
        with open(self.soul_file, 'w') as f:
            json.dump(self.soul, f, indent=2)

    def get_brain(self, agent_name: str) -> AgentBrain:
        if agent_name not in self.agents:
            self.agents[agent_name] = AgentBrain(agent_name, os.path.join(self.base_dir, "chromadb"))
        return self.agents[agent_name]

    def update_soul(self, key: str, value: Any):
        self.soul[key] = value
        self._save_soul()

    def increment_soul(self, key: str, amount: int = 1):
        if key in self.soul:
            self.soul[key] += amount
        else:
            self.soul[key] = amount
        self._save_soul()

    def get_soul(self) -> dict:
        self.soul["last_active"] = datetime.utcnow().isoformat()
        return self.soul

    def backup_to_github(self, github_token: str, repo_name: str):
        pass

memory_system = MemorySystem()