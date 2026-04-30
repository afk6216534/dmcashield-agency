# DMCAShield Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Clone & Setup
```bash
cd "F:/Anti gravity projects/Dmca company"
# Backend setup
cd dmcashield-agency/backend
pip install -r requirements.txt

# Frontend setup  
cd ../frontend
npm install
```

### Step 2: Configure API Keys
```bash
cp .env.example .env
# Edit .env and add:
# GOOGLE_PLACES_API_KEY=your_key
# OPENROUTER_API_KEY=your_key
# HUNTER_IO_API_KEY=your_key (optional)
```

### Step 3: Start Redis
```bash
redis-server --daemonize yes
```

### Step 4: Launch System
```bash
# Terminal 1: Start Celery Worker
cd backend
celery -A main.celery_app worker --loglevel=info

# Terminal 2: Start FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Start Frontend
cd ../frontend
npm start

# Terminal 4: Start DeepSleep Monitor
python -m deepsleep --auto-heal
```

### Step 5: Launch Your First Task
1. Open http://localhost:3000
2. Click "Launch Task"
3. Enter:
   - Business Type: restaurant
   - City: Austin
   - State: TX
4. Click "Launch Campaign"

## 📊 What Happens Next

```
✅ System scrapes business data (30 seconds)
✅ Validates emails and scores leads (1 minute)
✅ Builds personalized email funnel (2 minutes)
✅ Starts sending emails (3 minutes)
✅ Tracks opens/replies in real-time
✅ Hot leads appear in Gmail "Important" folder
```

## 🔥 Department Status Check
```bash
curl http://localhost:8000/api/status
```

Expected response:
```json
{
  "system": {"status": "operational"},
  "departments_status": {
    "scraping": "online",
    "marketing": "online",
    "email_sending": "online",
    "tracking": "online",
    "sales": "online",
    "jarvis": "online"
  }
}
```

## 📈 Monitor Progress
- **Dashboard:** http://localhost:3000 - Real-time stats
- **API Docs:** http://localhost:8000/docs - Swagger UI
- **Hot Leads:** http://localhost:3000/hot-leads

## 🆘 Troubleshooting

### Redis not running?
```bash
redis-cli ping  # Should return PONG
```

### Backend not starting?
```bash
cd backend
python -c "from main import app; print('OK')"
```

### Frontend not loading?
```bash
cd frontend
npm run build  # Check for build errors
```

## 🎯 Success Metrics
- 100+ leads processed/hour
- 98.5%+ email deliverability
- 35-45% open rates
- 12-18% reply rates
- 24/7 autonomous operation

*Zero Human Company — You sleep, the system works*
