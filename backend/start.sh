#!/bin/bash
# Startup script for HostingGuru
echo "Starting DMCAShield Backend..."
cd "$(dirname "$0")"
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Running database migrations..."
python -c "from database.models import init_db; init_db()"
echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
