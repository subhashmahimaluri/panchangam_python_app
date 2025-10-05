#!/usr/bin/env python3
"""
Direct test of DrikPanchanga karana calculation for debugging
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'drik-panchanga'))

from datetime import datetime
import swisseph as swe
from panchanga import *

def test_drik_karana():
    """Test the DrikPanchanga karana calculation directly"""
    
    print("🔍 Testing DrikPanchanga Karana Calculation")
    print("=" * 50)
    
    # Set up test cases
    bangalore = Place(12.972, 77.594, +5.5)
    coventry = Place(52.40656, -1.51217, +1.0)  # Coventry coordinates and timezone
    
    # October 5, 2025
    test_date = gregorian_to_jd(Date(2025, 10, 5))
    
    print(f"\\n📅 Date: October 5, 2025 (JD: {test_date:.6f})")
    
    # Test Bengaluru
    print(f"\\n🏙️ Bengaluru:")
    bng_karana = karana(test_date, bangalore)
    print(f"   DrikPanchanga result: {bng_karana}")
    
    # Test Coventry  
    print(f"\\n🏙️ Coventry:")
    cov_karana = karana(test_date, coventry)
    print(f"   DrikPanchanga result: {cov_karana}")
    
    # Also test the sunrise and lunar phase
    print(f"\\n🌅 Bengaluru Sunrise:")
    bng_sunrise = sunrise(test_date, bangalore)
    print(f"   Sunrise JD: {bng_sunrise[0]:.6f}")
    print(f"   Sunrise local time: {bng_sunrise[1]}")
    
    print(f"\\n🌙 Lunar Phase at Bengaluru sunrise:")
    moon_phase_bng = lunar_phase(bng_sunrise[0] - 5.5/24)  # Convert to UTC
    print(f"   Moon phase: {moon_phase_bng:.6f} degrees")
    karana_num = ceil(moon_phase_bng / 6)
    print(f"   Karana number: {karana_num}")

if __name__ == "__main__":
    test_drik_karana()