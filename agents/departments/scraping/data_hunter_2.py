"""
DataHunter-2 Agent - Email Extraction
Uses Hunter.io (free tier) to locate primary email addresses for businesses.
"""

import json
import requests
from typing import Dict, Any

class DataHunter2:
    """Extract primary email address using Hunter.io API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hunter.io/v2/domain-search"

    def find_email(self, domain: str) -> Dict[str, Any]:
        """Return the most confidence email for the given domain."""
        params = {"domain": domain, "api_key": self.api_key, "limit": 1}
        response = requests.get(self.base_url, params=params, timeout=30)
        if response.status_code != 200:
            return {"error": f"Hunter.io request failed ({response.status_code})"}
        data = response.json()
        emails = data.get("data", {}).get("emails", [])
        if not emails:
            return {"email": None, "confidence": 0}
        best = emails[0]
        return {"email": best.get("value"), "confidence": best.get("score", 0)}

# Example usage
if __name__ == "__main__":
    hunter = DataHunter2("YOUR_HUNTER_IO_API_KEY")
    result = hunter.find_email("example.com")
    print(json.dumps(result, indent=2))