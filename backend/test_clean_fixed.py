#!/usr/bin/env python3
"""
Clean, working sunrise/sunset calculation using Swiss Ephemeris
"""
import swisseph as swe
import math
from datetime import datetime, timezone, timedelta

def calculate_sunrise_sunset_clean(year, month, day, latitude, longitude):
    """
    Clean implementation of sunrise/sunset calculation
    """
    print(f"Calculating for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}")
    
    # Initialize Swiss Ephemeris
    swe.set_ephe_path('')
    
    sunrise_jd = None
    sunset_jd = None
    
    # Search from 4 AM to 8 PM local time  
    for hour in range(4, 20):
        for minute in [0, 15, 30, 45]:
            # Use IST time directly (no UTC conversion needed for local calculations)
            hour_decimal = hour + minute/60.0
            # Convert IST to UTC for Swiss Ephemeris (subtract 5.5 hours)
            utc_hour = hour_decimal - 5.5
            if utc_hour < 0:
                utc_hour += 24
            elif utc_hour >= 24:
                utc_hour -= 24
                
            jd = swe.julday(year, month, day, utc_hour)
            
            # Get sun position
            sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
            if not sun_result:
                continue
                
            ra = sun_result[0][5]  # Right ascension
            dec = sun_result[0][1]  # Declination
            
            # Calculate altitude
            altitude = calculate_sun_altitude_clean(jd, ra, dec, latitude, longitude)
            
            # Look for horizon crossing (-0.833° for atmospheric refraction)
            if altitude >= -0.833 and sunrise_jd is None:
                sunrise_jd = jd
                print(f"Sunrise found at hour {hour_decimal}: altitude = {altitude:.2f}°")
            
            if altitude < -0.833 and sunrise_jd is not None and sunset_jd is None and hour > 12:
                sunset_jd = jd
                print(f"Sunset found at hour {hour_decimal}: altitude = {altitude:.2f}°")
                break
    
    # Convert to readable times
    if sunrise_jd:
        sunrise_time = jd_to_time_string(sunrise_jd)
    else:
        sunrise_time = "No Rise"
        
    if sunset_jd:
        sunset_time = jd_to_time_string(sunset_jd)
    else:
        sunset_time = "No Set"
    
    return sunrise_time, sunset_time

def calculate_sun_altitude_clean(jd, ra, dec, latitude, longitude):
    """
    Calculate sun altitude above horizon
    """
    # Greenwich Mean Sidereal Time
    gmst = swe.sidtime(jd) * 15  # Convert hours to degrees
    
    # Local sidereal time
    lst = gmst + longitude
    
    # Hour angle
    hour_angle = lst - ra
    
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

def jd_to_time_string(jd):
    """
    Convert Julian Day to readable time string
    """
    cal_date = swe.revjul(jd)
    year, month, day, hour_float = cal_date
    
    # The JD is already in UTC, convert to IST (UTC + 5:30)
    ist_hours = hour_float + 5.5  # Add 5:30 hours
    
    # Handle day overflow
    if ist_hours >= 24:
        ist_hours -= 24
    elif ist_hours < 0:
        ist_hours += 24
    
    hours = int(ist_hours)
    minutes = int((ist_hours - hours) * 60)
    
    # Format as 12-hour time
    if hours == 0:
        time_str = f"12:{minutes:02d} AM"
    elif hours < 12:
        time_str = f"{hours}:{minutes:02d} AM"
    elif hours == 12:
        time_str = f"12:{minutes:02d} PM"
    else:
        time_str = f"{hours-12}:{minutes:02d} PM"
    
    return time_str

if __name__ == "__main__":
    # Test for Bengaluru on January 5, 2025
    sunrise, sunset = calculate_sunrise_sunset_clean(2025, 1, 5, 12.9716, 77.5946)
    print(f"\nResults:")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")