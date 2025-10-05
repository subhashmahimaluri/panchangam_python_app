#!/usr/bin/env python3

"""
Test the new drik-panchanga based implementation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
from app.services.astronomical import calculate_sunrise_sunset, calculate_moonrise_moonset

def test_bengaluru_oct_5_2025():
    """Test Bengaluru calculations for October 5, 2025"""
    
    # Bengaluru coordinates
    latitude = 12.9716
    longitude = 77.5946
    city = "Bengaluru"
    
    # Date: October 5, 2025
    test_date = datetime(2025, 10, 5)
    
    print(f"Testing calculations for {test_date.strftime('%B %d, %Y')} in {city}")
    print(f"Coordinates: {latitude}°N, {longitude}°E")
    print("=" * 60)
    
    # Calculate sunrise and sunset
    sunrise, sunset = calculate_sunrise_sunset(test_date, latitude, longitude, city)
    print(f"Sunrise: {sunrise}")
    print(f"Sunset:  {sunset}")
    
    # Calculate moonrise and moonset
    moonrise, moonset = calculate_moonrise_moonset(test_date, latitude, longitude, city)
    print(f"Moonrise: {moonrise}")
    print(f"Moonset:  {moonset}")
    
    print("\n" + "=" * 60)
    print("COMPARISON WITH AUTHORITATIVE SOURCES:")
    print("DrikPanchang.com:")
    print("  Sunrise:  06:16 AM")
    print("  Sunset:   06:02 PM") 
    print("  Moonrise: 04:54 PM")
    print("  Moonset:  05:08 AM, Oct 06")
    
    print("\nProKerala.com:")
    print("  Sunrise:  06:12 AM")
    print("  Sunset:   06:03 PM")
    print("  Moonrise: 04:47 PM")
    print("  Moonset:  05:06 AM, Oct 06")

def test_coventry_oct_5_2025():
    """Test Coventry calculations for October 5, 2025"""
    
    # Coventry coordinates (UK)
    latitude = 52.4068
    longitude = -1.5197
    city = "Coventry"
    
    # Date: October 5, 2025
    test_date = datetime(2025, 10, 5)
    
    print(f"\n\nTesting calculations for {test_date.strftime('%B %d, %Y')} in {city}")
    print(f"Coordinates: {latitude}°N, {longitude}°W")
    print("=" * 60)
    
    # Calculate sunrise and sunset
    sunrise, sunset = calculate_sunrise_sunset(test_date, latitude, longitude, city)
    print(f"Sunrise: {sunrise}")
    print(f"Sunset:  {sunset}")
    
    # Calculate moonrise and moonset
    moonrise, moonset = calculate_moonrise_moonset(test_date, latitude, longitude, city)
    print(f"Moonrise: {moonrise}")
    print(f"Moonset:  {moonset}")

if __name__ == "__main__":
    test_bengaluru_oct_5_2025()
    test_coventry_oct_5_2025()