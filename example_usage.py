#!/usr/bin/env python3
"""
Example usage of Panchangam API
"""
import requests
import json
from datetime import date

# API endpoint
API_BASE = "http://localhost:8000/api"

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ API is healthy")
            return True
        else:
            print("✗ API health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Make sure the server is running.")
        return False

def get_panchangam_data(city, latitude, longitude, date_str=None):
    """Get Panchangam data for a city"""
    if not date_str:
        date_str = date.today().isoformat()
    
    payload = {
        "date": date_str,
        "latitude": latitude,
        "longitude": longitude,
        "city": city
    }
    
    try:
        response = requests.post(f"{API_BASE}/panchangam", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def print_panchangam_summary(data):
    """Print a summary of Panchangam data"""
    if not data:
        return
    
    print(f"\n🏙️  Panchangam for {data['location']['city']} on {data['date']}")
    print("=" * 50)
    
    # Basic times
    print(f"🌅 Sunrise: {data['sunrise']}")
    print(f"🌇 Sunset: {data['sunset']}")
    print(f"🌙 Moonrise: {data['moonrise']}")
    print(f"🌚 Moonset: {data['moonset']}")
    
    # Hindu calendar
    print(f"\n📅 Hindu Calendar:")
    print(f"   Tithi: {data['tithi']['name']}")
    print(f"   Nakshatra: {data['nakshatra']['name']}")
    print(f"   Karana: {data['karana']['name']}")
    print(f"   Yoga: {data['yoga']['name']}")
    
    # Auspicious periods
    print(f"\n✨ Auspicious Periods:")
    auspicious = data['auspicious_periods']
    print(f"   Abhijit Muhurat: {auspicious['abhijit_muhurat']['start']} - {auspicious['abhijit_muhurat']['end']}")
    print(f"   Brahma Muhurat: {auspicious['brahma_muhurat']['start']} - {auspicious['brahma_muhurat']['end']}")
    print(f"   Pradosha Time: {auspicious['pradosha_time']['start']} - {auspicious['pradosha_time']['end']}")
    
    # Inauspicious periods
    print(f"\n⚠️  Inauspicious Periods:")
    inauspicious = data['inauspicious_periods']
    print(f"   Rahu Kalam: {inauspicious['rahu']['start']} - {inauspicious['rahu']['end']}")
    print(f"   Gulika Kalam: {inauspicious['gulika']['start']} - {inauspicious['gulika']['end']}")
    print(f"   Yamaganda: {inauspicious['yamaganda']['start']} - {inauspicious['yamaganda']['end']}")
    
    if inauspicious['varjyam']:
        print(f"   Varjyam:")
        for i, period in enumerate(inauspicious['varjyam'], 1):
            print(f"     {i}. {period['start']} - {period['end']}")

def main():
    """Main function to demonstrate API usage"""
    print("Panchangam API Example")
    print("=====================")
    
    # Check API health
    if not test_api_health():
        return
    
    # Test cities
    cities = [
        ("Bengaluru", 12.9719, 77.593),
        ("Coventry", 52.40656, -1.51217)
    ]
    
    for city, lat, lon in cities:
        print(f"\nFetching data for {city}...")
        data = get_panchangam_data(city, lat, lon)
        print_panchangam_summary(data)
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")
    print("For full API documentation, visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()