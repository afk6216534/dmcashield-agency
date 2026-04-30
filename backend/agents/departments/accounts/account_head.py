from typing import Dict
from agents.base_agent import BaseAgent

class AccountHead(BaseAgent):
    def __init__(self):
        super().__init__("AccountHead")

    def manage_account(self, account_id: str) -> Dict:
        return {"account_id": account_id, "status": "managed"}

    def start(self):
        return {"status": "online", "accounts_active": 0}
