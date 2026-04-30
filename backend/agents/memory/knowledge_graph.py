import uuid
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

@dataclass
class Entity:
    id: str
    type: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    embeddings: List[float] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass  
class Relationship:
    id: str
    from_entity: str
    to_entity: str
    relation_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class KnowledgeGraph:
    def __init__(self, persist_dir: str = "data/knowledge"):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        self.entities_file = os.path.join(persist_dir, "entities.json")
        self.relations_file = os.path.join(persist_dir, "relations.json")
        
        self._load()
    
    def _load(self):
        if os.path.exists(self.entities_file):
            try:
                with open(self.entities_file, 'r') as f:
                    data = json.load(f)
                    self.entities = [Entity(**e) for e in data]
            except:
                self.entities = []
        else:
            self.entities = []
            
        if os.path.exists(self.relations_file):
            try:
                with open(self.relations_file, 'r') as f:
                    data = json.load(f)
                    self.relations = [Relationship(**r) for r in data]
            except:
                self.relations = []
        else:
            self.relations = []
    
    def _save(self):
        with open(self.entities_file, 'w') as f:
            json.dump([asdict(e) for e in self.entities], f, indent=2)
        with open(self.relations_file, 'w') as f:
            json.dump([asdict(r) for r in self.relations], f, indent=2)
    
    def add_entity(self, entity_type: str, name: str, properties: Dict = None) -> Entity:
        entity = Entity(
            id=f"{entity_type}_{uuid.uuid4().hex[:8]}",
            type=entity_type,
            name=name,
            properties=properties or {}
        )
        self.entities.append(entity)
        self._save()
        return entity
    
    def add_relation(self, from_name: str, to_name: str, relation_type: str, properties: Dict = None) -> Optional[Relationship]:
        from_ent = next((e for e in self.entities if e.name == from_name), None)
        to_ent = next((e for e in self.entities if e.name == to_name), None)
        
        if not from_ent or not to_ent:
            return None
            
        relation = Relationship(
            id=f"rel_{uuid.uuid4().hex[:8]}",
            from_entity=from_ent.id,
            to_entity=to_ent.id,
            relation_type=relation_type,
            properties=properties or {}
        )
        self.relations.append(relation)
        self._save()
        return relation
    
    def find_entities(self, entity_type: str = None, name_contains: str = None) -> List[Entity]:
        results = self.entities
        if entity_type:
            results = [e for e in results if e.type == entity_type]
        if name_contains:
            results = [e for e in results if name_contains.lower() in e.name.lower()]
        return results
    
    def get_connected(self, entity_name: str, relation_type: str = None) -> List[Entity]:
        entity = next((e for e in self.entities if e.name == entity_name), None)
        if not entity:
            return []
        
        related_ids = set()
        for r in self.relations:
            if r.from_entity == entity.id:
                related_ids.add(r.to_entity)
            elif r.to_entity == entity.id:
                related_ids.add(r.from_entity)
        
        results = []
        for e in self.entities:
            if e.id in related_ids:
                if relation_type:
                    rel = next((r for r in self.relations if 
                              (r.from_entity == entity.id and r.to_entity == e.id) or
                              (r.from_entity == e.id and r.to_entity == entity.id) and
                              r.relation_type == relation_type), None)
                    if rel:
                        results.append(e)
                else:
                    results.append(e)
        return results
    
    def get_entity_graph(self, entity_name: str, depth: int = 2) -> Dict:
        entity = next((e for e in self.entities if e.name == entity_name), None)
        if not entity:
            return {}
        
        graph = {
            "center": asdict(entity),
            "connections": []
        }
        
        for r in self.relations:
            if r.from_entity == entity.id:
                target = next((e for e in self.entities if e.id == r.to_entity), None)
                if target:
                    graph["connections"].append({
                        "entity": asdict(target),
                        "relationship": r.relation_type
                    })
            elif r.to_entity == entity.id:
                source = next((e for e in self.entities if e.id == r.from_entity), None)
                if source:
                    graph["connections"].append({
                        "entity": asdict(source),
                        "relationship": r.relation_type
                    })
        return graph
    
    def query(self, question: str) -> Dict:
        keywords = question.lower().split()
        results = {
            "entities": [],
            "relationships": [],
            "answer": ""
        }
        
        for e in self.entities:
            match = any(kw in e.name.lower() or kw in e.type.lower() for kw in keywords)
            if match:
                results["entities"].append(asdict(e))
        
        return results

knowledge_graph = KnowledgeGraph()