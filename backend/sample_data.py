"""
Sample Data Generator for DMCAShield System
Creates test leads, tasks, and email accounts for system testing.
"""

import json
from datetime import datetime

def generate_sample_leads():
    """Generate 10 sample leads for testing."""
    leads = []
    businesses = [
        {"name": "Joe's Diner", "type": "restaurant", "city": "Austin", "state": "TX", "rating": 3.2, "reviews": 14},
        {"name": "Smith Dental Care", "type": "dentist", "city": "Houston", "state": "TX", "rating": 2.8, "reviews": 23},
        {"name": "Glamour Salon", "type": "salon", "city": "Dallas", "state": "TX", "rating": 3.5, "reviews": 8},
        {"name": "City General Hospital", "type": "clinic", "city": "San Antonio", "state": "TX", "rating": 2.5, "reviews": 45},
        {"name": "Luxury Inn", "type": "hotel", "city": "Austin", "state": "TX", "rating": 3.0, "reviews": 31},
    ]
    
    for i, biz in enumerate(businesses, 1):
        lead = {
            "id": f"lead-00{i}",
            "business_name": biz["name"],
            "owner_name": f"Owner {i}",
            "email_primary": f"contact@business{i}.com",
            "phone": f"(512) 555-010{i}",
            "city": biz["city"],
            "state": biz["state"],
            "niche": biz["type"],
            "current_rating": biz["rating"],
            "negative_review_count": biz["reviews"],
            "temperature": "cold",
            "lead_score": 5,
            "status": "scraped"
        }
        leads.append(lead)
    
    return leads

def generate_sample_tasks():
    """Generate sample tasks."""
    tasks = [
        {"id": "task-001", "business_type": "restaurant", "city": "Austin", "state": "TX", "status": "active"},
        {"id": "task-002", "business_type": "dentist", "city": "Houston", "state": "TX", "status": "paused"},
        {"id": "task-003", "business_type": "salon", "city": "Dallas", "state": "TX", "status": "complete"}
    ]
    return tasks

def generate_sample_email_accounts():
    """Generate sample email accounts."""
    accounts = [
        {"id": "acc-001", "email": "marketing@dmcashield.com", "status": "active", "daily_limit": 40},
        {"id": "acc-002", "email": "outreach@dmcashield.com", "status": "warmup", "daily_limit": 15},
    ]
    return accounts

if __name__ == "__main__":
    print("Sample Leads:")
    print(json.dumps(generate_sample_leads(), indent=2))
    print("\nSample Tasks:")
    print(json.dumps(generate_sample_tasks(), indent=2))
    print("\nSample Accounts:")
    print(json.dumps(generate_sample_email_accounts(), indent=2))
