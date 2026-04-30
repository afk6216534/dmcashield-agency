import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SalesFunnelAutomation:
    def __init__(self, persist_file: str = "data/sales_funnel.json"):
        self.persist_file = persist_file
        self.funnels: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        import os
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    self.funnels = json.load(f)
            except:
                pass
    
    def _save(self):
        import os
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump(self.funnels, f, indent=2)
    
    def create_funnel(self, name: str, steps: List[Dict]) -> str:
        funnel_id = f"funnel_{uuid.uuid4().hex[:8]}"
        
        self.funnels[funnel_id] = {
            "id": funnel_id,
            "name": name,
            "steps": [{"day": i * 3, "subject": s.get("subject"), "body": s.get("body")} for i, s in enumerate(steps)],
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "leads_enrolled": 0
        }
        
        self._save()
        return funnel_id
    
    def get_funnel(self, funnel_id: str) -> Optional[Dict]:
        return self.funnels.get(funnel_id)
    
    def enroll_lead(self, funnel_id: str, lead_id: str) -> bool:
        if funnel_id not in self.funnels:
            return False
        
        self.funnels[funnel_id]["leads_enrolled"] = self.funnels[funnel_id].get("leads_enrolled", 0) + 1
        self._save()
        return True
    
    def get_lead_sequence(self, funnel_id: str, day: int) -> Optional[Dict]:
        funnel = self.funnels.get(funnel_id)
        if not funnel:
            return None
        
        for step in funnel.get("steps", []):
            if step.get("day") == day:
                return step
        return None
    
    def list_funnels(self) -> List[Dict]:
        return list(self.funnels.values())

DEFAULT_FUNNELS = [
    {
        "name": "DMCA Service Intro",
        "steps": [
            {"subject": "Can I help remove those negative reviews?", "body": "Hi {{name}},\n\nI noticed your business has some negative reviews online that might be hurting your reputation.\n\nWe specialize in legal DMCA removal for fake/illegal content. Would you like a free consultation?\n\nBest,\nDMCAShield"},
            {"subject": "Following up on review removal", "body": "Hey {{name}},\n\nJust wanted to follow up on my last email. We're seeing great results helping businesses like yours remove problematic content.\n\nAny questions?\n\nBest"},
            {"subject": "Quick question for you", "body": "Hi {{name}},\n\nOne quick question - have you had a chance to think about removing those negative reviews?\n\nWe're happy to answer any questions.\n\nBest"},
            {"subject": "Last try - I promise", "body": "Hey {{name}},\n\nThis is my last email, I promise. But I had to reach out one more time.\n\nIf you're not interested, no worries - but if you are, let's talk.\n\n\nBest"}
        ]
    }
]

def init_default_funnels():
    for funnel in DEFAULT_FUNNELS:
        sales_funnel.create_funnel(funnel["name"], funnel["steps"])

sales_funnel = SalesFunnelAutomation()

class GoogleSheetsIntegration:
    def __init__(self, config_file: str = "data/sheets_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        import os
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"enabled": False, "spreadsheet_id": "", "sheets": {}}
    
    def _save_config(self):
        import os
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, spreadsheet_id: str):
        self.config["enabled"] = True
        self.config["spreadsheet_id"] = spreadsheet_id
        self._save_config()
    
    async def export_leads(self, leads: List[Dict]):
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            
            gc = gspread.service_account(filename="credentials.json")
            sh = gc.open_by_key(self.config.get("spreadsheet_id"))
            
            worksheet = sh.sheet1
            rows = [["Business", "Owner", "Email", "Phone", "City", "State", "Rating", "Score", "Status"]]
            
            for lead in leads:
                rows.append([
                    lead.get("business_name", ""),
                    lead.get("owner_name", ""),
                    lead.get("email_primary", ""),
                    lead.get("phone", ""),
                    lead.get("city", ""),
                    lead.get("state", ""),
                    lead.get("current_rating", 0),
                    lead.get("lead_score", 0),
                    lead.get("status", "")
                ])
            
            worksheet.append_rows(rows)
            return {"exported": len(leads)}
            
        except Exception as e:
            print(f"Google Sheets export error: {e}")
            return {"error": str(e)}
    
    async def export_hot_leads(self):
        from database.models import SessionLocal, Lead
        
        db = SessionLocal()
        try:
            hot_leads = db.query(Lead).filter(Lead.temperature == "hot").all()
            leads = [{
                "business_name": l.business_name,
                "owner_name": l.owner_name,
                "email_primary": l.email_primary,
                "phone": l.phone,
                "city": l.city,
                "state": l.state,
                "current_rating": l.current_rating,
                "lead_score": l.lead_score,
                "status": l.status
            } for l in hot_leads]
            
            return await self.export_leads(leads)
        finally:
            db.close()
    
    def get_config(self) -> dict:
        return self.config

google_sheets = GoogleSheetsIntegration()