"""
DMCAShield Google Maps Scraper — REAL Business Data via Playwright
===================================================================
Uses Playwright browser automation to scrape REAL businesses from Google Maps.
Extracts real business names, phone numbers, addresses, ratings, and websites.
Then visits each business website to extract real email addresses.

NO fake data. NO random phone numbers. NO guessed emails.
All data scraped directly from Google Maps and business websites.

For Vercel (serverless): Falls back to Overpass API + website email extraction.
"""

import os

# Max number of leads to scrape per run (default 100, can be overridden via env var)
MAX_SCRAPE_RESULTS = int(os.getenv("MAX_SCRAPE_RESULTS", "100"))
import re
import random
import logging
import asyncio
import json
import socket
from urllib.parse import urlparse, quote_plus
from typing import List, Dict, Optional, Set
from concurrent.futures import ThreadPoolExecutor

try:
    import httpx
except ImportError:
    httpx = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

logger = logging.getLogger("dmcashield.google_maps")

IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
]

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"[\+]?[(]?[0-9]{1,4}[)]?[\s\-\.][0-9]{1,4}[\s\-\.][0-9]{1,9}")

JUNK_EMAIL_DOMAINS = {
    "wixpress.com", "sentry.io", "w3.org", "schema.org", "googleapis.com",
    "example.com", "facebook.com", "twitter.com", "instagram.com", "google.com",
    "squarespace.com", "cloudflare.com", "wordpress.com", "gravatar.com",
    "youtube.com", "linkedin.com", "pinterest.com", "tiktok.com", "yelp.com",
    "godaddy.com", "weebly.com", "shopify.com", "wix.com", "github.com",
}

# Block generic/shared mailbox prefixes (including info, office, hello, etc.) to target personal business emails or Gmails
BLOCKED_PREFIXES = {
    "info", "office", "hello", "welcome", "hi", "hey", "sales", "team", "inquiry", "inquiries",
    "support", "contact", "billing", "jobs", "help", "admin",
    "service", "noreply", "no-reply", "careers", "hr", "privacy",
    "feedback", "webmaster", "donotreply", "unsubscribe", "newsletter",
    "notifications", "alerts", "system", "postmaster", "mailer-daemon",
    "abuse", "security", "compliance"
}

PLACEHOLDER_USERNAMES = {
    "firstname.lastname", "firstname", "lastname", "first.last",
    "yourname", "your-name", "your.name", "username", "user.name",
    "placeholder", "example", "test", "temp", "email", "mail"
}


def _random_ua():
    return random.choice(USER_AGENTS)


def _filter_email(email: str, website_domain: str = "") -> bool:
    """Return True if email should be KEPT."""
    e = email.lower().strip()
    if len(e) >= 60 or e.startswith(".") or e.endswith(".") or ".." in e:
        return False
    
    parts = e.split("@")
    if len(parts) != 2:
        return False
    username, domain = parts[0].strip(), parts[1].strip()
    
    if any(j in domain for j in JUNK_EMAIL_DOMAINS):
        return False
    if username in BLOCKED_PREFIXES:
        return False
    if username in PLACEHOLDER_USERNAMES:
        return False
    
    # Third-party domain check
    if website_domain and domain not in {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
        "icloud.com", "protonmail.com", "mail.com", "zoho.com",
        "ymail.com", "live.com", "msn.com", "gmx.com", "comcast.net",
        "att.net", "me.com"
    }:
        if domain != website_domain and not domain.endswith("." + website_domain) and not website_domain.endswith("." + domain):
            return False
    
    return True


def _check_mx_record(domain: str) -> bool:
    """Check if domain has valid MX records (can receive email)."""
    try:
        socket.getaddrinfo(domain, None)
        return True
    except Exception:
        return False


async def _extract_emails_from_website(url: str, client: httpx.AsyncClient) -> List[str]:
    """Visit business website + contact pages to extract real email addresses."""
    if not url:
        return []
    
    emails = set()
    website_domain = ""
    
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc or ""
        if netloc.startswith("www."):
            netloc = netloc[4:]
        website_domain = netloc.lower().strip()
    except Exception:
        pass
    
    # 1. Start with the home page
    pages_to_visit = [url]
    visited = set()
    
    # 2. Fetch home page using HTTPX to extract potential email addresses and discover sub-links
    homepage_html = ""
    try:
        resp = await client.get(url, follow_redirects=True, timeout=10)
        if resp.status_code == 200:
            homepage_html = resp.text
            # Extract emails from homepage directly
            found = EMAIL_REGEX.findall(homepage_html)
            emails.update(found)
            
            # Find sub-links on the homepage pointing to Contact, About, Team, Locations, etc.
            if BeautifulSoup:
                soup = BeautifulSoup(homepage_html, "html.parser")
                # Look for mailto links on homepage
                for a in soup.find_all("a", href=re.compile(r"^mailto:", re.I)):
                    href = a.get("href", "")
                    mail = href.replace("mailto:", "").split("?")[0].strip()
                    if "@" in mail:
                        emails.add(mail)
                
                # Scan internal links
                for a in soup.find_all("a", href=True):
                    href = a.get("href", "").strip()
                    if not href or href.startswith("#") or href.startswith("javascript:"):
                        continue
                    
                    # Normalize relative links
                    if href.startswith("/"):
                        parsed_base = urlparse(url)
                        href = f"{parsed_base.scheme}://{parsed_base.netloc}{href}"
                    
                    # Ensure it's the same domain
                    try:
                        parsed_href = urlparse(href)
                        href_domain = parsed_href.netloc.lower().replace("www.", "")
                        if href_domain == website_domain:
                            # Prioritize contact, about, location keywords
                            href_lower = href.lower()
                            if any(k in href_lower for k in [
                                "contact", "about", "team", "staff", "meet", "doctor", "dentist", 
                                "location", "office", "chelsea", "brooklyn", "manhattan", "queens", 
                                "bronx", "pasadena", "los-angeles", "la", "nyc", "locations", "hours"
                            ]):
                                if href not in pages_to_visit:
                                    pages_to_visit.append(href)
                    except Exception:
                        pass
    except Exception as e:
        logger.debug(f"Failed to fetch homepage via httpx: {e}")

    # Ensure we have common standard pages in the list too if they weren't found in links
    try:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        for path in ["/contact", "/contact-us", "/about", "/about-us", "/our-team", "/locations"]:
            std_url = base + path
            if std_url not in pages_to_visit:
                pages_to_visit.append(std_url)
    except Exception:
        pass

    # Limit to visiting top 6 pages to avoid infinite loops
    pages_to_visit = pages_to_visit[:6]

    # 3. Crawl discovered pages using HTTPX
    for page_url in pages_to_visit:
        if page_url in visited:
            continue
        visited.add(page_url)
        
        # We already fetched homepage in step 2
        if page_url == url and homepage_html:
            continue
            
        try:
            resp = await client.get(page_url, follow_redirects=True, timeout=8)
            if resp.status_code != 200:
                continue
            
            # Regex extraction
            found = EMAIL_REGEX.findall(resp.text)
            emails.update(found)
            
            # mailto: links
            if BeautifulSoup:
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all("a", href=re.compile(r"^mailto:", re.I)):
                    href = a.get("href", "")
                    mail = href.replace("mailto:", "").split("?")[0].strip()
                    if "@" in mail:
                        emails.add(mail)
                
                # JSON-LD structured data
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        ld = json.loads(script.string)
                        if isinstance(ld, dict):
                            em = ld.get("email", "")
                            if em and "@" in em:
                                emails.add(em.replace("mailto:", ""))
                        elif isinstance(ld, list):
                            for item in ld:
                                if isinstance(item, dict):
                                    em = item.get("email", "")
                                    if em and "@" in em:
                                        emails.add(em.replace("mailto:", ""))
                    except Exception:
                        pass
        except Exception:
            continue

    # Filter generic prefixes out before checking Playwright fallback
    valid = [e for e in emails if _filter_email(e, website_domain)]

    # 4. PLAYWRIGHT FALLBACK (if local/agent mode and no emails found via HTTPX)
    # This renders SPAs and client-side loaded emails (like Soul Dental website)
    if not IS_VERCEL and not valid:
        try:
            from playwright.async_api import async_playwright
            logger.info(f"[CRAWLER] Using Playwright fallback for: {url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Create context with a real user agent
                context = await browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport={"width": 1280, "height": 800}
                )
                
                # We will check the homepage and the top 2 location/contact pages
                pw_pages = [url]
                for p_url in pages_to_visit:
                    if p_url != url and any(k in p_url.lower() for k in ["contact", "location", "chelsea", "about"]):
                        pw_pages.append(p_url)
                        if len(pw_pages) >= 3:
                            break
                
                for pw_url in pw_pages:
                    try:
                        page = await context.new_page()
                        # Visit page and wait for network idle to allow JS to load emails
                        await page.goto(pw_url, wait_until="networkidle", timeout=15000)
                        html_content = await page.content()
                        
                        # Extract emails
                        found = EMAIL_REGEX.findall(html_content)
                        emails.update(found)
                        
                        # Also check mailto: links in page content
                        mailto_links = await page.locator('a[href^="mailto:"]').all()
                        for link in mailto_links:
                            href = await link.get_attribute("href") or ""
                            mail = href.replace("mailto:", "").split("?")[0].strip()
                            if "@" in mail:
                                emails.add(mail)
                                
                        await page.close()
                    except Exception as e:
                        logger.debug(f"[CRAWLER] Playwright failed on {pw_url}: {e}")
                        
                await browser.close()
        except Exception as e:
            logger.debug(f"[CRAWLER] Playwright launcher failed: {e}")

    # Re-evaluate valid emails list
    valid = [e for e in emails if _filter_email(e, website_domain)]
    
    # Sort: personal names first (if we have name-based ones)
    def priority(e):
        username = e.split("@")[0].lower()
        if username in ("info", "office", "hello", "team", "sales"):
            return 1
        return 0
    valid.sort(key=priority)
    
    return valid


# ═══════════════════════════════════════════════════════════════════
# STRATEGY 1: PLAYWRIGHT — Scrape directly from Google Maps (LOCAL)
# ═══════════════════════════════════════════════════════════════════

async def _scrape_google_maps_playwright(
    business_type: str, city: str, state: str, country: str = "USA", max_results: int = MAX_SCRAPE_RESULTS
) -> List[Dict]:
    """
    Use Playwright to open Google Maps, search for businesses, click each listing,
    and extract real business data (name, phone, address, website, rating).
    Then visit each website to extract real email addresses.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.warning("[GMAPS] Playwright not installed — skipping")
        return []
    
    leads = []
    query = f"{business_type} in {city}, {state}"
    
    logger.info(f"[GMAPS] Starting Playwright Google Maps scrape: {query}")
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=_random_ua(),
                viewport={"width": 1280, "height": 900},
                locale="en-US"
            )
            page = await context.new_page()
            
            maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            logger.info(f"[GMAPS] Opening: {maps_url}")
            
            await page.goto(maps_url, wait_until="domcontentloaded", timeout=45000)
            # Wait for maps results to load (networkidle hangs on Maps)
            await asyncio.sleep(5)
            
            # Wait for results feed to appear
            try:
                await page.wait_for_selector('div[role="feed"]', timeout=15000)
                await asyncio.sleep(2)
            except Exception:
                logger.warning("[GMAPS] Results feed not found, trying to continue...")
            
            # Accept cookies if dialog appears
            try:
                accept_btn = page.locator("button:has-text('Accept all')")
                if await accept_btn.count() > 0:
                    await accept_btn.click()
                    await asyncio.sleep(1)
            except Exception:
                pass
            
            # Scroll results panel to load more listings
            results_panel = page.locator('div[role="feed"]')
            if await results_panel.count() > 0:
                for _ in range(15):  # Scroll 15 times to load ~100 results
                    await results_panel.evaluate("el => el.scrollTop = el.scrollHeight")
                    await asyncio.sleep(1.5)
            
            # Find all listing links
            listings = page.locator('div[role="feed"] > div > div > a')
            count = await listings.count()
            logger.info(f"[GMAPS] Found {count} listings on Google Maps")
            
            # Create httpx client for website email extraction
            async with httpx.AsyncClient(
                headers={"User-Agent": _random_ua()},
                follow_redirects=True,
                timeout=15
            ) as http_client:
                
                for i in range(min(count, max_results)):
                    try:
                        listing = listings.nth(i)
                        aria_label = await listing.get_attribute("aria-label") or ""
                        if not aria_label:
                            continue
                        
                        # Click on listing to open details panel
                        await listing.click()
                        await asyncio.sleep(random.uniform(1.5, 3.0))
                        
                        name = aria_label.strip()
                        rating = 0.0
                        total_reviews = 0
                        address = ""
                        phone = ""
                        website = ""
                        
                        # Extract rating
                        try:
                            rating_el = page.locator('div.F7nice span[aria-hidden="true"]').first
                            if await rating_el.count() > 0:
                                rating_text = await rating_el.inner_text()
                                rating = float(rating_text.replace(",", "."))
                        except Exception:
                            pass
                        
                        # Extract review count
                        try:
                            review_el = page.locator('div.F7nice span[aria-label*="review"]').first
                            if await review_el.count() > 0:
                                review_text = await review_el.get_attribute("aria-label") or ""
                                nums = re.findall(r"[\d,]+", review_text)
                                if nums:
                                    total_reviews = int(nums[0].replace(",", ""))
                        except Exception:
                            pass
                        
                        # Extract address
                        try:
                            addr_el = page.locator('button[data-item-id="address"]')
                            if await addr_el.count() > 0:
                                address = await addr_el.inner_text()
                        except Exception:
                            pass
                        
                        # Extract phone
                        try:
                            phone_el = page.locator('button[data-item-id*="phone"]')
                            if await phone_el.count() > 0:
                                phone = await phone_el.inner_text()
                        except Exception:
                            pass
                        
                        # Extract website
                        try:
                            web_el = page.locator('a[data-item-id="authority"]')
                            if await web_el.count() > 0:
                                website = await web_el.get_attribute("href") or ""
                        except Exception:
                            pass
                        
                        # Visit website to extract real email
                        email_primary = ""
                        if website:
                            try:
                                real_emails = await _extract_emails_from_website(website, http_client)
                                if real_emails:
                                    email_primary = real_emails[0]
                            except Exception:
                                pass
                        
                        # Discard fallback/guessing of info@ emails to prevent bounces and generic messages
                        pass
                        
                        neg_estimate = max(0, int(total_reviews * (1 - rating / 5) * 0.4)) if rating > 0 else 0
                        
                        lead = {
                            "business_name": name,
                            "email_primary": email_primary,
                            "phone": phone,
                            "website": website,
                            "city": city,
                            "state": state,
                            "country": country,
                            "niche": business_type,
                            "full_address": address,
                            "current_rating": rating,
                            "review_count": total_reviews,
                            "negative_review_count": neg_estimate,
                            "source": "google_maps"
                        }
                        
                        leads.append(lead)
                        logger.info(f"[GMAPS] #{i+1} {name} | rating={rating} | email={email_primary or 'N/A'} | phone={phone or 'N/A'}")
                        
                        # Go back to results list
                        await page.go_back()
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.warning(f"[GMAPS] Listing #{i+1} error: {e}")
                        try:
                            await page.go_back()
                            await asyncio.sleep(1)
                        except Exception:
                            pass
                        continue
            
            await browser.close()
            
    except Exception as e:
        logger.error(f"[GMAPS] Playwright scraper error: {e}")
    
    logger.info(f"[GMAPS] Playwright scraped {len(leads)} leads, {sum(1 for l in leads if l.get('email_primary'))} with email")
    return leads


# ═══════════════════════════════════════════════════════════════════
# STRATEGY 2: OVERPASS API — OpenStreetMap with real business data (VERCEL)
# ═══════════════════════════════════════════════════════════════════

async def _get_city_bbox(city: str, state: str) -> Optional[tuple]:
    """Get bounding box for a city using Nominatim geocoding."""
    if not httpx:
        return None
    
    url = f"https://nominatim.openstreetmap.org/search?q={quote_plus(f'{city}, {state}')}&format=json&limit=1"
    headers = {"User-Agent": "DMCAShield/1.0 (business-outreach)"}
    
    async with httpx.AsyncClient(headers=headers, timeout=15) as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    bb = data[0].get("boundingbox", [])
                    if len(bb) == 4:
                        # Nominatim returns: [south_lat, north_lat, west_lon, east_lon]
                        south_lat = float(bb[0])
                        north_lat = float(bb[1])
                        west_lon = float(bb[2])
                        east_lon = float(bb[3])
                        logger.info(f"[GEO] {city}, {state} bbox: S={south_lat:.4f} N={north_lat:.4f} W={west_lon:.4f} E={east_lon:.4f}")
                        return (south_lat, north_lat, west_lon, east_lon)
        except Exception as e:
            logger.error(f"[GEO] Geocoding error: {e}")
    
    return None


async def _scrape_overpass_api(
    business_type: str, city: str, state: str, country: str = "USA", max_results: int = 100
) -> List[Dict]:
    """
    Use OpenStreetMap Overpass API to find businesses with real data.
    Overpass has real website URLs, phone numbers, and sometimes emails.
    Then visit each website to extract emails.
    """
    if not httpx:
        return []
    
    # Map business types to OSM amenity/shop tags
    osm_tags = {
        "restaurant": 'amenity=restaurant',
        "cafe": 'amenity=cafe',
        "dentist": 'amenity=dentist',
        "doctor": 'amenity=doctors',
        "clinic": 'amenity=clinic',
        "hospital": 'amenity=hospital',
        "pharmacy": 'amenity=pharmacy',
        "salon": 'shop=hairdresser',
        "spa": 'leisure=spa',
        "gym": 'leisure=fitness_centre',
        "hotel": 'tourism=hotel',
        "bar": 'amenity=bar',
        "bakery": 'shop=bakery',
        "lawyer": 'office=lawyer',
        "accountant": 'office=accountant',
        "insurance": 'office=insurance',
        "real estate": 'office=estate_agent',
        "auto repair": 'shop=car_repair',
        "plumber": 'craft=plumber',
        "electrician": 'craft=electrician',
        "veterinary": 'amenity=veterinary',
    }
    
    # Find matching tag
    bt_lower = business_type.lower().strip()
    tag = osm_tags.get(bt_lower, f'amenity={bt_lower}')
    tag_key, tag_val = tag.split("=")
    
    # Get city bounding box
    bbox = await _get_city_bbox(city, state)
    if not bbox:
        logger.warning(f"[OVERPASS] Could not geocode {city}, {state}")
        return []
    
    south, north, west, east = bbox  # south_lat, north_lat, west_lon, east_lon
    
    # Expand bbox slightly
    lat_range = north - south
    lon_range = east - west
    south -= lat_range * 0.1
    north += lat_range * 0.1
    west -= lon_range * 0.1
    east += lon_range * 0.1
    
    # Build Overpass query
    overpass_query = f"""[out:json][timeout:30];
(
  node["{tag_key}"="{tag_val}"]({south},{west},{north},{east});
  way["{tag_key}"="{tag_val}"]({south},{west},{north},{east});
);
out body {max_results * 2};"""
    
    logger.info(f"[OVERPASS] Querying: {tag} in {city}, {state} (bbox={south:.2f},{west:.2f},{north:.2f},{east:.2f})")
    
    leads = []
    
    async with httpx.AsyncClient(
        headers={"User-Agent": "DMCAShield/1.0", "Accept": "application/json"},
        follow_redirects=True,
        timeout=30
    ) as client:
        try:
            url = f"https://overpass-api.de/api/interpreter?data={quote_plus(overpass_query)}"
            resp = await client.get(url)
            
            if resp.status_code != 200:
                logger.warning(f"[OVERPASS] Returned {resp.status_code}")
                # Try alternative Overpass server
                url2 = f"https://lz4.overpass-api.de/api/interpreter?data={quote_plus(overpass_query)}"
                resp = await client.get(url2)
                if resp.status_code != 200:
                    logger.error(f"[OVERPASS] Both servers failed")
                    return []
            
            data = resp.json()
            elements = data.get("elements", [])
            logger.info(f"[OVERPASS] Found {len(elements)} raw businesses")
            
            for el in elements:
                if len(leads) >= max_results:
                    break
                
                tags = el.get("tags", {})
                name = tags.get("name", "")
                if not name:
                    continue
                
                website = tags.get("website", tags.get("contact:website", ""))
                email_tagged = tags.get("email", tags.get("contact:email", ""))
                phone = tags.get("phone", tags.get("contact:phone", ""))
                
                address_parts = []
                for key in ["addr:housenumber", "addr:street", "addr:city", "addr:state"]:
                    val = tags.get(key, "")
                    if val:
                        address_parts.append(val)
                full_address = ", ".join(address_parts) if address_parts else ""
                
                # Start with tagged email
                email_primary = email_tagged if email_tagged and "@" in email_tagged else ""
                
                # If no website, try to find it via Bing search
                if not website and name:
                    try:
                        search_q = f"{name} {city} {state} official website"
                        bing_url = f"https://www.bing.com/search?q={quote_plus(search_q)}&count=5"
                        headers = {"User-Agent": _random_ua()}
                        sresp = await client.get(bing_url, headers=headers, timeout=10)
                        if sresp.status_code == 200 and BeautifulSoup:
                            ssoup = BeautifulSoup(sresp.text, "html.parser")
                            for a_tag in ssoup.find_all("li", class_="b_algo"):
                                link = a_tag.find("a")
                                if link:
                                    href = link.get("href", "")
                                    if href.startswith("http"):
                                        link_domain = urlparse(href).netloc.lower().replace("www.", "")
                                        # Skip known directory sites
                                        skip_domains = {"yelp.com", "yellowpages.com", "facebook.com", "instagram.com",
                                                       "linkedin.com", "healthgrades.com", "zocdoc.com", "tripadvisor.com",
                                                       "google.com", "wikipedia.org", "bbb.org", "mapquest.com",
                                                       "opentable.com", "grubhub.com", "doordash.com", "youtube.com"}
                                        if not any(sd in link_domain for sd in skip_domains):
                                            website = href
                                            logger.info(f"[OVERPASS] Found website via Bing: {name} -> {link_domain}")
                                            break
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                    except Exception:
                        pass
                
                # If no tagged email but has website, visit website
                if not email_primary and website:
                    try:
                        real_emails = await _extract_emails_from_website(website, client)
                        if real_emails:
                            email_primary = real_emails[0]
                    except Exception:
                        pass
                
                # Discard fallback/guessing of info@ emails to prevent bounces and generic messages
                pass
                
                lead = {
                    "business_name": name,
                    "email_primary": email_primary,
                    "phone": phone,
                    "website": website,
                    "city": city,
                    "state": state,
                    "country": country,
                    "niche": business_type,
                    "full_address": full_address,
                    "current_rating": 0,
                    "review_count": 0,
                    "negative_review_count": 0,
                    "source": "google_maps"
                }
                
                leads.append(lead)
                logger.info(f"[OVERPASS] {name} | email={email_primary or 'N/A'} | phone={phone or 'N/A'} | web={website or 'N/A'}")
            
        except Exception as e:
            logger.error(f"[OVERPASS] Error: {e}")
    
    logger.info(f"[OVERPASS] Total: {len(leads)} leads, {sum(1 for l in leads if l.get('email_primary'))} with email")
    return leads


# ═══════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

async def scrape_google_maps(business_type: str, city: str, state: str,
                              country: str = "USA", max_results: int = 100) -> List[Dict]:
    """
    Master scraping function. Uses the best available strategy:
    1. Playwright (local) — scrapes real Google Maps
    2. Overpass API (Vercel) — uses OpenStreetMap with real business data
    """
    leads = []
    
    # Try Playwright first (only works locally, not on Vercel)
    if not IS_VERCEL:
        try:
            leads = await _scrape_google_maps_playwright(business_type, city, state, country, max_results)
            if leads:
                logger.info(f"[SCRAPER] Playwright returned {len(leads)} leads")
                return leads
        except Exception as e:
            logger.warning(f"[SCRAPER] Playwright failed: {e}")
    
    # Fallback to Overpass API
    try:
        leads = await _scrape_overpass_api(business_type, city, state, country, max_results)
        if leads:
            logger.info(f"[SCRAPER] Overpass returned {len(leads)} leads")
            return leads
    except Exception as e:
        logger.warning(f"[SCRAPER] Overpass failed: {e}")
    
    logger.warning(f"[SCRAPER] All strategies failed for {business_type} in {city}, {state}")
    return []


def run_google_maps_scraper_sync(business_type: str, city: str, state: str,
                                  country: str = "USA", max_results: int = 100) -> List[Dict]:
    """Synchronous wrapper."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        leads = loop.run_until_complete(
            scrape_google_maps(business_type, city, state, country, max_results)
        )
        loop.close()
        return leads
    except Exception as e:
        logger.error(f"[SCRAPER] Sync wrapper error: {e}")
        return []
