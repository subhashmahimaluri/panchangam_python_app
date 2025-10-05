#!/usr/bin/env python3
"""
Direct test for the periods endpoint to identify issues
"""
import sys
import os
sys.path.append('.')

import asyncio
from datetime import datetime
from app.routers.panchangam import calculate_panchangam_periods
from app.models.panchangam import PeriodRequest

async def test_periods_endpoint():
    """Test the periods endpoint directly"""
    print("Testing periods endpoint...")
    
    # Create test request
    request = PeriodRequest(
        date="2025-10-05",
        latitude=12.9719,
        longitude=77.593
    )
    
    try:
        # Call the endpoint function directly
        response = await calculate_panchangam_periods(request)
        
        print("SUCCESS!")
        print(f"Date: {response.date}")
        print(f"Location: {response.location}")
        print(f"Sunrise: {response.sunrise}")
        print(f"Tithis count: {len(response.tithis)}")
        print(f"Nakshatras count: {len(response.nakshatras)}")
        
        if response.tithis:
            print(f"Sample Tithi: {response.tithis[0].name}")
            print(f"  Start: {response.tithis[0].start}")
            print(f"  End: {response.tithis[0].end}")
            print(f"  Formatted: {response.tithis[0].start_formatted} - {response.tithis[0].end_formatted}")
            
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_periods_endpoint())
    if success:
        print("\n✅ Endpoint test PASSED")
    else:
        print("\n❌ Endpoint test FAILED")