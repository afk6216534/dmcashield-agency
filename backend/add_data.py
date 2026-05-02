# Add Sample Data to DMCAShield Database
import sqlite3
import uuid
from datetime import datetime

DB_PATH = "dmcashield.db"

# Sample Leads
leads_data = [
    ("lead-001", "Joe's Diner", "joe@joesdiner.com", "(512) 555-0101", "Austin", "TX", 78, "hot"),
    ("lead-002", "Smith Dental Care", "dr.smith@smithdental.com", "(713) 555-0202", "Houston", "TX", 85, "hot"),
    ("lead-003", "Glamour Salon", "info@glamoursalon.com", "(214) 555-0303", "Dallas", "TX", 72, "warm"),
    ("lead-004", "City General Hospital", "admin@citygeneral.org", "(210) 555-0404", "San Antonio", "TX", 68, "warm"),
    ("lead-005", "Luxury Inn Hotel", "bookings@luxuryinn.com", "(512) 555-0505", "Austin", "TX", 65, "warm"),
    ("lead-006", "Tech Repair Shop", "tech@techrepair.com", "(512) 555-0606", "Austin", "TX", 58, "cold"),
    ("lead-007", "Fitness First Gym", "info@fitnessfirst.com", "(713) 555-0707", "Houston", "TX", 55, "cold"),
    ("lead-008", "Blue Moon Cafe", "owner@bluemooncafe.com", "(214) 555-0808", "Dallas", "TX", 62, "warm"),
    ("lead-009", "Quick Fix Auto", "service@quickfixauto.com", "(210) 555-0909", "San Antonio", "TX", 48, "cold"),
    ("lead-010", "Wellness Center", "contact@wellnesscenter.com", "(512) 555-1010", "Austin", "TX", 75, "hot"),
]

# Sample Tasks  
tasks_data = [
    ("task-001", "DMCA Scraper - Restaurant targets", "Finding restaurant targets with negative reviews", "active", 73),
    ("task-002", "Email Outreach Campaign", "Sending follow-up emails to warm leads", "active", 45),
    ("task-003", "Lead Validation Pipeline", "Validating scraped lead data", "active", 89),
    ("task-004", "Review Monitor - Austin", "Monitoring new reviews in Austin", "paused", 34),
    ("task-005", "Cold Email Sequence", "Sending cold emails to new prospects", "pending", 0),
]

# Sample Campaigns
campaigns_data = [
    ("camp-001", "DMCA Removal Outreach", "Remove Your Negative Reviews Today", "Our legal team can help remove false negative reviews...", "active", 1247, 349, 89),
    ("camp-002", "Review Response Campaign", "Professional Response Service", "We respond to reviews professionally...", "active", 892, 234, 56),
    ("camp-003", "Partner Invitation", "Join Our Partner Program", "Partner with us for mutual growth...", "active", 456, 123, 34),
]

# Sample Email Accounts
accounts_data = [
    ("acc-001", "outreach@dmcashield.com", "resend", "active", 234, 500, 98),
    ("acc-002", "sales@dmcashield.com", "resend", "active", 156, 500, 95),
    ("acc-003", "support@dmcashield.com", "gmail", "warming", 0, 100, 100),
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Insert Leads
for lead in leads_data:
    c.execute("INSERT OR REPLACE INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))", 
              (lead[0], lead[1], lead[2], lead[3], lead[4], lead[5], lead[6], lead[7]))

# Insert Tasks
for task in tasks_data:
    c.execute("INSERT OR REPLACE INTO tasks VALUES (?, ?, ?, ?, ?, datetime('now'))",
              (task[0], task[1], task[2], task[3], task[4]))

# Insert Campaigns  
for camp in campaigns_data:
    c.execute("INSERT OR REPLACE INTO campaigns VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
              (camp[0], camp[1], camp[2], camp[3], camp[4], camp[5], camp[6]))

# Insert Accounts
for acc in accounts_data:
    c.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
              (acc[0], acc[1], acc[2], acc[3], acc[4], acc[5], acc[6]))

conn.commit()
conn.close()

print("✅ Sample data added successfully!")
print(f"   - {len(leads_data)} leads")
print(f"   - {len(tasks_data)} tasks")
print(f"   - {len(campaigns_data)} campaigns")
print(f"   - {len(accounts_data)} email accounts")