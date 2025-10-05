@echo off
REM Panchangam Calendar App - Windows Development Startup Script
REM This script starts both frontend (Next.js) and backend (FastAPI) servers

echo.
echo 🚀 Starting Panchangam Calendar App...
echo ==================================

REM Check if directories exist
if not exist "frontend" (
    echo ❌ Frontend directory not found!
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Backend directory not found!
    pause
    exit /b 1
)

REM Start Backend Server
echo 🐍 Starting FastAPI Backend Server...
cd backend

if not exist "requirements.txt" (
    echo ❌ Backend requirements.txt not found!
    pause
    exit /b 1
)

REM Install backend dependencies
echo 📦 Installing backend dependencies...
pip install -r requirements.txt >nul 2>&1

REM Start backend in new window
echo 🔧 Starting backend server on http://localhost:8000...
start "FastAPI Backend" cmd /k "python run_server.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

cd ..

REM Start Frontend Server
echo ⚛️ Starting Next.js Frontend Server...
cd frontend

REM Check if pnpm is installed
pnpm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pnpm is not installed. Please install pnpm first:
    echo    npm install -g pnpm
    pause
    exit /b 1
)

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
pnpm install

REM Start frontend in new window
echo 🔧 Starting frontend server on http://localhost:3000...
start "Next.js Frontend" cmd /k "pnpm dev"

cd ..

echo.
echo ✅ Both servers are starting!
echo ==================================
echo 🌐 Frontend: http://localhost:3000
echo 🔌 Backend:  http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo 🧪 Demo:     Open demo.html in browser
echo.
echo Check the opened terminal windows for server status
echo Close the terminal windows to stop the servers
echo ==================================
pause