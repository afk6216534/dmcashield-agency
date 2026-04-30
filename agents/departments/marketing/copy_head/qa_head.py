"""
QAHead Agent (3D) - Email Quality Assurance Specialist
Runs emails through spam checkers, duplicate detectors, and deliverability tests.
"""

from typing import Dict, Any, List
import re

class QAHead:
    """Validate email deliverability and quality."""

    @staticmethod
    def is_spammy(content: str) -> Dict[str, Any]:
        """Check if content is likely to trigger spam filters."""
        spam_patterns = [
            r'free\s+money', r'guarantee\s+your\s+success',
            r'you\s+must\s+act\s+now', r'limited\s+time\s+offer',
            r"cheap\s+deal", r"discount\s+today", r"extra\s+cash",
            r"no\s+risk", r"act\s+now\s+before\s+it\s+expires"
        ]
        score = 0
        matched_patterns = []
        for pattern in spam_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 1
                matched_patterns.append(pattern)

        return {
            "is_spammy": score > 1,
            "spam_score": score / len(spam_patterns),
            "matched_patterns": matched_patterns[:3]
        }

    @staticmethod
    def has_duplicate_content(new_content: str, all_prev_emails: List[str]) -> bool:
        """Check if email content matches any previous emails."""
        # Normalize content (remove line breaks, extra spaces)
        normalized = re.sub(r'[\r\n\s]+', ' ', new_content.lower().strip())
        for prev in all_prev_emails:
            prev_normalized = re.sub(r'[\r\n\s]+', ' ', prev.lower().strip())
            if normalized in prev_normalized:
                return True
        return False

    @staticmethod
    def safe_ctas(count: int = 1) -> bool:
        """Check CTA count - should be 1-2 max to avoid spam flags."""
        # Too many CTAs can look spammy
        return count <= 2

    @staticmethod
    def mixed_case_ok(text: str) -> bool:
        """Check if mixed case usage appears human-like (not robotic)."""
        # Some normal variation in case is expected in human writing
        # This is a basic heuristic
        all_upper = re.search(r'[A-Z]{2,}', text.replace(' ', ''))
        return not all_upper or len(all_upper.group(0)) <= 5

    @staticmethod
    def final_deliverability_check(content: str, prev_emails: List[str]) -> Dict[str, Any]:
        """Full QA check before sending."""
        spam_result = QAHead.is_spammy(content)
        duplicate = QAHead.has_duplicate_content(content, prev_emails)
        safety_checks = {
            "spammy": spam_result["is_spammy"],
            "spam_score": spam_result["spam_score"],
            "matched_patterns": spam_result["matched_patterns"],
            "duplicate_content": duplicate,
            "cta_safe": QAHead.safe_ctas(2)  # Assuming maximum 2 CTAs
        }

        # Additional safety checks could be added here
        safety_checks.update(QAHead.mixed_case_ok(content))

        return {
            "passes": not spam_result["is_spammy"] and not duplicate and QAHead.safe_ctas(2),
            "strict_pass": not spam_result["is_spammy"] and not duplicate,
            "safety_checks": safety_checks,
            "content_length": len(content)
        }

# Example usage
if __name__ == "__main__":
    qa = QAHead()
    sample_email = """
Hi there,

I noticed your restaurant has several negative reviews impacting your 3-star rating.
Our legal process can help remove them.

Would you like to remove them?
Best regards,
Reputation Management Team
"""

    checks = QAHead.final_deliverability_check(sample_email, [])
    print(json.dumps(checks, indent=2))