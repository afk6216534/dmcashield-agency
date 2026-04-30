"""
PatternFinder Agent - Recognizes Winning Patterns
Analyzes campaign data to identify what works best.
"""

import json
from typing import Dict, Any, List
from collections import Counter

class PatternFinder:
    """Find patterns in successful campaigns."""

    def __init__(self):
        self.success_patterns = []
        self.failure_patterns = []

    def analyze_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single campaign for patterns."""
        open_rate = campaign_data.get("open_rate", 0)
        reply_rate = campaign_data.get("reply_rate", 0)
        subject_style = campaign_data.get("subject_style", "")
        body_style = campaign_data.get("body_style", "")
        send_time = campaign_data.get("send_time", "")

        # Classify as success or failure
        if open_rate > 35 and reply_rate > 15:
            category = "success"
        elif open_rate < 20 or reply_rate < 5:
            category = "failure"
        else:
            category = "neutral"

        pattern = {
            "campaign_id": campaign_data.get("id"),
            "category": category,
            "open_rate": open_rate,
            "reply_rate": reply_rate,
            "subject_style": subject_style,
            "body_style": body_style,
            "send_time": send_time,
            "niche": campaign_data.get("niche", ""),
            "email_number": campaign_data.get("email_number", 0)
        }

        if category == "success":
            self.success_patterns.append(pattern)
        elif category == "failure":
            self.failure_patterns.append(pattern)

        return pattern

    def get_top_patterns(self, metric: str = "open_rate", top_n: int = 5) -> List[Dict[str, Any]]:
        """Get top performing patterns by metric."""
        sorted_patterns = sorted(
            self.success_patterns,
            key=lambda x: x.get(metric, 0),
            reverse=True
        )
        return sorted_patterns[:top_n]

    def find_best_send_time(self, niche: str = None) -> Dict[str, Any]:
        """Find optimal send time based on historical data."""
        patterns = self.success_patterns
        if niche:
            patterns = [p for p in patterns if p.get("niche") == niche]

        if not patterns:
            return {"best_time": "09:00", "confidence": 0.5}

        time_counter = Counter(p.get("send_time") for p in patterns)
        best_time = time_counter.most_common(1)[0][0]
        confidence = time_counter.most_common(1)[0][1] / len(patterns)

        return {
            "best_time": best_time,
            "confidence": confidence,
            "sample_size": len(patterns)
        }

# Example usage
if __name__ == "__main__":
    finder = PatternFinder()
    campaigns = [
        {"id": "c1", "open_rate": 42.5, "reply_rate": 18.3, "subject_style": "curiosity", "send_time": "09:30", "niche": "restaurant"},
        {"id": "c2", "open_rate": 28.1, "reply_rate": 8.7, "subject_style": "direct", "send_time": "14:00", "niche": "dentist"}
    ]
    for c in campaigns:
        finder.analyze_campaign(c)
    print(json.dumps(finder.find_best_send_time("restaurant"), indent=2))
