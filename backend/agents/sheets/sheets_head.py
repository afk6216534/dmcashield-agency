import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Dict, List, Any
from datetime import datetime

from agents.memory.agent_brain import memory_system

class SheetsHeadAgent:
    def __init__(self):
        self.name = "SheetsHead"
        self.brain = memory_system.get_brain(self.name)
        self.client = None
        self.spreadsheet = None
        self._init_google_sheets()

    def _init_google_sheets(self):
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            self.client = gspread.authorize(creds)
        except Exception as e:
            self.brain.remember(f"Google Sheets init failed: {str(e)}", "error")
            self.client = None

    def create_workbook(self, name: str = "DMCA Agency Dashboard"):
        if not self.client:
            return {"error": "Google Sheets not configured"}
        
        try:
            spreadsheet = self.client.create(name)
            spreadsheet.share("", perm_type="anyone", role="writer")
            
            self.spreadsheet = spreadsheet
            
            self._setup_tabs(spreadsheet)
            
            return {"spreadsheet_id": spreadsheet.id, "url": spreadsheet.url}
        except Exception as e:
            self.brain.remember(f"Workbook creation failed: {str(e)}", "error")
            return {"error": str(e)}

    def _setup_tabs(self, spreadsheet):
        tabs = [
            "Email Accounts",
            "Cold Leads",
            "Warm Leads",
            "Hot Leads",
            "Converted",
            "Archived",
            "Task Overview",
            "Performance"
        ]
        
        for i, tab_name in enumerate(tabs):
            try:
                if i == 0:
                    spreadsheet.sheet1.title = tab_name
                else:
                    spreadsheet.add_worksheet(tab_name, 1000, 26)
            except:
                pass

    def update_lead_sheet(self, temperature: str, leads: List[Dict]):
        if not self.client or not self.spreadsheet:
            return
        
        try:
            tab_map = {
                "cold": "Cold Leads",
                "warm": "Warm Leads",
                "hot": "Hot Leads",
                "converted": "Converted"
            }
            
            tab_name = tab_map.get(temperature, "Cold Leads")
            sheet = self.spreadsheet.worksheet(tab_name)
            
            headers = ["Lead ID", "Business Name", "Owner", "Email", "City", "State", "Niche", "Rating", "Negative Reviews", "Last Contact"]
            rows = []
            
            for lead in leads:
                rows.append([
                    lead.get("id", ""),
                    lead.get("business_name", ""),
                    lead.get("owner_name", ""),
                    lead.get("email_primary", ""),
                    lead.get("city", ""),
                    lead.get("state", ""),
                    lead.get("niche", ""),
                    str(lead.get("current_rating", "")),
                    str(lead.get("negative_review_count", "")),
                    lead.get("updated_at", "")
                ])
            
            if rows:
                sheet.clear()
                sheet.append_row(headers)
                for row in rows:
                    sheet.append_row(row)
                
        except Exception as e:
            self.brain.remember(f"Sheet update failed: {str(e)}", "error")

    def update_account_sheet(self, accounts: List[Dict]):
        if not self.client or not self.spreadsheet:
            return
        
        try:
            sheet = self.spreadsheet.worksheet("Email Accounts")
            
            headers = ["Account ID", "Email", "Display Name", "Daily Limit", "Sent Today", "Status", "Health Score", "Blacklist Status"]
            rows = []
            
            for acc in accounts:
                rows.append([
                    acc.get("id", ""),
                    acc.get("email_address", ""),
                    acc.get("display_name", ""),
                    str(acc.get("daily_limit", "")),
                    str(acc.get("sent_today", "")),
                    acc.get("status", ""),
                    str(acc.get("health_score", "")),
                    acc.get("blacklist_status", "")
                ])
            
            sheet.clear()
            sheet.append_row(headers)
            for row in rows:
                sheet.append_row(row)
                
        except Exception as e:
            self.brain.remember(f"Account sheet update failed: {str(e)}", "error")

    def update_task_sheet(self, tasks: List[Dict]):
        if not self.client or not self.spreadsheet:
            return
        
        try:
            sheet = self.spreadsheet.worksheet("Task Overview")
            
            headers = ["Task ID", "Business Type", "City", "State", "Total Leads", "Scraped", "Emailed", "Hot", "Status", "Completion %"]
            rows = []
            
            for task in tasks:
                rows.append([
                    task.get("id", ""),
                    task.get("business_type", ""),
                    task.get("city", ""),
                    task.get("state", ""),
                    str(task.get("leads_total", "")),
                    str(task.get("leads_scraped", "")),
                    str(task.get("leads_emailed", "")),
                    str(task.get("leads_hot", "")),
                    task.get("status", ""),
                    f"{task.get('funnel_completion_rate', 0):.1f}%"
                ])
            
            sheet.clear()
            sheet.append_row(headers)
            for row in rows:
                sheet.append_row(row)
                
        except Exception as e:
            self.brain.remember(f"Task sheet update failed: {str(e)}", "error")

    def start(self):
        return {"status": "online" if self.client else "offline"}

sheets_head = SheetsHeadAgent()