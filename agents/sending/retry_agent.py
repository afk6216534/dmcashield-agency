import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class RetryAgent:
    def __init__(self, data_file: str = "data/retry_log.json"):
        self.data_file = data_file
        self.failed_sends: List[Dict] = []
        self.retry_history: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.failed_sends = data.get("failed_sends", [])
                    self.retry_history = data.get("retry_history", [])
            except:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump({"failed_sends": self.failed_sends, "retry_history": self.retry_history}, f, indent=2)

    MAX_RETRIES = 3
    RETRY_DELAY_MINUTES = 30

    def record_failure(self, lead_id: str, email: str, subject: str, account_id: str, error: str) -> Dict:
        entry = {
            "id": f"fail_{len(self.failed_sends) + 1}",
            "lead_id": lead_id,
            "email": email,
            "subject": subject,
            "account_id": account_id,
            "error": error,
            "failed_at": datetime.utcnow().isoformat(),
            "retry_count": 0,
            "last_retry": None,
            "status": "pending"
        }
        self.failed_sends.append(entry)
        self._save()
        return entry

    def get_pending_retries(self) -> List[Dict]:
        now = datetime.utcnow()
        pending = []
        for f in self.failed_sends:
            if f.get("status") != "pending":
                continue
            if f["retry_count"] >= self.MAX_RETRIES:
                continue
            last = f.get("last_retry") or f.get("failed_at")
            last_dt = datetime.fromisoformat(last)
            if now - last_dt >= timedelta(minutes=self.RETRY_DELAY_MINUTES):
                pending.append(f)
        return pending

    def execute_retry(self, fail_entry: Dict, new_account: Dict) -> Dict:
        fail_entry["retry_count"] += 1
        fail_entry["last_retry"] = datetime.utcnow().isoformat()

        success = random.random() > 0.3

        record = {
            "fail_id": fail_entry["id"],
            "lead_id": fail_entry["lead_id"],
            "email": fail_entry["email"],
            "subject": fail_entry["subject"],
            "new_account": new_account.get("email", "unknown"),
            "attempt": fail_entry["retry_count"],
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.retry_history.append(record)

        if success:
            fail_entry["status"] = "recovered"
        elif fail_entry["retry_count"] >= self.MAX_RETRIES:
            fail_entry["status"] = "permanent_failure"

        self._save()
        return record

    def get_stats(self) -> Dict:
        total = len(self.failed_sends)
        recovered = len([f for f in self.failed_sends if f.get("status") == "recovered"])
        permanent = len([f for f in self.failed_sends if f.get("status") == "permanent_failure"])
        pending = len([f for f in self.failed_sends if f.get("status") == "pending"])
        return {
            "total_failures": total,
            "recovered": recovered,
            "permanent_failures": permanent,
            "pending_retries": pending,
            "recovery_rate": round((recovered / max(1, total)) * 100, 1),
            "retry_attempts": len(self.retry_history)
        }

    def get_failures_by_account(self, account_id: str) -> List[Dict]:
        return [f for f in self.failed_sends if f.get("account_id") == account_id]

    def clear_resolved(self):
        self.failed_sends = [f for f in self.failed_sends if f.get("status") in ("pending", "permanent_failure")]
        self._save()


retry_agent = RetryAgent()
