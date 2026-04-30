# DMCAShield - Team Collaboration Guide

## FOR ALL AI SYSTEMS WORKING TOGETHER

### This System Has:
- **Frontend**: http://localhost:5177 (14 pages - dmcashield/frontend)
- **Backend**: http://localhost:8000 (main_simple.py working)

### Quick Start:
```bash
# Terminal 1 - Frontend
cd dmcashield/frontend && npx vite --port 5175 --host

# Terminal 2 - Backend  
cd dmcashield-agency/backend && python -m uvicorn main_simple:app --port 8000
```

---

## RULES - FOLLOW THIS ORDER:

### 1. Every Session Start:
```
1. Read: .claude/conversation_history/metadata.json
2. Read: dmcashield-agency/TEAMS_COORDINATION.md  
3. Read: dmcashield-agency/TEAM_CHAT.md
4. Ask user what they want
```

### 2. What NOT to Do:
- ❌ Don't recreate existing pages
- ❌ Don't overwrite working code
- ❌ Don't ignore history files
- ❌ Don't duplicate features

### 3. What TO Do:
- ✅ Add NEW features only
- ✅ Check what exists first
- ✅ Save progress immediately
- ✅ Update TEAM_CHAT.md when done

---

## Pages That Exist (14 Total):
1. Dashboard - Main overview
2. LaunchTask - Start campaigns
3. LeadDatabase - Browse leads
4. EmailAccounts - Gmail/Resend/SendGrid
5. Analytics - Lead scoring, funnel
6. TaskManager - Track campaigns  
7. HotLeads - Priority leads
8. Settings - System config
9. CampaignManager - Templates, A/B testing
10. EmailWarmup - 28-day warmup
11. AIResponseHandler - Auto-reply
12. CampaignScheduler - Schedule campaigns
13. Integrations - Slack/Telegram
14. SelfLearning - AI patterns

---

## New Files Added This Session:
- dmcashield/frontend/src/pages/Integrations.jsx
- dmcashield/frontend/src/pages/SelfLearning.jsx
- dmcashield-agency/skills/predictive_analytics.json
- dmcashield-agency/skills/sentiment_analyzer.json
- dmcashield-agency/skills/autonomous_decider.json
- dmcashield-agency/skills/continuous_learner.json
- dmcashield-agency/skills/human_collaborator.json
- dmcashield-agency/backend/main_simple.py

---

## Team Communication:
After completing any work, update:
1. `.claude/conversation_history/metadata.json`
2. `dmcashield-agency/TEAM_CHAT.md`

**Follow these rules to avoid rework and loops!**

*Last updated: April 30, 2026*