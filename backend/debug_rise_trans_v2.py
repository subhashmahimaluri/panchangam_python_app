#!/usr/bin/env python3

"""
Test different approaches to the rise_trans function
"""

import swisseph as swe

def test_different_approaches():
    """Test different parameter combinations for rise_trans"""
    
    print("Testing different approaches to rise_trans...")
    
    # Bengaluru coordinates
    lat = 12.9716
    lon = 77.5946
    
    # October 5, 2025
    jd = swe.julday(2025, 10, 5, 0.0)
    
    print(f"Julian Day: {jd}")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    
    # Test 1: Basic rise_trans without rsmi parameter
    try:
        print("\\nTest 1: Basic rise_trans for sunrise...")
        result = swe.rise_trans(jd, swe.SUN, lon, lat)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Using integer flags
    try:
        print("\\nTest 2: Using integer flags...")
        flag = int(swe.BIT_DISC_CENTER) + int(swe.CALC_RISE)
        result = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=flag)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Check what the constants actually are
    print("\\nTest 3: Checking Swiss Ephemeris constants...")
    try:
        print(f"swe.SUN: {swe.SUN}")
        print(f"swe.MOON: {swe.MOON}")
        print(f"swe.BIT_DISC_CENTER: {swe.BIT_DISC_CENTER}")
        print(f"swe.CALC_RISE: {swe.CALC_RISE}")
        print(f"swe.CALC_SET: {swe.CALC_SET}")
    except Exception as e:
        print(f"Error checking constants: {e}")
    
    # Test 4: Try different parameter order
    try:
        print("\\nTest 4: Different parameter order...")
        result = swe.rise_trans(jd, 0, lon, lat, rsmi=1)  # 0 = Sun, 1 = rise
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Try with altitude parameter
    try:
        print("\\nTest 5: With altitude parameter...")
        result = swe.rise_trans(jd, 0, lon, lat, rsmi=1, horhgt=0.0, atpress=1013.25, attemp=15.0)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_different_approaches()