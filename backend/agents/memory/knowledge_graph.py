import uuid
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from sentence_transformers import SentenceTransformer
import numpy as np
from chromadb import Client
from chromadb.config import Settings

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

class ChromaVectorStore:
    def __init__(self, path: str = "backend/agents/memory/chroma_db"):
        self.path = path
        self.client = Client(Settings(anonymized_telemetry=False))
        self.default_collection = None
        self._initialize_default_collection()

    def _initialize_default_collection(self):
        try:
            self.default_collection = self.client.get_collection("dmcashield_knowledge")
        except:
            self.default_collection = self.client.create_collection("dmcashield_knowledge")

    def get_collection(self, name: str):
        try:
            return self.client.get_collection(name=name)
        except:
            return self.client.create_collection(name=name)

    def add(self, embedding: List[float], metadata: Dict[str, Any], text: str, id: str = None):
        """Add document with embedding to ChromaDB"""
        doc_id = id or str(uuid.uuid4().hex[:12])
        try:
            self.default_collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata]
            )
            return doc_id
        except Exception as e:
            print(f"[Warning] Could not add to ChromaDB: {e}")
            return None

class KnowledgeGraph:
    def __init__(self, persist_dir: str = "data/knowledge"):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self.entities_file = os.path.join(persist_dir, "entities.json")
        self.relations_file = os.path.join(persist_dir, "relations.json")

        # Initialize ChromaDB for vector search
        self.vector_store = ChromaVectorStore()
        self.knowledge_collection = self.vector_store.get_collection("dmcashield_knowledge")

        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[Warning] Could not load embedding model: {e}")
            self.embedding_model = None

        self._load()

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text if model available"""
        if self.embedding_model:
            emb = self.embedding_model.encode([text])
            return emb[0].tolist()
        return [0.0] * 384

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
        os.makedirs(self.persist_dir, exist_ok=True)
        with open(self.entities_file, 'w') as f:
            json.dump([asdict(e) for e in self.entities], f, indent=2)
        with open(self.relations_file, 'w') as f:
            json.dump([asdict(r) for r in self.relations], f, indent=2)

    def add_entity(self, entity_type: str, name: str, properties: Dict = None, embedding: List[float] = None) -> Entity:
        entity = Entity(
            id=f"{entity_type}_{uuid.uuid4().hex[:8]}",
            type=entity_type,
            name=name,
            properties=properties or {}
        )
        self.entities.append(entity)
        self._save()
        return entity

    def add_relation(self, from_entity: Union[str, Entity], to_entity: Union[str, Entity], relation_type: str, properties: Dict = None) -> Optional[Relationship]:
        from_id = from_entity if isinstance(from_entity, str) else from_entity.id
        to_id = to_entity if isinstance(to_entity, str) else to_entity.id

        from_ent = next((e for e in self.entities if e.id == from_id), None)
        to_ent = next((e for e in self.entities if e.id == to_id), None)

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

    def add_knowledge_document(self, content: str, metadata: Dict = None, category: str = None) -> Dict:
        """Add a knowledge document with semantic embeddings"""
        doc_id = str(uuid.uuid4().hex[:12])

        # Generate embedding
        embedding = self._get_embedding(content)

        metadata = metadata or {}
        metadata.update({
            'category': category or 'general',
            'created_at': datetime.utcnow().isoformat(),
            'source': 'internet_learning',
            'content_length': len(content)
        })

        # Store in ChromaDB
        try:
            self.knowledge_collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata]
            )
        except Exception as e:
            print(f"[Warning] Could not store in ChromaDB: {e}")

        # Store in JSON as fallback
        entity = self.add_entity(
            entity_type='knowledge_document',
            name=doc_id,
            properties={
                'category': category,
                'metadata': metadata,
                'content': content[:500],  # Store a preview
                'has_embedding': len(embedding) > 0,
                'embedding': embedding
            }
        )

        return {
            'id': doc_id,
            'entity_id': entity.id,
            'category': category,
            'created_at': datetime.utcnow().isoformat()
        }

    def semantic_search(self, query: str, n_results: int = 5, filter_dict: Dict = None) -> Dict:
        """Perform semantic search on knowledge documents"""
        query_embedding = self._get_embedding(query)

        # Try ChromaDB first
        try:
            results = self.knowledge_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_dict
            )

            if results and results.get('documents'):
                return {
                    'documents': results['documents'][0],
                    'metadatas': results['metadatas'][0] if results.get('metadatas') else [],
                    'ids': results['ids'][0] if results.get('ids') else [],
                    'source': 'chromadb'
                }
        except Exception as e:
            print(f"[Warning] ChromaDB query failed: {e}")

        # Fallback: keyword search on entities
        keywords = query.lower().split()
        fallback_results = []
        for entity in self.entities:
            if entity.type != 'knowledge_document':
                continue
            for kw in keywords:
                if kw in entity.name.lower() or kw in str(entity.properties).lower():
                    fallback_results.append({
                        'content': entity.properties.get('content', ''),
                        'metadata': entity.properties.get('metadata', {}),
                        'category': entity.properties.get('category', 'general')
                    })
                    break

        return {
            'documents': [r['content'] for r in fallback_results[:n_results]],
            'metadatas': [r['metadata'] for r in fallback_results[:n_results]],
            'ids': [entity.id for entity in self.entities[:n_results] if entity.type == 'knowledge_document'],
            'source': 'fallback'
        }

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
                              ((r.from_entity == entity.id and r.to_entity == e.id) or
                               (r.from_entity == e.id and r.to_entity == entity.id)) and
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

    def query(self, question: str, use_semantic: bool = True) -> Dict:
        if use_semantic and self.embedding_model:
            search_results = self.semantic_search(question)
        else:
            keywords = question.lower().split()
            search_results = {
                'entities': [],
                'relationships': [],
                'answer': ""
            }
            for e in self.entities:
                match = any(kw in e.name.lower() or kw in e.type.lower() for kw in keywords)
                if match:
                    search_results['entities'].append(asdict(e))

        return search_results

knowledge_graph = KnowledgeGraph()

# Global vector store instance for internet learning
vector_store = ChromaVectorStore()