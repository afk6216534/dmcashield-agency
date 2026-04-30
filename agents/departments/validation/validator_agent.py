"""
ValidatorAgent - Data Cleaning and Basic Validation
Removes duplicates, fixes formatting, validates all fields.
"""

import re
from typing import Dict, Any, List

class ValidatorAgent:
    """Clean and validate lead data."""

    @staticmethod
    def clean_business_name(name: str) -> str:
        """Remove extra spaces, standardize capitalization."""
        if not name:
            return ""
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name.strip())
        # Title case (but preserve known acronyms like LLC, Inc, etc.)
        # Simple approach: title case, then fix known cases
        name = name.title()
        # Fix common business suffixes
        suffixes = ['Llc', 'Inc', 'Corp', 'Ltd', 'Ll', 'Co']
        for suffix in suffixes:
            name = re.sub(rf'\b{suffix}\b', suffix.upper(), name)
        return name

    @staticmethod
    def standardize_address(address: str) -> str:
        """Standardize address format."""
        if not address:
            return ""
        # Remove extra spaces
        address = re.sub(r'\s+', ' ', address.strip())
        # Title case
        address = address.title()
        return address

    @staticmethod
    def validate_and_clean_email(email: str) -> Dict[str, Any]:
        """Validate email format and clean."""
        if not email:
            return {"valid": False, "cleaned": "", "reason": "empty"}
        email = email.strip().lower()
        # Basic email regex
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return {"valid": False, "cleaned": "", "reason": "invalid_format"}
        # Split and clean local part and domain
        local, domain = email.split('@')
        # Remove any dots in local part? (Gmail ignores dots, but we keep as is for uniqueness)
        # We'll just return as is
        return {"valid": True, "cleaned": email, "reason": "valid"}

    @staticmethod
    def remove_duplicates(leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate leads based on email or business name+address."""
        seen = set()
        unique_leads = []
        for lead in leads:
            # Create a key from email if available, else from business name and address
            email = lead.get("email_primary", "").lower()
            if email and email != "":
                key = f"email:{email}"
            else:
                name = lead.get("business_name", "").lower().strip()
                addr = lead.get("address", "").lower().strip()
                key = f"name_addr:{name}|{addr}"
            if key not in seen:
                seen.add(key)
                unique_leads.append(lead)
        return unique_leads

    @staticmethod
    def validate_lead_structure(lead: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure lead has all required fields and correct types."""
        required_fields = [
            "business_name", "owner_name", "email_primary", "phone",
            "address", "city", "state", "country", "google_maps_url"
        ]
        missing = []
        for field in required_fields:
            if not lead.get(field):
                missing.append(field)
        # We'll allow some fields to be optional in practice, but flag for review
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "warnings": []  # Could add warnings for low confidence, etc.
        }

# Example usage
if __name__ == "__main__":
    validator = ValidatorAgent()
    # Test cleaning
    dirty_name = "  joe's diner llc  "
    clean_name = validator.clean_business_name(dirty_name)
    print(f"Cleaned name: '{clean_name}'")
    # Test email validation
    email_result = validator.validate_and_clean_email("  Info@JoeS.Diner.Com  ")
    print(f"Email result: {email_result}")