#!/usr/bin/env python3
"""
Comprehensive karana boundary analysis to understand expected timing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime, timedelta
import swisseph as swe
from app.utils.timezone import get_julian_day_ut
from app.services.hindu_calendar import lunar_phase, solar_longitude, lunar_longitude
from app.utils.constants import KARANA_NAMES
from math import ceil

def analyze_karana_boundaries():
    """Analyze karana boundaries around expected times"""
    
    print("🔍 Comprehensive Karana Boundary Analysis")
    print("=" * 60)
    
    # Expected transition times from user feedback:
    # Bengaluru: Garija from Oct 05 03:04 PM – Oct 06 01:48 AM
    # Coventry: Garija from Oct 05 10:34 AM – Oct 05 09:18 PM
    
    transitions = [
        {
            "location": "Bengaluru", 
            "tz_offset": 5.5,
            "expected_start": "2025-10-05T15:04:00",  # 3:04 PM
            "expected_end": "2025-10-06T01:48:00"     # 1:48 AM next day
        },
        {
            "location": "Coventry",
            "tz_offset": 1.0, 
            "expected_start": "2025-10-05T10:34:00",  # 10:34 AM
            "expected_end": "2025-10-05T21:18:00"     # 9:18 PM
        }
    ]
    
    for trans in transitions:
        print(f"\n🏙️ {trans['location']} Analysis:")
        print("-" * 40)
        
        # Check karana 30 minutes before, at, and after expected start/end times
        for time_key in ['expected_start', 'expected_end']:
            base_time = datetime.fromisoformat(trans[time_key])
            print(f"\n  Around {time_key} ({base_time.strftime('%m/%d %H:%M')}):")
            
            for offset_minutes in [-30, 0, +30]:
                test_time = base_time + timedelta(minutes=offset_minutes)
                test_jd = get_julian_day_ut(test_time) - trans['tz_offset']/24.0  # Convert to UTC
                
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
                
                marker = "<-- TARGET" if offset_minutes == 0 else ""
                print(f"    {test_time.strftime('%m/%d %H:%M')} | Moon: {moon_phase:6.2f}° | K{karana_num:2d} ({KARANA_NAMES[karana_index]}) {marker}")

if __name__ == "__main__":
    analyze_karana_boundaries()