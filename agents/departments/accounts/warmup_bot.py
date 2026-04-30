"""
WarmupBot Agent - Email Account Warmup Manager
Manages account warmup schedule: 5→10→20→40 emails/day over 4 weeks.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

class WarmupBot:
    """Manages email account warmup to build sender reputation."""

    # Standard 4-week warmup schedule (emails per day)
    WARMUP_SCHEDULE = {
        "week_1": [5, 10, 15, 20, 25, 30, 35],       # Days 1-7
        "week_2": [40, 45, 50, 55, 60, 65, 70],      # Days 8-14
        "week_3": [80, 90, 100, 110, 120, 130, 140],  # Days 15-21
        "week_4": [40, 40, 40, 40, 40, 40, 40]       # Days 22-28 (active)
    }

    def __init__(self):
        self.accounts = {}

    def add_account(self, account_id: str, email: str) -> Dict[str, Any]:
        """Initialize account warmup state."""
        self.accounts[account_id] = {
            "email_address": email,
            "status": "warmup",
            "warmup_day": 1,
            "daily_limit": 5,  # Start with 5/day
            "sent_today": 0,
            "total_sent": 0,
            "health_score": 100,
            "created_at": datetime.utcnow().isoformat(),
            "next_increase": datetime.utcnow() + timedelta(days=1),
            "reputation": "building"
        }
        return self.accounts[account_id]

    def get_daily_limit(self, account_id: str, day: int = None) -> int:
        """Get current daily send limit for account."""
        if account_id not in self.accounts:
            return 0
        
        account = self.accounts[account_id]
        if account["status"] != "warmup":
            return account.get("daily_limit", 40)
        
        # Calculate limit based on warmup day
        day = day or account["warmup_day"]
        
        if day <= 7:
            limit = min(5 * day, 35)
        elif day <= 14:
            limit = min(40 + (day - 7) * 5, 70)
        elif day <= 21:
            limit = min(80 + (day - 14) * 10, 140)
        else:
            limit = 40  # Active sending at safe volume
        
        return limit

    def can_send_email(self, account_id: str) -> Dict[str, Any]:
        """Check if account can send email today."""
        if account_id not in self.accounts:
            return {"can_send": False, "reason": "account_not_found"}
        
        account = self.accounts[account_id]
        
        if account["status"] == "paused":
            return {"can_send": False, "reason": "account_paused"}
        
        if account["status"] == "blacklisted":
            return {"can_send": False, "reason": "account_blacklisted"}
        
        daily_limit = self.get_daily_limit(account_id)
        
        if account["sent_today"] >= daily_limit:
            return {
                "can_send": False,
                "reason": "daily_limit_reached",
                "limit": daily_limit,
                "sent_today": account["sent_today"]
            }
        
        return {
            "can_send": True,
            "limit": daily_limit,
            "remaining": daily_limit - account["sent_today"],
            "warmup_day": account["warmup_day"]
        }

    def record_send(self, account_id: str, success: bool = True) -> Dict[str, Any]:
        """Record an email send event."""
        if account_id not in self.accounts:
            return {"error": "account_not_found"}
        
        account = self.accounts[account_id]
        account["sent_today"] += 1
        account["total_sent"] += 1
        
        if not success:
            account["health_score"] -= 10
            if account["health_score"] < 30:
                account["status"] = "blacklisted"
        
        return {
            "account": account_id,
            "sent_today": account["sent_today"],
            "daily_limit": self.get_daily_limit(account_id),
            "health": account["health_score"]
        }

    def next_day(self, account_id: str) -> Dict[str, Any]:
        """Advance account to next warmup day."""
        if account_id not in self.accounts:
            return {"error": "account_not_found"}
        
        account = self.accounts[account_id]
        account["warmup_day"] += 1
        account["sent_today"] = 0
        
        # Check if warmup complete
        if account["warmup_day"] > 28:
            account["status"] = "active"
            account["reputation"] = "established"
        
        new_limit = self.get_daily_limit(account_id)
        account["daily_limit"] = new_limit
        
        return {
            "warmup_day": account["warmup_day"],
            "daily_limit": new_limit,
            "status": account["status"]
        }

# Example usage
if __name__ == "__main__":
    warmup = WarmupBot()
    acc = warmup.add_account("acc-001", "marketing@company.com")
    print(f"Day 1 limit: {warmup.get_daily_limit('acc-001', 1)}")
    print(f"Day 7 limit: {warmup.get_daily_limit('acc-001', 7)}")
    print(f"Day 30 limit: {warmup.get_daily_limit('acc-001', 30)}")
