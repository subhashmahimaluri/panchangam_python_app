#!/usr/bin/env python3
"""
Debug script to understand the karana calculation discrepancy
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
import swisseph as swe
from app.utils.timezone import get_julian_day_ut
from app.services.hindu_calendar import lunar_phase
from app.utils.constants import KARANA_NAMES
from math import ceil

def debug_karana_calculation():
    """Debug the karana calculation differences"""
    
    print("🔍 Debugging Karana Calculation for October 5, 2025")
    print("=" * 60)
    
    # Convert date to Julian Day
    date_obj = datetime.fromisoformat("2025-10-05")
    jd = get_julian_day_ut(date_obj)
    
    print(f"Base JD: {jd:.6f}")
    
    # Test different times of day
    test_times = [
        ("Sunrise (6:00 AM)", 6.0/24.0),
        ("Mid-morning (9:00 AM)", 9.0/24.0), 
        ("Noon (12:00 PM)", 12.0/24.0),
        ("Afternoon (3:00 PM)", 15.0/24.0),
        ("Evening (6:00 PM)", 18.0/24.0),
        ("Night (9:00 PM)", 21.0/24.0)
    ]
    
    # Test for Bengaluru timezone (UTC+5.5)
    print(f"\\n🏙️ Bengaluru (UTC+5.5):")
    print("-" * 30)
    for time_name, time_offset in test_times:
        test_jd = jd + time_offset - 5.5/24.0  # Convert to UTC
        moon_phase_val = lunar_phase(test_jd)
        karana_num = ceil(moon_phase_val / 6)
        
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
        
        print(f"{time_name:20} | Moon Phase: {moon_phase_val:6.2f}° | Karana: {karana_num:2d} ({KARANA_NAMES[karana_index]})")
    
    # Test for Coventry timezone (UTC+1)
    print(f"\\n🏙️ Coventry (UTC+1):")
    print("-" * 30)
    for time_name, time_offset in test_times:
        test_jd = jd + time_offset - 1.0/24.0  # Convert to UTC
        moon_phase_val = lunar_phase(test_jd)
        karana_num = ceil(moon_phase_val / 6)
        
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
        
        print(f"{time_name:20} | Moon Phase: {moon_phase_val:6.2f}° | Karana: {karana_num:2d} ({KARANA_NAMES[karana_index]})")

if __name__ == "__main__":
    debug_karana_calculation()