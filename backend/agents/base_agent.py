"""BaseAgent provides minimal common functionality for all agents in the system.
It can be expanded later with messaging, memory, or other shared utilities.
"""

class BaseAgent:
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        # Placeholder for future shared initialization (e.g., MessageBus subscription)

    def start(self):
        return {"status": "online", "agent": self.name}
