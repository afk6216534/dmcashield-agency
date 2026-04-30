"""
External Integrations - Connect DMCAShield with Cloned Repos
====================================================
Features from: ListMonk, Mautic, Coolify, and more
"""

import os
import json
import httpx
from datetime import datetime
from typing import Dict, List, Optional, Any

# ===== LISTMONK INTEGRATION =====
class ListMonkIntegration:
    """Connect to ListMonk for advanced email campaigns"""
    
    def __init__(self, config_file: str = "data/listmonk.json"):
        self.config_file = config_file
        self.config = self._load()
        self.base_url = self.config.get("base_url", "http://localhost:9000")
        self.api_key = self.config.get("api_key", "")
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"base_url": "", "api_key": ""}
    
    def configure(self, base_url: str, api_key: str):
        self.config = {"base_url": base_url, "api_key": api_key}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_lists(self) -> List[Dict]:
        """Get mailing lists from ListMonk"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/lists",
                auth=("listmonk", self.api_key)
            )
            return response.json().get("data", []) if response.status_code == 200 else []
        except:
            return []
    
    def get_subscribers(self, list_id: int = None) -> List[Dict]:
        """Get subscribers"""
        try:
            url = f"{self.base_url}/api/subscribers"
            if list_id:
                url += f"?list_id={list_id}"
            response = httpx.get(url, auth=("listmonk", self.api_key))
            return response.json().get("data", []) if response.status_code == 200 else []
        except:
            return []
    
    def add_subscriber(self, email: str, name: str, list_id: int = 1) -> bool:
        """Add subscriber to list"""
        try:
            response = httpx.post(
                f"{self.base_url}/api/subscribers",
                auth=("listmonk", self.api_key),
                json={
                    "email": email,
                    "name": name,
                    "list_ids": [list_id]
                }
            )
            return response.status_code in [200, 201]
        except:
            return False
    
    def create_campaign(self, subject: str, body: str, list_ids: List[int]) -> Optional[Dict]:
        """Create email campaign"""
        try:
            response = httpx.post(
                f"{self.base_url}/api/campaigns",
                auth=("listmonk", self.api_key),
                json={
                    "subject": subject,
                    "body": body,
                    "list_ids": list_ids,
                    "send_now": False
                }
            )
            return response.json() if response.status_code in [200, 201] else None
        except:
            return None
    
    def get_campaign_stats(self, campaign_id: int) -> Dict:
        """Get campaign statistics"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/campaigns/{campaign_id}",
                auth=("listmonk", self.api_key)
            )
            return response.json().get("data", {}) if response.status_code == 200 else {}
        except:
            return {}

listmonk = ListMonkIntegration()

# ===== MAUTIC INTEGRATION =====
class MauticIntegration:
    """Connect to Mautic for marketing automation"""
    
    def __init__(self, config_file: str = "data/mautic.json"):
        self.config_file = config_file
        self.config = self._load()
        self.base_url = self.config.get("base_url", "")
        self.api_key = self.config.get("api_key", "")
        self.client = None
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"base_url": "", "api_key": ""}
    
    def configure(self, base_url: str, api_key: str):
        self.config = {"base_url": base_url, "api_key": api_key}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_auth(self):
        return (self.api_key, "")
    
    def get_contacts(self, search: str = None) -> List[Dict]:
        """Get contacts from Mautic"""
        try:
            params = {}
            if search:
                params["search"] = search
            response = httpx.get(
                f"{self.base_url}/api/contacts",
                auth=self._get_auth(),
                params=params
            )
            return response.json().get("contacts", {}).values() if response.status_code == 200 else []
        except:
            return []
    
    def create_contact(self, email: str, first_name: str = "", last_name: str = "") -> Optional[int]:
        """Create new contact"""
        try:
            response = httpx.post(
                f"{self.base_url}/api/contacts/new",
                auth=self._get_auth(),
                json={
                    "email": email,
                    "firstname": first_name,
                    "lastname": last_name
                }
            )
            if response.status_code in [200, 201]:
                return response.json().get("contact", {}).get("id")
        except:
            pass
        return None
    
    def add_to_segment(self, contact_id: int, segment_id: int) -> bool:
        """Add contact to segment"""
        try:
            response = httpx.post(
                f"{self.base_url}/api/segments/{segment_id}/contact/{contact_id}/add",
                auth=self._get_auth()
            )
            return response.status_code in [200, 201]
        except:
            return False
    
    def get_campaigns(self) -> List[Dict]:
        """Get marketing campaigns"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/campaigns",
                auth=self._get_auth()
            )
            return response.json().get("campaigns", {}).values() if response.status_code == 200 else []
        except:
            return []

mautic = MauticIntegration()

# ===== COOLIFY INTEGRATION =====
class CoolifyIntegration:
    """Connect to Coolify for deployment"""
    
    def __init__(self, config_file: str = "data/coolify.json"):
        self.config_file = config_file
        self.config = self._load()
        self.base_url = self.config.get("base_url", "")
        self.api_key = self.config.get("api_key", "")
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"base_url": "", "api_key": ""}
    
    def configure(self, base_url: str, api_key: str):
        self.config = {"base_url": base_url, "api_key": api_key}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def get_projects(self) -> List[Dict]:
        """Get Coolify projects"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/projects",
                headers=self._get_headers()
            )
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def get_applications(self, project_id: str) -> List[Dict]:
        """Get applications in project"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/projects/{project_id}/applications",
                headers=self._get_headers()
            )
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def deploy_application(self, application_id: str) -> bool:
        """Trigger deployment"""
        try:
            response = httpx.post(
                f"{self.base_url}/api/applications/{application_id}/deploy",
                headers=self._get_headers()
            )
            return response.status_code in [200, 201]
        except:
            return False
    
    def get_deployments(self, application_id: str) -> List[Dict]:
        """Get deployment history"""
        try:
            response = httpx.get(
                f"{self.base_url}/api/applications/{application_id}/deployments",
                headers=self._get_headers()
            )
            return response.json() if response.status_code == 200 else []
        except:
            return []

coolify = CoolifyIntegration()

# ===== POSthog INTEGRATION =====
class PosthogIntegration:
    """Connect to Posthog for analytics"""
    
    def __init__(self, config_file: str = "data/posthog.json"):
        self.config_file = config_file
        self.config = self._load()
        self.api_key = self.config.get("api_key", "")
        self.host = self.config.get("host", "https://app.posthog.com")
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"api_key": "", "host": ""}
    
    def configure(self, api_key: str, host: str = "https://app.posthog.com"):
        self.config = {"api_key": api_key, "host": host}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def capture_event(self, event: str, properties: Dict = None, distinct_id: str = "dmcashield"):
        """Capture event"""
        try:
            httpx.post(
                f"{self.host}/capture/",
                json={
                    "api_key": self.api_key,
                    "event": event,
                    "properties": properties or {},
                    "distinct_id": distinct_id
                }
            )
        except:
            pass
    
    def track_lead_scraped(self, business_type: str, location: str):
        self.capture_event("lead_scraped", {"type": business_type, "location": location})
    
    def track_email_sent(self, lead_email: str):
        self.capture_event("email_sent", {"email": lead_email})
    
    def track_hot_lead(self, lead_score: int):
        self.capture_event("hot_lead_detected", {"score": lead_score})

posthog = PosthogIntegration()

# ===== HUGINN INTEGRATION (Patterns) =====
class HuginnIntegration:
    """Use Huginn automation patterns"""
    
    def __init__(self):
        self.workflows = {
            "daily_scrape": {
                "name": "Daily Lead Scraping",
                "schedule": "0 6 * * *",
                "actions": ["scrape_google_maps", "enrich_leads", "save_to_db"]
            },
            "email_sequence": {
                "name": "Email Follow-up Sequence", 
                "schedule": "0 9 * * *",
                "actions": ["check_responses", "send_followup", "update_lead_status"]
            },
            "hot_lead_alert": {
                "name": "Hot Lead Alert",
                "schedule": "*/15 * * * *",
                "actions": ["check_hot_leads", "send_alert"]
            },
            "weekly_report": {
                "name": "Weekly Report",
                "schedule": "0 18 * * 0",
                "actions": ["generate_report", "send_email"]
            }
        }
    
    def get_workflows(self) -> List[Dict]:
        return [
            {"id": k, **v} for k, v in self.workflows.items()
        ]
    
    def trigger_workflow(self, workflow_id: str) -> bool:
        """Trigger a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return False
        
        # Execute workflow actions
        for action in workflow.get("actions", []):
            print(f"Executing: {action}")
        
        return True

huginn = HuginnIntegration()

# ===== UNIFIED EXTERNAL CONNECTORS =====
class ExternalConnectors:
    """All external integrations unified"""
    
    def __init__(self):
        self.listmonk = listmonk
        self.mautic = mautic
        self.coolify = coolify
        self.posthog = posthog
        self.huginn = huginn
    
    def get_status(self) -> Dict:
        return {
            "listmonk": bool(self.listmonk.api_key),
            "mautic": bool(self.mautic.api_key),
            "coolify": bool(self.coolify.api_key),
            "posthog": bool(self.posthog.api_key),
            "huginn": True
        }

external_connectors = ExternalConnectors()