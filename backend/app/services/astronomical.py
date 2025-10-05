"""
Core astronomical calculations using Swiss Ephemeris
Based on the proven drik-panchanga implementation
"""
import swisseph as swe
import math
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional, List
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime, utc_to_local, format_time_12hour
from app.utils.constants import SUN, MOON, SIDEREAL_FLAG

# Initialize Swiss Ephemeris - use built-in ephemeris data
swe.set_ephe_path('')  # Use built-in ephemeris data

def to_dms(deg: float) -> List[int]:
    """Convert decimal degrees to degrees, minutes, seconds"""
    d = int(deg)
    mins = (deg - d) * 60
    m = int(mins)
    s = int(round((mins - m) * 60))
    return [d, m, s]

def from_dms(degs: int, mins: int, secs: int) -> float:
    """Convert degrees, minutes, seconds to decimal degrees"""
    return degs + mins/60 + secs/3600

def calculate_sunrise_sunset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate accurate sunrise and sunset times using Swiss Ephemeris
    Uses a robust iterative approach instead of the broken rise_trans function
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone calculation
        
    Returns:
        Tuple of (sunrise_time, sunset_time) in "HH:MM AM/PM" format
    """
    try:
        year, month, day = date.year, date.month, date.day
        print(f"Calculating sunrise/sunset for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}, City: {city}")
        
        # Julian Day for midnight UTC
        jd_start = swe.julday(year, month, day, 0.0)
        
        # Get timezone offset for the city
        tz_offset = get_timezone_offset(city, longitude, date)
        print(f"Using timezone offset: {tz_offset} hours for {city}")
        
        # Find sunrise and sunset using iterative search
        sunrise_jd = find_sun_event(jd_start, latitude, longitude, True)  # True for sunrise
        sunset_jd = find_sun_event(jd_start, latitude, longitude, False)  # False for sunset
        
        sunrise_time = "No Rise"
        sunset_time = "No Set"
        
        if sunrise_jd:
            sunrise_local_jd = sunrise_jd + tz_offset/24
            sunrise_time = format_jd_to_time(sunrise_local_jd)
        
        if sunset_jd:
            sunset_local_jd = sunset_jd + tz_offset/24
            sunset_time = format_jd_to_time(sunset_local_jd)
        
        print(f"Results - Sunrise: {sunrise_time}, Sunset: {sunset_time}")
        return sunrise_time, sunset_time
            
    except Exception as e:
        print(f"Error calculating sunrise/sunset: {e}")
        import traceback
        traceback.print_exc()
        return "Calc Error", "Calc Error"

def find_sun_event(jd_start: float, latitude: float, longitude: float, is_sunrise: bool) -> Optional[float]:
    """
    Find the exact Julian Day of sunrise or sunset using iterative search
    
    Args:
        jd_start: Starting Julian Day (midnight UTC)
        latitude: Observer latitude in degrees
        longitude: Observer longitude in degrees  
        is_sunrise: True for sunrise, False for sunset
        
    Returns:
        Julian Day of the event in UTC, or None if not found
    """
    try:
        # Search range: 24 hours from start
        search_duration = 1.0  # 1 day
        step_size = 1.0 / (24 * 20)  # 3-minute intervals for higher precision
        
        # Target altitude for sun: -0.833 degrees (accounts for atmospheric refraction)
        target_altitude = -0.833
        
        previous_altitude = None
        previous_jd = None
        
        # Coarse search to find approximate crossing
        for i in range(int(search_duration / step_size)):
            jd = jd_start + i * step_size
            altitude = calculate_body_altitude(jd, swe.SUN, latitude, longitude)
            
            if previous_altitude is not None:
                # Check for crossing
                if is_sunrise:
                    # Sunrise: altitude crosses from below to above target
                    if previous_altitude <= target_altitude < altitude:
                        # Refine with binary search
                        return binary_search_crossing(
                            previous_jd, jd, swe.SUN, latitude, longitude, target_altitude, is_sunrise
                        )
                else:
                    # Sunset: altitude crosses from above to below target
                    if previous_altitude >= target_altitude > altitude:
                        # Refine with binary search
                        return binary_search_crossing(
                            previous_jd, jd, swe.SUN, latitude, longitude, target_altitude, is_sunrise
                        )
            
            previous_altitude = altitude
            previous_jd = jd
        
        return None
        
    except Exception as e:
        print(f"Error in find_sun_event: {e}")
        return None

def find_moon_event(jd_start: float, latitude: float, longitude: float, is_moonrise: bool) -> Optional[float]:
    """
    Find the exact Julian Day of moonrise or moonset using iterative search
    
    Args:
        jd_start: Starting Julian Day (midnight UTC)
        latitude: Observer latitude in degrees
        longitude: Observer longitude in degrees
        is_moonrise: True for moonrise, False for moonset
        
    Returns:
        Julian Day of the event in UTC, or None if not found
    """
    try:
        # Search range: 48 hours from start (moon events can span days)
        search_duration = 2.0  # 2 days
        step_size = 1.0 / (24 * 6)  # 10-minute intervals for higher precision
        
        # Target altitude for moon: 0.0 degrees (geometric horizon)
        target_altitude = 0.0
        
        previous_altitude = None
        previous_jd = None
        
        # Coarse search to find approximate crossing
        for i in range(int(search_duration / step_size)):
            jd = jd_start + i * step_size
            altitude = calculate_body_altitude(jd, swe.MOON, latitude, longitude)
            
            if previous_altitude is not None:
                # Check for crossing
                if is_moonrise:
                    # Moonrise: altitude crosses from below to above target
                    if previous_altitude <= target_altitude < altitude:
                        # Refine with binary search
                        return binary_search_crossing(
                            previous_jd, jd, swe.MOON, latitude, longitude, target_altitude, is_moonrise
                        )
                else:
                    # Moonset: altitude crosses from above to below target
                    if previous_altitude >= target_altitude > altitude:
                        # Refine with binary search
                        return binary_search_crossing(
                            previous_jd, jd, swe.MOON, latitude, longitude, target_altitude, is_moonrise
                        )
            
            previous_altitude = altitude
            previous_jd = jd
        
        return None
        
    except Exception as e:
        print(f"Error in find_moon_event: {e}")
        return None

def calculate_body_altitude(jd: float, body: int, latitude: float, longitude: float) -> float:
    """
    Calculate altitude of a celestial body above horizon
    
    Args:
        jd: Julian Day Number
        body: Swiss Ephemeris body constant (swe.SUN, swe.MOON, etc.)
        latitude: Observer latitude in degrees
        longitude: Observer longitude in degrees
        
    Returns:
        Altitude in degrees (negative = below horizon)
    """
    try:
        # Get body position
        result = swe.calc_ut(jd, body, swe.FLG_SWIEPH)
        if not result:
            return -90.0
            
        # Get ecliptic coordinates
        ecliptic_lon = result[0][0]  # Ecliptic longitude
        ecliptic_lat = result[0][1]  # Ecliptic latitude
        
        # Get obliquity of ecliptic
        obliquity = swe.calc_ut(jd, swe.ECL_NUT, 0)[0][0]
        
        # Convert to equatorial coordinates
        ra, dec = ecliptic_to_equatorial(ecliptic_lon, ecliptic_lat, obliquity)
        
        # Calculate Greenwich Mean Sidereal Time
        gmst = swe.sidtime(jd) * 15  # Convert hours to degrees
        
        # Calculate Local Sidereal Time
        lst = gmst + longitude
        
        # Calculate Hour Angle
        hour_angle = lst - ra
        
        # Normalize hour angle to [-180, 180]
        while hour_angle > 180:
            hour_angle -= 360
        while hour_angle < -180:
            hour_angle += 360
        
        # Convert to radians
        lat_rad = math.radians(latitude)
        dec_rad = math.radians(dec)
        ha_rad = math.radians(hour_angle)
        
        # Calculate altitude using spherical trigonometry
        sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
                   math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
        
        # Clamp to avoid numerical errors
        sin_alt = max(-1.0, min(1.0, sin_alt))
        altitude = math.degrees(math.asin(sin_alt))
        
        return altitude
        
    except Exception as e:
        print(f"Error calculating body altitude: {e}")
        return -90.0

def ecliptic_to_equatorial(ecliptic_lon: float, ecliptic_lat: float, obliquity: float) -> Tuple[float, float]:
    """
    Convert ecliptic coordinates to equatorial coordinates
    
    Args:
        ecliptic_lon: Ecliptic longitude in degrees
        ecliptic_lat: Ecliptic latitude in degrees
        obliquity: Obliquity of ecliptic in degrees
        
    Returns:
        Tuple of (right_ascension, declination) in degrees
    """
    # Convert to radians
    lon_rad = math.radians(ecliptic_lon)
    lat_rad = math.radians(ecliptic_lat)
    obl_rad = math.radians(obliquity)
    
    # Calculate right ascension
    sin_ra = math.sin(lon_rad) * math.cos(obl_rad) - math.tan(lat_rad) * math.sin(obl_rad)
    cos_ra = math.cos(lon_rad)
    ra = math.degrees(math.atan2(sin_ra, cos_ra))
    
    # Normalize RA to [0, 360)
    if ra < 0:
        ra += 360
    
    # Calculate declination
    sin_dec = math.sin(lat_rad) * math.cos(obl_rad) + math.cos(lat_rad) * math.sin(obl_rad) * math.sin(lon_rad)
    dec = math.degrees(math.asin(sin_dec))
    
    return ra, dec

def binary_search_crossing(
    start_jd: float, 
    end_jd: float, 
    body: int, 
    latitude: float, 
    longitude: float, 
    target_altitude: float, 
    is_rising: bool
) -> float:
    """
    Use binary search to find precise moment when body crosses target altitude
    
    Args:
        start_jd: Start Julian Day
        end_jd: End Julian Day
        body: Swiss Ephemeris body constant
        latitude: Observer latitude
        longitude: Observer longitude
        target_altitude: Target altitude in degrees
        is_rising: True for rising, False for setting
        
    Returns:
        Julian Day of precise crossing moment
    """
    tolerance = 1.0 / (24 * 60 * 60)  # 1 second tolerance
    iterations = 0
    max_iterations = 20
    
    while (end_jd - start_jd) > tolerance and iterations < max_iterations:
        mid_jd = (start_jd + end_jd) / 2
        iterations += 1
        
        altitude = calculate_body_altitude(mid_jd, body, latitude, longitude)
        
        if is_rising:
            if altitude < target_altitude:
                start_jd = mid_jd
            else:
                end_jd = mid_jd
        else:
            if altitude > target_altitude:
                start_jd = mid_jd
            else:
                end_jd = mid_jd
    
    return (start_jd + end_jd) / 2

def get_timezone_offset(city: str, longitude: float, date: datetime = None) -> float:
    """
    Get timezone offset for a given city/longitude, considering daylight saving time
    
    Args:
        city: City name
        longitude: Longitude in degrees
        date: Date to check for DST (default: None)
        
    Returns:
        Timezone offset in hours from UTC
    """
    # City-specific timezone mappings with DST consideration
    city_timezones = {
        "bengaluru": 5.5,   # IST (no DST)
        "bangalore": 5.5,   # IST (no DST)
        "mumbai": 5.5,      # IST (no DST)
        "delhi": 5.5,       # IST (no DST)
        "chennai": 5.5,     # IST (no DST)
        "kolkata": 5.5,     # IST (no DST)
        "hyderabad": 5.5,   # IST (no DST)
        "pune": 5.5,        # IST (no DST)
        
        # UK uses BST (UTC+1) in summer, GMT (UTC+0) in winter
        # October 5, 2025 would be BST (UTC+1)
        "coventry": 1.0,    # BST in October
        "london": 1.0,      # BST in October
        "manchester": 1.0,  # BST in October
        "birmingham": 1.0,  # BST in October
        
        # USA East Coast uses EDT (UTC-4) in summer, EST (UTC-5) in winter
        # October 5, 2025 would be EDT (UTC-4) - DST ends first Sunday of November
        "new york": -4.0,   # EDT in October
        "newyork": -4.0,    # EDT in October
        "miami": -4.0,      # EDT in October
        
        # USA West Coast uses PDT (UTC-7) in summer, PST (UTC-8) in winter
        "los angeles": -7.0, # PDT in October
        
        # USA Central uses CDT (UTC-5) in summer, CST (UTC-6) in winter
        "chicago": -5.0,    # CDT in October
        
        "lima": -5.0,       # PET (Peru Time, no DST)
        
        "harare": 2.0,      # CAT (Central Africa Time, no DST)
        "johannesburg": 2.0, # SAST (no DST)
        "cape town": 2.0,   # SAST (no DST)
        
        # Australia uses AEDT (UTC+11) in summer, AEST (UTC+10) in winter
        # October 5 is spring in Australia - DST starts first Sunday of October
        # So October 5, 2025 would be AEDT (UTC+11)
        "canberra": 11.0,   # AEDT in October
        "sydney": 11.0,     # AEDT in October
        "melbourne": 11.0,  # AEDT in October
        "brisbane": 10.0,   # AEST (Queensland doesn't use DST)
        "perth": 8.0,       # AWST (Western Australia doesn't use DST)
    }
    
    # Check for exact city match first
    city_lower = city.lower().replace(" ", "").replace("-", "")
    if city_lower in city_timezones:
        return city_timezones[city_lower]
    
    # Fallback: estimate timezone from longitude
    # Rough approximation: 15 degrees longitude = 1 hour
    estimated_offset = longitude / 15.0
    
    # Round to nearest 0.5 hours (most timezones are multiples of 0.5)
    return round(estimated_offset * 2) / 2

def format_jd_to_time(jd: float) -> str:
    """
    Convert Julian Day to local time string in HH:MM AM/PM format
    
    Args:
        jd: Julian Day Number (already in local time)
        
    Returns:
        Time string in "HH:MM AM/PM" format
    """
    try:
        cal_date = swe.revjul(jd)
        year, month, day, hour_float = cal_date[:4]
        
        hours = int(hour_float)
        minutes = int((hour_float - hours) * 60)
        
        # Handle overflow
        if hours >= 24:
            hours -= 24
        
        # Format as 12-hour time
        if hours == 0:
            return f"12:{minutes:02d} AM"
        elif hours < 12:
            return f"{hours}:{minutes:02d} AM"
        elif hours == 12:
            return f"12:{minutes:02d} PM"
        else:
            return f"{hours-12}:{minutes:02d} PM"
    except Exception as e:
        print(f"Error formatting time: {e}")
        return "Time Error"

def calculate_moonrise_moonset(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate accurate moonrise and moonset times using Swiss Ephemeris
    Uses a robust iterative approach instead of the broken rise_trans function
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone calculation
        
    Returns:
        Tuple of (moonrise_time, moonset_time) in "HH:MM AM/PM" format
    """
    try:
        year, month, day = date.year, date.month, date.day
        print(f"Calculating moonrise/moonset for {year}-{month:02d}-{day:02d}, City: {city}")
        
        # Julian Day for midnight UTC
        jd_start = swe.julday(year, month, day, 0.0)
        
        # Get timezone offset for the city
        tz_offset = get_timezone_offset(city, longitude, date)
        
        # Find moonrise and moonset using iterative search
        moonrise_jd = find_moon_event(jd_start, latitude, longitude, True)  # True for moonrise
        moonset_jd = find_moon_event(jd_start, latitude, longitude, False)  # False for moonset
        
        moonrise_time = "No Rise"
        moonset_time = "No Set"
        
        if moonrise_jd:
            moonrise_local_jd = moonrise_jd + tz_offset/24
            moonrise_time = format_jd_to_time(moonrise_local_jd)
        
        if moonset_jd:
            moonset_local_jd = moonset_jd + tz_offset/24
            
            # Check if moonset is on the next day
            moonset_date = swe.revjul(moonset_local_jd)
            if moonset_date[2] > day:  # Day is different
                moonset_time = format_jd_to_time(moonset_local_jd) + " (+1)"
            else:
                moonset_time = format_jd_to_time(moonset_local_jd)
        
        print(f"Results - Moonrise: {moonrise_time}, Moonset: {moonset_time}")
        return moonrise_time, moonset_time
            
    except Exception as e:
        print(f"Error calculating moonrise/moonset: {e}")
        import traceback
        traceback.print_exc()
        return "Calc Error", "Calc Error"

def solar_longitude(jd: float) -> float:
    """Solar longitude at given instant (julian day) jd"""
    data = swe.calc_ut(jd, swe.SUN, flags=swe.FLG_SWIEPH)
    return data[0][0]  # in degrees

def lunar_longitude(jd: float) -> float:
    """Lunar longitude at given instant (julian day) jd"""
    data = swe.calc_ut(jd, swe.MOON, flags=swe.FLG_SWIEPH)
    return data[0][0]  # in degrees

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