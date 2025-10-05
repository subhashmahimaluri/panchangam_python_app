# Panchangam Calendar App - Development Plan

## Project Overview

Full-stack Panchangam calendar application with Next.js 15 frontend and Python FastAPI backend.

### Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, React, pnpm
- **Backend**: Python 3.11+, FastAPI, pyswisseph
- **Features**: Daily Panchangam for Bengaluru and Coventry with accurate astronomical calculations

## Estimated Timeline: 6-8 hours for complete MVP

## Phase 1: Project Setup & Structure (30 mins)

- [COMPLETE] Create TodoList.md with detailed project breakdown
- [COMPLETE] Set up project folder structure for both frontend and backend
- [COMPLETE] Initialize Next.js 15 frontend with TypeScript and App Router using pnpm
- [COMPLETE] Set up Python FastAPI backend with project structure
- [COMPLETE] Create startup scripts for running both servers from root directory

## Phase 2: Frontend Development (2 hours)

- [PENDING] Create TypeScript interfaces for Panchangam data models
- [PENDING] Build React components for city dropdown and date picker
- [PENDING] Create main home page component with data display
- [PENDING] Create responsive UI for displaying Panchangam data
- [PENDING] Integrate frontend with backend API calls

## Phase 3: Backend Core Setup (1 hour)

- [PENDING] Install and configure pyswisseph for astronomical calculations
- [PENDING] Create Pydantic models for API request/response
- [PENDING] Create FastAPI endpoint /api/panchangam with proper error handling

## Phase 4: Astronomical Calculations (2.5 hours)

- [PENDING] Implement core astronomical calculation functions (sunrise, sunset, moonrise, moonset)
- [PENDING] Implement Hindu calendar calculations (Tithi, Nakshatra, Karana, Yoga)
- [PENDING] Implement inauspicious period calculations (Rahu Kalam, Gulika, Yamaganda, Varjyam)
- [PENDING] Implement auspicious period calculations (Abhijit, Brahma, Pradosha)

## Phase 5: Integration & Polish (1 hour)

- [PENDING] Add timezone handling and local time formatting
- [PENDING] Create unit tests for backend calculation functions
- [PENDING] Test complete application with both cities (Bengaluru & Coventry)

## Phase 6: Documentation (30 mins)

- [PENDING] Create documentation and setup instructions

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

## Next Steps

Starting with Phase 1: Project setup and folder structure creation.
