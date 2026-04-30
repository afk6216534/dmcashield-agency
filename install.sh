#!/bin/bash
# DMCAShield Agency - Quick Install Script
# ===================================

set -e

echo "============================================"
echo "DMCAShield Agency - Installer"
echo "============================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required. Install from python.org"
    exit 1
fi

echo "✓ Python found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js required. Install from nodejs.org"
    exit 1
fi

echo "✓ Node.js found"

# Create directories
mkdir -p backend/data
mkdir -p backend/logs
mkdir -p frontend/dist

echo "✓ Directories created"

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -q fastapi uvicorn sqlalchemy pydantic python-dotenv chromadb httpx beautifulsoup4

echo "✓ Backend dependencies installed"

# Install frontend dependencies  
echo "Installing frontend dependencies..."
cd ../frontend
npm install -q

echo "✓ Frontend dependencies installed"

# Copy environment example
if [ ! -f .env ]; then
    cp ../backend/.env.example .env 2>/dev/null || echo "DMCASHIELD_API=http://localhost:8000" > .env
fi

echo "✓ Environment configured"

# Create startup script
cat > ../start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Start backend
echo "Starting DMCAShield Backend..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo "Starting DMCAShield Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "============================================"
echo "DMCAShield Agency is running!"
echo "============================================"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"

# Handle cleanup
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
EOF

chmod +x ../start.sh

echo ""
echo "============================================"
echo "✅ Installation Complete!"
echo "============================================"
echo ""
echo "To start DMCAShield:"
echo "  ./start.sh"
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend:   http://localhost:5173"
echo "Docs:      http://localhost:8000/docs"
echo ""
echo "Quick start:"
echo '  curl -X POST http://localhost:8000/api/email-accounts \'
echo '    -H "Content-Type: application/json" \'
echo '    -d "{\"email_address\": \"you@gmail.com\", \"app_password\": \"xxx\"}"'
echo ""
echo '  curl -X POST http://localhost:8000/api/tasks \'
echo '    -H "Content-Type: application/json" \'
echo '    -d "{\"business_type\": \"restaurant\", \"city\": \"Austin\", \"state\": \"TX\"}"'
echo ""