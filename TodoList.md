# Panchangam Calendar App - Development Plan

## Project Overview

Full-stack Panchangam calendar application with Next.js 15 frontend and Python FastAPI backend.

### Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, React, pnpm
- **Backend**: Python 3.11+, FastAPI, pyswisseph
- **Features**: Daily Panchangam for Bengaluru and Coventry with accurate astronomical calculations

## Estimated Timeline: 6-8 hours for complete MVP

## Phase 1: Project Setup & Structure (30 mins) ✅ COMPLETE

- [COMPLETE] Create TodoList.md with detailed project breakdown
- [COMPLETE] Set up project folder structure for both frontend and backend
- [COMPLETE] Initialize Next.js 15 frontend with TypeScript and App Router using pnpm
- [COMPLETE] Set up Python FastAPI backend with project structure
- [COMPLETE] Create startup scripts for running both servers from root directory

## Phase 2: Frontend Development (2 hours) 🔄 IN PROGRESS

- [COMPLETE] Create TypeScript interfaces for Panchangam data models
- [COMPLETE] Build React components for city dropdown and date picker
- [COMPLETE] Create main home page component with data display
- [COMPLETE] Create responsive UI for displaying Panchangam data
- [ISSUE] ⚠️ Frontend-Backend connectivity issue (API health check failing)
- [PENDING] Fix CORS/network connectivity between frontend and backend

## Phase 3: Backend Core Setup (1 hour) ✅ COMPLETE

- [COMPLETE] Install and configure pyswisseph for astronomical calculations
- [COMPLETE] Create Pydantic models for API request/response
- [COMPLETE] Create FastAPI endpoint /api/panchangam with proper error handling

## Phase 4: Astronomical Calculations (2.5 hours) ✅ COMPLETE

- [COMPLETE] Implement core astronomical calculation functions (sunrise, sunset, moonrise, moonset)
- [COMPLETE] Implement Hindu calendar calculations (Tithi, Nakshatra, Karana, Yoga)
- [COMPLETE] Implement inauspicious period calculations (Rahu Kalam, Gulika, Yamaganda, Varjyam)
- [COMPLETE] Implement auspicious period calculations (Abhijit, Brahma, Pradosha)

## Phase 5: Integration & Polish (1 hour) 🔄 IN PROGRESS

- [COMPLETE] Add timezone handling and local time formatting
- [PENDING] Create unit tests for backend calculation functions
- [ISSUE] ⚠️ Frontend cannot connect to backend API (showing "Backend API is not available!")
- [PENDING] Test complete application with both cities (Bengaluru & Coventry)

## Phase 6: Documentation (30 mins) ✅ COMPLETE

- [COMPLETE] Create comprehensive README.md with setup instructions
- [COMPLETE] Create demo.html for testing backend API
- [COMPLETE] Create example_usage.py for programmatic API testing

## Project Structure Preview

```
panchangam_python_app/
├── frontend/                 # Next.js 15 App
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx         # Main home page
│   │   └── api/
│   ├── components/
│   │   ├── CitySelector.tsx
│   │   ├── DatePicker.tsx
│   │   ├── PanchangamDisplay.tsx
│   │   └── ui/
│   ├── types/
│   │   └── panchangam.ts    # TypeScript interfaces
│   ├── utils/
│   │   └── api.ts          # API client functions
│   ├── package.json
│   └── next.config.js
├── backend/                 # FastAPI App
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app entry
│   │   ├── models/
│   │   │   └── panchangam.py # Pydantic models
│   │   ├── routers/
│   │   │   └── panchangam.py # API endpoints
│   │   ├── services/
│   │   │   ├── astronomical.py # Core calculations
│   │   │   ├── hindu_calendar.py # Tithi, Nakshatra, etc.
│   │   │   └── muhurat.py  # Auspicious/Inauspicious periods
│   │   └── utils/
│   │       ├── timezone.py
│   │       └── constants.py
│   ├── tests/
│   │   └── test_calculations.py
│   ├── requirements.txt
│   └── README.md
├── README.md               # Main project documentation
└── TodoList.md            # This file
```

## Key Features to Implement

### Frontend Features

- City dropdown (Bengaluru/Coventry)
- Date picker (default: today)
- Real-time API calls on city/date change
- Responsive card/table layout for Panchangam data
- Separate sections for auspicious/inauspicious periods
- Local timezone display formatting

### Backend Features

- Swiss Ephemeris integration for accurate calculations
- RESTful API endpoint `/api/panchangam`
- Comprehensive Panchangam calculations:
  - Solar/Lunar events (sunrise, sunset, moonrise, moonset)
  - Hindu calendar elements (Tithi, Nakshatra, Karana, Yoga)
  - Muhurat calculations (Rahu Kalam, Gulika, Yamaganda, Varjyam)
  - Auspicious periods (Abhijit, Brahma, Pradosha)
- Timezone-aware time formatting
- Error handling and validation

## Sample API Request/Response

### Request

```json
POST /api/panchangam
{
  "date": "2025-10-05",
  "latitude": 12.9719,
  "longitude": 77.593,
  "city": "Bengaluru"
}
```

### Response

```json
{
  "location": {
    "city": "Bengaluru",
    "latitude": 12.9719,
    "longitude": 77.593
  },
  "date": "2025-10-05",
  "sunrise": "06:09 AM",
  "sunset": "06:32 PM",
  "moonrise": "05:43 AM",
  "moonset": "06:08 PM",
  "tithi": {
    "name": "Krishna Paksha Trayodashi",
    "start": "2025-10-04T17:09:00+05:30",
    "end": "2025-10-05T15:04:00+05:30"
  },
  "nakshatra": {
    "name": "Shatabhisha",
    "start": "2025-10-04T09:09:00+05:30",
    "end": "2025-10-05T08:01:00+05:30"
  },
  "karana": {
    "name": "Taitila",
    "start": "2025-10-05T04:11:00+05:30",
    "end": "2025-10-05T15:04:00+05:30"
  },
  "yoga": {
    "name": "Ganda",
    "start": "2025-10-04T19:25:00+05:30",
    "end": "2025-10-05T16:33:00+05:30"
  },
  "inauspicious_periods": {
    "rahu": { "start": "16:32", "end": "18:02" },
    "gulika": { "start": "14:03", "end": "15:33" },
    "yamaganda": { "start": "09:00", "end": "10:30" },
    "varjyam": [
      { "start": "12:34", "end": "13:21" },
      { "start": "17:12", "end": "18:04" }
    ]
  },
  "auspicious_periods": {
    "abhijit_muhurat": { "start": "11:59", "end": "12:40" },
    "brahma_muhurat": { "start": "04:20", "end": "05:08" },
    "pradosha_time": { "start": "16:30", "end": "18:00" }
  }
}
```

## Development Notes

- Use Swiss Ephemeris for maximum astronomical accuracy
- All times should be in local timezone for the selected city
- Modular code structure for easy maintenance and expansion
- Comprehensive error handling for edge cases
- Unit tests for critical calculation functions
- Responsive design for mobile and desktop use

## Current Status Summary

### ✅ COMPLETED:

- **Backend**: Fully functional with all Panchangam calculations
  - FastAPI server running on localhost:8000
  - Swiss Ephemeris integration working
  - All required endpoints implemented (/health, /api/panchangam)
  - Comprehensive astronomical calculations
  - CORS middleware configured
- **Frontend Structure**: Complete React/Next.js app
  - Next.js 15 with TypeScript
  - All components created (CitySelector, DatePicker, PanchangamDisplay)
  - TypeScript interfaces defined
  - Running on localhost:3001 (port 3000 was in use)

### 🔄 CURRENT ISSUES:

1. **Frontend-Backend Connectivity**: Fixed CORS configuration
   - Backend API is healthy and responds correctly to curl commands
   - CORS configuration updated to include localhost:3001
   - Frontend may need browser refresh to pick up changes
   - Testing connectivity now...

### 📋 IMMEDIATE NEXT STEPS:

1. Debug and fix the frontend-backend API connectivity issue
2. Verify CORS configuration between localhost:3001 and localhost:8000
3. Test complete data flow from frontend to backend
4. Add remaining unit tests
5. Final integration testing

### 🌐 SERVERS RUNNING:

- **Backend**: http://localhost:8000 ✅ Healthy
- **Frontend**: http://localhost:3001 ✅ Running (shows API connection error)
- **API Docs**: http://localhost:8000/docs ✅ Available
- **Demo Page**: Available at /demo.html ✅ Working
