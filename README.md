# Panchangam Calendar API

A comprehensive Panchangam calendar application with accurate astronomical calculations using Swiss Ephemeris.

## Project Overview

This full-stack application provides accurate Hindu calendar (Panchangam) data including:

- Solar and lunar events (sunrise, sunset, moonrise, moonset)
- Hindu calendar elements (Tithi, Nakshatra, Karana, Yoga)
- Auspicious periods (Abhijit Muhurat, Brahma Muhurat, Pradosha Time)
- Inauspicious periods (Rahu Kalam, Gulika Kalam, Yamaganda, Varjyam)

## Architecture

### Backend (Python FastAPI)

- **Framework**: FastAPI with async support
- **Calculations**: pyswisseph (Swiss Ephemeris) for astronomical accuracy
- **API**: RESTful JSON API with comprehensive error handling
- **Timezone**: Proper timezone handling for different cities

### Frontend (Next.js 15 - In Development)

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **Demo**: HTML demo page available for testing

## Supported Cities

1. **Bengaluru, India**

   - Latitude: 12.9719°
   - Longitude: 77.593°
   - Timezone: Asia/Kolkata (IST)

2. **Coventry, UK**
   - Latitude: 52.40656°
   - Longitude: -1.51217°
   - Timezone: Europe/London (GMT/BST)

## Quick Start

### Option 1: Run Both Servers (Recommended)

From the root directory, choose one of these methods:

**Method A: Using Shell Script (macOS/Linux)**

```bash
./start-dev.sh
```

**Method B: Using Batch Script (Windows)**

```batch
start-dev.bat
```

**Method C: Using npm scripts**

```bash
npm install  # Install concurrently package
npm run dev  # Start both servers
```

**Method D: Using Makefile**

```bash
make install  # Install dependencies
make dev      # Start both servers
```

### Option 2: Run Servers Separately

### Prerequisites

- Python 3.11+
- pip package manager
- pnpm (for frontend development)

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
python run_server.py
```

The API will be available at `http://localhost:8000`

## Available Commands

Once the servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Demo Page**: Open `demo.html` in your browser

### Additional Commands

```bash
# Install all dependencies
npm run install:all

# Start individual servers
npm run backend   # Backend only
npm run frontend  # Frontend only

# Build for production
npm run build

# Clean build files
npm run clean

# Using Make commands
make help      # Show available commands
make install   # Install dependencies
make backend   # Start backend only
make frontend  # Start frontend only
```

## Demo

Open `demo.html` in your browser to test the API with a user-friendly interface.

## Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Setup (Next.js 15)

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies with pnpm:

```bash
pnpm install
```

3. Start the development server:

```bash
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## Status

**Backend**: Complete and functional with comprehensive API endpoints.
**Frontend**: Next.js 15 structure in place, using pnpm for package management.
**Demo**: HTML demo page available for immediate testing.
