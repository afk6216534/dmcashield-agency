"""
InsightBot Agent - Analytics and Reporting
Generates weekly intelligence reports for all departments.
"""

import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

class InsightBot:
    """Analyzes tracking data and generates optimization insights."""

    def __init__(self):
        self.report_cache = {}

    def generate_weekly_report(self, tracking_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create weekly intelligence report from tracking data."""
        # In production, would query database for last week's data
        # This is simplified for demonstration
        
        if not tracking_data:
            return {"error": "No tracking data available"}

        # Analyze open rates by subject line pattern
        subject_performance = {}
        body_performance = {}
        time_performance = {}

        for record in tracking_data:
            subject = record.get("subject_line", "")
            body_style = record.get("body_style", "standard")
            send_time = record.get("send_time", "")
            opened = record.get("opened", False)
            replied = record.get("replied", False)

            # Subject line analysis
            if subject not in subject_performance:
                subject_performance[subject] = {"sent": 0, "opened": 0}
            subject_performance[subject]["sent"] += 1
            if opened:
                subject_performance[subject]["opened"] += 1

            # Body style analysis
            if body_style not in body_performance:
                body_performance[body_style] = {"sent": 0, "replied": 0}
            body_performance[body_style]["sent"] += 1
            if replied:
                body_performance[body_style]["replied"] += 1

            # Time analysis (hour of day)
            hour = int(send_time.split(":")[0]) if send_time and ":" in send_time else 12
            hour_bucket = f"{(hour//2)*2:02d}-{(hour//2)*2+2:02d}"
            if hour_bucket not in time_performance:
                time_performance[hour_bucket] = {"sent": 0, "opened": 0}
            time_performance[hour_bucket]["sent"] += 1
            if opened:
                time_performance[hour_bucket]["opened"] += 1

        # Calculate rates
        best_subject = max(
            ((k, v["opened"]/v["sent"]) for k, v in subject_performance.items() if v["sent"] > 0),
            key=lambda x: x[1], default=("", 0)
        )
        best_body = max(
            ((k, v["replied"]/v["sent"]) for k, v in body_performance.items() if v["sent"] > 0),
            key=lambda x: x[1], default=("", 0)
        )
        best_time = max(
            ((k, v["opened"]/v["sent"]) for k, v in time_performance.items() if v["sent"] > 0),
            key=lambda x: x[1], default=("", 0)
        )

        # Calculate overall metrics
        total_sent = len(tracking_data)
        total_opened = sum(1 for t in tracking_data if t.get("opened", False))
        total_replied = sum(1 for t in tracking_data if t.get("replied", False))

        return {
            "report_period": "last_7_days",
            "total_emails_sent": total_sent,
            "open_rate": round(total_opened/total_sent*100, 2) if total_sent > 0 else 0,
            "reply_rate": round(total_replied/total_sent*100, 2) if total_sent > 0 else 0,
            "best_performing_subject": {
                "pattern": best_subject[0],
                "open_rate": round(best_subject[1]*100, 2)
            },
            "best_performing_body": {
                "style": best_body[0],
                "reply_rate": round(best_body[1]*100, 2)
            },
            "best_send_time": {
                "time_range": best_time[0],
                "open_rate": round(best_time[1]*100, 2)
            },
            "recommendations": [
                f"Use subject lines similar to '{best_subject[0]}' for higher opens",
                f"Adopt '{best_body[0]}' email style for better replies",
                f"Schedule sends during {best_time[0]} for optimal engagement"
            ]
        }

# Example usage
if __name__ == "__main__":
    insight = InsightBot()
    # Simulated data
    sample_data = [
        {"subject_line": "Quick question about your business", "opened": True, "replied": False, "send_time": "09:30"},
        {"subject_line": "Can I help improve your rating?", "opened": False, "replied": False, "send_time": "14:15"},
        {"subject_line": "Those negative reviews are costing you customers", "opened": True, "replied": True, "send_time": "10:00"}
    ]
    report = insight.generate_weekly_report(sample_data)
    print(json.dumps(report, indent=2))
