# TEAM_SHARE — v5.4 Status
# Last Updated: 2026-06-05 13:08 PKT

## 🔴 LIVE DEPLOYMENTS
- **Frontend**: https://dmcashield.netlify.app
- **Backend**: https://dmcashield-agency.vercel.app
- **Local Dev Server**: http://localhost:5177 (Frontend) | http://localhost:8000 (Backend)

## CURRENT VERSION: v5.4 (Deployed & Live)

### v5.4 — Persistent Real-World Scraping Tasks & Lead Database with Cloud Sync Integration
- **SQLite Task Database Integration**: Wired `GET /api/tasks` to query the SQLite `scrape_tasks` table (with fallback to `DEMO_TASKS`), mapping lead counts dynamically to ensure UI responsiveness.
- **Real-World Scraper Activation**: Configured `POST /api/tasks` to run the real HTTP and OpenStreetMap business scraper pipeline synchronously, saving scraped businesses to `real_leads` in the database.
- **SQLite Lead Database Integration**: Connected `/api/leads`, `/api/leads/<lead_id>`, `/api/leads/export`, `/api/leads/scored`, `/api/leads/<lead_id>/full`, and `/api/leads/important` to read dynamically from the SQLite `real_leads` and `email_log` tables.
- **Automated Cloud Sync Persistence**: Integrated `save_all_tasks_to_cloud` and `save_all_leads_to_cloud` in `agents/cloud_db.py` to backup and restore tasks and leads automatically to `kvdb.io` bucket `5xaC4pip12aoA57uV6EGiq`. This makes all scrapings permanent across Vercel container recycles and synced across other dev computers.
- **Mark Important Synchronized**: Connected `/api/leads/<lead_id>/mark-important` to update the lead status/notes in SQLite and automatically push the backup update to the cloud.


---

## 📊 System Status

### Active Endpoints & Verification (Live on Vercel)
- `/api/db/info` → Verified production environment active
- `/api/gmail/status` → Verified clean disconnected/connected status (reads env vars + DB)
- `/api/real-leads` → Verified real SQLite CRUD operations
- `/api/scrape` → Verified live Houston Dentist scrape -> 3 real leads successfully generated and saved!

---

## 🔧 TASKS FOR TEAM

### Claude Code (Frontend) — ALL COMPLETED ✅
- [x] **Settings.jsx** — Wired Gmail config card to connection test and save endpoints
- [x] **LaunchTask.jsx** — Wired to `POST /api/scrape` and added scraping history table
- [x] **LeadDatabase.jsx** — Verified Demo/Real toggle reads active SQLite database
- [x] **CampaignManager.jsx** — Resolved syntax errors and verified build output
- [x] **Sidebar.jsx** — Configured routing for boss view pages (CEO, JARVIS, Departments)
- [x] **App.jsx** — Added routing definitions for boss view pages

### OpenCode (Backend) — ALL COMPLETED ✅
- [x] **cloud_db.py** — Added dynamic migrations for schema upgrades
- [x] **http_scraper.py** — Added OpenStreetMap Nominatim scraper fallback
- [x] **main.py** — Adjusted local run block to default to port 8000 for local frontend alignment
- [x] **start_services.bat** — Updated backend run command to execute the Flask app locally on port 8000
- [x] **Live Testing** — Verified local and live Vercel deployments run scraping pipelines without errors

---

## 💾 RESUME SYSTEM
Type "continue" in any new session to reload context.
All frontend and backend updates pushed, tested, and fully live!
