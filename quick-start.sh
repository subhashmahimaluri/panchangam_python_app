#!/bin/bash

# Simple script to test both servers
echo "🚀 Starting Panchangam servers..."

# Kill any existing processes
pkill -f "next dev" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "run_server.py" 2>/dev/null || true

echo "🐍 Starting backend..."
cd backend && python run_server.py &

echo "⚛️ Starting frontend..."
cd ../frontend && pnpm dev &

echo "✅ Both servers starting..."
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"

# Keep script running
wait