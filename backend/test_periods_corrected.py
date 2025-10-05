#!/usr/bin/env python3
"""
Test the corrected periods calculation
"""
import requests
import json
from datetime import datetime

def test_corrected_periods():
    """Test the corrected periods endpoint"""
    print("🔧 Testing corrected periods calculation...")
    
    # Test data
    test_date = "2025-10-05"
    latitude = 12.9719
    longitude = 77.593
    
    # API endpoint
    url = "http://127.0.0.1:8000/api/periods"
    
    # Request data
    data = {
        "date": test_date,
        "latitude": latitude,
        "longitude": longitude
    }
    
    try:
        # Make API call
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"✅ SUCCESS! Corrected periods calculation:")
        print(f"Date: {result['date']}")
        print(f"Hindu Day Window: {result.get('hindu_day_start', 'N/A')} to {result.get('hindu_day_end', 'N/A')}")
        
        print(f"\nTithis: {len(result['tithis'])} periods")
        for i, tithi in enumerate(result['tithis'], 1):
            print(f"  {i}. {tithi['name']} - {tithi['start_formatted']} to {tithi['end_formatted']}")
        
        print(f"\nNakshatras: {len(result['nakshatras'])} periods")
        for i, nakshatra in enumerate(result['nakshatras'], 1):
            print(f"  {i}. {nakshatra['name']} - {nakshatra['start_formatted']} to {nakshatra['end_formatted']}")
        
        print(f"\nKaranas: {len(result['karanas'])} periods")
        for i, karana in enumerate(result['karanas'], 1):
            start_date = datetime.fromisoformat(karana['start'].replace('Z', '').replace('+05:30', ''))
            end_date = datetime.fromisoformat(karana['end'].replace('Z', '').replace('+05:30', ''))
            duration = end_date - start_date
            print(f"  {i}. {karana['name']} - {karana['start_formatted']} to {karana['end_formatted']} (Duration: {duration})")
        
        print(f"\nYogas: {len(result['yogas'])} periods")
        for i, yoga in enumerate(result['yogas'], 1):
            print(f"  {i}. {yoga['name']} - {yoga['start_formatted']} to {yoga['end_formatted']}")
        
        print(f"\nAuspicious Periods: {len(result.get('auspicious_periods', []))} periods")
        for i, period in enumerate(result.get('auspicious_periods', []), 1):
            print(f"  {i}. {period['name']} - {period['start_formatted']} to {period['end_formatted']}")
        
        print(f"\nInauspicious Periods: {len(result.get('inauspicious_periods', []))} periods")
        for i, period in enumerate(result.get('inauspicious_periods', []), 1):
            print(f"  {i}. {period['name']} - {period['start_formatted']} to {period['end_formatted']}")
        
        # Check for overlaps with Hindu day
        hindu_start = datetime.fromisoformat(result['hindu_day_start'])
        hindu_end = datetime.fromisoformat(result['hindu_day_end'])
        
        print(f"\n🔍 Hindu Day Overlap Analysis:")
        print(f"Hindu Day: {hindu_start} to {hindu_end}")
        
        print("\nTithis overlap check:")
        for tithi in result['tithis']:
            start = datetime.fromisoformat(tithi['start'].replace('Z', '').replace('+05:30', ''))
            end = datetime.fromisoformat(tithi['end'].replace('Z', '').replace('+05:30', ''))
            overlaps = start < hindu_end and end > hindu_start
            print(f"  {tithi['name']}: {start} to {end} -> {'✅ OVERLAPS' if overlaps else '❌ NO OVERLAP'}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_corrected_periods()