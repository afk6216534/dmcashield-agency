"""
Advanced Monitoring Dashboard - Real-time system oversight
Provides comprehensive visibility into all 12 departments
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import json
import os
import threading
import time
from collections import defaultdict, deque

@dataclass
class PerformanceMetric:
    """Tracks performance metrics for each department"""
    department: str
    metric_name: str
    value: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    unit: str = "count"

@dataclass
class Alert:
    """System alerts and notifications"""
    id: str = field(default_factory=lambda: str(os.urandom(8).hex()))
    severity: str = "info"  # info, warning, critical
    department: str = ""
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    resolved: bool = False
    acknowledged: bool = False

class MonitoringDashboard:
    """Enterprise-grade monitoring and observability system"""

    def __init__(self):
        self.departments = self._initialize_departments()
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.alerts: List[Alert] = []
        self.performance_baselines: Dict[str, Dict] = {}
        self.auto_scaling_config = self._load_scaling_config()
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None

    def _initialize_departments(self) -> Dict[str, Dict]:
        """Initialize all 12 departments with their metrics"""
        return {
            "ceo": {
                "name": "Chief Executive Officer",
                "role": "Strategic coordination & task prioritization",
                "metrics": ["tasks_coordinated", "decisions_made", "departments_healthy"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "scraping": {
                "name": "Lead Generation",
                "role": "Web scraping & data acquisition",
                "metrics": ["leads_found", "pages_scraped", "success_rate"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "leads_today": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "validation": {
                "name": "Lead Validation",
                "role": "Data enrichment & quality assurance",
                "metrics": ["leads_validated", "enrichment_rate", "accuracy_score"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "marketing": {
                "name": "Campaign Management",
                "role": "Email sequences & A/B testing",
                "metrics": ["campaigns_active", "emails_created", "open_rate"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "sequences_active": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "email_sending": {
                "name": "Email Delivery",
                "role": "SMTP delivery & account management",
                "metrics": ["emails_sent", "delivery_rate", "bounce_rate"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "daily_volume": 0,
                "accounts_active": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "tracking": {
                "name": "Engagement Tracking",
                "role": "Analytics & behavioral monitoring",
                "metrics": ["events_tracked", "clicks_recorded", "engagement_score"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "sales": {
                "name": "Lead Conversion",
                "role": "Hot lead handling & closing",
                "metrics": ["leads_converted", "conversion_rate", "revenue_tracked"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "hot_leads": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "sheets": {
                "name": "Reporting & Dashboards",
                "role": "Data visualization & exports",
                "metrics": ["reports_generated", "sheets_updated", "data_accuracy"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "accounts": {
                "name": "Account Management",
                "role": "Email accounts & reputation",
                "metrics": ["accounts_managed", "warmup_progress", "reputation_score"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "accounts_warming": 0,
                "daily_limits": {},
                "last_activity": datetime.utcnow().isoformat()
            },
            "tasks": {
                "name": "Task Coordination",
                "role": "Queue management & scheduling",
                "metrics": ["tasks_processed", "queue_efficiency", "avg_completion_time"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "active_tasks": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "ml": {
                "name": "Machine Learning",
                "role": "Predictive modeling & optimization",
                "metrics": ["models_trained", "prediction_accuracy", "learning_rate"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "models_active": 0,
                "last_retraining": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat()
            },
            "jarvis": {
                "name": "Natural Language Interface",
                "role": "Human-AI interaction & commands",
                "metrics": ["queries_processed", "response_time", "satisfaction_score"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "queries_today": 0,
                "last_activity": datetime.utcnow().isoformat()
            },
            "memory": {
                "name": "Persistent Memory",
                "role": "Long-term storage & audit trail",
                "metrics": ["memories_stored", "retrieval_time", "storage_used"],
                "health_score": 100,
                "status": "operational",
                "queue_depth": 0,
                "throughput": 0,
                "total_memories": 0,
                "last_backup": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat()
            }
        }

    def _load_scaling_config(self) -> Dict[str, Any]:
        """Load auto-scaling configuration"""
        return {
            "enabled": True,
            "check_interval": 30,  # seconds
            "scale_up_threshold": 80,  # % utilization
            "scale_down_threshold": 20,  # % utilization
            "max_workers": 100,
            "min_workers": 1,
            "departments": {
                "email_sending": {"max_workers": 50, "scale_by_queue": True},
                "scraping": {"max_workers": 30, "scale_by_queue": True},
                "validation": {"max_workers": 25, "scale_by_queue": True},
                "marketing": {"max_workers": 20, "scale_by_queue": False},
                "sales": {"max_workers": 15, "scale_by_queue": True},
                "tracking": {"max_workers": 20, "scale_by_queue": False},
                "ml": {"max_workers": 10, "scale_by_queue": False},
            }
        }

    def update_department_metric(self, department: str, metric: str, value: float, unit: str = "count"):
        """Update a performance metric for a department"""
        metric_obj = PerformanceMetric(
            department=department,
            metric_name=metric,
            value=value,
            unit=unit
        )
        self.metrics_history[department].append(metric_obj)

        # Update department state
        if department in self.departments:
            self.departments[department]["last_activity"] = datetime.utcnow().isoformat()

            # Update specific metrics
            if metric == "queue_depth":
                self.departments[department]["queue_depth"] = value
            elif metric == "throughput":
                self.departments[department]["throughput"] = value

        # Check for alerts
        self._check_alert_conditions(department, metric, value)

    def _check_alert_conditions(self, department: str, metric: str, value: float):
        """Check if metric triggers an alert"""
        alerts = []

        # Queue depth alerts
        if metric == "queue_depth" and value > 100:
            alerts.append(Alert(
                severity="warning" if value < 500 else "critical",
                department=department,
                message=f"High queue depth: {value} items pending"
            ))

        # Health score alerts
        if metric == "health_score" and value < 70:
            alerts.append(Alert(
                severity="warning" if value > 50 else "critical",
                department=department,
                message=f"Low health score: {value}%"
            ))

        # Throughput alerts
        if metric == "throughput" and value == 0:
            # Check if department should be active
            if department in ["email_sending", "scraping", "sales"]:
                alerts.append(Alert(
                    severity="warning",
                    department=department,
                    message=f"Zero throughput - possible stall"
                ))

        for alert in alerts:
            self.alerts.append(alert)

    def get_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview"""
        now = datetime.utcnow()

        # Calculate aggregate metrics
        total_queues = sum(d.get("queue_depth", 0) for d in self.departments.values())
        total_throughput = sum(d.get("throughput", 0) for d in self.departments.values())
        avg_health = sum(d.get("health_score", 100) for d in self.departments.values()) / len(self.departments)

        # Active alerts
        active_alerts = [a for a in self.alerts if not a.resolved]
        critical_alerts = [a for a in active_alerts if a.severity == "critical"]
        warning_alerts = [a for a in active_alerts if a.severity == "warning"]

        # System health
        system_health = "healthy" if avg_health > 90 else "degraded" if avg_health > 70 else "critical"

        # Department status summary
        status_summary = {}
        for dept_key, dept in self.departments.items():
            status_summary[dept_key] = {
                "name": dept["name"],
                "status": dept["status"],
                "health_score": dept["health_score"],
                "queue_depth": dept.get("queue_depth", 0),
                "throughput": dept.get("throughput", 0),
                "last_activity": dept["last_activity"],
                "role": dept["role"]
            }

        return {
            "timestamp": now.isoformat(),
            "system_health": {
                "overall": system_health,
                "average_health_score": round(avg_health, 2),
                "total_departments": len(self.departments),
                "operational_departments": sum(1 for d in self.departments.values() if d["status"] == "operational"),
                "total_alerts": len(active_alerts),
                "critical_alerts": len(critical_alerts),
                "warning_alerts": len(warning_alerts)
            },
            "aggregate_metrics": {
                "total_queue_depth": total_queues,
                "total_throughput": total_throughput,
                "alerts_active": len(active_alerts)
            },
            "departments": status_summary,
            "alerts": {
                "critical": [asdict(a) for a in critical_alerts],
                "warning": [asdict(a) for a in warning_alerts],
                "all_active": [asdict(a) for a in active_alerts]
            },
            "auto_scaling": {
                "enabled": self.auto_scaling_config["enabled"],
                "next_check_in": self.auto_scaling_config["check_interval"]
            }
        }

    def get_department_detail(self, department: str) -> Dict[str, Any]:
        """Get detailed information for a specific department"""
        if department not in self.departments:
            raise ValueError(f"Unknown department: {department}")

        dept = self.departments[department]

        # Get recent metrics
        recent_metrics = list(self.metrics_history[department])[-50:]

        return {
            "name": dept["name"],
            "role": dept["role"],
            "status": dept["status"],
            "health_score": dept["health_score"],
            "current_metrics": {
                "queue_depth": dept.get("queue_depth", 0),
                "throughput": dept.get("throughput", 0),
                "last_activity": dept["last_activity"]
            },
            "department_specific": {k: v for k, v in dept.items()
                                   if k not in ["name", "role", "metrics", "health_score", "status", "queue_depth", "throughput", "last_activity"]},
            "recent_performance": [
                {
                    "metric": m.metric_name,
                    "value": m.value,
                    "unit": m.unit,
                    "timestamp": m.timestamp
                }
                for m in recent_metrics
            ],
            "performance_trends": self._calculate_trends(department, recent_metrics)
        }

    def _calculate_trends(self, department: str, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Calculate performance trends"""
        if not metrics:
            return {}

        # Group by metric type
        by_type = defaultdict(list)
        for m in metrics:
            by_type[m.metric_name].append(m.value)

        trends = {}
        for metric_name, values in by_type.items():
            if len(values) >= 2:
                trend = "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "stable"
                change_pct = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
                trends[metric_name] = {
                    "trend": trend,
                    "change_percentage": round(change_pct, 2),
                    "current": values[-1],
                    "previous": values[0]
                }

        return trends

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                return True
        return False

    def start_monitoring(self):
        """Start background monitoring thread"""
        if self.running:
            return

        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.running:
            try:
                # Check system health
                overview = self.get_overview()

                # Auto-scaling check
                if self.auto_scaling_config["enabled"]:
                    self._auto_scale_check(overview)

                # Health check
                for dept_key, dept in self.departments.items():
                    last_activity = datetime.fromisoformat(dept["last_activity"].replace("Z", "+00:00"))
                    if (datetime.utcnow() - last_activity).total_seconds() > 300:  # 5 minutes
                        self.update_department_metric(dept_key, "health_score", max(50, dept["health_score"] - 10))

                time.sleep(self.auto_scaling_config["check_interval"])

            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(30)

    def _auto_scale_check(self, overview: Dict[str, Any]):
        """Check and perform auto-scaling"""
        total_queue = overview["aggregate_metrics"]["total_queue_depth"]

        for dept_key in self.auto_scaling_config["departments"]:
            if dept_key in self.departments:
                dept = self.departments[dept_key]
                queue_depth = dept.get("queue_depth", 0)

                # Scale up if queue is large
                if queue_depth > 50 and self.auto_scaling_config["departments"][dept_key]["scale_by_queue"]:
                    # Would trigger scale up in real implementation
                    pass

# Global monitoring instance
monitoring_dashboard = MonitoringDashboard()