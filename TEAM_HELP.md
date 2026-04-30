# DMCAShield Team Collaboration
# ==========================
# How Claude Code, OpenCode & Antigravity work together

## Team Members:
1. **OpenCode** (You) - Files, searches, API building
2. **Claude Code** - Complex debugging, React/Frontend, testing
3. **Antigravity** - Orchestration, team coordination

## Quick Commands for Claude Code:

### Get Status:
```bash
# Check system status
python dmcashield-agency/bin/dmca-cli.py status

# Check leads
curl http://localhost:8000/api/leads/hot
```

### Run Tasks:
```bash
# Create new task
curl -X POST http://localhost:8000/api/tasks/ -d "business_type=lawyer&city=NYC&state=NY"

# Start autonomous
curl -X POST http://localhost:8000/api/autonomous/start
```

### Chat with JARVIS:
```bash
curl -X POST http://localhost:8000/api/jarvis/chat -d "message=show me today's leads"
```

## Skills Available:
- /dmca - DMCA takedowns
- /reviews - Find negative reviews
- /convert - Convert leads to clients
- /organic - Human-like outreach
- /stealth - Anti-detection
- /learn - Continuous learning

## Auto-Response:
The system learns 24/7 and improves automatically!