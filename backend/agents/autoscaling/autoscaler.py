"""
Auto-Scaling System for DMCAShield Agency
=======================================
Dynamically allocates resources based on queue sizes and system load
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import os
import json

class AutoScaler:
    """Monitors system load and auto-scales agent workers"""

    def __init__(self):
        self.scaling_config = {
            "send_queue_threshold_high": 50,
            "send_queue_threshold_low": 10,
            "max_workers": 10,
            "min_workers": 2,
            "scale_up_increment": 2,
            "scale_down_increment": 1,
            "check_interval_seconds": 30,
            "cpu_threshold_high": 80.0,
            "cpu_threshold_low": 30.0
        }
        self.worker_pools = {}
        self.monitoring_active = False
        self.monitor_thread = None
        self.current_workers = {
            "send_head": 2,
            "scrape_head": 1,
            "marketing_head": 1,
            "analytics_head": 1
        }

    def start_monitoring(self):
        """Start the auto-scaling monitor"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        print("Auto-scaler monitoring started")

    def stop_monitoring(self):
        """Stop the auto-scaling monitor"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Auto-scaler monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._check_and_scale()
                time.sleep(self.scaling_config["check_interval_seconds"])
            except Exception as e:
                print(f"Auto-scaler error: {e}")
                time.sleep(5)

    def _check_and_scale(self):
        """Check system metrics and scale accordingly"""
        # Get current queue sizes
        queue_sizes = self._get_queue_sizes()
        system_load = self._get_system_load()

        # Scale send_head workers based on queue
        send_queue_size = queue_sizes.get("send_queue", 0)
        self._scale_worker_pool("send_head", send_queue_size)

        # Scale other workers based on system load
        for worker_type in ["scrape_head", "marketing_head", "analytics_head"]:
            current_load = system_load.get(worker_type, 0)
            self._scale_generic_worker(worker_type, current_load)

        # Save state to persistent memory
        self._save_scaling_state()

    def _get_queue_sizes(self) -> Dict[str, int]:
        """Get current queue sizes from agents"""
        sizes = {}
        try:
            from agents.email_sending.send_head import send_head
            sizes["send_queue"] = len(send_head.send_queue)
        except:
            sizes["send_queue"] = 0

        # Add other queues as needed
        return sizes

    def _get_system_load(self) -> Dict[str, float]:
        """Get system load percentages"""
        load = {}
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            load["overall"] = max(cpu_percent, memory_percent)
            load["send_head"] = cpu_percent * 0.3  # Placeholder weights
            load["scrape_head"] = cpu_percent * 0.2
            load["marketing_head"] = cpu_percent * 0.2
            load["analytics_head"] = cpu_percent * 0.3
        except ImportError:
            # psutil not available, use placeholder
            load = {k: 50.0 for k in ["overall", "send_head", "scrape_head", "marketing_head", "analytics_head"]}

        return load

    def _scale_worker_pool(self, worker_type: str, queue_size: int):
        """Scale worker pool based on queue size"""
        current = self.current_workers.get(worker_type, 2)

        if queue_size > self.scaling_config["send_queue_threshold_high"]:
            # Scale up
            new_count = min(current + self.scaling_config["scale_up_increment"],
                           self.scaling_config["max_workers"])
            if new_count != current:
                self._adjust_workers(worker_type, new_count)
                print(f"Scaled {worker_type} UP to {new_count} workers (queue: {queue_size})")

        elif queue_size < self.scaling_config["send_queue_threshold_low"]:
            # Scale down
            new_count = max(current - self.scaling_config["scale_down_increment"],
                           self.scaling_config["min_workers"])
            if new_count != current:
                self._adjust_workers(worker_type, new_count)
                print(f"Scaled {worker_type} DOWN to {new_count} workers (queue: {queue_size})")

    def _scale_generic_worker(self, worker_type: str, load: float):
        """Scale worker based on system load"""
        current = self.current_workers.get(worker_type, 1)

        if load > self.scaling_config["cpu_threshold_high"]:
            new_count = min(current + 1, self.scaling_config["max_workers"])
            if new_count != current:
                self._adjust_workers(worker_type, new_count)
                print(f"Scaled {worker_type} UP to {new_count} (load: {load:.1f}%)")

        elif load < self.scaling_config["cpu_threshold_low"]:
            new_count = max(current - 1, self.scaling_config["min_workers"])
            if new_count != current:
                self._adjust_workers(worker_type, new_count)
                print(f"Scaled {worker_type} DOWN to {new_count} (load: {load:.1f}%)")

    def _adjust_workers(self, worker_type: str, new_count: int):
        """Adjust number of workers for a given type"""
        self.current_workers[worker_type] = new_count

        # In a real implementation, this would start/stop Docker containers or processes
        # For now, we just update the count
        print(f"Adjusted {worker_type} workers to {new_count}")

    def _save_scaling_state(self):
        """Save scaling state to persistent memory"""
        try:
            from agents.memory.persistent_memory import persistent_memory
            state = {
                "timestamp": datetime.utcnow().isoformat(),
                "current_workers": self.current_workers,
                "config": self.scaling_config
            }
            persistent_memory.save_conversation(
                role="autoscaler",
                content=json.dumps(state),
                encrypted=False
            )
        except Exception as e:
            print(f"Failed to save scaling state: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get current auto-scaler status"""
        return {
            "active": self.monitoring_active,
            "current_workers": self.current_workers.copy(),
            "config": self.scaling_config.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def update_config(self, new_config: Dict[str, Any]):
        """Update scaling configuration"""
        self.scaling_config.update(new_config)
        print(f"Auto-scaler config updated: {new_config}")
        self._save_scaling_state()

# Global auto-scaler instance
auto_scaler = AutoScaler()