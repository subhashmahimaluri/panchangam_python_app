# 🚀 Quick Start Guide - Panchangam Calendar App

## All Methods to Run Both Frontend & Backend

### 1. Shell Scripts (macOS/Linux)

```bash
# Full-featured script with cleanup and error handling
./start-dev.sh

# Simple quick start
./quick-start.sh
```

### 2. Batch Script (Windows)

```batch
# Windows users
start-dev.bat
```

### 3. npm Scripts

```bash
# Install root dependencies first
npm install

# Start both servers with concurrently
npm run dev

# Other commands
npm run backend     # Backend only
npm run frontend    # Frontend only
npm run install:all # Install all dependencies
npm run build       # Build frontend
npm run clean       # Clean build files
```

### 4. Make Commands

```bash
# Show all available commands
make help

# Start both servers
make dev

# Individual servers
make backend
make frontend

# Setup
make install
```

### 5. Manual (Individual Terminals)

**Terminal 1 - Backend:**

```bash
cd backend
pip install -r requirements.txt
python run_server.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
pnpm install
pnpm dev
```

## 🌐 Access Points

Once running, access these URLs:

- **Frontend App**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Demo Page**: Open `demo.html` in browser

## 🛑 Stopping Servers

- **Scripts**: Press `Ctrl+C` in the terminal
- **Windows**: Close the opened command windows
- **Manual**: Press `Ctrl+C` in each terminal

## 📝 Notes

- Scripts automatically install dependencies
- Backend starts first, then frontend
- Both servers support hot reloading
- All scripts include error handling and cleanup
