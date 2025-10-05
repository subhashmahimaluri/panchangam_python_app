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
        # Convert to UTC for Swiss Ephemeris
        utc_date = date.replace(tzinfo=timezone.utc)
        jd = get_julian_day_ut(utc_date)
        
        print(f"Calculating sunrise/sunset for JD: {jd}, Lat: {latitude}, Lon: {longitude}")
        
        # Try multiple calculation methods
        # Method 1: Use rise_trans with different flags
        try:
            sunrise_result = swe.rise_trans(
                jd, SUN, longitude, latitude, 
                rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER
            )
            
            sunset_result = swe.rise_trans(
                jd, SUN, longitude, latitude, 
                rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER
            )
            
            print(f"Method 1 - Sunrise result: {sunrise_result}")
            print(f"Method 1 - Sunset result: {sunset_result}")
            
            if sunrise_result[0] == swe.OK and sunset_result[0] == swe.OK:
                sunrise_jd = sunrise_result[1][0]
                sunset_jd = sunset_result[1][0]
                
                # Convert back to local time
                sunrise_dt = julian_day_to_datetime(sunrise_jd, city)
                sunset_dt = julian_day_to_datetime(sunset_jd, city)
                
                print(f"Method 1 success - Sunrise: {sunrise_dt}, Sunset: {sunset_dt}")
                
                return format_time_12hour(sunrise_dt), format_time_12hour(sunset_dt)
                
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        # Method 2: Use iterative approach to find rise/set times
        return calculate_solar_times_iterative(jd, latitude, longitude, city)
            
    except Exception as e:
        print(f"Error calculating sunrise/sunset: {e}")
        # Return error message instead of hardcoded values
        return "Calc Error", "Calc Error"

def calculate_solar_times_iterative(
    jd: float, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Calculate sunrise/sunset using iterative method to find horizon crossing
    
    Args:
        jd: Julian Day Number
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name
        
    Returns:
        Tuple of (sunrise_time, sunset_time)
    """
    try:
        print(f"Using iterative solar calculation for JD: {jd}")
        
        sunrise_jd = None
        sunset_jd = None
        
        # Search in 24-hour window with 10-minute intervals
        start_jd = jd
        end_jd = jd + 1.0
        interval = 10.0 / (24 * 60)  # 10 minutes in Julian days
        
        search_jd = start_jd
        prev_altitude = None
        
        while search_jd <= end_jd:
            # Get sun position
            sun_pos = swe.calc_ut(search_jd, SUN, swe.FLG_SWIEPH)
            if sun_pos[1] != swe.OK:
                search_jd += interval
                continue
                
            sun_ra = sun_pos[0][5]  # Right ascension
            sun_dec = sun_pos[0][1]  # Declination
            
            # Calculate altitude
            altitude = calculate_altitude(search_jd, sun_ra, sun_dec, latitude, longitude)
            
            if prev_altitude is not None:
                # Check for sunrise (crossing -0.833 degrees upward)
                if prev_altitude < -0.833 and altitude >= -0.833 and sunrise_jd is None:
                    # Refine with binary search
                    sunrise_jd = binary_search_crossing(search_jd - interval, search_jd, 
                                                       latitude, longitude, SUN, -0.833, True)
                
                # Check for sunset (crossing -0.833 degrees downward)
                if prev_altitude >= -0.833 and altitude < -0.833 and sunset_jd is None and sunrise_jd is not None:
                    # Refine with binary search
                    sunset_jd = binary_search_crossing(search_jd - interval, search_jd, 
                                                      latitude, longitude, SUN, -0.833, False)
            
            prev_altitude = altitude
            search_jd += interval
        
        # Convert to local times
        if sunrise_jd:
            sunrise_dt = julian_day_to_datetime(sunrise_jd, city)
            sunrise_str = format_time_12hour(sunrise_dt)
        else:
            sunrise_str = "No Rise"
        
        if sunset_jd:
            sunset_dt = julian_day_to_datetime(sunset_jd, city)
            sunset_str = format_time_12hour(sunset_dt)
        else:
            sunset_str = "No Set"
        
        print(f"Iterative calculation - Sunrise: {sunrise_str}, Sunset: {sunset_str}")
        
        return sunrise_str, sunset_str
        
    except Exception as e:
        print(f"Error in iterative solar calculation: {e}")
        return "Calc Error", "Calc Error"

def binary_search_crossing(
    start_jd: float, 
    end_jd: float, 
    latitude: float, 
    longitude: float, 
    body: int, 
    target_altitude: float, 
    rising: bool
) -> float:
    """
    Use binary search to find precise moment of altitude crossing
    
    Args:
        start_jd: Start Julian Day
        end_jd: End Julian Day
        latitude: Observer latitude
        longitude: Observer longitude
        body: Celestial body (SUN or MOON)
        target_altitude: Target altitude in degrees
        rising: True for rising, False for setting
        
    Returns:
        Julian Day of crossing
    """
    tolerance = 1.0 / (24 * 60 * 60)  # 1 second tolerance
    
    while (end_jd - start_jd) > tolerance:
        mid_jd = (start_jd + end_jd) / 2
        
        # Get body position
        body_pos = swe.calc_ut(mid_jd, body, swe.FLG_SWIEPH)
        if body_pos[1] != swe.OK:
            return mid_jd
        
        body_ra = body_pos[0][5]
        body_dec = body_pos[0][1]
        
        altitude = calculate_altitude(mid_jd, body_ra, body_dec, latitude, longitude)
        
        if rising:
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
        # Convert to UTC for Swiss Ephemeris
        utc_date = date.replace(tzinfo=timezone.utc)
        jd = get_julian_day_ut(utc_date)
        
        print(f"Calculating moonrise/moonset for JD: {jd}")
        
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
        
        print(f"Moonrise result: {moonrise_result}")
        print(f"Moonset result: {moonset_result}")
        
        if moonrise_result[0] == swe.OK and moonset_result[0] == swe.OK:
            moonrise_jd = moonrise_result[1][0]
            moonset_jd = moonset_result[1][0]
            
            # Convert back to local time
            moonrise_dt = julian_day_to_datetime(moonrise_jd, city)
            moonset_dt = julian_day_to_datetime(moonset_jd, city)
            
            print(f"Calculated moonrise: {moonrise_dt}, moonset: {moonset_dt}")
            
            return format_time_12hour(moonrise_dt), format_time_12hour(moonset_dt)
        else:
            # Calculate using lunar position method
            return calculate_lunar_times_precise(jd, latitude, longitude, city)
            
    except Exception as e:
        print(f"Error calculating moonrise/moonset: {e}")
        return calculate_lunar_times_precise(jd, latitude, longitude, city)



def calculate_lunar_times_precise(
    jd: float, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Tuple[str, str]:
    """
    Precise calculation for moonrise/moonset using lunar position
    
    Args:
        jd: Julian Day Number
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name
        
    Returns:
        Tuple of (moonrise_time, moonset_time)
    """
    try:
        print(f"Using precise lunar calculation for JD: {jd}")
        
        # Search for moonrise and moonset in 24-hour window
        start_jd = jd
        end_jd = jd + 1.0
        
        moonrise_jd = None
        moonset_jd = None
        
        # Search with 1-hour increments
        search_jd = start_jd
        prev_altitude = None
        
        while search_jd <= end_jd:
            # Calculate moon position
            moon_pos = swe.calc_ut(search_jd, MOON, swe.FLG_SWIEPH)[0]
            moon_ra = moon_pos[5]  # Right ascension
            moon_dec = moon_pos[1]  # Declination
            
            # Calculate altitude
            altitude = calculate_altitude(search_jd, moon_ra, moon_dec, latitude, longitude)
            
            if prev_altitude is not None:
                # Check for rising (crossing horizon upward)
                if prev_altitude < 0 and altitude >= 0 and moonrise_jd is None:
                    moonrise_jd = search_jd - 1/24  # Approximate to previous hour
                
                # Check for setting (crossing horizon downward)
                if prev_altitude >= 0 and altitude < 0 and moonset_jd is None:
                    moonset_jd = search_jd - 1/24  # Approximate to previous hour
            
            prev_altitude = altitude
            search_jd += 1/24  # Increment by 1 hour
        
        # Convert to local times
        if moonrise_jd:
            moonrise_dt = julian_day_to_datetime(moonrise_jd, city)
            moonrise_str = format_time_12hour(moonrise_dt)
        else:
            moonrise_str = "No Rise"
        
        if moonset_jd:
            moonset_dt = julian_day_to_datetime(moonset_jd, city)
            moonset_str = format_time_12hour(moonset_dt)
        else:
            moonset_str = "No Set"
        
        print(f"Precise lunar calculation - Moonrise: {moonrise_str}, Moonset: {moonset_str}")
        
        return moonrise_str, moonset_str
        
    except Exception as e:
        print(f"Error in precise lunar calculation: {e}")
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