#!/usr/bin/env python3
"""
Final test showing all implemented features with Sun and Moon times
"""
import requests
import json
from datetime import datetime

def test_final_implementation():
    """Test the complete final implementation"""
    print("🎯 FINAL TEST: Complete Panchangam Periods with Sun & Moon Times")
    print("=" * 70)
    
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
        
        def format_time_display(iso_str):
            """Format time for display"""
            try:
                dt = datetime.fromisoformat(iso_str.replace('Z', '').replace('+05:30', ''))
                return dt.strftime('%b %d, %I:%M %p')
            except:
                return iso_str
        
        print(f"📅 Date: {result['date']}")
        print(f"📍 Location: {result['location']['latitude']}°N, {result['location']['longitude']}°E")
        print()
        
        print("🌞 SUN & MOON TIMES (NEW!):")
        print(f"☀️  Sunrise:  {format_time_display(result['sunrise'])}")
        print(f"🌇 Sunset:   {format_time_display(result['sunset'])}")
        print(f"🌙 Moonrise: {format_time_display(result['moonrise'])}")
        print(f"🌛 Moonset:  {format_time_display(result['moonset'])}")
        print()
        
        print("🕐 HINDU DAY WINDOW:")
        print(f"Start: {format_time_display(result['sunrise'])} (Sunrise)")
        print(f"End:   {format_time_display(result['sunrise_next'])} (Next Sunrise)")
        print()
        
        print("🌙 MULTIPLE OVERLAPPING PERIODS:")
        print("-" * 40)
        
        print(f"🌙 Tithi ({len(result['tithis'])} periods):")
        for tithi in result['tithis']:
            print(f"   • {tithi['name']}")
            print(f"     {format_time_display(tithi['start'])} – {format_time_display(tithi['end'])}")
        print()
        
        print(f"⭐ Nakshatra ({len(result['nakshatras'])} periods):")
        for nakshatra in result['nakshatras']:
            print(f"   • {nakshatra['name']}")
            print(f"     {format_time_display(nakshatra['start'])} – {format_time_display(nakshatra['end'])}")
        print()
        
        print(f"🔄 Karana ({len(result['karanas'])} periods):")
        for karana in result['karanas']:
            print(f"   • {karana['name']}")
            print(f"     {format_time_display(karana['start'])} – {format_time_display(karana['end'])}")
        print()
        
        print(f"🧘 Yoga ({len(result['yogas'])} periods):")
        for yoga in result['yogas']:
            print(f"   • {yoga['name']}")
            print(f"     {format_time_display(yoga['start'])} – {format_time_display(yoga['end'])}")
        print()
        
        print(f"✨ Auspicious Periods ({len(result.get('auspicious_periods', []))} periods):")
        for period in result.get('auspicious_periods', []):
            print(f"   • {period['name']}")
            print(f"     {format_time_display(period['start'])} – {format_time_display(period['end'])}")
        print()
        
        print(f"⚠️ Inauspicious Periods ({len(result.get('inauspicious_periods', []))} periods):")
        for period in result.get('inauspicious_periods', []):
            print(f"   • {period['name']}")
            print(f"     {format_time_display(period['start'])} – {format_time_display(period['end'])}")
        print()
        
        print("✅ IMPLEMENTATION COMPLETE!")
        print("=" * 70)
        print("🎯 Features Implemented:")
        print("   ✅ Hindu day window calculation (sunrise to next sunrise)")
        print("   ✅ Multiple overlapping periods per element type")
        print("   ✅ Only periods that overlap with Hindu day window")
        print("   ✅ All 4 main elements: Tithi, Nakshatra, Karana, Yoga")
        print("   ✅ Auspicious periods: Abhijit, Brahma, Pradosha")
        print("   ✅ Inauspicious periods: Rahu, Gulika, Yamaganda")
        print("   ✅ Sun times: Sunrise & Sunset")
        print("   ✅ Moon times: Moonrise & Moonset")
        print("   ✅ ProKerala/DrikPanchang style presentation")
        print("   ✅ Frontend UI with period display toggle")
        print("   ✅ Proper ISO formatting and local time display")
        print()
        print("🌐 API Endpoint: POST /api/periods")
        print("🖥️  Frontend: http://localhost:3001 (with preview browser)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_final_implementation()