import os
import json
import httpx
from datetime import datetime
from typing import Dict, List, Optional

class TwilioSMS:
    def __init__(self, config_file: str = "data/twilio_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"enabled": False, "account_sid": "", "auth_token": "", "from_number": ""}
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, account_sid: str, auth_token: str, from_number: str):
        self.config["enabled"] = True
        self.config["account_sid"] = account_sid
        self.config["auth_token"] = auth_token
        self.config["from_number"] = from_number
        self._save_config()
    
    async def send_sms(self, to_number: str, message: str) -> Dict:
        if not self.config.get("enabled"):
            return {"error": "Twilio not configured"}
        
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.config['account_sid']}/Messages.json"
            
            auth = (self.config["account_sid"], self.config["auth_token"])
            data = {
                "To": to_number,
                "From": self.config["from_number"],
                "Body": message
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, auth=auth)
                
            if response.status_code == 201:
                return {"success": True, "sid": response.json().get("sid")}
            else:
                return {"error": response.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def send_hot_lead_alert(self, lead: Dict) -> Dict:
        message = f"🔥 HOT LEAD: {lead.get('business_name')} - {lead.get('email_primary')} - Score: {lead.get('lead_score')}"
        return await self.send_sms(lead.get("phone", ""), message)
    
    def is_configured(self) -> bool:
        return self.config.get("enabled", False)

twilio_sms = TwilioSMS()

class SlackIntegration:
    def __init__(self, config_file: str = "data/slack_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"enabled": False, "webhook_url": "", "channel": ""}
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, webhook_url: str, channel: str = None):
        self.config["enabled"] = True
        self.config["webhook_url"] = webhook_url
        if channel:
            self.config["channel"] = channel
        self._save_config()
    
    async def send_message(self, message: str, blocks: List[Dict] = None) -> Dict:
        if not self.config.get("enabled"):
            return {"error": "Slack not configured"}
        
        try:
            payload = {"text": message}
            if blocks:
                payload["blocks"] = blocks
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.config["webhook_url"],
                    json=payload
                )
            
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"error": response.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def send_hot_lead_alert(self, lead: Dict) -> Dict:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🔥 HOT LEAD ALERT", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Business:*\n{lead.get('business_name')}"},
                    {"type": "mrkdwn", "text": f"*Owner:*\n{lead.get('owner_name')}"},
                    {"type": "mrkdwn", "text": f"*Email:*\n{lead.get('email_primary')}"},
                    {"type": "mrkdwn", "text": f"*Phone:*\n{lead.get('phone')}"},
                    {"type": "mrkdwn", "text": f"*Score:*\n{lead.get('lead_score')}"},
                    {"type": "mrkdwn", "text": f"*Location:*\n{lead.get('city')}, {lead.get('state')}"}
                ]
            }
        ]
        
        message = f"🔥 New hot lead: {lead.get('business_name')} - {lead.get('email_primary')}"
        return await self.send_message(message, blocks)
    
    async def send_daily_report(self, stats: Dict) -> Dict:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "📊 Daily Report", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Emails Sent:*\n{stats.get('emails_sent_today', 0)}"},
                    {"type": "mrkdwn", "text": f"*Hot Leads:*\n{stats.get('hot_leads', 0)}"},
                    {"type": "mrkdwn", "text": f"*Total Leads:*\n{stats.get('total_leads', 0)}"},
                    {"type": "mrkdwn", "text": f"*Active Tasks:*\n{stats.get('active_tasks', 0)}"}
                ]
            }
        ]
        
        message = f"📊 DMCAShield Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
        return await self.send_message(message, blocks)
    
    def is_configured(self) -> bool:
        return self.config.get("enabled", False)

slack_integration = SlackIntegration()

class LeadEnrichmentAPI:
    def __init__(self, config_file: str = "data/enrichment_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"hunter_api_key": "", "clearbit_api_key": ""}
    
    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, hunter_api_key: str = None, clearbit_api_key: str = None):
        if hunter_api_key:
            self.config["hunter_api_key"] = hunter_api_key
        if clearbit_api_key:
            self.config["clearbit_api_key"] = clearbit_api_key
        self._save_config()
    
    async def find_email_hunter(self, domain: str, name: str = None) -> Optional[str]:
        api_key = self.config.get("hunter_api_key")
        if not api_key:
            return None
        
        try:
            url = f"https://api.hunter.io/v2/domain-search"
            params = {"domain": domain, "api_key": api_key}
            if name:
                params["first_name"] = name.split()[0] if name else ""
                params["last_name"] = name.split()[-1] if name and len(name.split()) > 1 else ""
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                data = response.json()
                
                emails = data.get("data", {}).get("emails", [])
                if emails:
                    return emails[0].get("value")
                    
        except Exception as e:
            print(f"Hunter API error: {e}")
        
        return None
    
    async def enrich_clearbit(self, domain: str) -> Dict:
        api_key = self.config.get("clearbit_api_key")
        if not api_key:
            return {}
        
        try:
            url = f"https://company.clearbit.com/api/v2/companies/find?domain={domain}"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "name": data.get("name"),
                        "legalName": data.get("legalName"),
                        "domain": data.get("domain"),
                        "metrics": data.get("metrics", {}),
                        "category": data.get("category"),
                        "description": data.get("description"),
                        "facebook": data.get("facebook"),
                        "linkedin": data.get("linkedin"),
                        "twitter": data.get("twitter")
                    }
                    
        except Exception as e:
            print(f"Clearbit API error: {e}")
        
        return {}
    
    async def get_social_profiles(self, domain: str) -> Dict:
        clearbit_data = await self.enrich_clearbit(domain)
        return clearbit_data

lead_enrichment = LeadEnrichmentAPI()

class ABTestingEngine:
    def __init__(self, persist_file: str = "data/ab_tests.json"):
        self.persist_file = persist_file
        self.tests: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'r') as f:
                    self.tests = json.load(f)
            except:
                pass
    
    def _save(self):
        os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
        with open(self.persist_file, 'w') as f:
            json.dump(self.tests, f, indent=2)
    
    def create_test(self, name: str, variants: List[Dict]) -> str:
        import uuid
        test_id = f"ab_{uuid.uuid4().hex[:8]}"
        
        self.tests[test_id] = {
            "id": test_id,
            "name": name,
            "variants": [{"name": v.get("name"), "weight": v.get("weight", 50)} for v in variants],
            "status": "active",
            "results": {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._save()
        return test_id
    
    def get_variant(self, test_id: str) -> Optional[Dict]:
        test = self.tests.get(test_id)
        if not test or test.get("status") != "active":
            return None
        
        import random
        variants = test.get("variants", [])
        weights = [v.get("weight", 50) for v in variants]
        total = sum(weights)
        
        rand = random.randint(0, total)
        cumulative = 0
        
        for i, v in enumerate(variants):
            cumulative += v.get("weight", 50)
            if rand <= cumulative:
                return v
        
        return variants[0] if variants else None
    
    def record_conversion(self, test_id: str, variant_name: str):
        if test_id in self.tests:
            results = self.tests[test_id].get("results", {})
            results[variant_name] = results.get(variant_name, 0) + 1
            self.tests[test_id]["results"] = results
            self._save()
    
    def get_results(self, test_id: str) -> Dict:
        return self.tests.get(test_id, {}).get("results", {})
    
    def list_tests(self) -> List[Dict]:
        return list(self.tests.values())

ab_testing = ABTestingEngine()

class MonitoringService:
    def __init__(self):
        self.metrics_file = "data/metrics.json"
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"requests": [], "errors": [], "alerts": []}
    
    def _save_metrics(self):
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_request(self, endpoint: str, duration_ms: float, status: int):
        self.metrics["requests"].append({
            "endpoint": endpoint,
            "duration_ms": duration_ms,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.metrics["requests"] = self.metrics["requests"][-1000:]
        self._save_metrics()
    
    def record_error(self, error: str, context: Dict = None):
        self.metrics["errors"].append({
            "error": error,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.metrics["errors"] = self.metrics["errors"][-100:]
        self._save_metrics()
    
    def send_alert(self, alert_type: str, message: str, severity: str = "warning"):
        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.metrics["alerts"].append(alert)
        self.metrics["alerts"] = self.metrics["alerts"][-50:]
        self._save_metrics()
        
        return alert
    
    def get_stats(self) -> Dict:
        requests = self.metrics.get("requests", [])
        
        if not requests:
            return {"total_requests": 0, "avg_duration": 0, "error_rate": 0}
        
        durations = [r.get("duration_ms", 0) for r in requests]
        errors = sum(1 for r in requests if r.get("status", 200) >= 400)
        
        return {
            "total_requests": len(requests),
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "error_rate": errors / len(requests) if requests else 0,
            "error_count": len(self.metrics.get("errors", [])),
            "alert_count": len(self.metrics.get("alerts", []))
        }

monitoring = MonitoringService()