#!/usr/bin/env python3
"""
Test the complete periods with sun and moon times
"""
import requests
import json
from datetime import datetime

def test_complete_periods():
    """Test the complete periods endpoint with sun and moon times"""
    print("🌞🌙 Testing complete periods with Sun and Moon times...")
    
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
        
        def format_time_nice(iso_str):
            """Format ISO time to nice display"""
            try:
                dt = datetime.fromisoformat(iso_str.replace('Z', '').replace('+05:30', ''))
                return dt.strftime('%b %d, %I:%M %p')
            except:
                return iso_str
        
        print("📅 Date & Location Info:")
        print(f"Date: {result['date']}")
        print(f"Location: {result['location']['latitude']}°, {result['location']['longitude']}°")
        print()
        
        print("🌞 Sun & Moon Times:")
        print(f"☀️  Sunrise: {format_time_nice(result['sunrise'])}")
        print(f"🌅 Sunset:  {format_time_nice(result['sunset'])}")
        print(f"🌙 Moonrise: {format_time_nice(result['moonrise'])}")
        print(f"🌛 Moonset:  {format_time_nice(result['moonset'])}")
        print()
        
        print("🕐 Hindu Day Window:")
        print(f"Start: {format_time_nice(result['sunrise'])}")
        print(f"End:   {format_time_nice(result['sunrise_next'])}")
        print()
        
        print("🌙 Tithis:")
        for i, tithi in enumerate(result['tithis'], 1):
            print(f"  {i}. {tithi['name']}")
            print(f"     {format_time_nice(tithi['start'])} – {format_time_nice(tithi['end'])}")
        print()
        
        print("⭐ Nakshatras:")
        for i, nakshatra in enumerate(result['nakshatras'], 1):
            print(f"  {i}. {nakshatra['name']}")
            print(f"     {format_time_nice(nakshatra['start'])} – {format_time_nice(nakshatra['end'])}")
        print()
        
        print("🔄 Karanas:")
        for i, karana in enumerate(result['karanas'], 1):
            print(f"  {i}. {karana['name']}")
            print(f"     {format_time_nice(karana['start'])} – {format_time_nice(karana['end'])}")
        print()
        
        print("🧘 Yogas:")
        for i, yoga in enumerate(result['yogas'], 1):
            print(f"  {i}. {yoga['name']}")
            print(f"     {format_time_nice(yoga['start'])} – {format_time_nice(yoga['end'])}")
        print()
        
        print("✨ Auspicious Periods:")
        for i, period in enumerate(result.get('auspicious_periods', []), 1):
            print(f"  {i}. {period['name']}")
            print(f"     {format_time_nice(period['start'])} – {format_time_nice(period['end'])}")
        print()
        
        print("⚠️ Inauspicious Periods:")
        for i, period in enumerate(result.get('inauspicious_periods', []), 1):
            print(f"  {i}. {period['name']}")
            print(f"     {format_time_nice(period['start'])} – {format_time_nice(period['end'])}")
        print()
        
        print("✅ SUCCESS: Complete periods with Sun & Moon times working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_complete_periods()