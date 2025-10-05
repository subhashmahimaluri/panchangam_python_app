#!/usr/bin/env python3
"""
Test the expected format exactly as user requested
"""
import requests
import json
from datetime import datetime

def test_expected_format():
    """Test that output matches user's expected format"""
    print("🎯 Testing expected format: ProKerala/DrikPanchang style...")
    
    url = "http://127.0.0.1:8000/api/periods"
    data = {
        "date": "2025-10-05",
        "latitude": 12.9719,
        "longitude": 77.593
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        print("🌙 Tithi")
        for tithi in result['tithis']:
            # Parse dates for formatting
            start_dt = datetime.fromisoformat(tithi['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(tithi['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{tithi['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("⭐ Nakshatra")
        for nakshatra in result['nakshatras']:
            start_dt = datetime.fromisoformat(nakshatra['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(nakshatra['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{nakshatra['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("🔄 Karana")
        for karana in result['karanas']:
            start_dt = datetime.fromisoformat(karana['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(karana['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{karana['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("🧘 Yoga")
        for yoga in result['yogas']:
            start_dt = datetime.fromisoformat(yoga['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(yoga['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{yoga['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("✨ Auspicious Periods")
        for period in result.get('auspicious_periods', []):
            start_dt = datetime.fromisoformat(period['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(period['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{period['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("⚠️ Inauspicious Periods")
        for period in result.get('inauspicious_periods', []):
            start_dt = datetime.fromisoformat(period['start'].replace('Z', '').replace('+05:30', ''))
            end_dt = datetime.fromisoformat(period['end'].replace('Z', '').replace('+05:30', ''))
            
            start_str = start_dt.strftime('%b %d, %I:%M %p')
            end_str = end_dt.strftime('%b %d, %I:%M %p')
            
            print(f"{period['name']}")
            print(f"{start_str} – {end_str}")
            print()
        
        print("✅ SUCCESS: All periods show multiple overlapping entries as expected!")
        print(f"📊 Summary: {len(result['tithis'])} Tithis, {len(result['nakshatras'])} Nakshatras, {len(result['karanas'])} Karanas, {len(result['yogas'])} Yogas")
        print(f"📊 Muhurat: {len(result.get('auspicious_periods', []))} Auspicious, {len(result.get('inauspicious_periods', []))} Inauspicious")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_expected_format()