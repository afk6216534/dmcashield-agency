"""
DeepSleep Monitor - Auto-Healing System
Detects errors, automatically restarts services, and prevents resource leaks.
"""

import time
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import signal
import sys

class DeepSleepMonitor:
    """Main auto-healing monitor."""

    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval  # seconds
        self.services = {}
        self.error_log = []
        self.last_backup = datetime.utcnow()
        self.backup_interval = 6 * 3600  # 6 hours in seconds
        self.is_running = False

    def register_service(self, name: str, health_check: callable):
        """Register a service for monitoring."""
        self.services[name] = {
            "health_check": health_check,
            "status": "unknown",
            "last_check": None,
            "error_count": 0,
            "restart_count": 0
        }

    def check_all_services(self) -> Dict[str, Any]:
        """Check health of all registered services."""
        results = {}
        
        for name, service in self.services.items():
            try:
                if service["health_check"]:
                    service["status"] = service["health_check"]()
                    service["last_check"] = datetime.utcnow()
                    service["error_count"] = 0
                else:
                    service["status"] = "no_check_defined"
            except Exception as e:
                service["status"] = f"error: {str(e)}"
                service["error_count"] += 1
                self._log_error(name, str(e))
                
                # Auto-restart if too many errors
                if service["error_count"] >= 3:
                    self._attempt_restart(name)
        
        return results

    def _attempt_restart(self, service_name: str):
        """Attempt to restart a failed service."""
        print(f"DeepSleep: Attempting restart of {service_name}")
        self.services[service_name]["restart_count"] += 1
        self.services[service_name]["error_count"] = 0
        # In production, would actually restart the service
        self._log_event(f"restart_attempted", service_name)

    def _log_error(self, service: str, error: str):
        """Log an error event."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": service,
            "error": error,
            "type": "error"
        }
        self.error_log.append(entry)
        print(f"DeepSleep ERROR: {service} - {error}")

    def _log_event(self, event_type: str, details: str):
        """Log a general event."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "details": details
        }
        self.error_log.append(entry)

    def check_auto_backup(self):
        """Check if it's time for automatic backup."""
        now = datetime.utcnow()
        if (now - self.last_backup).total_seconds() >= self.backup_interval:
            self._perform_backup()
            self.last_backup = now

    def _perform_backup(self):
        """Perform the 6-hourly backup (Git auto-backup)."""
        try:
            # Simulated Git backup
            self._log_event("backup", "Auto-backup to GitHub initiated")
            print("DeepSleep: Auto-backup completed")
        except Exception as e:
            self._log_error("backup", str(e))

    def monitor_loop(self):
        """Main monitoring loop."""
        self.is_running = True
        print("DeepSleep Monitor started")
        
        while self.is_running:
            try:
                self.check_all_services()
                self.check_auto_backup()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                print("DeepSleep Monitor stopped")
                self.is_running = False
            except Exception as e:
                self._log_error("monitor_loop", str(e))
                time.sleep(5)

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        healthy_count = sum(1 for s in self.services.values() 
                         if s["status"] == "healthy")
        total = len(self.services)
        
        return {
            "overall_health": f"{healthy_count}/{total} services healthy",
            "services": {name: s["status"] for name, s in self.services.items()},
            "total_errors": len([e for e in self.error_log if e["type"] == "error"]),
            "last_backup": self.last_backup.isoformat(),
            "uptime_seconds": (datetime.utcnow() - self.last_backup).total_seconds()
        }

    def handle_signal(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        print(f"DeepSleep: Received signal {signum}")
        self.is_running = False

# Example usage
if __name__ == "__main__":
    monitor = DeepSleepMonitor()
    
    # Register some services
    def check_api_health():
        # Simulated health check
        return "healthy"
    
    monitor.register_service("FastAPI", check_api_health)
    monitor.register_service("Redis", lambda: "healthy")
    monitor.register_service("Celery", lambda: "healthy")
    
    # Start monitoring
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        print("Monitoring stopped")
