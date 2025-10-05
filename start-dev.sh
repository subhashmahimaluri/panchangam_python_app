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
    
    # Kill backend and frontend processes
    if [ ! -z "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Kill any remaining processes
    pkill -f "next dev" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "run_server.py" 2>/dev/null || true
    
    echo "✅ Servers stopped."
}

# Set up trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

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

# Keep script running and wait for user interrupt
echo "⏳ Servers are running... Press Ctrl+C to stop"
while true; do
    # Check if both processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process died unexpectedly"
        cleanup
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend process died unexpectedly"
        cleanup
        exit 1
    fi
    
    sleep 2
done