from typing import Dict, List, Callable
import uuid

class Message:
    def __init__(self, from_agent: str, to_agent: str, message_type: str, payload: Dict):
        self.message_id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.payload = payload
        self.timestamp = __import__('datetime').datetime.utcnow().isoformat() + "Z"

class MessageBus:
    def __init__(self):
        self.messages: List[Message] = []
        self.subscriptions: Dict[str, List[Callable]] = {}

    def subscribe(self, agent_name: str, handler: Callable):
        if agent_name not in self.subscriptions:
            self.subscriptions[agent_name] = []
        self.subscriptions[agent_name].append(handler)

    def publish(self, message: Message):
        self.messages.append(message)
        if message.to_agent in self.subscriptions:
            for handler in self.subscriptions[message.to_agent]:
                handler(message)

    def send_handoff(self, from_agent: str, to_agent: str, payload: Dict, notes: str = ""):
        msg = Message(from_agent, to_agent, "handoff", {
            "payload": payload,
            "notes": notes
        })
        self.publish(msg)
        return msg

    def list_messages(self, agent: str = None) -> List[Dict]:
        if agent:
            return [m.__dict__ for m in self.messages if m.to_agent == agent]
        return [m.__dict__ for m in self.messages]

create_handoff_message = lambda **kwargs: Message(
    from_agent=kwargs.get("from_agent", "unknown"),
    to_agent=kwargs.get("to_agent", "unknown"),
    message_type="handoff",
    payload=kwargs.get("payload", {})
)
