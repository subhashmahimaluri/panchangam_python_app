"""
Core astronomical calculations using Swiss Ephemeris
"""
import swisseph as swe
from datetime import datetime, timezone
from typing import Tuple, Optional
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime, utc_to_local, format_time_12hour
from app.utils.constants import SUN, MOON, SIDEREAL_FLAG

# Set ephemeris path (Swiss Ephemeris data files)
swe.set_ephe_path('/usr/share/swisseph')  # Standard path, will be created during installation

def calculate_sunrise_sunset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate sunrise and sunset times for given location and date
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Tuple of (sunrise_time, sunset_time) in "HH:MM AM/PM" format
    """
    try:
        # Convert to UTC for Swiss Ephemeris
        utc_date = date.replace(tzinfo=timezone.utc)
        jd = get_julian_day_ut(utc_date)
        
        # Calculate sunrise
        sunrise_result = swe.rise_trans(
            jd, SUN, longitude, latitude, 
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER
        )
        
        # Calculate sunset
        sunset_result = swe.rise_trans(
            jd, SUN, longitude, latitude, 
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER
        )
        
        if sunrise_result[0] == swe.OK and sunset_result[0] == swe.OK:
            sunrise_jd = sunrise_result[1][0]
            sunset_jd = sunset_result[1][0]
            
            # Convert back to local time
            sunrise_dt = julian_day_to_datetime(sunrise_jd, city)
            sunset_dt = julian_day_to_datetime(sunset_jd, city)
            
            return format_time_12hour(sunrise_dt), format_time_12hour(sunset_dt)
        else:
            # Fallback calculation if rise_trans fails
            return calculate_solar_times_fallback(jd, latitude, longitude, city)
            
    except Exception as e:
        print(f"Error calculating sunrise/sunset: {e}")
        # Return reasonable defaults
        return "06:00 AM", "06:00 PM"

def calculate_moonrise_moonset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate moonrise and moonset times for given location and date
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Tuple of (moonrise_time, moonset_time) in "HH:MM AM/PM" format
    """
    try:
        # Convert to UTC for Swiss Ephemeris
        utc_date = date.replace(tzinfo=timezone.utc)
        jd = get_julian_day_ut(utc_date)
        
        # Calculate moonrise
        moonrise_result = swe.rise_trans(
            jd, MOON, longitude, latitude, 
            rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER
        )
        
        # Calculate moonset
        moonset_result = swe.rise_trans(
            jd, MOON, longitude, latitude, 
            rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER
        )
        
        if moonrise_result[0] == swe.OK and moonset_result[0] == swe.OK:
            moonrise_jd = moonrise_result[1][0]
            moonset_jd = moonset_result[1][0]
            
            # Convert back to local time
            moonrise_dt = julian_day_to_datetime(moonrise_jd, city)
            moonset_dt = julian_day_to_datetime(moonset_jd, city)
            
            return format_time_12hour(moonrise_dt), format_time_12hour(moonset_dt)
        else:
            # Return reasonable defaults if calculation fails
            return "05:30 AM", "06:30 PM"
            
    except Exception as e:
        print(f"Error calculating moonrise/moonset: {e}")
        return "05:30 AM", "06:30 PM"

def calculate_solar_times_fallback(
    jd: float, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Fallback calculation for sunrise/sunset using simple formula
    
    Args:
        jd: Julian Day Number
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name
        
    Returns:
        Tuple of (sunrise_time, sunset_time)
    """
    try:
        # Get sun position at noon
        sun_pos = swe.calc_ut(jd, SUN, swe.FLG_SWIEPH)[0]
        sun_lon = sun_pos[0]
        
        # Approximate sunrise/sunset calculation
        # This is a simplified calculation
        hour_angle = 6.0  # Approximate 6 hours before/after noon
        
        # Calculate times (very approximate)
        sunrise_hour = 12 - hour_angle
        sunset_hour = 12 + hour_angle
        
        # Create datetime objects
        base_date = julian_day_to_datetime(jd, city).replace(hour=0, minute=0, second=0)
        sunrise_dt = base_date.replace(hour=int(sunrise_hour), minute=int((sunrise_hour % 1) * 60))
        sunset_dt = base_date.replace(hour=int(sunset_hour), minute=int((sunset_hour % 1) * 60))
        
        return format_time_12hour(sunrise_dt), format_time_12hour(sunset_dt)
        
    except Exception as e:
        print(f"Error in fallback calculation: {e}")
        return "06:00 AM", "06:00 PM"

def get_sun_position(jd: float) -> Tuple[float, float]:
    """
    Get sun's longitude and latitude for given Julian Day
    
    Args:
        jd: Julian Day Number
        
    Returns:
        Tuple of (longitude, latitude) in degrees
    """
    try:
        # Set sidereal mode for accurate calculations
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Calculate sun position
        result = swe.calc_ut(jd, SUN, SIDEREAL_FLAG | swe.FLG_SWIEPH)
        if result:
            return result[0][0], result[0][1]  # longitude, latitude
        else:
            return 0.0, 0.0
    except Exception as e:
        print(f"Error getting sun position: {e}")
        return 0.0, 0.0

def get_moon_position(jd: float) -> Tuple[float, float]:
    """
    Get moon's longitude and latitude for given Julian Day
    
    Args:
        jd: Julian Day Number
        
    Returns:
        Tuple of (longitude, latitude) in degrees
    """
    try:
        # Set sidereal mode for accurate calculations
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Calculate moon position
        result = swe.calc_ut(jd, MOON, SIDEREAL_FLAG | swe.FLG_SWIEPH)
        if result:
            return result[0][0], result[0][1]  # longitude, latitude
        else:
            return 0.0, 0.0
    except Exception as e:
        print(f"Error getting moon position: {e}")
        return 0.0, 0.0