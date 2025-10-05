#!/usr/bin/env python3
"""
Test Swiss Ephemeris calculations directly
"""
import swisseph as swe
import math
from datetime import datetime, timezone

# Initialize Swiss Ephemeris
swe.set_ephe_path('')

def test_basic_ephemeris():
    """Test basic Swiss Ephemeris functionality"""
    print("Testing Swiss Ephemeris...")
    
    # Test date: January 5, 2025
    date = datetime(2025, 1, 5, 12, 0, 0, tzinfo=timezone.utc)
    jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)
    print(f"Julian Day: {jd}")
    
    # Test Sun position calculation
    print("\n--- Sun Position Test ---")
    try:
        sun_result = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        print(f"Sun calculation result: {sun_result}")
        if sun_result:
            print(f"Sun longitude: {sun_result[0][0]:.6f}°")
            print(f"Sun latitude: {sun_result[0][1]:.6f}°")
            print(f"Sun distance: {sun_result[0][2]:.6f} AU")
    except Exception as e:
        print(f"Sun calculation error: {e}")
    
    # Test rise/transit/set calculations for Bengaluru
    lat = 12.9716
    lon = 77.5946
    
    print(f"\n--- Sunrise/Sunset Test for Bengaluru (Lat: {lat}, Lon: {lon}) ---")
    
    # Test simple rise_trans call
    try:
        print("Testing sunrise calculation...")
        sunrise = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER)
        print(f"Sunrise result: {sunrise}")
        
        if sunrise[0] == swe.OK:
            sunrise_jd = sunrise[1][0]
            sunrise_dt = swe.revjul(sunrise_jd)
            print(f"Sunrise JD: {sunrise_jd}")
            print(f"Sunrise date/time: {sunrise_dt}")
        else:
            print(f"Sunrise calculation failed with code: {sunrise[0]}")
            
    except Exception as e:
        print(f"Sunrise calculation error: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        print("\nTesting sunset calculation...")
        sunset = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=swe.CALC_SET | swe.BIT_DISC_CENTER)
        print(f"Sunset result: {sunset}")
        
        if sunset[0] == swe.OK:
            sunset_jd = sunset[1][0]
            sunset_dt = swe.revjul(sunset_jd)
            print(f"Sunset JD: {sunset_jd}")
            print(f"Sunset date/time: {sunset_dt}")
        else:
            print(f"Sunset calculation failed with code: {sunset[0]}")
            
    except Exception as e:
        print(f"Sunset calculation error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_approach():
    """Test with a simpler approach using known working methods"""
    print("\n=== Testing Simple Approach ===")
    
    # Use a very basic approach
    year, month, day = 2025, 1, 5
    hour = 6.0  # Start search at 6 AM local time
    
    lat = 12.9716
    lon = 77.5946
    
    # Convert to Julian Day
    jd = swe.julday(year, month, day, hour)
    print(f"Starting JD: {jd}")
    
    # Calculate sun positions at different times
    print("\nSun positions throughout the day:")
    for h in range(4, 20, 2):  # From 4 AM to 6 PM
        test_jd = swe.julday(year, month, day, h)
        
        try:
            sun_pos = swe.calc_ut(test_jd, swe.SUN, swe.FLG_SWIEPH)
            if sun_pos:
                ra = sun_pos[0][5]  # Right ascension 
                dec = sun_pos[0][1] # Declination
                
                # Calculate altitude
                gmst = swe.sidtime(test_jd) * 15  # Convert to degrees
                lst = gmst + lon
                hour_angle = lst - ra
                
                lat_rad = math.radians(lat)
                dec_rad = math.radians(dec)
                ha_rad = math.radians(hour_angle)
                
                sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
                          math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
                altitude = math.degrees(math.asin(sin_alt))
                
                print(f"  {h:02d}:00 - Altitude: {altitude:6.2f}°")
                
        except Exception as e:
            print(f"  {h:02d}:00 - Error: {e}")

if __name__ == "__main__":
    test_basic_ephemeris()
    test_simple_approach()