#!/usr/bin/env python3
"""
Final working sunrise/sunset calculation
"""
import swisseph as swe
import math
from datetime import datetime, timezone, timedelta

def calculate_sunrise_sunset_final(year, month, day, latitude, longitude):
    """
    Calculate sunrise/sunset times accurately
    """
    print(f"Calculating for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}")
    
    # Initialize Swiss Ephemeris
    swe.set_ephe_path('')
    
    sunrise_time = None
    sunset_time = None
    
    # Create base Julian Day at midnight UTC
    base_jd = swe.julday(year, month, day, 0.0)
    
    print("\nScanning sun positions throughout the day:")
    
    # Scan every hour from midnight to midnight UTC
    for hour_utc in range(0, 24):
        jd = base_jd + hour_utc / 24.0
        
        # Get sun position
        sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        if not sun_result:
            continue
            
        ra = sun_result[0][5]  # Right ascension
        dec = sun_result[0][1]  # Declination
        
        # Calculate altitude
        altitude = calculate_sun_altitude(jd, ra, dec, latitude, longitude)
        
        # Convert to IST for display
        ist_hour = (hour_utc + 5.5) % 24
        print(f"  {hour_utc:02d}:00 UTC ({ist_hour:04.1f} IST): altitude = {altitude:6.2f}°")
        
        # Check for sunrise (first time altitude > -0.833°)
        if altitude > -0.833 and sunrise_time is None:
            sunrise_time = jd_to_ist_time(jd)
            print(f"  >>> SUNRISE detected at {hour_utc:02d}:00 UTC")
        
        # Check for sunset (first time after 12:00 UTC when altitude < -0.833°)
        if altitude < -0.833 and hour_utc > 6 and sunset_time is None:
            sunset_time = jd_to_ist_time(jd)
            print(f"  >>> SUNSET detected at {hour_utc:02d}:00 UTC")
    
    return sunrise_time or "No Rise", sunset_time or "No Set"

def calculate_sun_altitude(jd, ra, dec, latitude, longitude):
    """Calculate sun altitude above horizon"""
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

def jd_to_ist_time(jd):
    """Convert Julian Day to IST time string"""
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

if __name__ == "__main__":
    # Test for Bengaluru on January 5, 2025
    sunrise, sunset = calculate_sunrise_sunset_final(2025, 1, 5, 12.9716, 77.5946)
    print(f"\nFinal Results:")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")