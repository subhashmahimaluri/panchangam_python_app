#!/usr/bin/env python3

"""
Test the actual drik-panchanga implementation
"""

import sys
import os

# Add the drik-panchanga directory to the path
sys.path.append('/Users/macbook/projects/panchangam_python_app/backend/drik-panchanga')

# Try to import and use the panchanga module
try:
    import panchanga
    from collections import namedtuple
    
    Place = namedtuple('Location', ['latitude', 'longitude', 'timezone'])
    Date = namedtuple('Date', ['year', 'month', 'day'])
    
    def test_drik_panchanga():
        """Test the drik-panchanga implementation"""
        
        print("Testing drik-panchanga implementation...")
        
        # Bengaluru coordinates and IST timezone
        place = Place(12.9716, 77.5946, 5.5)
        
        # October 5, 2025
        date = Date(2025, 10, 5)
        
        # Convert to Julian Day
        jd = panchanga.gregorian_to_jd(date)
        print(f"Julian Day: {jd}")
        
        # Test sunrise calculation
        try:
            sunrise_result = panchanga.sunrise(jd, place)
            print(f"Sunrise result: {sunrise_result}")
            
            # Format the result
            if len(sunrise_result) >= 2:
                time_dms = sunrise_result[1]  # Should be [hours, minutes, seconds]
                if len(time_dms) >= 2:
                    hours = time_dms[0]
                    minutes = time_dms[1]
                    
                    # Convert to 12-hour format
                    if hours == 0:
                        sunrise_str = f"12:{minutes:02d} AM"
                    elif hours < 12:
                        sunrise_str = f"{hours}:{minutes:02d} AM"
                    elif hours == 12:
                        sunrise_str = f"12:{minutes:02d} PM"
                    else:
                        sunrise_str = f"{hours-12}:{minutes:02d} PM"
                    
                    print(f"Sunrise: {sunrise_str}")
                
        except Exception as e:
            print(f"Sunrise error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test sunset calculation
        try:
            sunset_result = panchanga.sunset(jd, place)
            print(f"Sunset result: {sunset_result}")
            
            # Format the result
            if len(sunset_result) >= 2:
                time_dms = sunset_result[1]  # Should be [hours, minutes, seconds]
                if len(time_dms) >= 2:
                    hours = time_dms[0]
                    minutes = time_dms[1]
                    
                    # Convert to 12-hour format
                    if hours == 0:
                        sunset_str = f"12:{minutes:02d} AM"
                    elif hours < 12:
                        sunset_str = f"{hours}:{minutes:02d} AM"
                    elif hours == 12:
                        sunset_str = f"12:{minutes:02d} PM"
                    else:
                        sunset_str = f"{hours-12}:{minutes:02d} PM"
                    
                    print(f"Sunset: {sunset_str}")
                
        except Exception as e:
            print(f"Sunset error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test moonrise calculation
        try:
            moonrise_result = panchanga.moonrise(jd, place)
            print(f"Moonrise result: {moonrise_result}")
            
            # Format the result
            if len(moonrise_result) >= 2:
                hours = moonrise_result[0]
                minutes = moonrise_result[1]
                
                # Convert to 12-hour format
                if hours == 0:
                    moonrise_str = f"12:{minutes:02d} AM"
                elif hours < 12:
                    moonrise_str = f"{hours}:{minutes:02d} AM"
                elif hours == 12:
                    moonrise_str = f"12:{minutes:02d} PM"
                else:
                    moonrise_str = f"{hours-12}:{minutes:02d} PM"
                
                print(f"Moonrise: {moonrise_str}")
                
        except Exception as e:
            print(f"Moonrise error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test moonset calculation
        try:
            moonset_result = panchanga.moonset(jd, place)
            print(f"Moonset result: {moonset_result}")
            
            # Format the result
            if len(moonset_result) >= 2:
                hours = moonset_result[0]
                minutes = moonset_result[1]
                
                # Check if next day
                if hours >= 24:
                    hours -= 24
                    day_suffix = " (+1)"
                else:
                    day_suffix = ""
                
                # Convert to 12-hour format
                if hours == 0:
                    moonset_str = f"12:{minutes:02d} AM{day_suffix}"
                elif hours < 12:
                    moonset_str = f"{hours}:{minutes:02d} AM{day_suffix}"
                elif hours == 12:
                    moonset_str = f"12:{minutes:02d} PM{day_suffix}"
                else:
                    moonset_str = f"{hours-12}:{minutes:02d} PM{day_suffix}"
                
                print(f"Moonset: {moonset_str}")
                
        except Exception as e:
            print(f"Moonset error: {e}")
            import traceback
            traceback.print_exc()
    
    if __name__ == "__main__":
        test_drik_panchanga()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Could not import panchanga module")
except Exception as e:
    print(f"General error: {e}")
    import traceback
    traceback.print_exc()