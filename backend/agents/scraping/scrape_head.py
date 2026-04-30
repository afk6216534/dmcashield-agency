import uuid
import json
from datetime import datetime
from typing import Dict, List, Any
import httpx
import asyncio
from bs4 import BeautifulSoup

from agents.memory.message_bus import MessageBus, create_handoff_message
from agents.memory.agent_brain import memory_system

class ScrapeHeadAgent:
    def __init__(self):
        self.name = "ScrapeHead"
        self.message_bus = MessageBus()
        self.brain = memory_system.get_brain(self.name)
        self.message_bus.subscribe(self.name, self.receive_message)
        self.team = ["DataHunter1", "DataHunter2", "DataHunter3", "VerifierAgent"]

    def receive_message(self, message):
        if message.message_type == "instruction" and message.payload.get("action") == "start_task":
            task_id = message.payload.get("task_id")
            self.process_task(task_id)

    async def scrape_google_maps(self, business_type: str, city: str, state: str, country: str) -> List[Dict]:
        results = []
        try:
            search_query = f"{business_type} {city} {state} {country}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('div', class_='section-result')
                
                for listing in listings[:20]:
                    try:
                        name_elem = listing.find('span', class_='section-result-title')
                        rating_elem = listing.find('span', class_='section-result-rating')
                        reviews_elem = listing.find('span', class_='section-result-review-count')
                        address_elem = listing.find('span', class_='section-result-location')
                        
                        if name_elem:
                            results.append({
                                "business_name": name_elem.text.strip(),
                                "current_rating": float(rating_elem.text.strip().replace('(', '').replace(')', '').split()[0]) if rating_elem else 0,
                                "reviews_count": int(reviews_elem.text.strip().replace('(', '').replace(')', '').split()[0]) if reviews_elem else 0,
                                "address": address_elem.text.strip() if address_elem else "",
                                "scraped_source": "google_maps"
                            })
                    except Exception as e:
                        continue
                        
        except Exception as e:
            self.brain.remember(f"Google Maps scrape error: {str(e)}", "error")
        
        return results

    async def find_email_from_website(self, website: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(website)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    if 'mailto:' in href:
                        return href.replace('mailto:', '')
                    text = link.get_text().lower()
                    if any(c in text for c in ['contact', 'email', 'reach', 'info']) and '@' in text:
                        email = text.split('@')[0].split()[-1] + '@' + text.split('@')[-1].split()[0]
                        if '.' in email.split('@')[-1]:
                            return email
                            
        except Exception:
            pass
        return ""

    async def find_email_via_hunter(self, name: str, domain: str, api_key: str = None) -> str:
        if not api_key:
            return ""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://api.hunter.io/v2/domain-search",
                    params={"domain": domain, "api_key": api_key}
                )
                data = response.json()
                emails = data.get("data", {}).get("emails", [])
                if emails:
                    return emails[0].get("value", "")
        except Exception:
            pass
        return ""

    def extract_domain(self, website: str) -> str:
        if website.startswith('http'):
            return website.split('//')[1].split('/')[0].replace('www.', '')
        return website.replace('www.', '')

    async def enrich_lead(self, lead: Dict) -> Dict:
        full_lead = lead.copy()
        full_lead["lead_id"] = str(uuid.uuid4())
        full_lead["scraped_at"] = datetime.utcnow().isoformat()
        full_lead["status"] = "scraped"
        
        if lead.get("website"):
            email = await self.find_email_from_website(lead["website"])
            if email:
                full_lead["email_primary"] = email
            else:
                domain = self.extract_domain(lead["website"])
                full_lead["email_primary"] = f"info@{domain}"
        
        return full_lead

    def verify_lead(self, lead: Dict) -> bool:
        if not lead.get("email_primary"):
            return False
        
        if "@" not in lead.get("email_primary", ""):
            return False
            
        if lead.get("scraped_source") == "google_maps" and not lead.get("business_name"):
            return False
            
        return True

    def score_lead(self, lead: Dict) -> int:
        score = 50
        
        if lead.get("email_primary"):
            score += 20
            
        if lead.get("current_rating", 0) < 3.5:
            score += 15
            
        if lead.get("reviews_count", 0) > 10:
            score += 10
            
        if lead.get("negative_review_count", 0) > 3:
            score += 5
            
        return min(score, 100)

    async def process_task(self, task_id: str):
        self.brain.remember(f"Processing task: {task_id}", "task_start")
        
        from database.models import SessionLocal, Task
        
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return
            
            task.status = "active"
            task.phase_scraping = "in_progress"
            db.commit()
            
            leads = await self.scrape_google_maps(
                task.business_type,
                task.city,
                task.state,
                task.country
            )
            
            enriched_leads = []
            for lead in leads:
                enriched = await self.enrich_lead(lead)
                if self.verify_lead(enriched):
                    enriched["lead_score"] = self.score_lead(enriched)
                    enriched["task_id"] = task_id
                    enriched_leads.append(enriched)
            
            task.leads_total = len(enriched_leads)
            task.leads_scraped = len(enriched_leads)
            task.phase_scraping = "complete"
            db.commit()
            
            handoff = create_handoff_message(
                from_agent=self.name,
                to_agent="EnrichHead",
                leads=enriched_leads,
                task_id=task_id,
                notes=f"{len(enriched_leads)} leads scraped and verified"
            )
            self.message_bus.messages.append(handoff)
            self._save_messages()
            
            self.brain.remember(
                f"Task {task_id} completed: {len(enriched_leads)} leads scraped",
                "task_complete",
                {"task_id": task_id, "leads_count": len(enriched_leads)}
            )
            
        finally:
            db.close()

    def _save_messages(self):
        self.message_bus._save_messages()

    def start(self):
        return {"status": "online", "team": self.team}

scrape_head = ScrapeHeadAgent()