import sqlite3
import os

# Update database dmcashield-agency/data/dmcashield.db
db_path = "data/dmcashield.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 1. Update gmail_config table
    c.execute("UPDATE gmail_config SET email = ?, status = 'disconnected', app_password_set = 0 WHERE id = 1", ('af6216em@gmail.com',))
    
    # 2. Insert into accounts table
    c.execute("INSERT OR REPLACE INTO accounts (id, email, provider, status, sent_today, daily_limit, health_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
              ('acc-gmail-primary', 'af6216em@gmail.com', 'gmail', 'active', 0, 500, 100))
    
    conn.commit()
    print("Database updated successfully!")
    conn.close()
else:
    print("Database file not found:", db_path)

# Update backend/.env file
env_path = "backend/.env"
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Replace the placeholder email
    if "GMAIL_EMAIL=your@gmail.com" in content:
        content = content.replace("GMAIL_EMAIL=your@gmail.com", "GMAIL_EMAIL=af6216em@gmail.com")
        print("Updated placeholder GMAIL_EMAIL in .env")
    else:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("GMAIL_EMAIL="):
                lines[i] = "GMAIL_EMAIL=af6216em@gmail.com"
                break
        content = '\n'.join(lines)
        print("Replaced GMAIL_EMAIL value in .env")
        
    with open(env_path, 'w') as f:
        f.write(content)
else:
    print(".env file not found:", env_path)
