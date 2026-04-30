"""
ReportGen Agent - Automated Reporting System
Generates daily/weekly reports for dashboard and email alerts.
"""

import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

class ReportGen:
    """Generate automated reports for monitoring."""

    def __init__(self):
        self.report_templates = {}

    def daily_summary(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Generate daily operations summary."""
        return {
            "report_type": "daily_summary",
            "date": datetime.utcnow().date().isoformat(),
            "system_health": stats.get("departments_status", {}),
            "lead_metrics": {
                "new_leads": stats.get("new_leads_today", 0),
                "total_leads": stats.get("total_leads", 0),
                "hot_leads": stats.get("hot_leads", 0)
            },
            "email_metrics": {
                "emails_sent": stats.get("emails_sent_today", 0),
                "open_rate": stats.get("open_rate", 0),
                "reply_rate": stats.get("reply_rate", 0)
            },
            "key_alerts": self._generate_alerts(stats),
            "recommendations": self._generate_recommendations(stats)
        }

    def weekly_performance(self, weekly_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weekly performance report."""
        return {
            "report_type": "weekly_performance",
            "week_ending": datetime.utcnow().date().isoformat(),
            "conversion_funnel": {
                "leads_scraped": weekly_stats.get("leads_scraped", 0),
                "leads_emailed": weekly_stats.get("leads_emailed", 0),
                "leads_opened": weekly_stats.get("leads_opened", 0),
                "leads_replied": weekly_stats.get("leads_replied", 0),
                "hot_leads": weekly_stats.get("hot_leads", 0),
                "converted_leads": weekly_stats.get("converted_leads", 0)
            },
            "department_performance": weekly_stats.get("department_efficiency", {}),
            "email_account_health": weekly_stats.get("account_health", {}),
            "top_performing_content": weekly_stats.get("top_content", {})
        }

    def _generate_alerts(self, stats: Dict[str, Any]) -> List[str]:
        """Generate priority alerts based on current stats."""
        alerts = []
        if stats.get("open_rate", 0) < 20:
            alerts.append("LOW OPEN RATE: Consider A/B testing subject lines")
        if stats.get("reply_rate", 0) < 5:
            alerts.append("LOW REPLY RATE: Review email personalization")
        if stats.get("blacklisted_accounts", 0) > 0:
            alerts.append(f"{stats['blacklisted_accounts']} EMAIL ACCOUNTS BLACKLISTED")
        if stats.get("queue_depth", 0) > 1000:
            alerts.append("HIGH EMAIL QUEUE: Consider scaling sender workers")
        return alerts

    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recs = []
        if stats.get("hot_leads", 0) > 5:
            recs.append("Consider increasing sales team capacity")
        if stats.get("avg_response_time", 0) > 3600:  # 1 hour
            recs.append("Improve reply response time for better conversion")
        return recs

# Example usage
if __name__ == "__main__":
    reporter = ReportGen()
    daily_stats = {
        "departments_status": {"scraping": "online", "validation": "online"},
        "new_leads_today": 125,
        "total_leads": 2450,
        "hot_leads": 8,
        "emails_sent_today": 85,
        "open_rate": 34.2,
        "reply_rate": 12.5
    }
    summary = reporter.daily_summary(daily_stats)
    print(json.dumps(summary, indent=2))
