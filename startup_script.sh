#!/bin/bash

# Start Redis server in background
redis-server --daemonize yes

# Wait for Redis to start
sleep 2

# Navigate to backend directory
cd backend

# Start Celery worker in background
celery -A main.celery_app worker --loglevel=info &

# Wait for Celery to initialize
sleep 5

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Wait for API to be ready
sleep 10

# Navigate to frontend directory
cd ../frontend

# Start frontend dev server
npm run dev &

# Wait for frontend to initialize
sleep 5

# Start DeepSleep monitoring in background (auto-healing)
python -m deepsleep --auto-heal --rotate-logs &

# Create a sample task to test the system
sleep 15
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"business_type":"restaurant","city":"Austin","state":"TX","country":"USA"}'

# Check system status
curl -s http://localhost:8000/api/status | jq .

echo "System startup and test completed. All services are running."