#!/usr/bin/env python3
"""
Test script to verify the accuracy of improved Panchangam calculations
Compare results with DrikPanchang reference implementation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
from app.services.hindu_calendar import (
    calculate_tithi, calculate_nakshatra, calculate_karana, calculate_yoga
)
from app.utils.timezone import get_julian_day_ut, local_to_utc

def test_panchangam_calculations():
    """Test Panchangam calculations for specific dates"""
    
    # Test cases - dates with known Panchangam data
    test_cases = [
        {
            "date": "2025-10-05",
            "city": "Bengaluru",
            "description": "October 5, 2025 - Bengaluru (Current test date)"
        },
        {
            "date": "2025-01-15",
            "city": "New York", 
            "description": "January 15, 2025 - New York (Winter)"
        },
        {
            "date": "2025-06-21",
            "city": "Canberra",
            "description": "June 21, 2025 - Canberra (Summer Solstice)"
        }
    ]
    
    print("=" * 80)
    print("IMPROVED PANCHANGAM CALCULATIONS TEST")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        date_str = test_case["date"]
        city = test_case["city"]
        description = test_case["description"]
        
        print(f"\nTest Case {i}: {description}")
        print("-" * 60)
        
        try:
            # Parse date and get Julian Day
            calc_date = datetime.fromisoformat(date_str)
            utc_date = local_to_utc(calc_date, city)
            jd = get_julian_day_ut(utc_date)
            
            print(f"Date: {date_str}")
            print(f"City: {city}")
            print(f"Julian Day: {jd:.6f}")
            print()
            
            # Calculate Panchangam elements
            print("PANCHANGAM CALCULATIONS:")
            print("-" * 30)
            
            # Tithi
            tithi_data = calculate_tithi(jd, city)
            print(f"Tithi: {tithi_data['name']}")
            print(f"  Start: {tithi_data['start']}")
            print(f"  End:   {tithi_data['end']}")
            print()
            
            # Nakshatra
            nakshatra_data = calculate_nakshatra(jd, city)
            print(f"Nakshatra: {nakshatra_data['name']}")
            print(f"  Start: {nakshatra_data['start']}")
            print(f"  End:   {nakshatra_data['end']}")
            print()
            
            # Karana
            karana_data = calculate_karana(jd, city)
            print(f"Karana: {karana_data['name']}")
            print(f"  Start: {karana_data['start']}")
            print(f"  End:   {karana_data['end']}")
            print()
            
            # Yoga
            yoga_data = calculate_yoga(jd, city)
            print(f"Yoga: {yoga_data['name']}")
            print(f"  Start: {yoga_data['start']}")
            print(f"  End:   {yoga_data['end']}")
            print()
            
        except Exception as e:
            print(f"ERROR in test case {i}: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    print()
    print("VERIFICATION INSTRUCTIONS:")
    print("1. Compare the above results with DrikPanchang.com")
    print("2. Check https://www.drikpanchang.com/panchang/")
    print("3. Select the corresponding date and city")
    print("4. Verify Tithi, Nakshatra, Karana, and Yoga values")
    print("5. Times should match within 5-10 minutes for good accuracy")

if __name__ == "__main__":
    test_panchangam_calculations()