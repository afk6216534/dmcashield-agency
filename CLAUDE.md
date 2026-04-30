# DMCAShield Agency - Architecture Documentation

## Overview
Autonomous AI agency for removing negative Google reviews via DMCA processes.
- Zero-human intervention capability
- 12 specialized departments
- Persistent memory with encryption
- Self-healing and auto-scaling

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │────│   FastAPI        │────│  Departments    │
│   (React)       │    │   Backend        │    │  (12 Agents)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
              ┌──────────────────┬───────────────────────┼───────────────────────┬───────────────────┐
              │                  │                       │                       │                   │
   ┌──────────▼──────────┐ ┌─────▼──────────┐     ┌──────▼──────────┐     ┌──────▼──────────┐ ┌────▼─────────┐
   │   Scraping         │ │   Validation   │     │   Marketing     │     │   Email Sending │ │   Sales      │
   └─────────────────────┘ └────────────────┘     └─────────────────┘     └─────────────────┘ └──────────────┘
              │                  │                       │                       │                   │
              └──────────────────┴───────────────────────┼───────────────────────┼───────────────────┘
                                                         │
                                               ┌─────────▼─────────┐
                                               │  JARVIS Interface │
                                               └───────────────────┘
```

## Department Structure

### 1. Scraping (Lead Generation)
- Google Maps, Hunter.io, Apollo.io
- Playwright automation
- Output: Verified leads (score ≥6)

### 2. Validation & Enrichment
- Email verification
- Competitor analysis
- Audience profiling

### 3. Marketing (5 Sub-Depts)
- **3A:** Psychological profiling
- **3B:** Funnel strategy (6-email sequence)
- **3C:** Copywriting (150-200 words)
- **3D:** Spam checking, deliverability
- **3E:** Competitive intelligence

### 4. Email Sending
- Multi-account rotation (40/day max)
- 3-7 min gaps
- Peak time optimization

### 5. Tracking & Analytics
- Open/click tracking
- Per-lead engagement scores
- Weekly reports

### 6. Sales & Replies
- Classification (INTERESTED/OBJECTION/NOT NOW/HOT/SPAM)
- Human-sounding AI replies
- Hot lead escalation

### 7. Google Sheets & Reporting
- Real-time dashboards
- Lead tracking

### 8. Account Management
- UI for adding accounts
- Warmup scheduling (5→40/day over 4 weeks)
- Blacklist recovery

### 9. Task Management
- Task lifecycle tracking
- Daily limits enforcement

### 10. ML Feedback & Learning
- Vector store (ChromaDB)
- Pattern learning
- Weekly system reports

### 11. JARVIS System
- Natural language commands
- Daily summaries
- Proactive notifications

### 12. Memory & Soul System
- SQLite + ChromaDB
- GitHub auto-backup (6h)
- Resume without user input

## API Endpoints

### Core Operations
- `POST /api/tasks` - Create lead generation task
- `GET /api/status` - System status and stats
- `GET /api/leads/hot` - Get hot leads
- `POST /api/email-accounts` - Add email account

### Email Operations
- `POST /api/queue/process` - Process email queue
- `POST /api/gmail/config` - Configure Gmail
- `POST /api/warmup/start` - Start warmup

### AI & Automation
- `POST /api/jarvis` - Natural language interface
- `POST /api/autonomous/start` - Start zero-human mode
- `POST /api/ai/config` - Configure AI settings

### Analytics
- `GET /api/monitoring/stats` - Monitoring stats
- `GET /api/abtests` - List A/B tests

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy (SQLite)
- Celery + Redis
- ChromaDB (Vector storage)
- Playwright

### Frontend
- React + Vite
- Tailwind CSS
- Recharts
- Socket.IO

### AI Models
- Claude Opus 4.6/4.7
- OpenRouter (Mistral, Qwen, Llama 3.1)
- LangChain, AutoGen, CrewAI

### Email Infrastructure
- Gmail SMTP/API
- Resend API
- imaplib

### Infrastructure
- Local deployment
- Render.com (free tier)
- Docker (optional)

## Data Flow

1. User submits business type/city/state
2. Scraping Dept collects leads
3. Validation enriches and scores
4. Marketing creates personalized funnel
5. Email Sending rotates accounts
6. Tracking monitors engagement
7. Sales handles replies
8. ML learns from patterns
9. JARVIS coordinates
10. Memory persists all state

## Security

- AES-256 encryption for credentials
- Encrypted conversation history
- Versioned backups
- Audit trails (FIPS-140-2 compliant)
- Role-based access control
- Tamper-proof logging

## Deployment

### Local Setup
```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Start backend
python backend/main.py

# Start frontend
npm run dev
```

### Docker
```bash
docker-compose up -d
```

### Auto-Scaling
- Kubernetes (optional)
- Resource-based worker scaling
- Queue-length monitoring

## Monitoring

- Real-time dashboard
- Email deliverability tracking
- Account health scores
- Automated alerts
- Performance metrics

## Troubleshooting

- Check `/health` endpoint
- Review audit logs
- Monitor account limits
- Verify email configurations
- Check queue processing

## Future Enhancements

- Multi-language support
- Additional review platforms
- Advanced NLP for reply generation
- Predictive analytics
- Mobile app