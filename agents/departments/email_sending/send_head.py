"""
SendHead Agent (4A) - Email Delivery Coordinator
Handles all email sending with rate limiting and account rotation.
"""

import time
import threading
from typing import Dict, Any, List
from queue import Queue, Empty
from datetime import datetime, timedelta

class SendHead:
    """Coordinates email sending across multiple accounts."""

    def __init__(self, max_emails_per_day: int = 40):
        self.send_queue = Queue()
        self.max_emails_per_day = max_emails_per_day
        self.email_accounts = {}
        self.sending_threads = []
        self.is_running = False
        self.min_gap_seconds = 180  # 3 minutes between sends

    def add_email_account(self, account_id: str, config: Dict[str, Any]) -> None:
        """Add an email account to the rotation pool."""
        self.email_accounts[account_id] = {
            "config": config,
            "sent_today": 0,
            "last_send": None,
            "status": "active",
            "health_score": 100
        }

    def queue_email(self, lead_id: str, account_id: str, 
                   subject: str, body: str) -> bool:
        """Add an email to the sending queue."""
        if account_id not in self.email_accounts:
            return False

        email_job = {
            "lead_id": lead_id,
            "account_id": account_id,
            "subject": subject,
            "body": body,
            "queued_at": datetime.utcnow().isoformat(),
            "attempts": 0
        }

        # Check account limits
        account = self.email_accounts[account_id]
        if account["sent_today"] >= self.max_emails_per_day:
            print(f"Account {account_id} hit daily limit")
            return False

        self.send_queue.put(email_job)
        return True

    def get_next_available_account(self) -> str:
        """Get next available account with capacity."""
        for acc_id, acc in self.email_accounts.items():
            if acc["status"] == "active" and acc["sent_today"] < self.max_emails_per_day:
                # Check cooldown
                if acc["last_send"]:
                    cooldown_remaining = (acc["last_send"] + 
                                         timedelta(seconds=self.min_gap_seconds)) - datetime.utcnow()
                    if cooldown_remaining.total_seconds() > 0:
                        continue
                return acc_id
        return None

    def _send_single_email(self, email_job: Dict[str, Any]) -> bool:
        """Simulate sending an email (replace with actual Gmail/smtp)."""
        account_id = email_job["account_id"]
        account = self.email_accounts[account_id]

        # Update account stats
        account["sent_today"] += 1
        account["last_send"] = datetime.utcnow()

        print(f"Sent email #{email_job['attempts']+1} for lead {email_job['lead_id']} via {account_id}")
        
        # Simulate success (in reality would catch exceptions)
        return True

    def _sender_worker(self, worker_id: int) -> None:
        """Background worker thread that processes the queue."""
        print(f"SendHead worker {worker_id} started")
        while self.is_running:
            try:
                email_job = self.send_queue.get(timeout=5)
                email_job["attempts"] += 1

                # Get available account
                account_id = self.get_next_available_account()
                if not account_id:
                    # Put back and wait
                    self.send_queue.put(email_job)
                    time.sleep(60)
                    continue

                # Reassign to available account
                email_job["account_id"] = account_id

                # Send
                success = self._send_single_email(email_job)
                if not success:
                    # Retry once
                    if email_job["attempts"] < 2:
                        self.send_queue.put(email_job)

                self.send_queue.task_done()
                time.sleep(self.min_gap_seconds)

            except Empty:
                continue
            except Exception as e:
                print(f"SendHead worker {worker_id} error: {e}")

    def start_sending(self, num_workers: int = 3) -> None:
        """Start background sender threads."""
        self.is_running = True
        for i in range(num_workers):
            t = threading.Thread(target=self._sender_worker, args=(i,))
            t.daemon = True
            t.start()
            self.sending_threads.append(t)
        print(f"SendHead started with {num_workers} workers")

    def stop_sending(self) -> None:
        """Stop all sender threads."""
        self.is_running = False
        print("SendHead stopping...")

# Example usage
if __name__ == "__main__":
    sender = SendHead()
    sender.add_email_account("acc-001", {"email": "leadgen@company.com"})
    sender.start_sending(num_workers=2)

    # Queue some emails
    for i in range(5):
        sender.queue_email(f"lead-{i}", "acc-001", 
                          f"Subject {i}", f"Body content {i}")

    time.sleep(60)
    sender.stop_sending()
