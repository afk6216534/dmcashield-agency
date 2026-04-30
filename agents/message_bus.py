"""
MessageBus - Inter-Department Communication System
Handles JSON-based messages between all 12 departments.
"""
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import redis

class MessageBus:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.channels = {
            'scraping': 'channel:scraping',
            'validation': 'channel:validation',
            'marketing': 'channel:marketing',
            'email_sending': 'channel:email_sending',
            'tracking': 'channel:tracking',
            'sales': 'channel:sales',
            'sheets': 'channel:sheets',
            'accounts': 'channel:accounts',
            'tasks': 'channel:tasks',
            'ml': 'channel:ml',
            'jarvis': 'channel:jarvis',
            'memory': 'channel:memory'
        }

    def send_message(self, from_agent: str, to_agent: str, message_type: str, 
                   payload: Dict[str, Any], priority: str = 'normal'):
        """Send a message from one agent to another."""
        message = {
            'message_id': f'msg-{uuid.uuid4().hex[:8]}',
            'from_agent': from_agent,
            'to_agent': to_agent,
            'message_type': message_type,
            'priority': priority,
            'payload': payload,
            'timestamp': datetime.utcnow().isoformat(),
            'read': False
        }
        
        # Store in Redis for persistence
        self.redis_client.rpush(self.channels[to_agent], json.dumps(message))
        self.redis_client.set(f"last_message:{to_agent}", json.dumps(message))
        
        # Also store in global message log
        self.redis_client.rpush('channel:global', json.dumps(message))
        
        return message['message_id']

    def get_messages(self, agent_name: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Retrieve messages for a specific agent."""
        messages_data = self.redis_client.lrange(self.channels[agent_name], 0, -1)
        messages = [json.loads(msg) for msg in messages_data]
        
        if unread_only:
            messages = [m for m in messages if not m['read']]
        
        # Mark as read when retrieved
        if messages:
            self.redis_client.delete(self.channels[agent_name])
        
        return messages

    def broadcast(self, from_agent: str, message_type: str, payload: Dict[str, Any], 
                  priority: str = 'normal'):
        """Send a message to all departments."""
        message_ids = []
        for channel in self.channels.keys():
            if channel != f"channel:{from_agent}":
                agent_name = channel.split(':')[1]
                msg_id = self.send_message(from_agent, agent_name, message_type, 
                                          payload, priority)
                message_ids.append(msg_id)
        return message_ids

    def create_handoff_message(self, from_agent: str, to_agent: str, 
                              payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured handoff message between departments."""
        return self.send_message(from_agent, to_agent, 'handoff', payload, 'high')

    def create_alert_message(self, agent_name: str, alert_type: str, 
                           details: Dict[str, Any]) -> Dict[str, Any]:
        """Create an urgent alert message."""
        return self.send_message('System', agent_name, 'alert', 
                               {'type': alert_type, 'details': details}, 'urgent')
