"""
DataHunter-1 Agent - Primary Business Data Extractor
Uses Playwright + Google Places API to extract structured business info.
"""

import asyncio
import json
import time
from typing import Dict, Optional
from playwright.async_api import async_playwright
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class DataHunter1:
    """Scrapes business names, addresses, and Google Business Profiles."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.service = build('places', 'v1', credentials=Credentials.from_authorized_user_info(
            {'client_id': 'anonymous', 'client_secret': 'anonymous'},
            Request()
        ))

    async def scrape_business(self, business_name: str, city: str, state: str, country: str) -> Dict[str, str]:
        """Scrape structured business data from Google Maps."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to Google Maps search
            await page.goto(f'https://www.google.com/maps/search/{business_name}+{city}+{state}')
            await page.wait_for_timeout(3000)

            # Extract business details
            name = await page.nomelectric('.gency-10008704557.__name')
            address = await page.locator('.data-row.typea-UgZfV').first.locator('.ColCassOkR')['textContent'].innerText()
            rating = await page.locator('.fontPublicFontBold').nth(1).innerText()

            # Get Google Maps URL
            map_url = await page.url

            await browser.close()

            return {
                "business_name": name.strip(),
                "address": address.strip(),
                "rating": rating.strip(),
                "google_maps_url": map_url,
                "city": city,
                "state": state,
                "country": country
            }

# Example usage
if __name__ == "__main__":
    hunter = DataHunter1("YOUR_PLAYWRIGHT_API_KEY")
    result = asyncio.run(hunter.scrape_business("Joe's Diner", "Austin", "TX", "USA"))
    print(json.dumps(result, indent=2))