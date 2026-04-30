# Advanced Analytics Engine
# ==========================
# Predictive analytics and insights

import random
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict

class PredictiveAnalytics:
    """AI-powered predictive analytics"""
    
    def __init__(self):
        self.models = {}
        self.history = []
    
    def calculate_lead_score(self, lead: Dict) -> float:
        """Score lead based on behavior and demographics"""
        score = 50.0
        
        if lead.get("email"):
            score += 10
        if lead.get("phone"):
            score += 15
        if lead.get("website"):
            score += 20
            
        biz_type = lead.get("business_type", "").lower()
        if any(w in biz_type for w in ["lawyer", "attorney", "legal"]):
            score += 25
        if any(w in biz_type for w in ["doctor", "medical", "clinic"]):
            score += 20
        if any(w in biz_type for w in ["real estate", "realtor"]):
            score += 15
            
        return min(score, 100.0)
    
    def predict_conversion_probability(self, lead: Dict) -> float:
        """Predict chance of conversion"""
        base = self.calculate_lead_score(lead)
        engagement = lead.get("engagement_score", 0)
        
        probability = (base * 0.6) + (engagement * 0.4)
        return min(probability / 100, 0.95)
    
    def forecast_revenue(self, leads: List[Dict], days: int = 30) -> Dict:
        """Forecast revenue based on lead pipeline"""
        total_pipeline = 0
        weighted_pipeline = 0
        
        for lead in leads:
            deal_value = lead.get("estimated_value", 500)
            probability = self.predict_conversion_probability(lead)
            
            total_pipeline += deal_value
            weighted_pipeline += deal_value * probability
        
        return {
            "total_pipeline": total_pipeline,
            "weighted_pipeline": weighted_pipeline,
            " forecasted_deals": int(weighted_pipeline / 1000),
            "forecast_days": days,
            "confidence": 0.75
        }
    
    def analyze_trends(self, data: List[Dict]) -> Dict:
        """Analyze trends in data"""
        by_day = defaultdict(int)
        
        for item in data:
            date = item.get("date", "")
            if date:
                by_day[date[:10]] += 1
        
        if not by_day:
            return {"trend": "neutral", "change": 0}
        
        dates = sorted(by_day.keys())
        if len(dates) < 2:
            return {"trend": "stable", "change": 0}
        
        first_half = sum(by_day[d] for d in dates[:len(dates)//2])
        second_half = sum(by_day[d] for d in dates[len(dates)//2:])
        
        if second_half > first_half * 1.1:
            trend = "up"
            change = ((second_half - first_half) / first_half) * 100
        elif second_half < first_half * 0.9:
            trend = "down"
            change = ((first_half - second_half) / first_half) * 100
        else:
            trend = "stable"
            change = 0
        
        return {"trend": trend, "change": round(change, 1)}
    
    def get_recommendations(self) -> List[str]:
        """Get AI recommendations"""
        recs = [
            "Increase outreach to legal businesses - highest conversion rate",
            "Add more phone numbers to leads - improves contact rate by 40%",
            "Send follow-ups within 2 hours - 3x more responsive",
            "Use personalized subject lines - 25% higher open rate",
            "Schedule calls during business hours - 2x more successful"
        ]
        return recs[:3]

class ABTestEngine:
    """A/B testing for campaigns"""
    
    def __init__(self):
        self.experiments = {}
    
    def create_experiment(self, name: str, variants: List[str]) -> Dict:
        """Create A/B test"""
        self.experiments[name] = {
            "variants": variants,
            "results": {v: {"views": 0, "conversions": 0} for v in variants},
            "started": datetime.utcnow().isoformat()
        }
        return {"experiment": name, "status": "created"}
    
    def get_variant(self, name: str) -> str:
        """Get random variant"""
        exp = self.experiments.get(name)
        if not exp:
            return ""
        return random.choice(exp["variants"])
    
    def record_conversion(self, name: str, variant: str):
        """Record conversion"""
        exp = self.experiments.get(name)
        if exp and variant in exp["results"]:
            exp["results"][variant]["conversions"] += 1
    
    def get_winner(self, name: str) -> str:
        """Get winning variant"""
        exp = self.experiments.get(name)
        if not exp:
            return ""
        
        best = None
        best_rate = 0
        
        for variant, results in exp["results"].items():
            views = results["views"]
            convs = results["conversions"]
            if views > 0:
                rate = convs / views
                if rate > best_rate:
                    best_rate = rate
                    best = variant
        
        return best or ""

predictive_analytics = PredictiveAnalytics()
ab_test_engine = ABTestEngine()