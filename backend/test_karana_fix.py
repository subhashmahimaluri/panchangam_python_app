#!/usr/bin/env python3
"""
Test script to verify the fixed Karana calculation accuracy
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
import swisseph as swe
from app.utils.timezone import get_julian_day_ut
from app.services.hindu_calendar import calculate_karana

def test_karana_accuracy():
    """Test Karana calculation for the problematic dates"""
    
    print("🔬 Testing Fixed Karana Calculation Accuracy")
    print("=" * 60)
    
    # Test cases based on user feedback
    test_cases = [
        {
            "date": "2025-10-05",
            "city": "Bengaluru",
            "expected_karana": "Garija",
            "expected_timing": "Oct 05 03:04 PM – Oct 06 01:48 AM"
        },
        {
            "date": "2025-10-05", 
            "city": "Coventry",
            "expected_karana": "Garija",
            "expected_timing": "Oct 05 10:34 AM – Oct 05 09:18 PM"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {case['city']} - {case['date']}")
        print("-" * 40)
        
        try:
            # Convert date to Julian Day
            date_obj = datetime.fromisoformat(case["date"])
            jd = get_julian_day_ut(date_obj)
            
            # Calculate our Karana
            our_karana = calculate_karana(jd, case["city"])
            
            print(f"🔹 Our App Result:")
            print(f"   Karana: {our_karana['name']}")
            print(f"   Timing: {our_karana['start']} to {our_karana['end']}")
            
            print(f"\n🔹 Expected (Reference):")
            print(f"   Karana: {case['expected_karana']}")
            print(f"   Timing: {case['expected_timing']}")
            
            # Check accuracy
            name_match = our_karana['name'] == case['expected_karana']
            print(f"\n✅ Name Accuracy: {'EXACT MATCH' if name_match else 'MISMATCH'}")
            
            if not name_match:
                print(f"❌ Expected: {case['expected_karana']}, Got: {our_karana['name']}")
            
        except Exception as e:
            print(f"❌ Error in test case {i}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_karana_accuracy()