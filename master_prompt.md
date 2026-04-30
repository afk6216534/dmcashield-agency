# ZERO HUMAN AGENTIC COMPANY — MASTER BUILD PROMPT
## DMCA Negative Review Removal Autonomous Agency System

**Mission:** Build a fully autonomous, zero-human AI company that removes negative Google reviews for businesses (restaurants, dentists, salons, etc.) through legal DMCA processes.

**Team:** Antigravity (Claude Opus 4.6) | Claude Code | OpenCode (Minimax 2.5)

**Core Principle:** After receiving this prompt, the system builds, tests, fixes, and iterates WITHOUT user input. It runs 24/7 with persistent memory across restarts.

---

## System Architecture — 12 Departments

```
CEO Agent (Master Orchestrator)
├── Dept 1 — Lead Scraping
├── Dept 2 — Data Validation & Enrichment
├── Dept 3 — Marketing (5 sub-depts)
│   ├── 3A — Lead Intelligence
│   ├── 3B — Funnel Strategy
│   ├── 3C — Copywriting
│   ├── 3D — Email QA
│   └── 3E — Competitive Intelligence
├── Dept 4 — Email Sending & Automation
├── Dept 5 — Tracking & Analytics
├── Dept 6 — Sales & Reply Management
├── Dept 7 — Google Sheets & Reporting
├── Dept 8 — Email Account Management
├── Dept 9 — Task Management & Control Tower
├── Dept 10 — ML Feedback & System Learning
├── Dept 11 — JARVIS System (Command Center)
└── Dept 12 — Memory & Soul System
```

---

## Department Summaries

### Dept 1 — Scraping
- Scrape: Business name, owner, email, phone, address, Google rating, negative reviews, competitors
- Tools: Google Maps, Hunter.io, Apollo.io, Playwright
- Output: Verified lead JSON with score ≥6

### Dept 2 — Validation & Enrichment
- Validate emails, find competitors, analyze audience, structure data
- Output: Enriched lead profile

### Dept 3 — Marketing (5 Sub-Depts)
- **3A:** Psychological profiling, emotion mapping
- **3B:** Funnel design (Cold→Warm→Hot, 6-email sequence)
- **3C:** Personalized email writing (150-200 words, human tone)
- **3D:** Spam checking, duplicate detection, deliverability (<3.0 spam score)
- **3E:** Competitive intelligence, trend reporting

### Dept 4 — Email Sending
- Multi-account rotation (40/day max per account)
- 3-7 min gaps between sends
- Peak time sending by niche
- Blacklist monitoring & recovery

### Dept 5 — Tracking
- Open/click tracking, reply detection
- Per-lead engagement scores
- Weekly intelligence reports

### Dept 6 — Sales & Replies
- Classify replies (INTERESTED/OBJECTION/NOT NOW/HOT/SPAM)
- Human-sounding AI replies (never reveal AI)
- Hot lead escalation to Gmail Important + user notification

### Dept 7 — Google Sheets
- Dashboard: Email accounts, leads (Cold/Warm/Hot/Converted), task progress
- Real-time updates

### Dept 8 — Account Management
- UI for adding accounts, warmup scheduling (5→40/day over 4 weeks)
- Blacklist recovery

### Dept 9 — Task Management
- Task lifecycle tracking
- Daily limits enforcement
- Dashboard overview

### Dept 10 — ML Learning
- Vector store per agent (ChromaDB)
- Learn winning patterns, adjust funnels/copy
- Weekly system reports

### Dept 11 — JARVIS
- Natural language command center
- Daily summaries
- Proactive notifications

### Dept 12 — Memory & Soul
- SQLite + ChromaDB + GitHub auto-backup every 6h
- Resume on boot without user input

---

## Workflow

1. User enters: Business Type, City, State, Country → Launch Task
2. Dept 1 scrapes → Dept 2 enriches → Dept 3 creates funnel & emails
3. Dept 4 sends (multi-account) → Dept 5 tracks → Dept 6 handles replies
4. Dept 7 reports → Dept 10 learns → System optimizes
5. Hot leads → Gmail Important → User closes deal

---

## Tech Stack (All Free)

**Backend:** Python FastAPI, Celery+Redis, SQLite, ChromaDB, Playwright, LangChain, CrewAI, AutoGen
**Models:** OpenRouter free models (Mistral, Qwen, Llama 3.1, Mixtral)
**Frontend:** React+Vite, Tailwind, Recharts, Socket.IO
**Email:** Gmail SMTP/API, imaplib
**Tracking:** Flask pixel server, Bitly
**Sheets:** Google Sheets API, gspread
**Notifications:** Pushover API
**Hosting:** Local + Render.com free tier

---

## UI Pages

1. Dashboard — System status, stats, active tasks, activity feed, JARVIS chat
2. Launch Task — Business type, city, state, bulk input
3. Lead Database — Filterable table, full profiles
4. Email Accounts — Status, health, add accounts (no coding)
5. Analytics — Charts, top performers, funnel viz
6. Task Manager — Pause/resume/cancel
7. Hot Leads — Ready-to-convert conversations
8. Settings — JARVIS config, agent models, limits, API keys

---

## Startup Sequence

1. Load soul.json → restore identity
2. Connect databases → load agent brains
3. Resume active tasks
4. Check email replies → process through Dept 6
5. Continue scheduled sends
6. Launch FastAPI + React dashboard
7. JARVIS: "System operational. X hot leads, Y new replies."

---

## Permissions

All teams have full access to:
- Add departments/agents/features
- Install free tools/libraries/APIs
- Clone repos from AI Resource Manager
- Make architectural decisions
- Improve system beyond this spec

**Minimum Viable:** All 12 departments functional, web dashboard, multi-account email, tracking, human-like replies, Sheets reporting, task management, persistent memory, JARVIS interface.

**Quality Standard:** Function like a $50K/month agency on autopilot. Every detail matters.

---

## Build Instructions

**Backend structure:**
```
backend/
├── main.py
├── agents/{all departments}
├── database/{models.py, leads.db, soul.json}
├── utils/{email_tools.py, scraper_tools.py, sheets_tools.py}
└── requirements.txt
```

**Frontend structure:**
```
frontend/src/
├── pages/{8 pages}
├── components/{JARVIS, AgentStatus, LeadCard, FunnelChart}
└── App.jsx
```

**Required packages:** See Tech Stack above.

---

## Communication Protocol

JSON messages between agents:
```json
{"from": "Dept1", "to": "Dept2", "type": "handoff", 
 "priority": "normal", "payload": {...}, "timestamp": "..."}
```
Types: handoff, update, alert, request, report, instruction

---

*End of Master Prompt — Build. Test. Fix. Ship.*