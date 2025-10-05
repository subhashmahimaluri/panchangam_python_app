#!/usr/bin/env python3
"""
Debug coordinate system and calculations
"""
import swisseph as swe
import math

def debug_sun_positions():
    """Debug sun positions around expected sunrise time"""
    print("=== Debugging Sun Positions ===")
    
    # Initialize Swiss Ephemeris
    swe.set_ephe_path('')
    
    # Bengaluru coordinates
    lat = 12.9716
    lon = 77.5946
    
    # January 5, 2025
    year, month, day = 2025, 1, 5
    
    # Expected sunrise: 6:43 AM IST = 1:13 AM UTC
    # Let's check times around 1:13 UTC
    
    print(f"Location: Bengaluru (Lat: {lat}, Lon: {lon})")
    print(f"Date: {year}-{month:02d}-{day:02d}")
    print()
    
    # Check altitudes from midnight to 6 AM UTC
    for hour_utc in [0, 1, 1.2, 1.4, 2, 3, 4, 5, 6]:
        jd = swe.julday(year, month, day, hour_utc)
        
        # Get sun position
        sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        if not sun_result:
            continue
            
        # Extract position data correctly
        sun_lon = sun_result[0][0]  # Longitude
        ra = sun_result[0][5]       # Right ascension 
        dec = sun_result[0][1]      # Declination
        
        # Debug: print raw results
        print(f"  Raw result: {sun_result[0][:6]}")
        
        # Calculate altitude
        altitude = calculate_sun_altitude(jd, ra, dec, lat, lon)
        
        # Convert to IST for display
        ist_hour = hour_utc + 5.5
        if ist_hour >= 24:
            ist_hour -= 24
            
        print(f"  {hour_utc:04.1f} UTC ({ist_hour:04.1f} IST): altitude = {altitude:7.2f}° (RA={ra:6.1f}°, Dec={dec:5.1f}°)")
        
        if -1 < altitude < 1:  # Near horizon
            print(f"    *** NEAR HORIZON ***")

def calculate_sun_altitude(jd, ra, dec, latitude, longitude):
    """Calculate sun altitude above horizon"""
    # Greenwich Mean Sidereal Time
    gmst = swe.sidtime(jd) * 15  # Convert hours to degrees
    
    # Local sidereal time
    lst = gmst + longitude
    
    # Hour angle
    hour_angle = lst - ra
    
    # Normalize hour angle to [-180, 180]
    while hour_angle > 180:
        hour_angle -= 360
    while hour_angle < -180:
        hour_angle += 360
    
    print(f"    Debug: GMST={gmst:6.1f}°, LST={lst:6.1f}°, HA={hour_angle:6.1f}°")
    
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

if __name__ == "__main__":
    debug_sun_positions()