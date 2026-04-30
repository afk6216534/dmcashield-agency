#!/bin/bash
set -e

echo "🚀 DMCAShield Autonomous System Starting..."
echo ""

# Step 1: Check and start Redis
echo "🔴 Starting Redis..."
redis-server --daemonize yes 2>/dev/null || echo "Redis already running"
sleep 2

# Step 2: Start Celery Worker
echo "🟡 Starting Celery Worker..."
cd backend
celery -A main.celery_app worker --loglevel=info &
CELERY_PID=$!
sleep 3

# Step 3: Start FastAPI
echo "🟢 Starting FastAPI Server..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
API_PID=$!
sleep 5

# Step 4: Start DeepSleep Monitor
echo "⚫ Starting DeepSleep Auto-Healing..."
cd ..
python -c "import sys; sys.path.append('.'); from deepsleep.deep_sleep_monitor import DeepSleepMonitor; import threading; m = DeepSleepMonitor(120); t = threading.Thread(target=m.monitor_loop, daemon=True); t.start()" &
DEEPSLEEP_PID=$!
sleep 2

# Step 5: Start Frontend
echo "🟣 Starting Frontend Dashboard..."
cd frontend
npm start &
FRONTEND_PID=$!
sleep 5

echo ""
echo "✅ DMCAShield System Started Successfully!"
echo ""
echo "🔗 Dashboard: http://localhost:3000"
echo "🔗 API Docs: http://localhost:8000/docs"
echo "🔗 Redis Monitor: redis-cli"
echo ""
echo "📊 System Status:"
curl -s http://localhost:8000/api/status | python3 -m json.tool 2>/dev/null || echo "  API initializing..."
echo ""

# Trap to cleanup on exit
trap 'echo "🛑 Stopping system..."; kill $CELERY_PID $API_PID $DEEPSLEEP_PID $FRONTEND_PID 2>/dev/null; exit' INT TERM

# Keep running
wait
