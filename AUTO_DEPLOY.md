# DMCAShield Auto-Deploy Setup - May 1, 2026

## Status
- **Backend**: RUNNING on HostingGuru (dmcashield-agency-8666.apps.hostingguru.io)
- **Frontend**: Ready to deploy to Vercel/Netlify

## Files Modified
- vite.config.js - Set deployed API URL
- .env.production - Updated API URL
- src/config/api.js - New centralized config
- src/App.jsx - Fixed WebSocket URL

## Backend (Working)
- Deployed: https://dmcashield-agency-8666.apps.hostingguru.io
- Status: RUNNING (may need 2-3 min cold start)

## Frontend Deploy Setup
```bash
cd dmcashield/frontend
npm run build  # Build for production
# Deploy dist/ to Vercel or Netlify
```

## GitHub Auto-Deploy
When you push to GitHub:
1. Backend → HostingGuru (auto-deploys on push)
2. Frontend → Need to deploy to Vercel/Netlify manually or set up GitHub Actions

## API Connection
Frontend is configured to use HostingGuru backend in production mode.