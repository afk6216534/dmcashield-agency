import os
import json
from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class DataHunter3(BaseAgent):
    def __init__(self):
        super().__init__("DataHunter3")
        self.message_bus = MessageBus()
        self.sources = ["linkedin", "facebook", "nextdoor"]

    def hunt(self, niche: str, city: str, limit: int = 50) -> List[Dict]:
        leads = []
        for i in range(min(limit, 10)):
            leads.append({
                "lead_id": f"dh3_{i}",
                "business_name": f"{niche} Experts {i}",
                "niche": niche,
                "city": city,
                "source": "facebook",
                "phone": f"555-03{i:03d}",
                "address": f"{i} Pine Rd",
                "rating": 1.8 + (i % 5) * 0.4,
                "reviews_count": 20 + i * 4
            })
        return leads

    def start(self):
        return {"status": "online", "source": "facebook", "hunting": True}
