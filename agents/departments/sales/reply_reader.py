"""
ReplyReader Agent - Classifies incoming replies into intent categories
Determines if lead is INTERESTED, OBJECTION, NOT NOW, HOT LEAD, or SPAM.
"""

import re
from typing import Dict, Any

class ReplyReader:
    """Analyze email replies and classify intent."""

    # Keywords for classification (can be expanded with ML)
    INTERESTED_KEYWORDS = [
        "tell me more", "how does it work", "what is the cost",
        "can you explain", "interested", "sounds good", "yes",
        "please send", "more information", "details", "cost",
        "price", "fee", "how much", "schedule a call"
    ]

    OBJECTION_KEYWORDS = [
        "too expensive", "not interested", "we handle it ourselves",
        "don't need", "not now", "maybe later", "busy",
        "not a priority", "we are fine", "we don't need help"
    ]

    NOT_NOW_KEYWORDS = [
        "follow up later", "check back in", "next month",
        "quarter", "busy right now", "currently occupied",
        "not this month", "reconsider later"
    ]

    HOT_LEAD_KEYWORDS = [
        "let's talk", "when can we meet", "schedule a call",
        "yes, let's do it", "send me the contract", "ready to proceed",
        "how do we start", "what's next", "i want to move forward",
        "book a call", "call me", "phone me"
    ]

    SPAM_KEYWORDS = [
        "unsubscribe", "stop emailing", "remove me from list",
        "this is spam", "opt out"
    ]

    def classify_reply(self, reply_text: str) -> Dict[str, Any]:
        """Classify reply into one of the intent categories."""
        text_lower = reply_text.lower().strip()

        # Check for spam first (auto-unsubscribe requests)
        for keyword in self.SPAM_KEYWORDS:
            if keyword in text_lower:
                return {
                    "intent": "SPAM",
                    "confidence": 0.95,
                    "matched_keyword": keyword,
                    "suggested_action": "unsubscribe and stop sequence"
                }

        # Count matches for each category
        scores = {
            "INTERESTED": 0,
            "OBJECTION": 0,
            "NOT_NOW": 0,
            "HOT_LEAD": 0
        }

        matched_keywords = {}

        for intent, keywords in [
            ("INTERESTED", self.INTERESTED_KEYWORDS),
            ("OBJECTION", self.OBJECTION_KEYWORDS),
            ("NOT_NOW", self.NOT_NOW_KEYWORDS),
            ("HOT_LEAD", self.HOT_LEAD_KEYWORDS)
        ]:
            matches = [kw for kw in keywords if kw in text_lower]
            scores[intent] = len(matches)
            if matches:
                matched_keywords[intent] = matches

        # Determine primary intent
        if max(scores.values()) == 0:
            # No clear keywords, default to neutral
            return {
                "intent": "NEUTRAL",
                "confidence": 0.3,
                "matched_keywords": {},
                "suggested_action": "send next funnel email"
            }

        primary_intent = max(scores, key=scores.get)
        confidence = min(0.95, 0.5 + (scores[primary_intent] * 0.15))

        # Special logic: HOT_LEAD overrides others if strong signal
        if primary_intent == "HOT_LEAD" and scores["HOT_LEAD"] >= 2:
            suggested_action = "escalate to human - hot lead ready to talk"
        elif primary_intent == "INTERESTED":
            suggested_action = "send more information or schedule call"
        elif primary_intent == "OBJECTION":
            suggested_action = "address objection or send case study"
        elif primary_intent == "NOT_NOW":
            suggested_action = "schedule follow-up for later"
        else:
            suggested_action = "send next funnel email"

        return {
            "intent": primary_intent,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "suggested_action": suggested_action,
            "raw_reply": reply_text[:200]  # truncate for storage
        }

    def is_hot_lead(self, reply_text: str) -> bool:
        """Quick check if reply indicates hot lead."""
        result = self.classify_reply(reply_text)
        return result["intent"] == "HOT_LEAD" and result["confidence"] > 0.7

# Example usage
if __name__ == "__main__":
    reader = ReplyReader()
    test_replies = [
        "Yes, I'm interested! How much does it cost?",
        "We handle our reviews ourselves, thanks.",
        "Can you follow up next month?",
        "Let's schedule a call for tomorrow to discuss.",
        "Please unsubscribe me from your list."
    ]
    for reply in test_replies:
        print(f"Reply: {reply}")
        print(f"Classification: {reader.classify_reply(reply)}")
        print("-" * 50)
