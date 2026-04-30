import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str = ''
    to_agent: str = ''
    message_type: str = 'update'
    priority: str = 'normal'
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    read: bool = False

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'from_agent': self.from_agent,
            'to_agent': self.to_agent,
            'message_type': self.message_type,
            'priority': self.priority,
            'payload': self.payload,
            'timestamp': self.timestamp,
            'read': self.read
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentMessage':
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            from_agent=data.get('from_agent', ''),
            to_agent=data.get('to_agent', ''),
            message_type=data.get('message_type', 'update'),
            priority=data.get('priority', 'normal'),
            payload=data.get('payload', {}),
            timestamp=data.get('timestamp', datetime.utcnow().isoformat()),
            read=data.get('read', False)
        )

class MessageBus:
    def __init__(self, db_path: str = "data/message_bus.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.messages: List[AgentMessage] = []
        self.subscribers: Dict[str, callable] = {}
        self._load_messages()

    def _load_messages(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                self.messages = [AgentMessage.from_dict(m) for m in data]
            except Exception:
                self.messages = []

    def _save_messages(self):
        with open(self.db_path, 'w') as f:
            json.dump([m.to_dict() for m in self.messages], f, indent=2)

    def send_message(self, from_agent: str, to_agent: str, message_type: str = "update",
                     priority: str = "normal", payload: Dict[str, Any] = None) -> AgentMessage:
        msg = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            priority=priority,
            payload=payload or {}
        )
        self.messages.append(msg)
        self._save_messages()
        if to_agent in self.subscribers:
            self.subscribers[to_agent](msg)
        return msg

    def get_messages_for(self, agent_name: str, unread_only: bool = False) -> List[AgentMessage]:
        messages = [m for m in self.messages if m.to_agent == agent_name]
        if unread_only:
            messages = [m for m in messages if not m.read]
        return messages

    def mark_read(self, message_id: str):
        for msg in self.messages:
            if msg.id == message_id:
                msg.read = True
                break
        self._save_messages()

    def subscribe(self, agent_name: str, callback):
        self.subscribers[agent_name] = callback

    def broadcast(self, from_agent: str, message_type: str, payload: Dict[str, Any]):
        msg = AgentMessage(
            from_agent=from_agent,
            to_agent="*",
            message_type=message_type,
            payload=payload
        )
        self.messages.append(msg)
        self._save_messages()
        return msg