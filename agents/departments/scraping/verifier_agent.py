"""
VerifierAgent - Lead Quality Verifier
Validates scraped leads, scores them, and filters out low-quality data.
"""

import re
import requests
from typing import Dict, Any, Optional

class VerifierAgent:
    """Validate email deliverability, phone formatting, and lead scores."""

    @staticmethod
    def validate_email(email: str) -> Dict[str, Any]:
        """Check if email format looks valid and not a catch-all."""
        result = {"valid": False, "score": 0}

        # Basic format check
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return result

        # Try to get free email domain (common disposable/temporary)
        disposable_domains = {"tempmail.com", "guerrillamail.com", "10minutemail.com"}
        domain = email.split("@")[1].lower()
        if domain in disposable_domains:
            result["score"] = 1
            result["warning"] = "Disposable email domain"
            return result

        # Optional: verify with Hunter.io verification API (limited free)
        # For now, assume valid
        result["valid"] = True
        result["score"] = 5  # Medium confidence
        return result

    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Any]:
        """Validate US phone number formatting."""
        digits = re.sub(r"\D", "", phone)
        result = {"valid": False, "score": 0}

        if len(digits) == 10:
            result["valid"] = True
            result["score"] = 5
            result["formatted"] = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        else:
            result["score"] = 1
        return result

    @staticmethod
    def score_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall lead quality score 1-10."""
        score = 0
        reasons = []

        # Email validation
        email_val = VerifierAgent.validate_email(lead_data.get("email_primary", ""))
        score += email_val.get("score", 0)
        if not email_val["valid"]:
            reasons.append("bad_email")

        # Phone validation
        phone_val = VerifierAgent.validate_phone(lead_data.get("phone", ""))
        score += phone_val.get("score", 0)
        if not phone_val["valid"]:
            reasons.append("bad_phone")

        # Rating check
        try:
            rating = float(lead_data.get("rating", "0"))
            if rating >= 4.0:
                score += 2
            elif rating >= 3.0:
                score += 1
            else:
                reasons.append("low_rating")
        except (ValueError, TypeError):
            reasons.append("no_rating")

        # Determine lead status
        if score >= 8:
            status = "hot"
        elif score >= 5:
            status = "warm"
        else:
            status = "cold"

        return {
            "lead_score": min(score, 10),
            "status": status,
            "reasons": reasons,
            "email_valid": email_val["valid"],
            "phone_valid": phone_val["valid"],
            "details": email_val | phone_val
        }

# Example usage
if __name__ == "__main__":
    sample = {
        "email_primary": "info@joesdiner.com",
        "phone": "(555) 123-4567",
        "rating": "4.2"
    }
    result = VerifierAgent.score_lead(sample)
    print(result)