#!/usr/bin/env python3
"""
Working sunrise/sunset calculation using Swiss Ephemeris correctly
"""
import swisseph as swe
import math

def calculate_sunrise_sunset_working(year, month, day, latitude, longitude):
    """
    Calculate sunrise/sunset using proper Swiss Ephemeris approach
    """
    print(f"Calculating for {year}-{month:02d}-{day:02d}, Lat: {latitude}, Lon: {longitude}")
    
    # Initialize Swiss Ephemeris
    swe.set_ephe_path('')
    
    sunrise_jd = None
    sunset_jd = None
    
    # Search every 10 minutes from midnight to midnight UTC
    for minute in range(0, 24 * 60, 10):  # Every 10 minutes
        hour_utc = minute / 60.0
        jd = swe.julday(year, month, day, hour_utc)
        
        # Get sun position in ecliptic coordinates
        sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        if not sun_result:
            continue
            
        sun_lon = sun_result[0][0]  # Ecliptic longitude
        sun_lat = sun_result[0][1]  # Ecliptic latitude
        
        # Convert ecliptic to equatorial coordinates
        obliquity = swe.calc_ut(jd, swe.ECL_NUT, 0)[0][0]  # Obliquity of ecliptic
        ra, dec = ecliptic_to_equatorial(sun_lon, sun_lat, obliquity)
        
        # Calculate altitude
        altitude = calculate_sun_altitude(jd, ra, dec, latitude, longitude)
        
        # Check for sunrise
        if altitude > -0.833 and sunrise_jd is None:
            sunrise_jd = jd
            ist_time = (hour_utc + 5.5) % 24
            print(f"Sunrise found at {hour_utc:05.2f} UTC ({ist_time:05.2f} IST): altitude = {altitude:.2f}°")
        
        # Check for sunset (after 6 hours UTC)
        if altitude < -0.833 and hour_utc > 6 and sunset_jd is None:
            sunset_jd = jd
            ist_time = (hour_utc + 5.5) % 24
            print(f"Sunset found at {hour_utc:05.2f} UTC ({ist_time:05.2f} IST): altitude = {altitude:.2f}°")
            break
    
    # Format results
    sunrise_time = format_ist_time(sunrise_jd) if sunrise_jd else "No Rise"
    sunset_time = format_ist_time(sunset_jd) if sunset_jd else "No Set"
    
    return sunrise_time, sunset_time

def ecliptic_to_equatorial(lon, lat, obliquity):
    """
    Convert ecliptic coordinates to equatorial coordinates
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

def calculate_sun_altitude(jd, ra, dec, latitude, longitude):
    """Calculate sun altitude above horizon"""
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

def format_ist_time(jd):
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
    sunrise, sunset = calculate_sunrise_sunset_working(2025, 1, 5, 12.9716, 77.5946)
    print(f"\nCalculated Results:")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
    print(f"\nExpected (timeanddate.com):")
    print(f"Sunrise: 6:43 AM")
    print(f"Sunset: 6:07 PM")