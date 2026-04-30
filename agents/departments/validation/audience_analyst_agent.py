"""
AudienceAnalyst Agent - Psychological Profiling
Analyzes review sentiment to determine emotional triggers and customer motivations.
"""

import json
import re
from collections import Counter
from typing import Dict, Any

class AudienceAnalystAgent:
    """Analyze customer reviews to extract emotional triggers."""

    POSITIVE_WORDS = {"best", "excellent", "amazing", "great", "love", "love it",
                     "love this", "wonderful", "fantastic", "perfect", "enjoy", "enjoyed"}
    NEGATIVE_WORDS = {"terrible", "awful", "horrible", "disgusting", "bad", "poor",
                     "waste", "hate", "hated", "broke", "broken"}
    URGENCY_WORDS = {"immediately", "now", "quickly", "instant", "asap"}

    def __init__(self):
        self.sentiment_keywords = {
            "positive": self.POSITIVE_WORDS,
            "negative": self.NEGATIVE_WORDS,
            "urgency": self.URGENCY_WORDS
        }

    def analyze_reviews(self, reviews: List[str]) -> Dict[str, Any]:
        """Analyze sentiment across customer reviews."""
        # Combine all reviews into single string for analysis
        combined_reviews = " ".join(reviews).lower()

        # Count occurrences of keywords
        sentiment_scores = {
            "positive": 0,
            "negative": 0,
            "urgency": 0
        }

        words = combined_reviews.split()
        for word in words:
            if word in self.NEGATIVE_WORDS:
                sentiment_scores["negative"] += 1
            elif word in self.POSITIVE_WORDS:
                sentiment_scores["positive"] += 1
            elif word in self.URGENCY_WORDS:
                sentiment_scores["urgency"] += 1

        # Determine dominant emotion
        max_score = max(sentiment_scores.values())
        dominant_emotion = max(sentiment_scores.keys(), key=lambda x: sentiment_scores[x])

        # Calculate sentiment ratios
        total_keywords = sum(sentiment_scores.values())
        ratios = {k: v/total_keywords if total_keywords > 0 else 0 for k, v in sentiment_scores.items()}

        # Extract common complaint themes (simplified)
        complaint_themes = [
            "long wait", "slow service", "expensive", "cold food", "poor quality",
            "rude staff", "dirty", "broken", "didn't work"
        ]
        found_themes = [theme for theme in complaint_themes
                       if theme in combined_reviews.lower()]

        return {
            "sentiment_ratios": sentiment_scores,
            "dominant_emotion": dominant_emotion,
            "overall_sentiment": "negative" if sentiment_scores["negative"] > sentiment_scores["positive"]
                            else "positive" if sentiment_scores["positive"] > sentiment_scores["negative"]
                            else "neutral",
            "emotional_trigger": dominant_emotion,
            "found_complaint_themes": found_themes,
            "average_length_per_review": len(combined_reviews) / (len(reviews) or 1)
        }

# Example usage
if __name__ == "__main__":
    sample_reviews = [
        "Bad service and the food was cold. Took forever to get our order.",
        "Love this place! Food is amazing and staff is super friendly!",
        "Terrible experience - food was cold and service was awful.",
        "Great place, will come back!"
    ]
    analyst = AudienceAnalystAgent()
    result = analyst.analyze_reviews(sample_reviews)
    print(json.dumps(result, indent=2))