#!/usr/bin/env python3
"""
Direct test to determine which Garija period should be shown
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
import swisseph as swe
from app.utils.timezone import get_julian_day_ut
from app.services.hindu_calendar import lunar_phase, solar_longitude, lunar_longitude
from app.utils.constants import KARANA_NAMES
from math import ceil

def test_karana_periods():
    """Test which karana periods are active throughout October 5, 2025"""
    
    print("🔍 Karana Periods Throughout October 5, 2025")
    print("=" * 60)
    
    # Convert date to Julian Day
    date_obj = datetime.fromisoformat("2025-10-05")
    jd = get_julian_day_ut(date_obj)
    
    # Test every 3 hours throughout the day for both locations
    test_times = []
    for hour in range(0, 24, 3):
        test_times.append((f"{hour:02d}:00", hour/24.0))
    
    print(f"\\n🏙️ Bengaluru (UTC+5.5) - Karana at different times:")
    print("-" * 50)
    for time_str, time_offset in test_times:
        test_jd = jd + time_offset - 5.5/24.0  # Convert to UTC
        
        solar_long = solar_longitude(test_jd)
        lunar_long = lunar_longitude(test_jd)
        moon_phase = (lunar_long - solar_long) % 360
        karana_num = ceil(moon_phase / 6)
        
        if karana_num > 60:
            karana_num = karana_num % 60
        if karana_num == 0:
            karana_num = 60
            
        # Map to name
        if karana_num <= 56:
            karana_index = (karana_num - 1) % 7
        else:
            karana_index = 7 + (karana_num - 57)
        karana_index = min(karana_index, len(KARANA_NAMES) - 1)
        
        print(f"{time_str} | Moon Phase: {moon_phase:6.2f}° | Karana: {karana_num:2d} ({KARANA_NAMES[karana_index]})")
    
    print(f"\\n🏙️ Coventry (UTC+1) - Karana at different times:")
    print("-" * 50)
    for time_str, time_offset in test_times:
        test_jd = jd + time_offset - 1.0/24.0  # Convert to UTC
        
        solar_long = solar_longitude(test_jd)
        lunar_long = lunar_longitude(test_jd)
        moon_phase = (lunar_long - solar_long) % 360
        karana_num = ceil(moon_phase / 6)
        
        if karana_num > 60:
            karana_num = karana_num % 60
        if karana_num == 0:
            karana_num = 60
            
        # Map to name
        if karana_num <= 56:
            karana_index = (karana_num - 1) % 7
        else:
            karana_index = 7 + (karana_num - 57)
        karana_index = min(karana_index, len(KARANA_NAMES) - 1)
        
        print(f"{time_str} | Moon Phase: {moon_phase:6.2f}° | Karana: {karana_num:2d} ({KARANA_NAMES[karana_index]})")

if __name__ == "__main__":
    test_karana_periods()