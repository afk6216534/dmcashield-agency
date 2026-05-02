import threading
import time
import requests
from bs4 import BeautifulSoup
import uuid
import numpy as np
from datetime import datetime
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse
import logging

from agents.memory.message_bus import MessageBus
from agents.memory.knowledge_graph import KnowledgeGraph, ChromaVectorStore
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)

class KnowledgeEmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

class InternetLearner:
    def __init__(self):
        self.message_bus = MessageBus()
        self.knowledge_graph = KnowledgeGraph()
        self.vector_store = ChromaVectorStore()
        self.embedding_service = KnowledgeEmbeddingService()

        # Configuration ---------------------------------------------------
        self.domain_sources = {
            "policy": [
                "https://www.copyright.gov",
                "https://www.dmca.com/faq"
            ],
            "marketing": [
                "https://marketingprofs.com",
                "https://www.marketingland.com"
            ],
            "email": [
                "https://mailgun.com/blog",
                "https://sendgrid.com/blog"
            ],
            "tech": [
                "https://www.zdnet.com",
                "https://www.techrepublic.com"
            ],
            "devtools": [
                "https://developer.mozilla.org",
                "https://web-scraping-api.com/blog"
            ]
        }
        # ---------------------------------------------------------------

        self.current_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _scrape_content(self, url: str) -> Optional[Dict]:
        headers = {'User-Agent': 'DMCAShield-Learner/1.0'}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract semantic content
            content_parts = []
            for selector in ['title', 'h1', 'h2', 'h2', 'p', 'blockquote']:
                for el in soup.select(selector):
                    text = el.get_text(strip=True)
                    if len(text) > 30:
                        content_parts.append(text)

            if not content_parts:
                return None

            return {
                'metadata': {
                    'title': soup.title.string if soup.title else url,
                    'url': url,
                    'timestamp': datetime.utcnow().isoformat(),
                    'chars': len(response.text)
                },
                'content': ' '.join(content_parts)
            }
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {e}")
            return None

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding vector"""
        try:
            return self.embedding_service.embed_texts([text])[0]
        except Exception as e:
            logging.error(f"Embedding generation failed: {e}")
            return np.zeros(384)

    def _classify_by_department(self, content: str, url: str) -> Set[str]:
        """Determine affected departments based on URL and content"""
        categories = set()
        parsed_url = urlparse(url)

        policy_hosts = ['copyright.gov', 'dmca.com']
        marketing_hosts = ['marketingprofs.com', 'marketingland.com']
        email_hosts = ['mailgun.com', 'sendgrid.com']
        tech_hosts = ['zdnet.com', 'techrepublic.com']
        devtools_hosts = ['developer.mozilla.org', 'web-scraping-api.com']

        if parsed_url.netloc in policy_hosts:
            categories.add('policy')
        elif parsed_url.netloc in marketing_hosts:
            categories.add('marketing')
        elif parsed_url.netloc in email_hosts:
            categories.add('email')
        elif parsed_url.netloc in tech_hosts:
            categories.add('tech')
        elif parsed_url.netloc in devtools_hosts:
            categories.add('devtools')

        return categories

    def _store_knowledge(self, content: str, metadata: Dict, embedding: np.ndarray):
        """Store knowledge in ChromaDB with embedding"""
        try:
            doc_id = str(uuid.uuid4().hex[:12])
            metadata.update({
                'embedding_source': 'internet_learning',
                'learning_timestamp': datetime.utcnow().isoformat(),
                'content_length': len(content)
            })

            self.knowledge_graph.add_knowledge_document(
                content=content,
                metadata=metadata,
                category=self._get_top_level_domain(urlparse(metadata.get('source', '')).netloc)
            )

            # Also store in vector store for fast retrieval
            self.vector_store.add(
                embedding=embedding.tolist(),
                metadata=metadata,
                text=content
            )
            return doc_id
        except Exception as e:
            logging.error(f"Storage failed: {e}")
            return None

    def _trigger_policy_update(self, affected_deps: Set[str], metadata: Dict):
        """Notify departments and JARVIS about policy implications"""
        if not affected_deps:
            return

        payload = {
            'type': 'policy_update',
            'affected_departments': list(affected_deps),
            'triggered_by': metadata.get('source', 'internet_snapshot'),
            'confidence': 0.8,  # Simplified - would come from analysis
            'timestamp': datetime.utcnow().isoformat()
        }

        for dep in affected_deps:
            self.message_bus.broadcast(
                from_agent="internet_learner",
                to_agent=dep,
                message_type="policy_update",
                payload=payload
            }

    def _processing_cycle(self):
        """Execute a single complete learning cycle"""
        logging.info("Starting knowledge collection cycle...")

        for category, urls in self.domain_sources.items():
            for url in urls:
                logging.info(f"Processing URL: {url} (category: {category})")
                page_data = self._scrape_content(url)

                if not page_data:
                    continue

                # Generate embedding
                embedding = self._generate_embedding(page_data['content'])

                # Classify by department
                deps = self._classify_by_department(page_data['content'], url)

                # Store knowledge
                doc_id = self._store_knowledge(
                    page_data['content'],
                    page_data['metadata'],
                    embedding
                )

                # Trigger department notifications
                self._trigger_policy_update(deps, page_data['metadata'])

                logging.info(f"Processed {url} - {len(page_data['content'])} chars, deps: {deps}")

        # Schedule next cycle
        if not self._stop_event.is_set():
            next_run = threading.Timer(
                3600,  # 1 hour
                lambda: threading.Thread(target=self._processing_cycle).start()
            )
            next_run.daemon = True
            next_run.start()

    def start_learning(self):
        """Initialize and start the continuous learning process"""
        logging.info("Initializing Internet Learner...")
        self.knowledge_graph._get_embedding("warmup")  # Test embedding
        self.vector_store._initialize_default_collection()
        self._processing_cycle()
        logging.info("Internet Learner started successfully")

    def stop_learning(self):
        """Gracefully stop the learning loop"""
        logging.info("Shutting down Internet Learner...")
        self._stop_event.set()
        if self.current_thread:
            self.current_thread.join(timeout=5)
        logging.info("Internet Learner stopped")

class AIPolicyAnalyst:
    """AI policy analysis engine that monitors knowledge updates"""
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.kg = knowledge_graph
        self.message_bus = MessageBus()
        self.policy_rules = {
            'policy': ['dmca', 'copyright', 'trademark'],
            'marketing': ['advertisement', 'endorsement'],
            'email': ['spam', 'compliance', 'unsubscribe']
        }

    def check_for_updates(self):
        """Check knowledge graph for new policy-relevant documents"""
        # Get recent documents
        recent = self.kg.semantic_search(
            "policy update OR DMCA update OR compliance change",
            n_results=5,
            filter_dict={"category": {"$in": ["policy", "legal", "regulatory"]}}
        )

        if not recent.get('documents'):
            return

        # For each relevant document, analyze impact
        for doc_id, content in zip(
            recent.get('ids', []),
            recent.get('documents', [])
        ):
            # Analyze and notify
            affected_deps = self._analyze_content_impact(content)
            if affected_deps:
                payload = {
                    'policy_update': content[:200],
                    'affected_departments': list(affected_deps),
                    'source_document_id': doc_id
                }
                self.message_bus.broadcast(
                    'learning',
                    'policy_update_detected',
                    payload
                )

    def _analyze_content_impact(self, content: str) -> Set[str]:
        """Simple keyword-based impact analysis"""
        policy_deps = set()
        lowercase = content.lower()

        if any(word in lowercase for word in self.policy_rules['policy']):
            affected = {'policy', 'legal', 'validation'}
        elif any(word in lowercase for word in self.policy_rules['marketing']):
            affected = {'marketing', 'email_sending'}
        elif any(word in lowercase for word in self.policy_rules['email']):
            affected = {'email_sending', 'accounts'}
        else:
            affected = set()

        return affected