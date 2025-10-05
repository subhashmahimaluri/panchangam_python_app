#!/usr/bin/env python3
"""
Correct sunrise/sunset calculation with proper timezone handling
"""
import swisseph as swe
import math

def calculate_sunrise_sunset_correct(year, month, day, latitude, longitude):
    """
    Calculate sunrise/sunset with better search algorithm
    """
    print(f"Calculating for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}")
    
    # Initialize Swiss Ephemeris
    swe.set_ephe_path('')
    
    # Base Julian Day at midnight UTC
    base_jd = swe.julday(year, month, day, 0.0)
    
    sunrise_jd = None
    sunset_jd = None
    
    # Search every 15 minutes throughout the day
    for quarter_hour in range(0, 24 * 4):  # 96 intervals of 15 minutes
        hour_utc = quarter_hour / 4.0
        jd = base_jd + hour_utc / 24.0
        
        # Get sun position
        sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        if not sun_result:
            continue
            
        ra = sun_result[0][5]  # Right ascension
        dec = sun_result[0][1]  # Declination
        
        # Calculate altitude
        altitude = calculate_sun_altitude(jd, ra, dec, latitude, longitude)
        
        # Check for sunrise (first time altitude crosses above -0.833°)
        if altitude > -0.833 and sunrise_jd is None:
            sunrise_jd = jd
            print(f"Sunrise found at {hour_utc:04.2f} UTC, altitude = {altitude:.2f}°")
        
        # Check for sunset (first time after noon when altitude crosses below -0.833°)
        if altitude < -0.833 and hour_utc > 6 and sunset_jd is None:
            sunset_jd = jd
            print(f"Sunset found at {hour_utc:04.2f} UTC, altitude = {altitude:.2f}°")
            break
    
    # Convert to IST and format
    sunrise_time = format_ist_time(sunrise_jd) if sunrise_jd else "No Rise"
    sunset_time = format_ist_time(sunset_jd) if sunset_jd else "No Set"
    
    return sunrise_time, sunset_time

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

def format_ist_time(jd):
    """Convert Julian Day to IST time string"""
    cal_date = swe.revjul(jd)
    year, month, day, hour_float_utc = cal_date
    
    # Convert UTC to IST
    ist_hour_float = hour_float_utc + 5.5
    
    # Handle day rollover
    if ist_hour_float >= 24:
        ist_hour_float -= 24
    elif ist_hour_float < 0:
        ist_hour_float += 24
    
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
    sunrise, sunset = calculate_sunrise_sunset_correct(2025, 1, 5, 12.9716, 77.5946)
    print(f"\nCalculated Results:")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
    print(f"\nExpected (timeanddate.com):")
    print(f"Sunrise: 6:43 AM")
    print(f"Sunset: 6:07 PM")