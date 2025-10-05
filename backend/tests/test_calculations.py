"""
Unit tests for Panchangam calculation functions
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.services.astronomical import calculate_sunrise_sunset, calculate_moonrise_moonset
from app.services.hindu_calendar import calculate_tithi, calculate_nakshatra
from app.utils.timezone import get_julian_day_ut

# Create test client
client = TestClient(app)

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "healthy" in response.json()["status"]
    
    def test_panchangam_endpoint_bengaluru(self):
        """Test panchangam endpoint with Bengaluru data"""
        test_data = {
            "date": "2025-10-05",
            "latitude": 12.9719,
            "longitude": 77.593,
            "city": "Bengaluru"
        }
        
        response = client.post("/api/panchangam", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["location"]["city"] == "Bengaluru"
        assert data["date"] == "2025-10-05"
        assert "sunrise" in data
        assert "sunset" in data
        assert "tithi" in data
        assert "nakshatra" in data
    
    def test_panchangam_endpoint_coventry(self):
        """Test panchangam endpoint with Coventry data"""
        test_data = {
            "date": "2025-10-05",
            "latitude": 52.40656,
            "longitude": -1.51217,
            "city": "Coventry"
        }
        
        response = client.post("/api/panchangam", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["location"]["city"] == "Coventry"
        assert data["date"] == "2025-10-05"
    
    def test_invalid_city(self):
        """Test with invalid city"""
        test_data = {
            "date": "2025-10-05",
            "latitude": 12.0,
            "longitude": 77.0,
            "city": "InvalidCity"
        }
        
        response = client.post("/api/panchangam", json=test_data)
        assert response.status_code == 400
    
    def test_get_cities(self):
        """Test get cities endpoint"""
        response = client.get("/api/cities")
        assert response.status_code == 200
        
        data = response.json()
        assert "cities" in data
        cities = data["cities"]
        assert len(cities) == 2
        
        city_names = [city["name"] for city in cities]
        assert "Bengaluru" in city_names
        assert "Coventry" in city_names

class TestAstronomicalCalculations:
    """Test astronomical calculation functions"""
    
    def test_sunrise_sunset_bengaluru(self):
        """Test sunrise/sunset calculation for Bengaluru"""
        date = datetime(2025, 10, 5)
        latitude = 12.9719
        longitude = 77.593
        city = "Bengaluru"
        
        sunrise, sunset = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Basic validation - should be reasonable times
        assert isinstance(sunrise, str)
        assert isinstance(sunset, str)
        assert "AM" in sunrise or "PM" in sunrise
        assert "PM" in sunset or "AM" in sunset
    
    def test_moonrise_moonset_bengaluru(self):
        """Test moonrise/moonset calculation for Bengaluru"""
        date = datetime(2025, 10, 5)
        latitude = 12.9719
        longitude = 77.593
        city = "Bengaluru"
        
        moonrise, moonset = calculate_moonrise_moonset(date, latitude, longitude, city)
        
        # Basic validation
        assert isinstance(moonrise, str)
        assert isinstance(moonset, str)

class TestHinduCalendar:
    """Test Hindu calendar calculations"""
    
    def test_tithi_calculation(self):
        """Test tithi calculation"""
        date = datetime(2025, 10, 5)
        jd = get_julian_day_ut(date)
        city = "Bengaluru"
        
        tithi_data = calculate_tithi(jd, city)
        
        assert "name" in tithi_data
        assert "start" in tithi_data
        assert "end" in tithi_data
        assert isinstance(tithi_data["name"], str)
        assert len(tithi_data["name"]) > 0
    
    def test_nakshatra_calculation(self):
        """Test nakshatra calculation"""
        date = datetime(2025, 10, 5)
        jd = get_julian_day_ut(date)
        city = "Bengaluru"
        
        nakshatra_data = calculate_nakshatra(jd, city)
        
        assert "name" in nakshatra_data
        assert "start" in nakshatra_data
        assert "end" in nakshatra_data
        assert isinstance(nakshatra_data["name"], str)
        assert len(nakshatra_data["name"]) > 0

class TestInputValidation:
    """Test input validation"""
    
    def test_invalid_date_format(self):
        """Test invalid date format"""
        test_data = {
            "date": "invalid-date",
            "latitude": 12.9719,
            "longitude": 77.593,
            "city": "Bengaluru"
        }
        
        response = client.post("/api/panchangam", json=test_data)
        assert response.status_code == 400
    
    def test_invalid_coordinates(self):
        """Test invalid coordinates"""
        test_data = {
            "date": "2025-10-05",
            "latitude": 95.0,  # Invalid latitude
            "longitude": 77.593,
            "city": "Bengaluru"
        }
        
        response = client.post("/api/panchangam", json=test_data)
        assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__, "-v"])