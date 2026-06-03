"""
DMCAShield HTTP Scraper
========================
Serverless-compatible business scraper using httpx + BeautifulSoup.
Works on Vercel (no Playwright/Chrome needed).

Scraping sources:
1. YellowPages.com — Business listings with phone, address, website
2. Direct website scraping — Extract emails from contact pages
3. Google search results — Find business info via web search
"""

import os
import re
import random
import logging
import asyncio
from urllib.parse import urlparse, quote_plus
from typing import List, Dict, Optional

try:
    import httpx
except ImportError:
    httpx = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

logger = logging.getLogger("dmcashield.scraper")


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"[\+]?[(]?[0-9]{1,4}[)]?[\s\-\.][0-9]{1,4}[\s\-\.][0-9]{1,9}")

JUNK_DOMAINS = {"wixpress.com", "sentry.io", "w3.org", "schema.org", "googleapis.com",
                "example.com", "facebook.com", "twitter.com", "instagram.com", "google.com",
                "squarespace.com", "cloudflare.com", "wordpress.com", "gravatar.com"}


def _random_ua():
    return random.choice(USER_AGENTS)


async def _extract_emails_from_url(url: str, client: httpx.AsyncClient) -> List[str]:
    """Extract email addresses from a website and its contact pages."""
    emails = set()
    
    try:
        resp = await client.get(url, follow_redirects=True, timeout=10)
        if resp.status_code == 200:
            emails.update(EMAIL_REGEX.findall(resp.text))
            
            # Also try common contact pages
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            for path in ["/contact", "/contact-us", "/about", "/about-us", "/contactus"]:
                try:
                    resp2 = await client.get(base + path, follow_redirects=True, timeout=8)
                    if resp2.status_code == 200:
                        emails.update(EMAIL_REGEX.findall(resp2.text))
                except Exception:
                    continue
    except Exception as e:
        logger.debug(f"Email extraction failed for {url}: {e}")
    
    # Filter junk emails
    filtered = [e for e in emails 
                if not any(j in e.lower() for j in JUNK_DOMAINS) 
                and len(e) < 60
                and not e.startswith(".")
                and not e.endswith(".")
                and ".." not in e]
    
    return filtered


async def _extract_phone_from_html(html: str) -> str:
    """Extract phone number from HTML content."""
    if not BeautifulSoup:
        phones = PHONE_REGEX.findall(html)
        valid = [p for p in phones if sum(c.isdigit() for c in p) >= 7]
        return valid[0] if valid else ""
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Check tel: links first
    tel_links = soup.find_all("a", href=re.compile(r"tel:"))
    if tel_links:
        return tel_links[0]["href"].replace("tel:", "").strip()
    
    # Fallback to regex on text
    phones = PHONE_REGEX.findall(soup.get_text())
    valid = [p for p in phones if sum(c.isdigit() for c in p) >= 7]
    return valid[0] if valid else ""


async def scrape_yellowpages(business_type: str, city: str, state: str,
                              max_results: int = 20) -> List[Dict]:
    """
    Scrape business listings from YellowPages.com.
    Returns list of lead dicts with business info.
    """
    if not httpx or not BeautifulSoup:
        logger.error("httpx and beautifulsoup4 are required. Install: pip install httpx beautifulsoup4")
        return []
    
    leads = []
    search_url = f"https://www.yellowpages.com/search?search_terms={quote_plus(business_type)}&geo_location_terms={quote_plus(f'{city}, {state}')}"
    
    logger.info(f"[SCRAPER] Searching YellowPages: {business_type} in {city}, {state}")
    
    async with httpx.AsyncClient(
        headers={"User-Agent": _random_ua()},
        follow_redirects=True,
        timeout=20
    ) as client:
        try:
            resp = await client.get(search_url)
            if resp.status_code != 200:
                logger.warning(f"[SCRAPER] YellowPages returned {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Find business listing cards
            results = soup.find_all("div", class_="result")
            if not results:
                results = soup.find_all("div", class_="search-results")
                if results:
                    results = results[0].find_all("div", class_=re.compile(r"result|listing"))
            
            logger.info(f"[SCRAPER] Found {len(results)} listings on YellowPages")
            
            for result in results[:max_results]:
                try:
                    lead = _parse_yellowpages_listing(result)
                    if lead and lead.get("business_name"):
                        lead["city"] = city
                        lead["state"] = state
                        lead["niche"] = business_type
                        lead["source"] = "yellowpages"
                        
                        # Try to get email from website
                        if lead.get("website"):
                            try:
                                emails = await _extract_emails_from_url(lead["website"], client)
                                if emails:
                                    lead["email_primary"] = emails[0]
                            except Exception:
                                pass
                        
                        # Generate fallback email if we have a website but no email
                        if not lead.get("email_primary") and lead.get("website"):
                            try:
                                domain = urlparse(lead["website"]).netloc.replace("www.", "")
                                if domain:
                                    lead["email_primary"] = f"info@{domain}"
                            except Exception:
                                pass
                        
                        leads.append(lead)
                        logger.info(f"[SCRAPER] Found: {lead['business_name']} | {lead.get('phone', 'no phone')}")
                
                except Exception as e:
                    logger.debug(f"[SCRAPER] Parse error: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"[SCRAPER] YellowPages error: {e}")
    
    return leads


def _parse_yellowpages_listing(result) -> Optional[Dict]:
    """Parse a single YellowPages listing into a lead dict."""
    lead = {}
    
    # Business name
    name_el = result.find("a", class_="business-name")
    if not name_el:
        name_el = result.find("h2")
    if name_el:
        lead["business_name"] = name_el.get_text(strip=True)
    
    # Phone
    phone_el = result.find("div", class_="phones")
    if phone_el:
        lead["phone"] = phone_el.get_text(strip=True)
    
    # Address
    addr_el = result.find("div", class_="street-address")
    locality_el = result.find("div", class_="locality")
    address_parts = []
    if addr_el:
        address_parts.append(addr_el.get_text(strip=True))
    if locality_el:
        address_parts.append(locality_el.get_text(strip=True))
    if address_parts:
        lead["full_address"] = ", ".join(address_parts)
    
    # Website
    website_el = result.find("a", class_="track-visit-website")
    if not website_el:
        website_el = result.find("a", attrs={"href": re.compile(r"http")})
    if website_el and website_el.get("href") and "yellowpages" not in website_el["href"]:
        lead["website"] = website_el["href"]
    
    # Rating
    rating_el = result.find("div", class_="ratings")
    if rating_el:
        rating_text = rating_el.get("data-rating", "") or ""
        try:
            lead["current_rating"] = float(rating_text)
        except (ValueError, TypeError):
            lead["current_rating"] = 0
    
    # Categories/niche info
    categories_el = result.find("div", class_="categories")
    if categories_el:
        lead["business_nature"] = categories_el.get_text(strip=True)
    
    return lead if lead.get("business_name") else None


async def scrape_yelp(business_type: str, city: str, state: str,
                       max_results: int = 20) -> List[Dict]:
    """
    Scrape business listings from Yelp.
    Returns list of lead dicts with business info.
    """
    if not httpx or not BeautifulSoup:
        return []
    
    leads = []
    search_url = f"https://www.yelp.com/search?find_desc={quote_plus(business_type)}&find_loc={quote_plus(f'{city}, {state}')}"
    
    logger.info(f"[SCRAPER] Searching Yelp: {business_type} in {city}, {state}")
    
    async with httpx.AsyncClient(
        headers={"User-Agent": _random_ua()},
        follow_redirects=True,
        timeout=20
    ) as client:
        try:
            resp = await client.get(search_url)
            if resp.status_code != 200:
                logger.warning(f"[SCRAPER] Yelp returned {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Yelp uses JSON-LD for business data
            import json
            scripts = soup.find_all("script", type="application/ld+json")
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        for item in data:
                            if item.get("@type") == "LocalBusiness":
                                lead = _parse_yelp_jsonld(item, city, state, business_type)
                                if lead:
                                    leads.append(lead)
                    elif isinstance(data, dict) and data.get("@type") == "LocalBusiness":
                        lead = _parse_yelp_jsonld(data, city, state, business_type)
                        if lead:
                            leads.append(lead)
                except (json.JSONDecodeError, TypeError):
                    continue
            
            # Fallback: parse HTML listings
            if not leads:
                listings = soup.find_all("div", attrs={"data-testid": re.compile(r"serp-ia")})
                for listing in listings[:max_results]:
                    try:
                        name_el = listing.find("a", class_=re.compile(r"link"))
                        if name_el:
                            name = name_el.get_text(strip=True)
                            if name:
                                lead = {
                                    "business_name": name,
                                    "city": city,
                                    "state": state,
                                    "niche": business_type,
                                    "source": "yelp",
                                }
                                # Try to get rating
                                rating_el = listing.find("div", attrs={"aria-label": re.compile(r"star")})
                                if rating_el:
                                    rating_text = rating_el.get("aria-label", "")
                                    nums = re.findall(r"[\d.]+", rating_text)
                                    if nums:
                                        lead["current_rating"] = float(nums[0])
                                
                                leads.append(lead)
                    except Exception:
                        continue
            
            logger.info(f"[SCRAPER] Found {len(leads)} listings on Yelp")
        
        except Exception as e:
            logger.error(f"[SCRAPER] Yelp error: {e}")
    
    return leads[:max_results]


def _parse_yelp_jsonld(data: dict, city: str, state: str, niche: str) -> Optional[Dict]:
    """Parse Yelp JSON-LD data into a lead dict."""
    name = data.get("name", "")
    if not name:
        return None
    
    address = data.get("address", {})
    rating = data.get("aggregateRating", {})
    
    lead = {
        "business_name": name,
        "city": city,
        "state": state,
        "niche": niche,
        "source": "yelp",
        "full_address": f"{address.get('streetAddress', '')}, {address.get('addressLocality', '')}, {address.get('addressRegion', '')}".strip(", "),
        "phone": data.get("telephone", ""),
        "current_rating": float(rating.get("ratingValue", 0)),
        "review_count": int(rating.get("reviewCount", 0)),
    }
    
    return lead


async def scrape_all_sources(business_type: str, city: str, state: str,
                              country: str = "USA", max_results: int = 20) -> List[Dict]:
    """
    Scrape from all available sources and deduplicate results.
    This is the main entry point for the scraping pipeline.
    """
    all_leads = []
    
    # Scrape from multiple sources
    try:
        yp_leads = await scrape_yellowpages(business_type, city, state, max_results)
        all_leads.extend(yp_leads)
        logger.info(f"[SCRAPER] YellowPages: {len(yp_leads)} leads")
    except Exception as e:
        logger.error(f"[SCRAPER] YellowPages failed: {e}")
    
    try:
        yelp_leads = await scrape_yelp(business_type, city, state, max_results)
        all_leads.extend(yelp_leads)
        logger.info(f"[SCRAPER] Yelp: {len(yelp_leads)} leads")
    except Exception as e:
        logger.error(f"[SCRAPER] Yelp failed: {e}")
    
    # Deduplicate by business name (case-insensitive)
    seen = set()
    unique_leads = []
    for lead in all_leads:
        key = lead.get("business_name", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            lead["country"] = country
            unique_leads.append(lead)
    
    logger.info(f"[SCRAPER] Total unique leads: {len(unique_leads)} (from {len(all_leads)} raw)")
    return unique_leads[:max_results]


def run_scraper_sync(business_type: str, city: str, state: str,
                     country: str = "USA", max_results: int = 20) -> List[Dict]:
    """Synchronous wrapper for the async scraper. Use from Flask routes."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        leads = loop.run_until_complete(
            scrape_all_sources(business_type, city, state, country, max_results)
        )
        loop.close()
        return leads
    except Exception as e:
        logger.error(f"[SCRAPER] Sync wrapper error: {e}")
        return []
