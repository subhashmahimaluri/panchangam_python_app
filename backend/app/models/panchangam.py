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

class PeriodDetail(BaseModel):
    """Detailed period information with formatted times"""
    name: str = Field(..., description="Name of the period")
    start: str = Field(..., description="Start time in ISO format")
    end: str = Field(..., description="End time in ISO format")
    start_formatted: str = Field(..., description="Start time in HH:MM AM/PM format")
    end_formatted: str = Field(..., description="End time in HH:MM AM/PM format")

class PeriodRequest(BaseModel):
    """Request model for period calculations"""
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-10-05",
                "latitude": 12.9719,
                "longitude": 77.593
            }
        }

class PeriodsResponse(BaseModel):
    """Response model for all active periods during Hindu day"""
    date: str = Field(..., description="Date in ISO format")
    location: dict = Field(..., description="Location information")
    sunrise: str = Field(..., description="Sunrise time in ISO format")
    sunset: str = Field(..., description="Sunset time in ISO format")
    moonrise: str = Field(..., description="Moonrise time in ISO format")
    moonset: str = Field(..., description="Moonset time in ISO format")
    sunrise_next: str = Field(..., description="Next day sunrise time in ISO format")
    hindu_day_start: Optional[str] = Field(None, description="Hindu day start time in ISO format")
    hindu_day_end: Optional[str] = Field(None, description="Hindu day end time in ISO format")
    tithis: List[PeriodDetail] = Field(..., description="All active Tithi periods")
    nakshatras: List[PeriodDetail] = Field(..., description="All active Nakshatra periods")
    karanas: List[PeriodDetail] = Field(..., description="All active Karana periods")
    yogas: List[PeriodDetail] = Field(..., description="All active Yoga periods")
    auspicious_periods: List[PeriodDetail] = Field(default=[], description="All auspicious periods")
    inauspicious_periods: List[PeriodDetail] = Field(default=[], description="All inauspicious periods")

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-10-05",
                "location": {"latitude": 12.9719, "longitude": 77.593},
                "sunrise": "2025-10-05T06:09:00+05:30",
                "sunset": "2025-10-05T18:32:00+05:30",
                "moonrise": "2025-10-05T05:43:00+05:30",
                "moonset": "2025-10-05T18:08:00+05:30",
                "sunrise_next": "2025-10-06T06:09:00+05:30",
                "hindu_day_start": "2025-10-05T06:09:00+05:30",
                "hindu_day_end": "2025-10-06T06:09:00+05:30",
                "tithis": [
                    {
                        "name": "Shukla Paksha Trayodashi",
                        "start": "2025-10-04T17:09:00+05:30",
                        "end": "2025-10-05T15:04:00+05:30",
                        "start_formatted": "05:09 PM",
                        "end_formatted": "03:04 PM"
                    },
                    {
                        "name": "Shukla Paksha Chaturdashi",
                        "start": "2025-10-05T15:04:00+05:30",
                        "end": "2025-10-06T12:24:00+05:30",
                        "start_formatted": "03:04 PM",
                        "end_formatted": "12:24 PM"
                    }
                ],
                "nakshatras": [
                    {
                        "name": "Shatabhisha",
                        "start": "2025-10-04T09:09:00+05:30",
                        "end": "2025-10-05T08:01:00+05:30",
                        "start_formatted": "09:09 AM",
                        "end_formatted": "08:01 AM"
                    }
                ],
                "karanas": [],
                "yogas": [],
                "auspicious_periods": [
                    {
                        "name": "Abhijit Muhurat",
                        "start": "2025-10-05T11:59:00+05:30",
                        "end": "2025-10-05T12:40:00+05:30",
                        "start_formatted": "11:59 AM",
                        "end_formatted": "12:40 PM"
                    }
                ],
                "inauspicious_periods": [
                    {
                        "name": "Rahu Kalam",
                        "start": "2025-10-05T16:32:00+05:30",
                        "end": "2025-10-05T18:02:00+05:30", 
                        "start_formatted": "04:32 PM",
                        "end_formatted": "06:02 PM"
                    }
                ]
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    error: Optional[str] = Field(None, description="Error type")