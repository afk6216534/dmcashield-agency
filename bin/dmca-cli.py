#!/usr/bin/env python3
"""
DMCAShield CLI - Direct commands for your AI team
=================================================
Give this file to Claude Code or use directly

Quick Tasks:
1. Scrape leads: python dmca-cli.py scrape lawyer NYC NY
2. Send emails: python dmca-cli.py send
3. Check leads: python dmca-cli.py leads
4. Start system: python dmca-cli.py start
5. Auto mode: python dmca-cli.py auto
"""

import requests
import sys
import json

BASE_URL = "http://localhost:8000"

def cmd_scrape(business, city, state):
    """Scrape leads"""
    r = requests.post(f"{BASE_URL}/api/tasks/", json={
        "business_type": business,
        "city": city,
        "state": state,
        "country": "USA"
    })
    print(r.text)

def cmd_leads():
    """Get hot leads"""
    r = requests.get(f"{BASE_URL}/api/sales/hot-leads")
    data = r.json()
    print(f"Hot leads: {len(data)}")
    for lead in data[:5]:
        print(f"  - {lead.get('name')} ({lead.get('email')})")

def cmd_start():
    """Start server"""
    print("Starting DMCAShield server...")
    r = requests.post(f"{BASE_URL}/api/autonomous/start")
    print(r.text)

def cmd_auto():
    """Start autonomous mode"""
    print("Starting autonomous mode 24/7...")
    r = requests.post(f"{BASE_URL}/api/autonomous/full_start")
    print(r.text)

def cmd_status():
    """Get system status"""
    r = requests.get(f"{BASE_URL}/api/analytics/dashboard")
    print(r.text)

def cmd_leads_all():
    """Get all leads"""
    r = requests.get(f"{BASE_URL}/api/leads/?limit=20")
    data = r.json()
    print(f"Total leads: {len(data)}")
    for lead in data:
        print(f"  - {lead.get('name')} | {lead.get('status')} | Score: {lead.get('score', 0)}")

def cmd_chat(msg):
    """Chat with JARVIS"""
    r = requests.post(f"{BASE_URL}/api/jarvis/chat", json={"message": msg})
    print(r.json().get("response", ""))

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "scrape":
        # python dmca-cli.py scrape lawyer NYC NY
        cmd_scrape(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "leads":
        cmd_leads()
    elif cmd == "leads-all":
        cmd_leads_all()
    elif cmd == "start":
        cmd_start()
    elif cmd == "auto":
        cmd_auto()
    elif cmd == "status":
        cmd_status()
    elif cmd == "chat":
        cmd_chat(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()