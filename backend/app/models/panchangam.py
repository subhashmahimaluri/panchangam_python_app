"""
Pydantic models for Panchangam API request and response
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    """Location information"""
    city: str = Field(..., description="City name")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")

class PeriodTime(BaseModel):
    """Time period with name and start/end times"""
    name: str = Field(..., description="Name of the period")
    start: str = Field(..., description="Start time in ISO format")
    end: str = Field(..., description="End time in ISO format")

class SimpleTime(BaseModel):
    """Simple time period with start and end"""
    start: str = Field(..., description="Start time in HH:MM format")
    end: str = Field(..., description="End time in HH:MM format")

class InauspiciousPeriods(BaseModel):
    """Inauspicious time periods"""
    rahu: SimpleTime = Field(..., description="Rahu Kalam period")
    gulika: SimpleTime = Field(..., description="Gulika Kalam period")
    yamaganda: SimpleTime = Field(..., description="Yamaganda Kalam period")
    varjyam: List[SimpleTime] = Field(..., description="Varjyam periods (can be multiple)")

class AuspiciousPeriods(BaseModel):
    """Auspicious time periods"""
    abhijit_muhurat: SimpleTime = Field(..., description="Abhijit Muhurat period")
    brahma_muhurat: SimpleTime = Field(..., description="Brahma Muhurat period")
    pradosha_time: SimpleTime = Field(..., description="Pradosha time period")

class PanchangamRequest(BaseModel):
    """Request model for Panchangam calculation"""
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    city: str = Field(..., description="City name")

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-10-05",
                "latitude": 12.9719,
                "longitude": 77.593,
                "city": "Bengaluru"
            }
        }

class PanchangamResponse(BaseModel):
    """Response model for Panchangam data"""
    location: Location = Field(..., description="Location information")
    date: str = Field(..., description="Date in ISO format")
    sunrise: str = Field(..., description="Sunrise time in HH:MM AM/PM format")
    sunset: str = Field(..., description="Sunset time in HH:MM AM/PM format")
    moonrise: str = Field(..., description="Moonrise time in HH:MM AM/PM format")
    moonset: str = Field(..., description="Moonset time in HH:MM AM/PM format")
    tithi: PeriodTime = Field(..., description="Tithi information")
    nakshatra: PeriodTime = Field(..., description="Nakshatra information")
    karana: PeriodTime = Field(..., description="Karana information")
    yoga: PeriodTime = Field(..., description="Yoga information")
    inauspicious_periods: InauspiciousPeriods = Field(..., description="Inauspicious time periods")
    auspicious_periods: AuspiciousPeriods = Field(..., description="Auspicious time periods")

    class Config:
        schema_extra = {
            "example": {
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
                    "rahu": {"start": "16:32", "end": "18:02"},
                    "gulika": {"start": "14:03", "end": "15:33"},
                    "yamaganda": {"start": "09:00", "end": "10:30"},
                    "varjyam": [
                        {"start": "12:34", "end": "13:21"},
                        {"start": "17:12", "end": "18:04"}
                    ]
                },
                "auspicious_periods": {
                    "abhijit_muhurat": {"start": "11:59", "end": "12:40"},
                    "brahma_muhurat": {"start": "04:20", "end": "05:08"},
                    "pradosha_time": {"start": "16:30", "end": "18:00"}
                }
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    error: Optional[str] = Field(None, description="Error type")