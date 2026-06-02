import unittest
import os
import sys
import time
import subprocess
import socket
import requests

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

BASE_URL = "http://127.0.0.1:8000"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

class TestRealFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_process = None
        if not is_port_open(8000):
            print("Starting FastAPI backend on port 8000...")
            cls.server_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main_simple:app", "--app-dir", "backend", "--host", "127.0.0.1", "--port", "8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for server to start
            for _ in range(10):
                if is_port_open(8000):
                    print("Backend started successfully!")
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Failed to start FastAPI backend")

    @classmethod
    def tearDownClass(cls):
        if cls.server_process:
            print("Stopping FastAPI backend...")
            cls.server_process.terminate()
            cls.server_process.wait()

    def test_gmail_test_invalid_credentials(self):
        """Call /api/gmail/test with invalid credentials and verify failure."""
        response = requests.post(f"{BASE_URL}/api/gmail/test", json={
            "email": "invalid_test_email@gmail.com",
            "app_password": "abcd efgh ijkl mnop"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get("success", False))
        self.assertIn("message", data)

    def test_real_leads_retrieval(self):
        """Retrieve leads via /api/real-leads and check schema properties."""
        response = requests.get(f"{BASE_URL}/api/real-leads")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("leads", data)
        self.assertIn("stats", data)
        self.assertEqual(data.get("source"), "real_database")
        
        # If there are leads, check fields
        if len(data["leads"]) > 0:
            lead = data["leads"][0]
            self.assertIn("id", lead)
            self.assertIn("business_name", lead)
            self.assertIn("email_primary", lead)
            self.assertIn("lead_score", lead)

    def test_add_and_delete_real_lead(self):
        """Test manually adding and deleting a real lead."""
        test_lead = {
            "business_name": "Test Bakery Houston",
            "email_primary": "bakery-test@example.com",
            "phone": "713-555-0123",
            "website": "https://testbakeryhouston.com",
            "city": "Houston",
            "state": "Texas",
            "niche": "bakery",
            "current_rating": 3.8,
            "review_count": 12,
            "negative_review_count": 3
        }
        
        # Add lead
        response = requests.post(f"{BASE_URL}/api/real-leads/add", json=test_lead)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data.get("status"), "added")
        lead_id = data["id"]
        
        # Verify it exists in database
        response_get = requests.get(f"{BASE_URL}/api/real-leads")
        leads = response_get.json()["leads"]
        found = False
        for lead in leads:
            if lead["id"] == lead_id:
                found = True
                self.assertEqual(lead["business_name"], test_lead["business_name"])
                self.assertEqual(lead["email_primary"], test_lead["email_primary"])
                self.assertEqual(lead["niche"], test_lead["niche"])
                self.assertEqual(lead["city"], test_lead["city"])
                break
        self.assertTrue(found)
        
        # Delete lead
        response_del = requests.delete(f"{BASE_URL}/api/real-leads/{lead_id}")
        self.assertEqual(response_del.status_code, 200)
        self.assertEqual(response_del.json().get("status"), "deleted")

    def test_run_scraper_pipeline_mock(self):
        """Test task creation triggers background thread scraping."""
        # Create a mock scraping task
        response = requests.post(f"{BASE_URL}/api/tasks", json={
            "business_type": "bakery-test",
            "city": "Houston",
            "state": "Texas",
            "country": "USA"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "launched")
        self.assertEqual(data.get("phase"), "scraping")
        task_id = data.get("task_id")
        self.assertTrue(task_id.startswith("task-"))

if __name__ == "__main__":
    unittest.main()
