#!/usr/bin/env python3
"""
Test the new sunrise/sunset calculation directly
"""
import sys
sys.path.append('/Users/macbook/projects/panchangam_python_app/backend')

from app.services.astronomical import calculate_sunrise_sunset
from datetime import datetime

# Test for Bengaluru on January 5, 2025
date = datetime(2025, 1, 5)
lat = 12.9716
lon = 77.5946
city = "Bengaluru"

print("Testing new sunrise/sunset calculation...")
sunrise, sunset = calculate_sunrise_sunset(date, lat, lon, city)
print(f"Results: Sunrise = {sunrise}, Sunset = {sunset}")