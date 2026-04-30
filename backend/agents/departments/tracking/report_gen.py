from typing import Dict, List
from agents.base_agent import BaseAgent

class ReportGen(BaseAgent):
    def __init__(self):
        super().__init__("ReportGen")
        self.reports = []

    def generate_report(self) -> Dict:
        if not hasattr(self, 'open_tracker'):
            self.open_tracker = self._get_agent('OpenTracker')
            self.click_tracker = self._get_agent('ClickTracker')

        # Aggregate tracking data
        total_emails = len(self.open_tracker.tracking_data)
        opened_emails = len(self.open_tracker.tracking_data)
        total_clicks = len(self.click_tracker.clicks)

        # Generate actionable report
        report = {
            "metrics": {
                "emails_sent": total_emails,
                "emails_opened": opened_emails,
                "emails_clicked": total_clicks,
                "open_rate": round(opened_emails/total_emails*100, 1) if total_emails > 0 else 0,
                "click_rate": round(total_clicks/total_emails*100, 1) if total_emails > 0 else 0
            },
            "insights": [],
            "recommendations": []
        }

        # Generate insights based on metrics
        if report["metrics"]["open_rate"] < 20:
            report["insights"].append("Subject lines need optimization")
            report["recommendations"].append("A/B test new subject formats")

        if report["metrics"]["click_rate"] < 5:
            report["insights"].append("Call-to-action effectiveness is low")
            report["recommendations"].append("Revise CTA text and placement")

        self.reports.append(report)
        return report

    def start(self):
        return {"status": "online", "reports_generated": 0}

    def _get_agent(self, agent_name: str):
        """Mock function to access other agents in system (placeholder)"""
        agents_map = {
            'OpenTracker': self._get_agent_from_tracking(),
            'ClickTracker': self._get_agent_from_click_tracking()
        }
        return agents_map.get(agent_name, None)

    def _get_agent_from_tracking(self):
        return self  # Simplified reference