import os
import json
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from functools import wraps
import time

class RateLimiter:
    def __init__(self, config_file: str = "data/rate_limits.json"):
        self.config_file = config_file
        self.limits = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "global": {"requests": 100, "window": 60},
            "endpoints": {
                "/api/tasks": {"requests": 10, "window": 60},
                "/api/leads": {"requests": 50, "window": 60},
                "/api/jarvis": {"requests": 30, "window": 60}
            }
        }
    
    def _save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.limits, f, indent=2)
    
    def is_allowed(self, key: str, endpoint: str) -> bool:
        now = time.time()
        
        limit_config = self.limits["endpoints"].get(endpoint, self.limits["global"])
        max_requests = limit_config["requests"]
        window = limit_config["window"]
        
        requests = self.limits.get("requests", {})
        
        if key not in requests:
            requests[key] = []
        
        requests[key] = [t for t in requests[key] if now - t < window]
        
        if len(requests[key]) >= max_requests:
            self.limits["requests"] = requests
            return False
        
        requests[key].append(now)
        self.limits["requests"] = requests
        self._save()
        
        return True
    
    def get_remaining(self, key: str, endpoint: str) -> int:
        now = time.time()
        limit_config = self.limits["endpoints"].get(endpoint, self.limits["global"])
        max_requests = limit_config["requests"]
        
        requests = self.limits.get("requests", {}).get(key, [])
        requests = [t for t in requests if now - t < limit_config["window"]]
        
        return max(0, max_requests - len(requests))

rate_limiter = RateLimiter()

class APIKeyManager:
    def __init__(self, keys_file: str = "data/api_keys.json"):
        self.keys_file = keys_file
        self.keys = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"keys": {}}
    
    def _save(self):
        os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
        with open(self.keys_file, 'w') as f:
            json.dump(self.keys, f, indent=2)
    
    def generate_key(self, name: str, permissions: list = None) -> str:
        key = f"dmca_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        self.keys["keys"][key_hash] = {
            "name": name,
            "permissions": permissions or ["read"],
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None
        }
        
        self._save()
        
        return key
    
    def validate_key(self, key: str) -> Optional[Dict]:
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        key_data = self.keys["keys"].get(key_hash)
        if key_data:
            key_data["last_used"] = datetime.utcnow().isoformat()
            self._save()
        
        return key_data
    
    def revoke_key(self, key: str):
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash in self.keys["keys"]:
            del self.keys["keys"][key_hash]
            self._save()
    
    def list_keys(self) -> list:
        return [
            {"name": v["name"], "permissions": v["permissions"], "created_at": v["created_at"]}
            for v in self.keys["keys"].values()
        ]

api_key_manager = APIKeyManager()

class SecurityHeaders:
    @staticmethod
    def get_headers() -> Dict:
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        }

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
    
    def get(self, key: str, default: any = None) -> any:
        config_file = os.path.join(self.config_dir, f"{key}.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return default
    
    def set(self, key: str, value: any):
        config_file = os.path.join(self.config_dir, f"{key}.json")
        with open(config_file, 'w') as f:
            json.dump(value, f, indent=2)
    
    def delete(self, key: str):
        config_file = os.path.join(self.config_dir, f"{key}.json")
        if os.path.exists(config_file):
            os.remove(config_file)

config_manager = ConfigManager()

DEPLOYMENT_CONFIG = {
    "version": "1.0.0",
    "environment": "production",
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 4,
        "timeout": 120
    },
    "database": {
        "url": "sqlite:///./dmcashield.db",
        "pool_size": 20,
        "max_overflow": 10
    },
    "cors": {
        "allow_origins": ["https://dmcashield.com"],
        "allow_credentials": True
    },
    "rate_limiting": {
        "enabled": True,
        "default_limit": 100,
        "default_window": 60
    },
    "security": {
        "require_api_key": False,
        "jwt_secret": "CHANGE_ME_IN_PRODUCTION"
    },
    "features": {
        "ai_responses": True,
        "multi_source_scraping": True,
        "gmail_integration": True,
        "slack_integration": True,
        "twilio_sms": True,
        "google_sheets": True,
        "webhooks": True
    },
    "email": {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "max_daily_per_account": 40,
        "warmup_enabled": True
    },
    "monitoring": {
        "enabled": True,
        "error_alerts": True,
        "performance_tracking": True
    }
}