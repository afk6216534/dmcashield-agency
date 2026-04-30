"""
DataHunter-3 Agent - Phone & Social Media Extraction
Uses Apollo.io free tier and social media scraping for contact enrichment.
"""

import requests
from typing import Dict, Any, List

class DataHunter3:
    """Extract phone numbers and social media profiles."""

    def __init__(self, apollo_api_key: str = None):
        self.apollo_api_key = apollo_api_key
        self.apollo_base = "https://api.apollo.io/v1"

    def find_phone_and_socials(self, business_name: str,
                                address: str = None) -> Dict[str, Any]:
        """Find phone and social media from business name."""
        result = {
            "phone": None,
            "facebook": None,
            "instagram": None,
            "linkedin": None,
            "website": None
        }

        # Apollo.io search (if API key available)
        if self.apollo_api_key:
            try:
                response = requests.post(
                    f"{self.apollo_base}/organizations/search",
                    headers={"Authorization": f"Bearer {self.apollo_api_key}"},
                    json={
                        "q_organization_name": business_name,
                        "page": 1,
                        "per_page": 1
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    orgs = response.json().get("organizations", [])
                    if orgs:
                        org = orgs[0]
                        result["phone"] = org.get("phone")
                        result["website"] = org.get("website_url")
                        # Extract social profiles
                        if org.get("linkedin_url"):
                            result["linkedin"] = org["linkedin_url"]
            except Exception:
                pass

        # Fallback: Google search for social media
        # (In production, would use serpapi or similar)

        return result

# Example usage
if __name__ == "__main__":
    hunter3 = DataHunter3()
    result = hunter3.find_phone_and_socials("Joe's Diner", "123 Main St")
    print(result)