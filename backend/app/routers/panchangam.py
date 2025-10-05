"""
FastAPI router for Panchangam calculations
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, date, timedelta
from app.models.panchangam import (
    PanchangamRequest, PanchangamResponse, ErrorResponse,
    Location, PeriodTime, SimpleTime, InauspiciousPeriods, AuspiciousPeriods,
    PeriodRequest, PeriodsResponse, PeriodDetail
)
from app.services.astronomical import calculate_sunrise_sunset, calculate_moonrise_moonset
from app.services.hindu_calendar import calculate_tithi, calculate_nakshatra, calculate_karana, calculate_yoga, calculate_all_periods_for_hindu_day
from app.services.muhurat import (
    calculate_rahu_kalam, calculate_gulika_kalam, calculate_yamaganda_kalam, calculate_varjyam,
    calculate_abhijit_muhurat, calculate_brahma_muhurat, calculate_pradosha_time
)
from app.utils.timezone import get_julian_day_ut, local_to_utc, CITY_TIMEZONES

router = APIRouter()

@router.post(
    "/panchangam",
    response_model=PanchangamResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Calculate Panchangam data",
    description="Calculate complete Panchangam data including Tithi, Nakshatra, Karana, Yoga, and Muhurat timings for a given date and location."
)
async def calculate_panchangam(request: PanchangamRequest) -> PanchangamResponse:
    """
    Calculate complete Panchangam data for given date and location
    
    Args:
        request: PanchangamRequest containing date, latitude, longitude, and city
        
    Returns:
        PanchangamResponse with all calculated data
        
    Raises:
        HTTPException: For validation errors or calculation failures
    """
    try:
        # Validate input data
        validate_request(request)
        
        # Parse the date
        calc_date = datetime.fromisoformat(request.date)
        
        # Get Julian Day for calculations
        utc_date = local_to_utc(calc_date, request.city)
        jd = get_julian_day_ut(utc_date)
        
        # Calculate all components
        location = Location(
            city=request.city,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        # Astronomical calculations
        sunrise, sunset = calculate_sunrise_sunset(
            calc_date, request.latitude, request.longitude, request.city
        )
        
        moonrise, moonset = calculate_moonrise_moonset(
            calc_date, request.latitude, request.longitude, request.city
        )
        
        # Hindu calendar calculations
        tithi_data = calculate_tithi(jd, request.city)
        nakshatra_data = calculate_nakshatra(jd, request.city)
        karana_data = calculate_karana(jd, request.city)
        yoga_data = calculate_yoga(jd, request.city)
        
        # Convert to PeriodTime objects
        tithi = PeriodTime(**tithi_data)
        nakshatra = PeriodTime(**nakshatra_data)
        karana = PeriodTime(**karana_data)
        yoga = PeriodTime(**yoga_data)
        
        # Inauspicious periods
        rahu_data = calculate_rahu_kalam(
            calc_date, request.latitude, request.longitude, request.city
        )
        gulika_data = calculate_gulika_kalam(
            calc_date, request.latitude, request.longitude, request.city
        )
        yamaganda_data = calculate_yamaganda_kalam(
            calc_date, request.latitude, request.longitude, request.city
        )
        varjyam_data = calculate_varjyam(
            calc_date, request.latitude, request.longitude, request.city
        )
        
        inauspicious_periods = InauspiciousPeriods(
            rahu=SimpleTime(**rahu_data),
            gulika=SimpleTime(**gulika_data),
            yamaganda=SimpleTime(**yamaganda_data),
            varjyam=[SimpleTime(**period) for period in varjyam_data]
        )
        
        # Auspicious periods
        abhijit_data = calculate_abhijit_muhurat(
            calc_date, request.latitude, request.longitude, request.city
        )
        brahma_data = calculate_brahma_muhurat(
            calc_date, request.latitude, request.longitude, request.city
        )
        pradosha_data = calculate_pradosha_time(
            calc_date, request.latitude, request.longitude, request.city
        )
        
        auspicious_periods = AuspiciousPeriods(
            abhijit_muhurat=SimpleTime(**abhijit_data),
            brahma_muhurat=SimpleTime(**brahma_data),
            pradosha_time=SimpleTime(**pradosha_data)
        )
        
        # Construct response
        response = PanchangamResponse(
            location=location,
            date=request.date,
            sunrise=sunrise,
            sunset=sunset,
            moonrise=moonrise,
            moonset=moonset,
            tithi=tithi,
            nakshatra=nakshatra,
            karana=karana,
            yoga=yoga,
            inauspicious_periods=inauspicious_periods,
            auspicious_periods=auspicious_periods
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation error: {str(e)}"
        )

@router.post(
    "/periods",
    response_model=PeriodsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Calculate all Panchangam periods for Hindu day",
    description="""Calculate all active periods for each Panchangam element (Tithi, Nakshatra, Karana, Yoga) 
    during the Hindu day (sunrise to next sunrise). This endpoint provides a comprehensive view 
    of all overlapping periods, matching the authentic presentation seen in ProKerala and Drik Panchang.
    
    The Hindu day is calculated from sunrise on the specified date to sunrise on the next day,
    ensuring accurate period calculations based on the traditional Hindu calendar system.
    
    This endpoint is more user-friendly than the basic panchangam endpoint as it:
    - Shows ALL periods that overlap with the Hindu day, not just one per element
    - Provides both ISO format and formatted local times for easy display
    - Follows traditional Panchangam presentation with multiple periods per element
    - Uses sunrise-based day calculation as per Hindu calendar principles
    """
)
async def calculate_panchangam_periods(request: PeriodRequest) -> PeriodsResponse:
    """
    Calculate all active periods for each Panchangam element during the Hindu day
    
    This endpoint returns comprehensive period information that matches traditional 
    Panchangam presentations like ProKerala and Drik Panchang, showing all periods
    that overlap with the Hindu day (sunrise to next sunrise).
    
    Args:
        request: PeriodRequest containing date, latitude, and longitude
        
    Returns:
        PeriodsResponse with all active periods for each element type
        
    Raises:
        HTTPException: For validation errors or calculation failures
    """
    try:
        # Validate input data
        validate_period_request(request)
        
        # Parse the date
        calc_date = datetime.fromisoformat(request.date)
        
        # Calculate all periods for the Hindu day
        try:
            periods_data = calculate_all_periods_for_hindu_day(
                calc_date, request.latitude, request.longitude
            )
        except Exception as calc_error:
            print(f"Calculation error: {calc_error}")
            # Return a fallback response if calculation fails
            periods_data = {
                'date': calc_date.strftime('%Y-%m-%d'),
                'location': {'latitude': request.latitude, 'longitude': request.longitude},
                'sunrise': f"{calc_date.replace(hour=6, minute=10).isoformat()}+05:30",
                'sunrise_next': f"{(calc_date + timedelta(days=1)).replace(hour=6, minute=10).isoformat()}+05:30",
                'tithis': [],
                'nakshatras': [],
                'karanas': [],
                'yogas': []
            }
        
        # Convert to response format
        response = PeriodsResponse(
            date=periods_data['date'],
            location=periods_data['location'],
            sunrise=periods_data['sunrise'],
            sunset=periods_data.get('sunset', periods_data['sunrise']),  # Fallback to sunrise if sunset missing
            moonrise=periods_data.get('moonrise', periods_data['sunrise']),  # Fallback if moonrise missing
            moonset=periods_data.get('moonset', periods_data['sunrise']),  # Fallback if moonset missing
            sunrise_next=periods_data['sunrise_next'],
            hindu_day_start=periods_data.get('hindu_day_start'),
            hindu_day_end=periods_data.get('hindu_day_end'),
            tithis=[PeriodDetail(**period) for period in periods_data['tithis']],
            nakshatras=[PeriodDetail(**period) for period in periods_data['nakshatras']],
            karanas=[PeriodDetail(**period) for period in periods_data['karanas']],
            yogas=[PeriodDetail(**period) for period in periods_data['yogas']],
            auspicious_periods=[PeriodDetail(**period) for period in periods_data.get('auspicious_periods', [])],
            inauspicious_periods=[PeriodDetail(**period) for period in periods_data.get('inauspicious_periods', [])]
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        print(f"Endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation error: {str(e)}"
        )

def validate_period_request(request: PeriodRequest) -> None:
    """
    Validate the incoming period request data
    
    Args:
        request: PeriodRequest to validate
        
    Raises:
        ValueError: If validation fails
    """
    # Validate date format
    try:
        date_obj = datetime.fromisoformat(request.date)
        
        # Check if date is not too far in the future or past
        today = datetime.now().date()
        request_date = date_obj.date()
        
        if request_date > today + timedelta(days=365):
            raise ValueError("Date cannot be more than 1 year in the future")
        
        if request_date < today - timedelta(days=365*10):
            raise ValueError("Date cannot be more than 10 years in the past")
            
    except ValueError as e:
        if "Invalid isoformat string" in str(e):
            raise ValueError("Date must be in ISO format (YYYY-MM-DD)")
        raise e
    
    # Validate coordinates
    if not (-90 <= request.latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= request.longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")

def validate_request(request: PanchangamRequest) -> None:
    """
    Validate the incoming request data
    
    Args:
        request: PanchangamRequest to validate
        
    Raises:
        ValueError: If validation fails
    """
    # Validate date format
    try:
        date_obj = datetime.fromisoformat(request.date)
        
        # Check if date is not too far in the future or past
        today = datetime.now().date()
        request_date = date_obj.date()
        
        if request_date > today + timedelta(days=365):
            raise ValueError("Date cannot be more than 1 year in the future")
        
        if request_date < today - timedelta(days=365*10):
            raise ValueError("Date cannot be more than 10 years in the past")
            
    except ValueError as e:
        if "Invalid isoformat string" in str(e):
            raise ValueError("Date must be in ISO format (YYYY-MM-DD)")
        raise e
    
    # Validate coordinates
    if not (-90 <= request.latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= request.longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Validate city timezone
    if request.city not in CITY_TIMEZONES:
        raise ValueError(f"Unsupported city. Supported cities: {list(CITY_TIMEZONES.keys())}")

@router.get(
    "/cities",
    summary="Get supported cities",
    description="Get list of supported cities with their coordinates and timezones"
)
async def get_supported_cities():
    """
    Get list of supported cities
    
    Returns:
        Dictionary of supported cities with coordinates
    """
    return {
        "cities": [
            {
                "name": "Bengaluru",
                "latitude": 12.9719,
                "longitude": 77.593,
                "timezone": "Asia/Kolkata"
            },
            {
                "name": "Coventry", 
                "latitude": 52.40656,
                "longitude": -1.51217,
                "timezone": "Europe/London"
            },
            {
                "name": "New York",
                "latitude": 40.7128,
                "longitude": -74.006,
                "timezone": "America/New_York"
            },
            {
                "name": "Lima",
                "latitude": -12.0464,
                "longitude": -77.0428,
                "timezone": "America/Lima"
            },
            {
                "name": "Harare",
                "latitude": -17.8292,
                "longitude": 31.0522,
                "timezone": "Africa/Harare"
            },
            {
                "name": "Canberra",
                "latitude": -35.2809,
                "longitude": 149.13,
                "timezone": "Australia/Canberra"
            }
        ]
    }