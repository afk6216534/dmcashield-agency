# DMCAShield Backend Service Configuration
# Runs 24/7 with auto-restart and self-healing

import uvicorn
import sys
import os
import signal
import time
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DB_PATH = PROJECT_ROOT / "dmcashield.db"

class GuardianAgent:
    """24/7 Autonomous Agent - Monitors and self-heals"""
    
    def __init__(self):
        self.process = None
        self.start_time = None
        self.restart_count = 0
        self.running = True
        
    def start_backend(self):
        """Start the backend server"""
        print("🛡️ DMCAShield Guardian - Starting 24/7 Service...")
        self.process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main_simple:app", 
             "--host", "127.0.0.1", "--port", "8000",
             "--reload"],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.start_time = time.time()
        print(f"✅ Backend started (PID: {self.process.pid})")
        
    def monitor(self):
        """Monitor and self-heal"""
        while self.running:
            try:
                # Check if process is alive
                if self.process.poll() is not None:
                    self.restart_count += 1
                    print(f"⚠️ Process died. Restart #{self.restart_count}...")
                    time.sleep(2)
                    self.start_backend()
                    
                # Health check
                try:
                    import requests
                    r = requests.get("http://localhost:8000/health", timeout=5)
                    if r.status_code != 200:
                        print("⚠️ Health check failed, restarting...")
                        self.process.terminate()
                        time.sleep(2)
                        self.start_backend()
                except:
                    pass
                    
                # Auto-reload on file changes
                self.check_file_changes()
                
                time.sleep(10)
                
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(5)
                
    def check_file_changes(self):
        """Check for file changes and auto-reload"""
        # The --reload flag handles this automatically
        pass
        
    def stop(self):
        """Stop the service"""
        self.running = False
        if self.process:
            self.process.terminate()
        print("🛡️ Service stopped")

if __name__ == "__main__":
    guardian = GuardianAgent()
    
    def signal_handler(sig, frame):
        print("\n🛡️ Shutting down...")
        guardian.running = False
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    guardian.start_backend()
    guardian.monitor()