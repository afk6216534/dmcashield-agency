"""
CopyWriter Agent (3C) - Personalized Email Generation
Creates 100-200 word emails with human-like tone and specific personalization.
Uses OpenRouter free models for generation.
"""

import json
import os
from typing import Dict, Any, List
from openai import OpenAI  # Using OpenAI-compatible client for OpenRouter

class CopyWriter:
    """Generates personalized email content."""

    def __init__(self, openrouter_api_key: str = None):
        self.api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        self.model = "mistralai/mistral-7b-instruct"  # Free tier

    def generate_email(self, lead_profile: Dict[str, Any],
                      funnel_stage: str,
                      angle: str,
                      email_number: int) -> Dict[str, Any]:
        """Generate a personalized email for the lead."""

        # Construct prompt
        prompt = self._build_prompt(lead_profile, funnel_stage, angle, email_number)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional copywriter for a DMCA review removal service. Write emails that are 150-200 words, sound human (not AI), use emotional triggers, and include clear CTAs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            email_content = response.choices[0].message.content.strip()

            # Extract subject line (assume first line is subject)
            lines = email_content.split('\n')
            subject_line = lines[0].replace('Subject:', '').strip()
            body = '\n'.join(lines[1:]).strip()

            # Clean up
            if not subject_line or len(subject_line) > 80:
                subject_line = self._generate_subject_line(lead_profile, angle)

            return {
                "subject_line": subject_line,
                "email_body": body,
                "word_count": len(body.split()),
                "angle": angle,
                "stage": funnel_stage,
                "email_number": email_number,
                "personalization_score": self._calc_personalization(body, lead_profile)
            }

        except Exception as e:
            return {
                "error": str(e),
                "subject_line": f"Quick question about {lead_profile.get('business_name', 'your business')}",
                "email_body": self._fallback_email(lead_profile, angle),
                "word_count": 150
            }

    def _build_prompt(self, lead: Dict[str, Any], stage: str, angle: str, num: int) -> str:
        """Build generation prompt."""
        return f"""
Write email #{num} for a {stage} funnel stage with angle: {angle}

Business: {lead.get('business_name')}
Owner: {lead.get('owner_name', 'Owner')}
Rating: {lead.get('current_rating')} stars
Negative reviews: {lead.get('negative_review_count')}
Worst review sample: {lead.get('worst_reviews', [''])[0] if lead.get('worst_reviews') else ''}
Competitors: {json.dumps(lead.get('competitor_info', {}).get('competitors', []))}

Make it personal, mentioning their business name and specific review issue.
Use {angle} as the main emotional trigger.
Length: 150-200 words. Sound human, not robotic.
Include a clear single CTA.
"""

    def _generate_subject_line(self, lead: Dict[str, Any], angle: str) -> str:
        """Generate A/B test subject lines."""
        templates = {
            "reputation": f"Your {lead.get('current_rating')}-star rating is costing you customers",
            "competitor": f"While {lead.get('business_name')} struggles, [Competitor] gains customers",
            "review_impact": f"Those {lead.get('negative_review_count')} bad reviews are worth ${lead.get('estimated_loss', 'thousands')}",
            "offer": f"Free audit for {lead.get('business_name')}",
            "case_study": f"How we helped a similar {lead.get('niche')} remove 12 bad reviews",
            "urgency": f"Last chance: Google review relief for {lead.get('business_name')}"
        }
        return templates.get(angle, f"Quick question about {lead.get('business_name')}")

    def _fallback_email(self, lead: Dict[str, Any], angle: str) -> str:
        """Fallback email if AI generation fails."""
        return f"""
Hi {lead.get('owner_name', 'there')},

I noticed {lead.get('business_name')} has {lead.get('negative_review_count')} negative reviews impacting your {lead.get('current_rating')}-star rating. 

Many {lead.get('niche')} businesses lose 15-30% of potential customers due to bad reviews. We specialize in legally removing fake or harmful reviews through DMCA processes.

Would you be open to a 10-minute call to see how we can help restore your online reputation?

Best,
[Your Name]
"""

    def _calc_personalization(self, body: str, lead: Dict[str, Any]) -> float:
        """Calculate personalization score (0-10)."""
        score = 0
        if lead.get('business_name') in body:
            score += 3
        if lead.get('owner_name') and lead.get('owner_name') in body:
            score += 2
        if lead.get('niche') and lead.get('niche') in body:
            score += 2
        if str(lead.get('negative_review_count')) in body:
            score += 1
        if str(lead.get('current_rating')) in body:
            score += 1
        # Check for specific review mention
        if lead.get('worst_reviews') and body in lead.get('worst_reviews')[0][:50]:
            score += 1
        return min(score, 10)

# Example usage
if __name__ == "__main__":
    writer = CopyWriter()
    sample_lead = {
        "business_name": "Joe's Diner",
        "owner_name": "Joe Smith",
        "current_rating": 3.2,
        "negative_review_count": 14,
        "niche": "restaurant",
        "worst_reviews": ["The food was cold and service was terrible..."],
        "competitor_info": {"competitors": [{"name": "Burger Barn", "rating": 4.5}]}
    }
    result = writer.generate_email(sample_lead, "intro", "reputation", 1)
    print(json.dumps(result, indent=2))
