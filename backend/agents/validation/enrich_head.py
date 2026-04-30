import uuid
import json
from datetime import datetime
from typing import Dict, List, Any
import httpx

from agents.memory.message_bus import MessageBus, create_handoff_message
from agents.memory.agent_brain import memory_system

class EnrichHeadAgent:
    def __init__(self):
        self.name = "EnrichHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["ValidatorAgent", "CompetitorSpyAgent", "AudienceAnalystAgent", "StructureBotAgent"]

    def receive_message(self, message):
        if message.message_type == "handoff":
            leads = message.payload.get("leads", [])
            task_id = message.payload.get("task_id")
            self.enrich_leads(leads, task_id)

    def validate_lead(self, lead: Dict) -> Dict:
        validated = lead.copy()
        validated["errors"] = []
        
        if not validated.get("email_primary"):
            validated["errors"].append("Missing primary email")
        elif "@" not in validated.get("email_primary", ""):
            validated["errors"].append("Invalid email format")
            validated["email_primary"] = None
        
        if validated.get("phone"):
            validated["phone"] = ''.join(c for c in validated["phone"] if c.isdigit() or c in ['+', '-', ' ', '(', ')'])
        
        if validated.get("city"):
            validated["city"] = validated["city"].title()
        if validated.get("state"):
            validated["state"] = validated["state"].title()
        if validated.get("business_name"):
            validated["business_name"] = validated["business_name"].strip()
        
        validated["is_valid"] = len(validated["errors"]) == 0
        return validated

    def remove_duplicates(self, leads: List[Dict]) -> List[Dict]:
        seen = set()
        unique_leads = []
        
        for lead in leads:
            key = (lead.get("email_primary", ""), lead.get("business_name", ""))
            if key not in seen and lead.get("email_primary"):
                seen.add(key)
                unique_leads.append(lead)
        
        return unique_leads

    async def find_competitors(self, business_name: str, city: str, state: str, niche: str) -> List[Dict]:
        competitors = []
        try:
            search_query = f"{niche or business_name} {city} {state}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('div', class_='section-result')
                
                for listing in listings[:5]:
                    try:
                        name_elem = listing.find('span', class_='section-result-title')
                        rating_elem = listing.find('span', class_='section-result-rating')
                        
                        if name_elem and business_name not in name_elem.text:
                            competitors.append({
                                "name": name_elem.text.strip(),
                                "rating": float(rating_elem.text.split()[0]) if rating_elem else 0
                            })
                    except:
                        continue
                        
        except Exception as e:
            self.brain.remember(f"Competitor search error: {str(e)}", "error")
        
        return competitors[:5]

    def analyze_audience(self, lead: Dict) -> Dict:
        niche = lead.get("niche", "")
        negative_count = lead.get("negative_review_count", 0)
        rating = lead.get("current_rating", 5.0)
        worst_reviews = lead.get("worst_reviews", [])
        
        pain_points = []
        if rating < 3.0:
            pain_points.append("Bad online reputation costing customers")
        if negative_count > 5:
            pain_points.append("Multiple negative reviews hurting trust")
        if niche == "restaurant":
            pain_points.append("Food service reputation is everything")
        elif niche == "dentist":
            pain_points.append("Trust is critical for dental patients")
        elif niche == "salon":
            pain_points.append("Reviews drive new customer bookings")
        
        emotional_triggers = {
            "fear": "losing more customers due to bad reviews",
            "trust": "100+ businesses trust us to fix their reputation",
            "greed": "imagine 50 more 5-star reviews this month",
            "urgency": "your competitors are already solving this"
        }
        
        send_times = {
            "restaurant": {"days": [1, 2, 3], "hours": [9, 10, 11]},
            "dentist": {"days": [0, 1, 2], "hours": [7, 8, 9]},
            "salon": {"days": [1, 2, 3], "hours": [10, 11, 12]},
            "law": {"days": [0, 1, 2, 3], "hours": [8, 9, 10]},
            "hotel": {"days": [0, 1, 2], "hours": [8, 9, 10]},
            "default": {"days": [1, 2, 3], "hours": [9, 10, 11]}
        }
        
        return {
            "pain_points": pain_points,
            "emotional_triggers": emotional_triggers,
            "send_schedule": send_times.get(niche.lower(), send_times["default"]),
            "recommended_tone": "professional" if niche in ["law", "dentist"] else "friendly",
            "estimated_revenue_impact": negative_count * 500
        }

    def create_master_profile(self, lead: Dict, competitors: List[Dict], audience_data: Dict) -> Dict:
        profile = lead.copy()
        
        profile["competitor_info"] = {
            "competitors": competitors,
            "best_competitor_rating": max([c["rating"] for c in competitors]) if competitors else 5.0,
            "your_rating_gap": 5.0 - lead.get("current_rating", 5.0)
        }
        
        profile["enrichment_data"] = {
            "pain_points": audience_data["pain_points"],
            "emotional_triggers": audience_data["emotional_triggers"],
            "send_schedule": audience_data["send_schedule"],
            "tone": audience_data["recommended_tone"],
            "revenue_impact": audience_data["estimated_revenue_impact"],
            "personalization_hooks": [
                f"Your {lead.get('business_name')} has {lead.get('negative_review_count', 0)} negative reviews",
                f"Competitors like {competitors[0]['name'] if competitors else 'others'} have better ratings"
            ]
        }
        
        profile["status"] = "enriched"
        profile["temperature"] = "warm"
        
        return profile

    async def enrich_leads(self, leads: List[Dict], task_id: str):
        self.brain.remember(f"Enriching {len(leads)} leads for task {task_id}", "enrichment_start")
        
        validated = [self.validate_lead(lead) for lead in leads]
        unique = self.remove_duplicates(validated)
        valid = [l for l in unique if l.get("is_valid")]
        
        enriched_leads = []
        for lead in valid:
            competitors = await self.find_competitors(
                lead.get("business_name", ""),
                lead.get("city", ""),
                lead.get("state", ""),
                lead.get("niche", "")
            )
            
            audience_data = self.analyze_audience(lead)
            profile = self.create_master_profile(lead, competitors, audience_data)
            enriched_leads.append(profile)
        
        from database.models import SessionLocal, Task
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.phase_validation = "complete"
                db.commit()
        finally:
            db.close()
        
        handoff = create_handoff_message(
            from_agent=self.name,
            to_agent="MarketingHead",
            leads=enriched_leads,
            task_id=task_id,
            notes=f"{len(enriched_leads)} leads enriched and ready for marketing"
        )
        self.message_bus.messages.append(handoff)
        self._save_messages()
        
        self.brain.remember(
            f"Enrichment complete: {len(enriched_leads)} leads ready for marketing",
            "enrichment_complete"
        )

    def _save_messages(self):
        self.message_bus._save_messages()

    def start(self):
        return {"status": "online", "team": self.team}

enrich_head = EnrichHeadAgent()