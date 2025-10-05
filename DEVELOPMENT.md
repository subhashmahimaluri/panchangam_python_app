# Development Guide - Panchangam Calendar App

## Running Both Servers

### Quick Start Options

**Option 1: Shell Script (macOS/Linux)**

```bash
./start-dev.sh     # Full featured script with error handling
./quick-start.sh   # Simple version
```

**Option 2: Batch Script (Windows)**

```batch
start-dev.bat
```

**Option 3: npm Scripts**

```bash
npm install        # Install concurrently
npm run dev        # Start both servers
```

**Option 4: Make Commands**

```bash
make dev           # Start both servers
make help          # Show all commands
```

## Package Management

This project uses **pnpm** for frontend package management instead of npm for improved performance and disk space efficiency.

## Quick Commands

### Frontend Development (Next.js 15)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run linting
pnpm lint

# Type checking
pnpm type-check

# Clean build cache
pnpm clean
```

### Backend Development (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start development server
python run_server.py

# Run tests
python -m pytest tests/ -v
```

## Development URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Demo Page**: Open `demo.html` in browser

## Project Structure

```
panchangam_python_app/
├── frontend/           # Next.js 15 + pnpm
│   ├── .pnpmrc        # pnpm configuration
│   ├── pnpm-lock.yaml # pnpm lockfile
│   └── ...
├── backend/           # FastAPI + pip
└── demo.html          # Standalone demo
```

## Notes

- The frontend uses pnpm for faster installs and better dependency management
- Backend uses standard pip for Python package management
- Both servers can run simultaneously for full-stack development
- The demo.html file provides a quick way to test the API without running the frontend
