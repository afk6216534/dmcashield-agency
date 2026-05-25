import uuid
import random
import smtplib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class WarmupEngine:
    def __init__(self, data_file: str = "data/warmup_engine.json"):
        self.data_file = data_file
        self.campaigns: Dict[str, Dict] = {}
        self.account_pairs: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.campaigns = data.get("campaigns", {})
                    self.account_pairs = data.get("account_pairs", [])
            except:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump({"campaigns": self.campaigns, "account_pairs": self.account_pairs}, f, indent=2)

    def register_account_pair(self, account_a: Dict, account_b: Dict) -> str:
        pair_id = f"pair_{uuid.uuid4().hex[:8]}"
        self.account_pairs.append({
            "id": pair_id,
            "account_a": account_a,
            "account_b": account_b,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        })
        self._save()
        return pair_id

    def start_campaign(self, account_id: str, credentials: Dict, target_days: int = 28) -> str:
        campaign_id = f"warmup_{account_id}_{uuid.uuid4().hex[:4]}"
        schedule = self._build_schedule(target_days)
        self.campaigns[campaign_id] = {
            "id": campaign_id,
            "account_id": account_id,
            "email": credentials.get("email"),
            "start_date": datetime.utcnow().isoformat(),
            "target_days": target_days,
            "current_day": 1,
            "total_sent": 0,
            "replies": 0,
            "bounces": 0,
            "status": "active",
            "schedule": schedule,
            "daily_log": []
        }
        self._save()
        return campaign_id

    def _build_schedule(self, days: int) -> List[Dict]:
        schedule = []
        ramp = {1: 2, 2: 3, 3: 5, 4: 7, 5: 10, 6: 12, 7: 15,
                8: 18, 9: 20, 10: 22, 11: 24, 12: 25, 13: 25,
                14: 25, 15: 28, 16: 30, 17: 32, 18: 35, 19: 35,
                20: 35, 21: 38, 22: 40, 23: 40, 24: 40, 25: 40,
                26: 40, 27: 40, 28: 40}
        for day in range(1, days + 1):
            limit = ramp.get(day, 40)
            hours = random.sample(range(8, 20), min(limit, 6))
            schedule.append({"day": day, "target": min(limit, 6), "send_hours": sorted(hours)})
        return schedule

    def send_warmup_batch(self, campaign_id: str, to_email: str, credentials: Dict, count: int = 3) -> Dict:
        campaign = self.campaigns.get(campaign_id)
        if not campaign or campaign.get("status") != "active":
            return {"sent": 0, "error": "campaign not active"}

        templates = [
            ("Quick question about your", "Hi there,\n\nQuick question about your services...\n\nBest,\n{sender}"),
            ("Interesting article I found", "Hey there,\n\nFound this article and thought you'd like it...\n\nCheers,\n{sender}"),
            ("Following up", "Hi there,\n\nJust following up on our conversation...\n\nBest,\n{sender}"),
            ("Your thoughts?", "Hey,\n\nWould love your thoughts on something...\n\nThanks,\n{sender}"),
            ("Quick observation", "Hi,\n\nNoticed something interesting about your industry...\n\nBest,\n{sender}"),
        ]

        sent = 0
        for i in range(min(count, 5)):
            if sent >= campaign["schedule"][campaign["current_day"] - 1]["target"]:
                break
            template = random.choice(templates)
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = template[0]
                msg["From"] = credentials.get("email")
                msg["To"] = to_email
                body = template[1].format(
                    sender=credentials.get("display_name", credentials.get("email", "Friend"))
                )
                msg.attach(MIMEText(body, "plain"))
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(credentials.get("email"), credentials.get("app_password"))
                    server.send_message(msg)
                sent += 1
                campaign["total_sent"] += 1
            except:
                campaign["bounces"] += 1

        campaign["daily_log"].append({
            "day": campaign["current_day"],
            "sent": sent,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()
        return {"sent": sent, "total": campaign["total_sent"], "day": campaign["current_day"]}

    def advance_day(self, campaign_id: str) -> bool:
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return False
        if campaign["current_day"] < campaign["target_days"]:
            campaign["current_day"] += 1
            if campaign["current_day"] >= campaign["target_days"]:
                campaign["status"] = "completed"
            self._save()
            return True
        return False

    def get_status(self, campaign_id: str) -> Optional[Dict]:
        c = self.campaigns.get(campaign_id)
        if not c:
            return None
        progress = round((c["current_day"] / c["target_days"]) * 100, 1)
        return {
            "id": c["id"],
            "email": c["email"],
            "day": c["current_day"],
            "of": c["target_days"],
            "progress_pct": progress,
            "total_sent": c["total_sent"],
            "replies": c["replies"],
            "bounces": c["bounces"],
            "status": c["status"],
            "today_target": c["schedule"][c["current_day"] - 1]["target"] if c["current_day"] <= len(c["schedule"]) else 0
        }

    def list_campaigns(self) -> List[Dict]:
        return [self.get_status(cid) for cid in self.campaigns if self.get_status(cid)]

    def pause(self, campaign_id: str):
        c = self.campaigns.get(campaign_id)
        if c and c["status"] == "active":
            c["status"] = "paused"
            self._save()

    def resume(self, campaign_id: str):
        c = self.campaigns.get(campaign_id)
        if c and c["status"] == "paused":
            c["status"] = "active"
            self._save()


warmup_engine = WarmupEngine()
