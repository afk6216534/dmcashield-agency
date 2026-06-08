# TEAM_SHARE — v5.6 Status
# Last Updated: 2026-06-08 15:30 PKT

## 🔴 LIVE DEPLOYMENTS
- **Frontend**: https://dmcashield.netlify.app
- **Backend**: https://dmcashield-agency.vercel.app
- **Local Dev Server**: http://localhost:5177 (Frontend) | http://localhost:8000 (Backend)

## CURRENT VERSION: v5.6 (Deployed & Live)

### v5.4 — Persistent SQLite Scrapes & Lead Database
- **SQLite Task Persistence**: Wired `GET /api/tasks` and `POST /api/tasks` to query and write real YellowPages/Nominatim task pipelines in SQLite `scrape_tasks` table.
- **SQLite Lead Database**: Connected all CRM lead views and filters to query dynamically from `real_leads` and `email_log` database tables.
- **Automated Cloud Backup Sync**: Integrated `save_all_tasks_to_cloud` and `save_all_leads_to_cloud` in `agents/cloud_db.py` to backup and restore state automatically to `kvdb.io`. Added automatic merge sorting to prevent Vercel container recycles from losing/overwriting local tasks.

### v5.5 — Unified Cold Drip Sequence Scheduler
- **Human-Like Drip Engine**: Built `agents/drip_sender.py` which manages a 5-step follow-up email sequence (Day 0→3→7→14→28) with randomized intervals and warmup limits (3-15 emails/day max).
- **Scraper Queue Transition**: Replaced the immediate bulk email blast in the scraper pipeline with a queue-based funnel (funnel_step = 0, status = 'queued') that waits for the drip scheduler to process them safely.
- **Drip Endpoints**: Added `POST /api/drip/send` (sends 3-5 emails per call) and `GET /api/drip/status` endpoints in backend.
- **Sync and Frontend UI**: Synchronized workflows tabs, cost widgets, and settings error notifications across Netlify and Vercel.

### v5.6 — Scaled Outreach & Delay Optimization
- **Scaled Warmup limits**: Scaled daily limits dynamically per active configured account (15-60 daily emails per account) to increase overall capacity.
- **Increased Batch Size**: Configured drip sender batch size to `10-20` emails per trigger (instead of 3-5) to meet expected outreach volume.
- **Vercel Timeout Guard**: Added dynamic Vercel environment detection to compress sleep delays between sends (0.1-0.3s) during serverless execution, preventing background thread cutoffs while keeping the natural 5-15s delay locally.

---

## 📊 System Status

### Active Endpoints & Verification (Live on Vercel)
- `/api/db/info` → Verified production environment active
- `/api/gmail/status` → Verified clean connected/disconnected state
- `/api/real-leads` → Verified real SQLite CRUD operations
- `/api/drip/status` → Verified drip scheduler telemetry active
- `/api/scrape` → Scraper pipeline active

---

## 🔧 TASKS FOR TEAM

### Claude Code (Frontend)
- [x] **Settings.jsx** — Gmail config card wired to connection tests
- [x] **LaunchTask.jsx** — Scraping history table and real scrape trigger
- [x] **LeadDatabase.jsx** — CRUD toggles reading active SQLite DB
- [x] **KnowledgeBase.jsx** — Workflows tab rendering DMCA and Dev automations
- [x] **CEOView.jsx** — Cost & Budget Optimization widgets active
- [x] **Sidebar.jsx & App.jsx** — Routing definitions and 55-repo badges

### OpenCode (Backend)
- [x] **cloud_db.py** — Dynamic migrations and cloud merge sync resolution
- [x] **real_lead_scraper.py** — Pipeline scraper queues leads instead of blasting
- [x] **drip_sender.py** — 5-email drip campaign warmup scheduler
- [x] **main.py & start_services.bat** — Drip endpoints and local alignment port updates

---

## 💾 RESUME SYSTEM
Type "continue" in any new session to reload context.
All frontend and backend updates pushed, tested, and fully live!
