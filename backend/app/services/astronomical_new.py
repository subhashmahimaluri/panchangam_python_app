"""
Core astronomical calculations using Swiss Ephemeris
"""
import swisseph as swe
import math
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime, utc_to_local, format_time_12hour
from app.utils.constants import SUN, MOON, SIDEREAL_FLAG

# Initialize Swiss Ephemeris - use built-in ephemeris data
swe.set_ephe_path('')  # Use built-in ephemeris data

def calculate_sunrise_sunset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate accurate sunrise and sunset times using Swiss Ephemeris
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Tuple of (sunrise_time, sunset_time) in "HH:MM AM/PM" format
    """
    try:
        year, month, day = date.year, date.month, date.day
        print(f"Calculating sunrise/sunset for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}")
        
        sunrise_jd = None
        sunset_jd = None
        
        # Search every 10 minutes from midnight to midnight UTC
        for minute in range(0, 24 * 60, 10):  # Every 10 minutes
            hour_utc = minute / 60.0
            jd = swe.julday(year, month, day, hour_utc)
            
            # Get sun position in ecliptic coordinates
            sun_result = swe.calc_ut(jd, SUN, swe.FLG_SWIEPH)
            if not sun_result:
                continue
                
            sun_lon = sun_result[0][0]  # Ecliptic longitude
            sun_lat = sun_result[0][1]  # Ecliptic latitude
            
            # Convert ecliptic to equatorial coordinates
            obliquity = swe.calc_ut(jd, swe.ECL_NUT, 0)[0][0]  # Obliquity of ecliptic
            ra, dec = ecliptic_to_equatorial(sun_lon, sun_lat, obliquity)
            
            # Calculate altitude
            altitude = calculate_sun_altitude_precise(jd, ra, dec, latitude, longitude)
            
            # Check for sunrise
            if altitude > -0.833 and sunrise_jd is None:
                sunrise_jd = jd
                print(f"Sunrise found at {hour_utc:05.2f} UTC: altitude = {altitude:.2f}°")
            
            # Check for sunset (after 6 hours UTC)
            if altitude < -0.833 and hour_utc > 6 and sunset_jd is None:
                sunset_jd = jd
                print(f"Sunset found at {hour_utc:05.2f} UTC: altitude = {altitude:.2f}°")
                break
        
        # Format results
        sunrise_time = format_ist_time_from_jd(sunrise_jd) if sunrise_jd else "No Rise"
        sunset_time = format_ist_time_from_jd(sunset_jd) if sunset_jd else "No Set"
        
        return sunrise_time, sunset_time
            
    except Exception as e:
        print(f"Error calculating sunrise/sunset: {e}")
        import traceback
        traceback.print_exc()
        return "Calc Error", "Calc Error"

def ecliptic_to_equatorial(lon: float, lat: float, obliquity: float) -> Tuple[float, float]:
    """
    Convert ecliptic coordinates to equatorial coordinates
    
    Args:
        lon: Ecliptic longitude in degrees
        lat: Ecliptic latitude in degrees  
        obliquity: Obliquity of ecliptic in degrees
        
    Returns:
        Tuple of (right_ascension, declination) in degrees
    """
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)
    obl_rad = math.radians(obliquity)
    
    # Convert to equatorial coordinates
    sin_ra = math.sin(lon_rad) * math.cos(obl_rad) - math.tan(lat_rad) * math.sin(obl_rad)
    cos_ra = math.cos(lon_rad)
    ra = math.degrees(math.atan2(sin_ra, cos_ra))
    
    # Normalize RA to [0, 360)
    if ra < 0:
        ra += 360
    
    sin_dec = math.sin(lat_rad) * math.cos(obl_rad) + math.cos(lat_rad) * math.sin(obl_rad) * math.sin(lon_rad)
    dec = math.degrees(math.asin(sin_dec))
    
    return ra, dec

def calculate_sun_altitude_precise(jd: float, ra: float, dec: float, latitude: float, longitude: float) -> float:
    """
    Calculate sun altitude above horizon
    
    Args:
        jd: Julian Day Number
        ra: Right ascension in degrees
        dec: Declination in degrees
        latitude: Observer latitude in degrees
        longitude: Observer longitude in degrees
        
    Returns:
        Altitude in degrees (negative = below horizon)
    """
    # Greenwich Mean Sidereal Time
    gmst = swe.sidtime(jd) * 15  # Convert hours to degrees
    
    # Local sidereal time
    lst = gmst + longitude
    
    # Hour angle
    hour_angle = lst - ra
    
    # Normalize hour angle
    while hour_angle > 180:
        hour_angle -= 360
    while hour_angle < -180:
        hour_angle += 360
    
    # Convert to radians
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(dec)
    ha_rad = math.radians(hour_angle)
    
    # Calculate altitude
    sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
               math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
    
    # Clamp to avoid math errors
    sin_alt = max(-1.0, min(1.0, sin_alt))
    altitude = math.degrees(math.asin(sin_alt))
    
    return altitude

def format_ist_time_from_jd(jd: float) -> str:
    """
    Convert Julian Day to IST time string
    
    Args:
        jd: Julian Day Number
        
    Returns:
        Time string in "HH:MM AM/PM" format
    """
    cal_date = swe.revjul(jd)
    year, month, day, hour_float_utc = cal_date
    
    # Convert UTC to IST
    ist_hour_float = hour_float_utc + 5.5
    if ist_hour_float >= 24:
        ist_hour_float -= 24
    
    hours = int(ist_hour_float)
    minutes = int((ist_hour_float - hours) * 60)
    
    # Format as 12-hour time
    if hours == 0:
        return f"12:{minutes:02d} AM"
    elif hours < 12:
        return f"{hours}:{minutes:02d} AM"
    elif hours == 12:
        return f"12:{minutes:02d} PM"
    else:
        return f"{hours-12}:{minutes:02d} PM"

def calculate_moonrise_moonset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate accurate moonrise and moonset times using Swiss Ephemeris
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Tuple of (moonrise_time, moonset_time) in "HH:MM AM/PM" format
    """
    try:
        year, month, day = date.year, date.month, date.day
        print(f"Calculating moonrise/moonset for {year}-{month:02d}-{day:02d}")
        
        moonrise_jd = None
        moonset_jd = None
        
        # Search every 30 minutes from midnight to midnight UTC
        for minute in range(0, 24 * 60, 30):  # Every 30 minutes
            hour_utc = minute / 60.0
            jd = swe.julday(year, month, day, hour_utc)
            
            # Get moon position in ecliptic coordinates
            moon_result = swe.calc_ut(jd, MOON, swe.FLG_SWIEPH)
            if not moon_result:
                continue
                
            moon_lon = moon_result[0][0]  # Ecliptic longitude
            moon_lat = moon_result[0][1]  # Ecliptic latitude
            
            # Convert ecliptic to equatorial coordinates
            obliquity = swe.calc_ut(jd, swe.ECL_NUT, 0)[0][0]  # Obliquity of ecliptic
            ra, dec = ecliptic_to_equatorial(moon_lon, moon_lat, obliquity)
            
            # Calculate altitude
            altitude = calculate_sun_altitude_precise(jd, ra, dec, latitude, longitude)
            
            # Check for moonrise
            if altitude > 0 and moonrise_jd is None:
                moonrise_jd = jd
                print(f"Moonrise found at {hour_utc:05.2f} UTC: altitude = {altitude:.2f}°")
            
            # Check for moonset (after moonrise found)
            if altitude < 0 and moonrise_jd is not None and moonset_jd is None:
                moonset_jd = jd
                print(f"Moonset found at {hour_utc:05.2f} UTC: altitude = {altitude:.2f}°")
                break
        
        # Format results
        moonrise_time = format_ist_time_from_jd(moonrise_jd) if moonrise_jd else "No Rise"
        moonset_time = format_ist_time_from_jd(moonset_jd) if moonset_jd else "No Set"
        
        return moonrise_time, moonset_time
            
    except Exception as e:
        print(f"Error calculating moonrise/moonset: {e}")
        import traceback
        traceback.print_exc()
        return "Calc Error", "Calc Error"

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