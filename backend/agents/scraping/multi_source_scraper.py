import uuid
import asyncio
import httpx
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class MultiSourceScraper:
    def __init__(self):
        self.sources = ["google_maps", "yellowpages", "yelp", "bing_local"]
    
    async def scrape_yellowpages(self, business_type: str, city: str, state: str) -> List[Dict]:
        results = []
        try:
            search_url = f"https://www.yellowpages.com/search?search_terms={business_type.replace(' ', '+')}&geo_location_terms={city}%2C+{state}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('div', class_='result')
                
                for listing in listings[:20]:
                    try:
                        name_elem = listing.find('a', class_='business-name')
                        phone_elem = listing.find('div', class_='phone')
                        address_elem = listing.find('div', class_='street-address')
                        rating_elem = listing.find('div', class_='rating')
                        
                        if name_elem:
                            results.append({
                                "business_name": name_elem.get_text(strip=True),
                                "phone": phone_elem.get_text(strip=True) if phone_elem else "",
                                "address": address_elem.get_text(strip=True) if address_elem else "",
                                "rating": float(rating_elem.get_text(strip=True).split()[0]) if rating_elem else 0,
                                "scraped_source": "yellowpages",
                                "source_url": name_elem.get('href', '') if name_elem else ""
                            })
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"YellowPages scrape error: {e}")
        
        return results
    
    async def scrape_yelp(self, business_type: str, city: str, state: str) -> List[Dict]:
        results = []
        try:
            search_url = f"https://www.yelp.com/search?find_desc={business_type.replace(' ', '+')}&find_loc={city}%2C+{state}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('li', class_='arrange-unit__09f24__orxkg')
                
                for listing in listings[:20]:
                    try:
                        name_elem = listing.find('a', class_='css-1m051bw')
                        rating_elem = listing.find('div', class_='i-stars')
                        review_elem = listing.find('span', class_='review-count')
                        address_elem = listing.find('p', class_='css-1ap4wc')
                        
                        if name_elem:
                            results.append({
                                "business_name": name_elem.get_text(strip=True),
                                "rating": float(rating_elem.get('aria-label', '0').split()[0]) if rating_elem else 0,
                                "reviews_count": int(review_elem.get_text(strip=True).split()[0]) if review_elem else 0,
                                "address": address_elem.get_text(strip=True) if address_elem else "",
                                "scraped_source": "yelp",
                                "source_url": f"https://www.yelp.com{name_elem.get('href', '')}"
                            })
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"Yelp scrape error: {e}")
        
        return results
    
    async def scrape_bing_local(self, business_type: str, city: str, state: str) -> List[Dict]:
        results = []
        try:
            search_url = f"https://www.bing.com/local/search?q={business_type.replace(' ', '+')}&l={city}%2C+{state}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('div', class_='sb_addrcal')
                
                for listing in listings[:15]:
                    try:
                        name_elem = listing.find('a', class_='b_title')
                        address_elem = listing.find('span', class_='b_address')
                        
                        if name_elem:
                            results.append({
                                "business_name": name_elem.get_text(strip=True),
                                "address": address_elem.get_text(strip=True) if address_elem else "",
                                "scraped_source": "bing_local"
                            })
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"BingLocal scrape error: {e}")
        
        return results
    
    async def scrape_all_sources(self, business_type: str, city: str, state: str) -> Dict[str, List[Dict]]:
        tasks = []
        
        if "yellowpages" in self.sources:
            tasks.append(self.scrape_yellowpages(business_type, city, state))
        
        if "yelp" in self.sources:
            tasks.append(self.scrape_yelp(business_type, city, state))
        
        if "bing_local" in self.sources:
            tasks.append(self.scrape_bing_local(business_type, city, state))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        combined = {}
        for source, result in zip(self.sources, results):
            if isinstance(result, list):
                combined[source] = result
        
        return combined
    
    def merge_leads(self, leads_by_source: Dict[str, List[Dict]]) -> List[Dict]:
        seen = {}
        merged = []
        
        for source, leads in leads_by_source.items():
            for lead in leads:
                name = lead.get("business_name", "").lower().strip()
                if not name:
                    continue
                
                if name not in seen:
                    seen[name] = lead
                    merged.append(lead)
                else:
                    existing = seen[name]
                    for key, value in lead.items():
                        if not existing.get(key):
                            existing[key] = value
        
        return merged
    
    def enable_source(self, source: str):
        if source not in self.sources:
            self.sources.append(source)
    
    def disable_source(self, source: str):
        if source in self.sources:
            self.sources.remove(source)

multi_source_scraper = MultiSourceScraper()