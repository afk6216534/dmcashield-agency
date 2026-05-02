import sqlite3, uuid

DB = "dmcashield.db"
conn = sqlite3.connect(DB)
c = conn.cursor()

# Check tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
print("Tables:", tables)

# Add minimal leads if empty
c.execute("SELECT COUNT(*) FROM leads")
if c.fetchone()[0] == 0:
    print("Adding leads...")
    leads = [
        (str(uuid.uuid4())[:8], "Joe's Diner", "joe@joesdiner.com", "(512) 555-0101", "Austin", "TX", 78, "hot"),
        (str(uuid.uuid4())[:8], "Smith Dental", "dr@smith.com", "(713) 555-0202", "Houston", "TX", 85, "hot"),
    ]
    for l in leads:
        c.execute("INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), '', '', 0, '', 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')", l)

# Add tasks if empty  
c.execute("SELECT COUNT(*) FROM tasks")
if c.fetchone()[0] == 0:
    print("Adding tasks...")
    tasks = [
        (str(uuid.uuid4())[:8], "DMCA Scraper", "Finding targets", "active", 73),
        (str(uuid.uuid4())[:8], "Email Outreach", "Sending emails", "active", 45),
    ]
    for t in tasks:
        c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, datetime('now'), '', '', '', '', '')", t)

conn.commit()
print("Done!")
conn.close()