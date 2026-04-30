#!/bin/bash
# Auto Deploy Script for DMCAShield

echo "🏗️ Building and deploying to Netlify..."

# Build frontend
cd dmcashield/frontend
npm run build

# Deploy to Netlify (requires netlify-cli installed and linked)
echo "Deploying..."
npx netlify deploy --prod --dir=dist

echo "✅ Deployed!"