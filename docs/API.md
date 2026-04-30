# DMCAShield Agency - Documentation

## Quick Start

### Installation

```bash
# Clone and navigate
cd dmcashield-agency

# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### First Run

1. Add email account:
```bash
curl -X POST http://localhost:8000/api/email-accounts \
  -H "Content-Type: application/json" \
  -d '{"email_address": "your@gmail.com", "app_password": "xxx"}'
```

2. Create task:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"business_type": "restaurant", "city": "Austin", "state": "TX"}'
```

3. Check dashboard:
```bash
curl http://localhost:8000/api/dashboard
```

## API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard` | GET | Main dashboard |
| `/api/tasks` | POST | Create task |
| `/api/tasks` | GET | List tasks |
| `/api/leads` | GET | List leads |
| `/api/hot-leads` | GET | Hot leads |
| `/api/jarvis` | POST | Natural language |
| `/api/email-accounts` | POST | Add email |
| `/api/analytics` | GET | Stats |

### Integrations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/gmail/config` | POST | Configure Gmail |
| `/api/sheets/config` | POST | Configure Sheets |
| `/api/slack/config` | POST | Configure Slack |
| `/api/sms/config` | POST | Configure Twilio |
| `/api/webhooks` | POST | Add webhook |

### AI & Automation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ai/config` | POST | Configure AI |
| `/api/ai/generate` | POST | Generate email |
| `/api/automations` | GET | List automations |
| `/api/abtests` | GET | A/B tests |

## Architecture

```
DMCAShield Agency
├── CEO Agent (Orchestrator)
├── ScrapeHead (Lead scraping)
├── EnrichHead (Validation)
├── MarketingHead (Content)
├── SendHead (Email sending)
├── AnalyticsHead (Tracking)
├── SalesHead (Conversions)
├── SheetsHead (Export)
├── AccountHead (Management)
├── TaskHead (Tasks)
├── MLHead (Learning)
├── JARVIS (Interface)
└── Memory (System)
```

## Pipeline

```
Task → Scrape → Validate → Enrich → Funnel → Send → Track → Convert
         ↓          ↓         ↓        ↓        ↓
       Google    Email    Score   Queue   Opens
       Maps      Hunter   Lead    Email  Replies
```

## Troubleshooting

### Emails not sending
1. Check credentials
2. Check warmup status
3. Check daily limit

### No leads scraped
1. Check business type
2. Check city/state
3. Try different sources

### No hot leads
1. Wait for replies
2. Check spam folder
3. Improve email content

## Environment Variables

```bash
OPENAI_API_KEY=sk-...
DMCASHIELD_API=http://localhost:8000
```

## License

MIT License - 2026 DMCAShield Agency