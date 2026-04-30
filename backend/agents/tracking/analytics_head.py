from datetime import datetime
from typing import Dict, List

class AnalyticsHeadAgent:
    def __init__(self):
        self.name = "AnalyticsHead"
        self.team = ["OpenTracker", "ClickTracker", "ReplyDetector", "InsightBot"]

    def track_email_opened(self, record_id: str, ip_address: str = None):
        from database.models import SessionLocal, EmailRecord
        db = SessionLocal()
        try:
            record = db.query(EmailRecord).filter(EmailRecord.id == record_id).first()
            if record:
                record.opened_count += 1
                record.first_open = record.first_open or datetime.utcnow()
                db.commit()
        finally:
            db.close()

    def track_link_click(self, record_id: str):
        from database.models import SessionLocal, EmailRecord
        db = SessionLocal()
        try:
            record = db.query(EmailRecord).filter(EmailRecord.id == record_id).first()
            if record:
                record.clicked_link = True
                db.commit()
        finally:
            db.close()

    def calculate_lead_temperature(self, lead_id: str) -> str:
        from database.models import SessionLocal, EmailRecord, Lead
        db = SessionLocal()
        try:
            records = db.query(EmailRecord).filter(EmailRecord.lead_id == lead_id).all()
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            
            if not records:
                return "cold"
            
            total_opens = sum(r.opened_count for r in records)
            total_replied = sum(1 for r in records if r.replied)
            
            if total_replied > 0:
                return "hot"
            elif total_opens >= 3:
                return "warm"
            elif total_opens >= 1:
                return "warm"
            else:
                return "cold"
        finally:
            db.close()

    def get_best_performers(self, limit: int = 5) -> Dict:
        from database.models import SessionLocal, EmailRecord
        
        db = SessionLocal()
        try:
            records = db.query(EmailRecord).all()
            
            subject_performance = {}
            for r in records:
                if r.subject_line not in subject_performance:
                    subject_performance[r.subject_line] = {
                        "opens": 0,
                        "clicks": 0,
                        "replies": 0,
                        "count": 0
                    }
                subject_performance[r.subject_line]["opens"] += r.opened_count
                subject_performance[r.subject_line]["clicks"] += 1 if r.clicked_link else 0
                subject_performance[r.subject_line]["replies"] += 1 if r.replied else 0
                subject_performance[r.subject_line]["count"] += 1
            
            best = sorted(
                subject_performance.items(),
                key=lambda x: x[1]["opens"],
                reverse=True
            )[:limit]
            
            return [{"subject": s, **data} for s, data in best]
        finally:
            db.close()

    def start(self):
        return {"status": "online", "team": self.team}

analytics_head = AnalyticsHeadAgent()