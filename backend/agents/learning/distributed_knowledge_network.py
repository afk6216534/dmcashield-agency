import uuid
from datetime import datetime
from typing import List, Dict, Any

from agents.memory.message_bus import MessageBus

class KnowledgeNetwork:
    """Simple newsletter‑style knowledge distribution system.
    Departments subscribe to topics (e.g., "policy_updates", "tech_trends").
    When new knowledge is added, the network broadcasts a concise summary
    to all subscribed agents via the MessageBus.
    """

    def __init__(self):
        self.message_bus = MessageBus()
        # topic -> set of subscriber agent names
        self.subscriptions: Dict[str, set] = {}
        # Store recent publications for reference
        self.publications: List[Dict[str, Any]] = []

    def subscribe(self, agent_name: str, topic: str):
        """Register an agent to receive updates for a given topic."""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(agent_name)
        print(f"[KnowledgeNetwork] {agent_name} subscribed to {topic}")

    def unsubscribe(self, agent_name: str, topic: str):
        """Remove an agent from a topic subscription list."""
        if topic in self.subscriptions and agent_name in self.subscriptions[topic]:
            self.subscriptions[topic].remove(agent_name)
            print(f"[KnowledgeNetwork] {agent_name} unsubscribed from {topic}")

    def publish(self, topic: str, title: str, summary: str, payload: Dict[str, Any] = None):
        """Publish a new knowledge item.
        The method stores the publication and notifies all subscribed agents.
        """
        publication = {
            "id": f"pub_{uuid.uuid4().hex[:8]}",
            "topic": topic,
            "title": title,
            "summary": summary,
            "payload": payload or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.publications.append(publication)

        # Notify subscribers via MessageBus
        if topic in self.subscriptions:
            for subscriber in self.subscriptions[topic]:
                self.message_bus.send_message(
                    from_agent="knowledge_network",
                    to_agent=subscriber,
                    message_type="knowledge_update",
                    priority="high",
                    payload={
                        "publication_id": publication["id"],
                        "title": title,
                        "summary": summary,
                        "topic": topic,
                        "timestamp": publication["timestamp"]
                    }
                )
        else:
            print(f"[KnowledgeNetwork] No subscribers for topic '{topic}'. Publication stored.")
        return publication["id"]

    def get_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return the most recent publications up to the given limit."""
        return self.publications[-limit:]

# Global instance for the system to use
knowledge_network = KnowledgeNetwork()
