"""
CompetitorSpy Agent - Competitive Intelligence
Finds local competitors and their Google ratings to use in email persuasion.
"""

import json
from typing import Dict, Any, List
from googleapiclient.discovery import build

class CompetitorSpyAgent:
    """Find and analyze competitors for a given business."""

    def __init__(self, google_api_key: str):
        self.service = build('places', 'v1', developerKey=google_api_key)

    def find_competitors(self, business: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find top 5 local competitors based on category and location."""
        # In a real system, would query Google Places API
        # This is a simplified implementation
        categories = self._infer_categories(business)
        competitors = []
        for cat in categories:
            # Simulated competitor search
            # Replace with actual Places API call in production
            pass
        return competitors

    def _infer_categories(self, business: Dict[str, Any]) -> List[str]:
        """Infer Google Places categories from business data."""
        name_lower = business.get("business_name", "").lower()
        niche = business.get("niche", "").lower()
        # Map common keywords to categories
        category_map = {
            "restaurant": ["restaurant", "food"],
            "dentist": ["dentist", "dental_care"],
            "salon": ["hair_salon", "beauty_salon"],
            "hotel": ["lodging", "hotel"],
            "clinic": ["doctor", "health"]
        }
        for key, cats in category_map.items():
            if key in name_lower or key in niche:
                return cats
        return ["local_business"]

    def analyze_competitor_ratings(self, competitors: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze rating distributions across competitors."""
        if not competitors:
            return {"average_rating": 0, "best_rating": 0, "worst_rating": 0}
        ratings = [c.get("rating", 0) for c in competitors]
        return {
            "average_rating": sum(ratings) / len(ratings) if ratings else 0,
            "best_rating": max(ratings) if ratings else 0,
            "worst_rating": min(ratings) if ratings else 0,
            "competitor_count": len(competitors)
        }

# Example usage
if __name__ == "__main__":
    # Example business
    biz = {
        "business_name": "Joe's Diner",
        "niche": "restaurant"
    }
    spy = CompetitorSpyAgent("YOUR_GOOGLE_API_KEY")
    categories = spy._infer_categories(biz)
    print(f"Inferred categories: {categories}")