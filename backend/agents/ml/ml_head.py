from datetime import datetime
from typing import Dict, List, Any

from agents.memory.agent_brain import memory_system

class MLHeadAgent:
    def __init__(self):
        self.name = "MLHead"
        self.brain = memory_system.get_brain(self.name)
        self.patterns = {}
        self.learning_loop_count = 0

    def analyze_email_performance(self) -> Dict:
        from database.models import SessionLocal, EmailRecord
        
        db = SessionLocal()
        try:
            emails = db.query(EmailRecord).all()
            
            if not emails:
                return {"message": "No email data to analyze yet"}
            
            subject_scores = {}
            body_scores = {}
            
            for email in emails:
                subject = email.subject_line
                open_count = email.opened_count
                replied = email.replied
                
                score = (open_count * 2) + (replied * 10)
                
                if subject not in subject_scores:
                    subject_scores[subject] = {"total_score": 0, "count": 0}
                subject_scores[subject]["total_score"] += score
                subject_scores[subject]["count"] += 1
            
            best_subjects = []
            for subj, data in subject_scores.items():
                avg = data["total_score"] / max(data["count"], 1)
                best_subjects.append({"subject": subj, "avg_score": avg})
            
            best_subjects.sort(key=lambda x: x["avg_score"], reverse=True)
            
            self.brain.learn(
                f"Best performing subject: {best_subjects[0]['subject'] if best_subjects else 'N/A'}",
                category="email_optimization"
            )
            
            return {
                "total_emails": len(emails),
                "best_subjects": best_subjects[:5],
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        finally:
            db.close()

    def analyze_funnel_performance(self) -> Dict:
        from database.models import SessionLocal, Lead
        
        db = SessionLocal()
        try:
            leads = db.query(Lead).all()
            
            cold = sum(1 for l in leads if l.temperature == "cold")
            warm = sum(1 for l in leads if l.temperature == "warm")
            hot = sum(1 for l in leads if l.temperature == "hot")
            converted = sum(1 for l in leads if l.status == "converted")
            
            total = len(leads) or 1
            
            return {
                "total_leads": len(leads),
                "temperature_distribution": {
                    "cold": cold,
                    "warm": warm,
                    "hot": hot,
                    "converted": converted
                },
                "conversion_rates": {
                    "cold_to_warm": round(warm / total * 100, 2),
                    "warm_to_hot": round(hot / max(warm, 1) * 100, 2),
                    "hot_to_converted": round(converted / max(hot, 1) * 100, 2)
                },
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        finally:
            db.close()

    def update_lead_scoring(self):
        from database.models import SessionLocal, Lead
        
        db = SessionLocal()
        try:
            leads = db.query(Lead).filter(Lead.status == "converted").all()
            
            if len(leads) < 5:
                return {"message": "Not enough data for scoring update"}
            
            factors = {
                "email_present": 0,
                "rating_low": 0,
                "review_count": 0,
                "niche_specific": 0
            }
            
            for lead in leads:
                if lead.email_primary:
                    factors["email_present"] += 1
                if lead.current_rating and lead.current_rating < 3.5:
                    factors["rating_low"] += 1
                if lead.negative_review_count and lead.negative_review_count > 3:
                    factors["review_count"] += 1
                if lead.niche:
                    factors["niche_specific"] += 1
            
            for key in factors:
                factors[key] = factors[key] / len(leads)
            
            self.brain.set_preference("lead_scoring_factors", factors)
            self.brain.learn(
                f"Updated lead scoring based on {len(leads)} converted leads",
                category="ml_update"
            )
            
            return {"message": "Lead scoring updated", "factors": factors}
        finally:
            db.close()

    def generate_weekly_report(self) -> Dict:
        self.learning_loop_count += 1
        
        email_analysis = self.analyze_email_performance()
        funnel_analysis = self.analyze_funnel_performance()
        
        report = {
            "week": self.learning_loop_count,
            "email_performance": email_analysis,
            "funnel_performance": funnel_analysis,
            "top_insights": [],
            "recommendations": [],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        if email_analysis.get("best_subjects"):
            report["top_insights"].append(
                f"Your best subject line has {email_analysis['best_subjects'][0]['avg_score']:.1f} avg engagement score"
            )
        
        if funnel_analysis.get("conversion_rates"):
            cold_to_warm = funnel_analysis["conversion_rates"]["cold_to_warm"]
            if cold_to_warm < 20:
                report["recommendations"].append(
                    "Cold-to-warm rate is low. Consider stronger subject lines or better send times."
                )
        
        self.brain.remember(
            f"Weekly report generated: {len(report['recommendations'])} recommendations",
            "report_generated"
        )
        
        return report

    def start(self):
        self.brain.remember("ML Learning Agent initialized", "system_start")
        return {"status": "online", "learning_cycle": self.learning_loop_count}

ml_head = MLHeadAgent()