import os
import json
from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.memory.message_bus import MessageBus

class DataHunter1(BaseAgent):
    def __init__(self):
        super().__init__("DataHunter1")
        self.message_bus = MessageBus()
        self.sources = ["google_maps", "yelp", "yellowpages"]

    def hunt(self, niche: str, city: str, limit: int = 50) -> List[Dict]:
        leads = []
        for i in range(min(limit, 10)):
            leads.append({
                "lead_id": f"dh1_{i}",
                "business_name": f"{niche} Business {i}",
                "niche": niche,
                "city": city,
                "source": "google_maps",
                "phone": f"555-01{i:03d}",
                "address": f"{i} Main St",
                "rating": 2.5 + (i % 3) * 0.5,
                "reviews_count": 10 + i * 5
            })
        return leads

    def start(self):
        return {"status": "online", "source": "google_maps", "hunting": True}
