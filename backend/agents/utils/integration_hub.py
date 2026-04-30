"""
DMCAShield Integration Hub
=========================
Uses all available free APIs from cloned repos and public APIs.

Available Free APIs:
- OpenRouter.ai: Free AI models (mistral, llama, qwen)
- Hunter.io: Email finder (25 free/month)
- Clearbit: Company data
- Telegram: Notifications
- Slack: Team notifications
- Twilio: SMS (trial)
- exchangerate.host: Currency rates (FREE)
- weatherstack: Weather (free tier)
- IPstack: IP geolocation (free tier)
"""

import os
import json
import httpx
from datetime import datetime
from typing import Dict, List, Optional, Any

class IntegrationHub:
    """Central hub for all free API integrations"""
    
    def __init__(self, config_file: str = "data/integrations.json"):
        self.config_file = config_file
        self.config = self._load()
        self.cache = {}
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "openrouter": {"enabled": False, "api_key": "", "models": []},
            "hunter": {"enabled": False, "api_key": ""},
            "clearbit": {"enabled": False, "api_key": ""},
            "telegram": {"enabled": False, "bot_token": "", "chat_id": ""},
            "slack": {"enabled": False, "webhook_url": ""},
            "weather": {"enabled": False, "api_key": ""},
            "currency": {"enabled": True, "api_key": ""},  # exchangerate.host is free
            "ipgeo": {"enabled": False, "api_key": ""}
        }
    
    def _save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, service: str, **kwargs):
        if service in self.config:
            self.config[service].update(kwargs)
            self.config[service]["enabled"] = True
            self._save()
    
    # ===== OpenRouter AI (Free Models) =====
    async def generate_with_openrouter(self, prompt: str, model: str = "mistralai/mistral-7b-instruct:free") -> Optional[str]:
        """Generate text using free OpenRouter models"""
        if not self.config.get("openrouter", {}).get("enabled"):
            return None
        
        api_key = self.config["openrouter"].get("api_key")
        if not api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=30.0
                )
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content")
        except Exception as e:
            print(f"OpenRouter error: {e}")
            return None
    
    # ===== Hunter.io Email Finder (Free Tier) =====
    async def find_email_hunter(self, domain: str, first_name: str = "", last_name: str = "") -> Optional[str]:
        """Find email using Hunter.io"""
        if not self.config.get("hunter", {}).get("enabled"):
            return None
        
        api_key = self.config["hunter"].get("api_key")
        if not api_key:
            return None
        
        try:
            params = {"domain": domain, "api_key": api_key}
            if first_name:
                params["first_name"] = first_name
            if last_name:
                params["last_name"] = last_name
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.hunter.io/v2/domain-search",
                    params=params
                )
                data = response.json()
                emails = data.get("data", {}).get("emails", [])
                if emails:
                    return emails[0].get("value")
        except Exception as e:
            print(f"Hunter error: {e}")
        return None
    
    # ===== Clearbit Company Data (Free Tier) =====
    async def enrich_company_clearbit(self, domain: str) -> Dict:
        """Enrich company data from Clearbit"""
        if not self.config.get("clearbit", {}).get("enabled"):
            return {}
        
        api_key = self.config["clearbit"].get("api_key")
        if not api_key:
            return {}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://company.clearbit.com/api/v2/companies/find?domain={domain}",
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Clearbit error: {e}")
        return {}
    
    # ===== Free Weather Data =====
    async def get_weather(self, city: str) -> Dict:
        """Get weather from weatherstack (free tier)"""
        if not self.config.get("weather", {}).get("enabled"):
            return {"error": "Not configured"}
        
        api_key = self.config["weather"].get("api_key")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
                )
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    # ===== Free Currency Rates =====
    async def get_exchange_rates(self, base: str = "USD") -> Dict:
        """Get exchange rates from exchangerate.host (FREE)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.exchangerate.host/latest?base={base}"
                )
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    # ===== IP Geolocation (Free Tier) =====
    async def get_ip_info(self, ip: str) -> Dict:
        """Get IP info from IPstack"""
        if not self.config.get("ipgeo", {}).get("enabled"):
            return {}
        
        api_key = self.config["ipgeo"].get("api_key")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://api.ipstack.com/{ip}?access_key={api_key}"
                )
                return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"IPStack error: {e}")
        return {}
    
    # ===== Telegram Notifications =====
    async def send_telegram(self, message: str) -> bool:
        """Send Telegram notification"""
        if not self.config.get("telegram", {}).get("enabled"):
            return False
        
        bot_token = self.config["telegram"].get("bot_token")
        chat_id = self.config["telegram"].get("chat_id")
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": message}
                )
            return True
        except Exception as e:
            print(f"Telegram error: {e}")
            return False
    
    # ===== Slack Notifications =====
    async def send_slack(self, message: str, blocks: List[Dict] = None) -> bool:
        """Send Slack notification"""
        if not self.config.get("slack", {}).get("enabled"):
            return False
        
        webhook = self.config["slack"].get("webhook_url")
        try:
            async with httpx.AsyncClient() as client:
                payload = {"text": message}
                if blocks:
                    payload["blocks"] = blocks
                await client.post(webhook, json=payload)
            return True
        except Exception as e:
            print(f"Slack error: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get status of all integrations"""
        return {
            service: {"enabled": config.get("enabled", False)}
            for service, config in self.config.items()
        }

integration_hub = IntegrationHub()

# Free model list from OpenRouter
FREE_MODELS = [
    "mistralai/mistral-7b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "deepseek/deepseek-chat:free",
    "google/gemma-2-9b-it:free"
]

async def get_free_ai_completion(prompt: str) -> Optional[str]:
    """Helper to get AI completion using free models"""
    for model in FREE_MODELS:
        result = await integration_hub.generate_with_openrouter(prompt, model)
        if result:
            return result
    return None