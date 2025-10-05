#!/bin/bash

# Panchangam Calendar App - Development Startup Script
# This script starts both frontend (Next.js) and backend (FastAPI) servers

set -e  # Exit on any error

echo "🚀 Starting Panchangam Calendar App..."
echo "=================================="

# Function to kill background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    
    # Kill any remaining processes
    pkill -f "next dev" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "run_server.py" 2>/dev/null || true
    
    echo "✅ Servers stopped."
    exit 0
}

# Set up trap to cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

# Check if directories exist
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found!"
    exit 1
fi

# Start Backend Server
echo "🐍 Starting FastAPI Backend Server..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ Backend requirements.txt not found!"
    exit 1
fi

# Check if virtual environment should be used
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install backend dependencies if needed
pip install -r requirements.txt > /dev/null 2>&1 || {
    echo "⚠️  Warning: Could not install backend dependencies"
}

# Start backend in background
echo "🔧 Starting backend server on http://localhost:8000..."
python run_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Return to root directory
cd ..

# Start Frontend Server
echo "⚛️  Starting Next.js Frontend Server..."
cd frontend

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed. Please install pnpm first:"
    echo "   npm install -g pnpm"
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
pnpm install

# Start frontend in background
echo "🔧 Starting frontend server on http://localhost:3000..."
pnpm dev &
FRONTEND_PID=$!

# Return to root directory
cd ..

echo ""
echo "✅ Both servers are running!"
echo "=================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🧪 Demo:     Open demo.html in browser"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "=================================="

# Wait for background processes
wait