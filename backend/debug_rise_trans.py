#!/usr/bin/env python3

"""
Debug the Swiss Ephemeris rise_trans function to understand the exact parameters needed
"""

import swisseph as swe

# Test the exact function signature used in drik-panchanga
def test_rise_trans_parameters():
    """Test the rise_trans function with proper parameters"""
    
    print("Testing Swiss Ephemeris rise_trans function...")
    
    # Bengaluru coordinates
    lat = 12.9716
    lon = 77.5946
    
    # October 5, 2025
    jd = swe.julday(2025, 10, 5, 0.0)
    tz_offset = 5.5
    
    print(f"Julian Day: {jd}")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    print(f"Timezone offset: {tz_offset}")
    
    try:
        # Test the exact call from drik-panchanga
        print("\nTesting sunrise calculation...")
        result = swe.rise_trans(jd - tz_offset/24, swe.SUN, lon, lat, rsmi=swe.BIT_DISC_CENTER + swe.CALC_RISE)
        print(f"Sunrise result: {result}")
        
        if result[0] == swe.OK:
            rise_jd = result[1][0]
            print(f"Sunrise JD: {rise_jd}")
            # Convert to local time
            local_jd = rise_jd + tz_offset/24
            print(f"Local JD: {local_jd}")
            
            # Convert to calendar date
            cal_date = swe.revjul(local_jd)
            print(f"Calendar date: {cal_date}")
        else:
            print(f"Error code: {result[0]}")
            
    except Exception as e:
        print(f"Error in sunrise calculation: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        print("\nTesting sunset calculation...")
        result = swe.rise_trans(jd - tz_offset/24, swe.SUN, lon, lat, rsmi=swe.BIT_DISC_CENTER + swe.CALC_SET)
        print(f"Sunset result: {result}")
        
        if result[0] == swe.OK:
            set_jd = result[1][0]
            print(f"Sunset JD: {set_jd}")
            # Convert to local time
            local_jd = set_jd + tz_offset/24
            print(f"Local JD: {local_jd}")
            
            # Convert to calendar date
            cal_date = swe.revjul(local_jd)
            print(f"Calendar date: {cal_date}")
        else:
            print(f"Error code: {result[0]}")
            
    except Exception as e:
        print(f"Error in sunset calculation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rise_trans_parameters()