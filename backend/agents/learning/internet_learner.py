import threading
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

import threading
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from agents.memory.message_bus import MessageBus
from agents.memory.knowledge_graph import knowledge_graph
from agents.memory.knowledge_graph import ChromaVectorStore

class KnowledgeEmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

class InternetLearner:
    def __init__(self):
        self.message_bus = MessageBus()
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
        self.vector_store = ChromaVectorStore()
        self.embedding_service = KnowledgeEmbeddingService()

    def _scrape_content(self, url: str) -> Optional[dict]:
        headers = {'User-Agent': 'DMCAShield-Learner/1.0'}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract semantic content
            content_elements = []
            for selector in ['title', 'h1', 'h2', 'p']:
                for el in soup.select(selector):
                    text = el.get_text(strip=True)
                    if len(text) > 30:
                        content_elements.append(text)

            if not content_elements:
                return None

            full_content = ' '.join(content_elements)
            return {
                'metadata': {
                    'title': soup.title.string if soup.title else url,
                    'url': url,
                    'timestamp': datetime.utcnow().isoformat()
                },
                'content': full_content
            }
        except Exception as e:
            print(f"[Warning] Failed to scrape {url}: {e}")
            return None

    def _embed_and_store(self, content: str, metadata: dict):
        """Store text with embeddings using ChromaDB"""
        query_emb = self.embedding_service.embed_texts([content])
        self.vector_store.add(
            embedding=query_emb.tolist()[0].tolist(),
            metadata=metadata,
            text=content
        )

    def _classify_by_department(self, content: str, url: str) -> Set[str]:
        """Determine which department this knowledge affects"""
        categories = set()
        parsed_url = urlparse(url)

        # Policy department mapping
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

    def _launch_ml_retraining(self, affected_departments: Set[str]):
        """Trigger targeted model retraining based on knowledge impact"""
        if not affected_departments:
            return False

        # Trigger targeted retraining
        msg = {
            'type': 'model_retrain',
            'departments': list(affected_departments),
            'triggered_at': datetime.utcnow().isoformat()
        }
        self.message_bus.broadcast('learning', 'model_update', msg)
        return True

    def _processing_cycle(self):
        """Execute a single learning cycle"""
        print("[InternetLearner] Starting processing cycle...")

        for dept, urls in self.domain_sources.items():
            for url in urls:
                page_data = self._scrape_content(url)
                if not page_data:
                    continue

                # Store knowledge
                import uuid
                doc_id = f"{dept}_{uuid.uuid4().hex[:8]}"
                metadata = page_data['metadata'].copy()
                analysis = self._classify_by_department(
                    page_data['content'], url
                )

                # Add semantic metadata
                metadata.update({
                    'category': dept,
                    'embedding_source': 'internet_learning',
                    'processing_timestamp': datetime.utcnow().isoformat()
                })

                self._embed_and_store(page_data['content'], metadata)

                # Trigger targeted department updates
                self._launch_ml_retraining(analysis)

        # Schedule next cycle
        threading.Timer(
            3600,
            lambda: threading.Thread(target=self._processing_cycle).start()
        ).start()

    def start_learning(self):
        """Initialize and start the learning process"""
        print("[InternetLearner] Initializing knowledge graph store...")
        self.vector_store = ChromaVectorStore()
        self._processing_cycle()

    def shutdown(self):
        """Gracefully stop the learning process"""
        print("[InternetLearner] Shutdown initiated")

    def __init__(self, sources: List[str] = None, interval_seconds: int = 3600):
        self.sources = sources or [
            "https://www.copyright.gov/",  # Example policy source
            "https://www.dmca.com/faq",   # DMCA FAQ
        ]
        self.interval_seconds = interval_seconds
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        """Start the background learning loop."""
        if not self._thread.is_alive():
            self._thread.start()
            print("[InternetLearner] Started background learning thread")

    def stop(self):
        """Stop the background learning loop."""
        self._stop_event.set()
        self._thread.join(timeout=5)
        print("[InternetLearner] Stopped background learning thread")

    def _run(self):
        while not self._stop_event.is_set():
            try:
                self._fetch_and_process()
            except Exception as e:
                print(f"[InternetLearner] Error during fetch: {e}")
            # Wait for interval or stop signal
            self._stop_event.wait(self.interval_seconds)

    def _fetch_and_process(self):
        """Fetch each source, extract meaningful text, store it, and trigger ML updates."""
        for url in self.sources:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                # Extract visible text
                texts = soup.stripped_strings
                content = " ".join(texts)
                if content:
                    store_in_knowledge_graph(content, url)
            except Exception as e:
                print(f"[InternetLearner] Failed to fetch {url}: {e}")
        # After processing all sources, signal ML retraining
        trigger_ml_retraining()
