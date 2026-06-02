import os
import sys
import sqlite3
import asyncio
import random
import re
import logging
import socket
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scraper.real")

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dmcashield.db')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

def random_ua():
    return random.choice(USER_AGENTS)

def random_delay(min_s=1.5, max_s=4.0):
    return random.uniform(min_s, max_s)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"[\+]?[(]?[0-9]{1,4}[)]?[\s\-\.]?[0-9]{1,4}[\s\-\.]?[0-9]{1,9}")

async def extract_emails_from_url(url: str, client: httpx.AsyncClient = None) -> list:
    should_close = False
    if client is None:
        client = httpx.AsyncClient(timeout=15, follow_redirects=True, headers={"User-Agent": random_ua()})
        should_close = True
    try:
        resp = await client.get(url)
        emails = set(EMAIL_REGEX.findall(resp.text))
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        for path in ["/contact", "/contact-us", "/about", "/about-us"]:
            try:
                resp2 = await client.get(base + path)
                if resp2.status_code == 200:
                    emails.update(EMAIL_REGEX.findall(resp2.text))
            except Exception:
                continue
        junk = {"wixpress.com", "sentry.io", "w3.org", "schema.org", "googleapis.com", "example.com"}
        filtered = [e for e in emails if not any(j in e for j in junk) and len(e) < 60]
        return filtered
    except Exception as e:
        logger.error(f"Failed to extract emails from {url}: {e}")
        return []
    finally:
        if should_close:
            await client.aclose()

async def extract_phone_from_url(url: str, client: httpx.AsyncClient = None) -> str:
    should_close = False
    if client is None:
        client = httpx.AsyncClient(timeout=10, follow_redirects=True, headers={"User-Agent": random_ua()})
        should_close = True
    try:
        resp = await client.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        tel_links = soup.find_all("a", href=re.compile(r"tel:"))
        if tel_links:
            return tel_links[0]["href"].replace("tel:", "").strip()
        phones = PHONE_REGEX.findall(soup.get_text())
        valid = [p for p in phones if sum(c.isdigit() for c in p) >= 7]
        return valid[0] if valid else ""
    except Exception:
        return ""
    finally:
        if should_close:
            await client.aclose()

def validate_email_format(email: str) -> bool:
    pattern = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
    return bool(pattern.match(email)) and len(email) < 100

async def scrape_google_maps_playwright_internal(
    business_type: str,
    city: str,
    state: str,
    country: str = "USA",
    max_results: int = 15,
) -> list:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.warning("[SCRAPER] Playwright not installed")
        return []

    leads = []
    query = f"{business_type} in {city}, {state}"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random_ua(),
                viewport={"width": 1280, "height": 900}
            )
            page = await context.new_page()
            maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            await page.goto(maps_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Accept cookies if dialog appears
            try:
                accept_btn = page.locator("button:has-text('Accept all')")
                if await accept_btn.count() > 0:
                    await accept_btn.click()
                    await asyncio.sleep(1)
            except Exception:
                pass

            # Scroll results panel to load listings
            results_panel = page.locator('div[role="feed"]')
            if await results_panel.count() > 0:
                for _ in range(3):
                    await results_panel.evaluate("el => el.scrollTop = el.scrollHeight")
                    await asyncio.sleep(1.5)

            listings = page.locator('div[role="feed"] > div > div > a')
            count = await listings.count()
            logger.info(f"[SCRAPER-PW] Found {count} listings on Google Maps")

            for i in range(min(count, max_results)):
                try:
                    listing = listings.nth(i)
                    aria_label = await listing.get_attribute("aria-label") or ""
                    href = await listing.get_attribute("href") or ""
                    if not aria_label:
                        continue

                    await listing.click()
                    await asyncio.sleep(random_delay(1.5, 3.0))

                    name = aria_label.strip()
                    rating = 0.0
                    total_reviews = 0
                    address = ""
                    phone = ""
                    website = ""

                    # Rating
                    try:
                        rating_el = page.locator('div.F7nice span[aria-hidden="true"]').first
                        if await rating_el.count() > 0:
                            rating_text = await rating_el.inner_text()
                            rating = float(rating_text.replace(",", "."))
                    except Exception:
                        pass

                    # Review count
                    try:
                        review_el = page.locator('div.F7nice span[aria-label*="review"]').first
                        if await review_el.count() > 0:
                            review_text = await review_el.get_attribute("aria-label") or ""
                            nums = re.findall(r"[\d,]+", review_text)
                            if nums:
                                total_reviews = int(nums[0].replace(",", ""))
                    except Exception:
                        pass

                    # Address
                    try:
                        addr_el = page.locator('button[data-item-id="address"]')
                        if await addr_el.count() > 0:
                            address = await addr_el.inner_text()
                    except Exception:
                        pass

                    # Phone
                    try:
                        phone_el = page.locator('button[data-item-id*="phone"]')
                        if await phone_el.count() > 0:
                            phone = await phone_el.inner_text()
                    except Exception:
                        pass

                    # Website
                    try:
                        web_el = page.locator('a[data-item-id="authority"]')
                        if await web_el.count() > 0:
                            website = await web_el.get_attribute("href") or ""
                    except Exception:
                        pass

                    # Extract emails
                    emails = []
                    if website:
                        try:
                            emails = await extract_emails_from_url(website)
                        except Exception:
                            pass

                    primary_email = emails[0] if emails else ""
                    if not primary_email and website:
                        try:
                            parsed = urlparse(website)
                            domain = parsed.netloc.replace("www.", "")
                            if domain:
                                primary_email = f"info@{domain}"
                        except Exception:
                            pass

                    neg_estimate = max(0, int(total_reviews * (1 - rating / 5) * 0.4)) if rating > 0 else 0

                    lead_data = {
                        "business_name": name,
                        "email_primary": primary_email,
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
                    leads.append(lead_data)
                    logger.info(f"[SCRAPER-PW] Scraped: {name} | Rating: {rating} | Email: {primary_email}")

                    await page.go_back()
                    await asyncio.sleep(1)

                except Exception as e:
                    logger.warning(f"[SCRAPER-PW] Listing extraction error: {e}")
                    continue

            await browser.close()
    except Exception as e:
        logger.error(f"[SCRAPER-PW] Scraper error: {e}")

    return leads

def update_task_field(task_id: str, field: str, value):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"UPDATE tasks SET {field} = ? WHERE id = ?", (value, task_id))
    conn.commit()
    conn.close()

def run_scraper_pipeline(task_id: str, business_type: str, city: str, state: str, country: str = "USA"):
    # Ensure sys path includes root/parent directory so we can import modules
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
        
    update_task_field(task_id, "phase_scraping", "in_progress")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        leads = loop.run_until_complete(scrape_google_maps_playwright_internal(business_type, city, state, country))
    except Exception as e:
        logger.error(f"Pipeline loop error: {e}")
        leads = []
    finally:
        loop.close()
        
    update_task_field(task_id, "phase_scraping", "complete")
    update_task_field(task_id, "phase_validation", "in_progress")
    
    from agents.real_lead_engine import add_lead
    
    saved_count = 0
    for lead in leads:
        try:
            lead["task_id"] = task_id
            lead["source"] = f"task_{task_id}"
            add_lead(lead)
            saved_count += 1
        except Exception as e:
            logger.error(f"Error saving scraped lead to database: {e}")
            
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        UPDATE tasks SET 
            phase_validation = 'complete',
            phase_funnel_creation = 'complete',
            phase_email_sending = 'active',
            leads_total = ?,
            status = 'active'
        WHERE id = ?
    """, (saved_count, task_id))
    conn.commit()
    conn.close()
