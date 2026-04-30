import uuid
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import httpx
from bs4 import BeautifulSoup

class ScrapeTools:
    """Enhanced scraping tools - inspired by Huginn agents"""
    
    @staticmethod
    async def scrape_google_maps(business_type: str, city: str, state: str, country: str = "USA") -> List[Dict]:
        results = []
        try:
            search_query = f"{business_type} {city} {state} {country}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                script_tags = soup.find_all('script')
                for script in script_tags:
                    if script.string and 'lat' in script.string.lower():
                        try:
                            data = json.loads(script.string)
                            if 'd' in data:
                                inner_data = json.loads(data['d'])
                                if 'd' in inner_data:
                                    results_data = json.loads(inner_data['d'])
                                    if isinstance(results_data, list):
                                        for item in results_data[:20]:
                                            if isinstance(item, list) and len(item) > 10:
                                                try:
                                                    business_name = str(item[2]) if len(item) > 2 else ""
                                                    rating = float(item[4]) if len(item) > 4 and item[4] else 0
                                                    results.append({
                                                        "business_name": business_name.split('•')[0].strip() if '•' in business_name else business_name,
                                                        "current_rating": rating,
                                                        "address": str(item[1]) if len(item) > 1 else "",
                                                        "scraped_source": "google_maps"
                                                    })
                                                except:
                                                    pass
                        except:
                            pass
                            
        except Exception as e:
            print(f"Google Maps scrape error: {e}")
        
        return results[:20]
    
    @staticmethod
    async def scrape_yelp(business_type: str, city: str, state: str) -> List[Dict]:
        results = []
        try:
            search_query = f"{business_type} {city} {state}"
            url = f"https://www.yelp.com/search?find_desc={search_query.replace(' ', '+')}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                listings = soup.find_all('div', {'class': 'container__09f24__mpR8'})
                
                for listing in listings[:15]:
                    try:
                        name_elem = listing.find('a', {'class': 'link__09f24__30wW'})
                        rating_elem = listing.find('span', {'class': 'css-1h1j96c'})
                        review_elem = listing.find('span', {'class': 'css-1h1j96c'})
                        
                        results.append({
                            "business_name": name_elem.text if name_elem else "",
                            "current_rating": float(rating_elem.get('aria-label', '0').split()[0]) if rating_elem else 0,
                            "scraped_source": "yelp"
                        })
                    except:
                        pass
                        
        except Exception as e:
            print(f"Yelp scrape error: {e}")
        
        return results
    
    @staticmethod
    async def find_emails_from_website(website: str) -> Dict[str, Any]:
        emails_found = []
        contact_pages = []
        
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(website)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    if 'mailto:' in href:
                        email = href.replace('mailto:', '').split('?')[0].strip()
                        if '@' in email and '.' in email:
                            emails_found.append(email)
                    
                    text = link.get_text().lower()
                    if any(term in text for term in ['contact', 'about', 'team', 'support']):
                        if href.startswith('http'):
                            contact_pages.append(href)
                
                for page_url in contact_pages[:3]:
                    try:
                        resp = await client.get(page_url)
                        page_soup = BeautifulSoup(resp.text, 'html.parser')
                        
                        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        matches = re.findall(email_pattern, resp.text)
                        for match in matches[:5]:
                            if match not in emails_found:
                                emails_found.append(match)
                    except:
                        pass
                        
        except Exception as e:
            print(f"Email scrape error: {e}")
        
        return {
            "emails": emails_found[:3],
            "contact_pages": contact_pages[:3],
            "primary_email": emails_found[0] if emails_found else None
        }
    
    @staticmethod
    async def find_social_media(website: str) -> Dict[str, str]:
        socials = {}
        
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(website)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                social_domains = {
                    'facebook': 'facebook.com',
                    'twitter': 'twitter.com',
                    'instagram': 'instagram.com',
                    'linkedin': 'linkedin.com',
                    'youtube': 'youtube.com'
                }
                
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '').lower()
                    for platform, domain in social_domains.items():
                        if domain in href:
                            socials[platform] = href
                            break
                            
        except Exception:
            pass
        
        return socials

import re