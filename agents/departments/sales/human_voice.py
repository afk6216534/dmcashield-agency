"""
HumanVoice Agent - Writes human-like email replies
Ensures AI responses sound natural, not robotic. Never reveals AI identity.
"""

import re
from typing import Dict, Any

class HumanVoice:
    """Generate human-like email replies."""

    @staticmethod
    def generate_reply(lead_data: Dict[str, Any], 
                       original_reply: str,
                       intent: str) -> Dict[str, Any]:
        """Generate a human-sounding reply based on intent."""
        
        business_name = lead_data.get("business_name", "your business")
        owner_name = lead_data.get("owner_name", "there")
        niche = lead_data.get("niche", "business")
        
        # Templates based on intent
        templates = {
            "INTERESTED": f"""Hi {owner_name},

Thanks for your interest! I'd be happy to explain how our DMCA process works.

We've helped over 500 {niche} businesses remove fake or harmful reviews legally. The process typically takes 7-14 days once we start.

Would you have 10 minutes this week for a quick call? I can show you exactly how we'd help {business_name}.

Best,
[Your Name]""",
            
            "OBJECTION": f"""Hi {owner_name},

I completely understand - managing your online reputation is something many businesses handle internally.

What most owners don't realize is that Google's algorithms automatically penalize businesses with multiple negative reviews, even if they're fake. One of our clients in {niche} lost 30% of new customer inquiries before working with us.

No pressure at all - just wanted to make sure you had the facts. If you ever want to discuss, my door is open.

Best,
[Your Name]""",
            
            "NOT_NOW": f"""Hi {owner_name},

Totally understand - things are busy! I'll circle back in about 6 weeks when things settle down.

In the meantime, if those negative reviews start impacting your new customer calls, just reply to this email and we can chat.

Best,
[Your Name]""",
            
            "HOT_LEAD": f"""Hi {owner_name},

Fantastic! I'm excited to help {business_name} get back to a 5-star rating.

Let's schedule a brief 10-minute call this week. What day works best for you - Tuesday afternoon or Thursday morning?

I'll send over a calendar invite once you let me know.

Looking forward to speaking with you,
[Your Name]""",
            
            "NEUTRAL": f"""Hi {owner_name},

Thanks for getting back to me!

I'd love to share how we've helped other {niche} businesses in {lead_data.get('city', 'your area')} improve their online reputation.

Would you be open to a brief 10-minute chat this week?

Best,
[Your Name]"""
        }
        
        reply_text = templates.get(intent, templates["NEUTRAL"])
        
        # Post-process to sound more human
        reply_text = HumanVoice._humanize(reply_text)
        
        return {
            "reply_text": reply_text,
            "intent": intent,
            "word_count": len(reply_text.split()),
            "tone": "professional_friendly",
            "cta_included": True,
            "human_score": HumanVoice._calc_human_score(reply_text)
        }
    
    @staticmethod
    def _humanize(text: str) -> str:
        """Add human-like elements to text."""
        # Remove any robotic patterns
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        # Ensure contractions are natural
        text = text.replace("I am", "I'm").replace("You are", "You're")
        text = text.replace("We are", "We're").replace("That is", "That's")
        return text.strip()
    
    @staticmethod
    def _calc_human_score(text: str) -> float:
        """Calculate how human-like the text sounds (0-10)."""
        score = 5.0
        
        # Check for contractions (human trait)
        if re.search(r"\b(I'm|you're|we're|that's|it's|don't|can't)\b", text, re.IGNORECASE):
            score += 2
            
        # Check for casual phrases
        casual = ["thanks", "totally", "actually", "just", "by the way"]
        for phrase in casual:
            if phrase in text.lower():
                score += 0.5
                
        # Check sentence variety
        sentences = re.split(r'[.!?]\s+', text)
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if 8 <= avg_len <= 20:
            score += 1.5
            
        return min(score, 10.0)

# Example usage
if __name__ == "__main__":
    voice = HumanVoice()
    sample_lead = {
        "business_name": "Joe's Diner",
        "owner_name": "Joe Smith",
        "niche": "restaurant",
        "city": "Austin"
    }
    result = voice.generate_reply(sample_lead, "Yes I'm interested!", "HOT_LEAD")
    print(result["reply_text"])
