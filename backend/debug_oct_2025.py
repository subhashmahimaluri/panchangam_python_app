#!/usr/bin/env python3
"""
Debug calculations for October 5, 2025, in Bengaluru
"""
import sys
sys.path.append('/Users/macbook/projects/panchangam_python_app/backend')

from app.services.astronomical import calculate_sunrise_sunset, calculate_moonrise_moonset
from datetime import datetime

# Test for October 5, 2025, Bengaluru
date = datetime(2025, 10, 5)
lat = 12.9716
lon = 77.5946
city = "Bengaluru"

print("=== Testing October 5, 2025, Bengaluru ===")
print(f"Coordinates: Lat {lat}, Lon {lon}")
print()

print("--- Sun Calculations ---")
sunrise, sunset = calculate_sunrise_sunset(date, lat, lon, city)
print(f"Our Results:")
print(f"  Sunrise: {sunrise}")
print(f"  Sunset: {sunset}")
print()

print("Expected (DrikPanchang):")
print(f"  Sunrise: 06:16 AM")
print(f"  Sunset: 06:02 PM")
print()

print("--- Moon Calculations ---")
moonrise, moonset = calculate_moonrise_moonset(date, lat, lon, city)
print(f"Our Results:")
print(f"  Moonrise: {moonrise}")
print(f"  Moonset: {moonset}")
print()

print("Expected (DrikPanchang):")
print(f"  Moonrise: 04:54 PM, Oct 05")
print(f"  Moonset: 05:08 AM, Oct 06")