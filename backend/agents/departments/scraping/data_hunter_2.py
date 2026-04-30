import os
import json
from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class DataHunter2(BaseAgent):
    def __init__(self):
        super().__init__("DataHunter2")
        self.message_bus = MessageBus()
        self.sources = ["yelp", "bbb", "angies_list"]

    def hunt(self, niche: str, city: str, limit: int = 50) -> List[Dict]:
        leads = []
        for i in range(min(limit, 10)):
            leads.append({
                "lead_id": f"dh2_{i}",
                "business_name": f"{niche} Pro {i}",
                "niche": niche,
                "city": city,
                "source": "yelp",
                "phone": f"555-02{i:03d}",
                "address": f"{i} Oak Ave",
                "rating": 2.0 + (i % 4) * 0.5,
                "reviews_count": 15 + i * 3
            })
        return leads

    def start(self):
        return {"status": "online", "source": "yelp", "hunting": True}
