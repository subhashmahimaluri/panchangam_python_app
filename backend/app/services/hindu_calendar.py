"""
Hindu calendar calculations - Tithi, Nakshatra, Karana, Yoga
Based on the proven DrikPanchanga implementation for maximum accuracy
"""
import swisseph as swe
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, List
from math import floor, ceil
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime
from app.utils.constants import (
    TITHI_NAMES, NAKSHATRA_NAMES, KARANA_NAMES, YOGA_NAMES, PAKSHA_NAMES,
    SUN, MOON, SIDEREAL_FLAG, NAKSHATRA_DEGREES, TITHI_DEGREES
)
from app.services.astronomical import (
    get_sun_position, get_moon_position, solar_longitude, lunar_longitude,
    calculate_sunrise_sunset, get_timezone_offset
)

# Helper functions for accurate calculations

def unwrap_angles(angles: List[float]) -> List[float]:
    """Add 360 to those elements in the input list so that
       all elements are sorted in ascending order."""
    result = angles[:]
    for i in range(1, len(angles)):
        if result[i] < result[i-1]: 
            result[i] += 360
    return result

def inverse_lagrange(x: List[float], y: List[float], ya: float) -> float:
    """Given two lists x and y, find the value of x = xa when y = ya, i.e., f(xa) = ya
    Uses inverse Lagrange interpolation for precise boundary timing"""
    assert len(x) == len(y)
    total = 0
    for i in range(len(x)):
        numer = 1
        denom = 1
        for j in range(len(x)):
            if j != i:
                numer *= (ya - y[j])
                denom *= (y[i] - y[j])
        total += numer * x[i] / denom
    return total

def lunar_phase(jd: float) -> float:
    """Calculate lunar phase (moon's longitude - sun's longitude)"""
    solar_long = solar_longitude(jd)
    lunar_long = lunar_longitude(jd)
    moon_phase = (lunar_long - solar_long) % 360
    return moon_phase

def get_sunrise_jd(jd: float, city: str, latitude: float, longitude: float) -> float:
    """Get sunrise Julian Day for calculations"""
    try:
        # Convert JD to date for sunrise calculation
        cal_date = swe.revjul(jd)
        date_obj = datetime(int(cal_date[0]), int(cal_date[1]), int(cal_date[2]))
        
        # Calculate sunrise
        sunrise_str, _ = calculate_sunrise_sunset(date_obj, latitude, longitude, city)
        
        # Convert sunrise time back to JD
        tz_offset = get_timezone_offset(city, longitude, date_obj)
        
        # Parse sunrise time
        if "AM" in sunrise_str or "PM" in sunrise_str:
            time_part = sunrise_str.replace(" AM", "").replace(" PM", "")
            hours, minutes = map(int, time_part.split(":"))
            if "PM" in sunrise_str and hours != 12:
                hours += 12
            elif "AM" in sunrise_str and hours == 12:
                hours = 0
        else:
            return jd  # Fallback
        
        # Calculate sunrise JD in UTC
        sunrise_hour = hours + minutes/60.0
        sunrise_local_jd = jd + (sunrise_hour - tz_offset) / 24.0
        
        return sunrise_local_jd - tz_offset/24.0  # Return in UTC
        
    except Exception as e:
        print(f"Error getting sunrise JD: {e}")
        return jd  # Fallback to input JD


def calculate_tithi(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Tithi (lunar day) using exact DrikPanchanga algorithm
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with tithi name, start time, and end time
    """
    try:
        # Set Lahiri Ayanamsa
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get city coordinates and timezone
        city_coords = get_city_coordinates(city)
        latitude = city_coords.get('latitude', 12.9719)
        longitude = city_coords.get('longitude', 77.593)
        tz_offset = get_timezone_offset(city, longitude)
        
        # Create place tuple for DrikPanchanga format
        place = (latitude, longitude, tz_offset)
        
        # 1. Find time of sunrise (in UTC)
        rise_result = calculate_sunrise_for_panchang(jd, place)
        rise_jd = rise_result[0] - tz_offset / 24  # Convert to UTC
        
        # 2. Find tithi at sunrise
        moon_phase = lunar_phase(rise_jd)
        today = ceil(moon_phase / 12)
        degrees_left = today * 12 - moon_phase
        
        # 3. Compute longitudinal differences at intervals from sunrise
        offsets = [0.25, 0.5, 0.75, 1.0]
        lunar_long_diff = [(lunar_longitude(rise_jd + t) - lunar_longitude(rise_jd)) % 360 for t in offsets]
        solar_long_diff = [(solar_longitude(rise_jd + t) - solar_longitude(rise_jd)) % 360 for t in offsets]
        relative_motion = [moon - sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff)]
        
        # 4. Find end time by 4-point inverse Lagrange interpolation
        y = relative_motion
        x = offsets
        approx_end = inverse_lagrange(x, y, degrees_left)
        ends_hours = (rise_jd + approx_end - jd) * 24 + tz_offset
        
        # 5. Check for skipped tithi
        moon_phase_tmrw = lunar_phase(rise_jd + 1)
        tomorrow = ceil(moon_phase_tmrw / 12)
        isSkipped = (tomorrow - today) % 30 > 1
        
        # Convert timing to proper format
        end_dt = jd_to_local_datetime_precise(jd + (ends_hours/24), city)
        
        # Calculate start time (previous tithi end)
        prev_today = (today - 2) % 30 + 1  # Previous tithi
        prev_degrees_left = prev_today * 12 - moon_phase
        prev_approx_end = inverse_lagrange(x, y, prev_degrees_left)
        start_hours = (rise_jd + prev_approx_end - jd) * 24 + tz_offset
        start_dt = jd_to_local_datetime_precise(jd + (start_hours/24), city)
        
        # Determine paksha and get proper name
        paksha = 0 if today <= 15 else 1
        tithi_index = (today - 1) % 15
        
        if paksha == 0:  # Shukla Paksha
            tithi_name = f"Shukla Paksha {TITHI_NAMES[tithi_index]}"
        else:  # Krishna Paksha
            tithi_name = f"Krishna Paksha {TITHI_NAMES[tithi_index]}"
        
        return {
            "name": tithi_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating tithi: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": "Shukla Paksha Pratipada",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def calculate_sunrise_for_panchang(jd: float, place: Tuple[float, float, float]) -> Tuple[float, List[int]]:
    """Calculate sunrise using DrikPanchanga method"""
    lat, lon, tz = place
    try:
        # Use our existing accurate sunrise calculation
        cal_date = swe.revjul(jd)
        date_obj = datetime(int(cal_date[0]), int(cal_date[1]), int(cal_date[2]))
        
        # Get city name from coordinates (reverse lookup)
        city = "Bengaluru"  # Default fallback
        for city_name, coords in get_city_coordinates_map().items():
            if abs(coords['latitude'] - lat) < 0.1 and abs(coords['longitude'] - lon) < 0.1:
                city = city_name
                break
        
        sunrise_str, _ = calculate_sunrise_sunset(date_obj, lat, lon, city)
        
        # Parse sunrise time and convert to JD
        if "AM" in sunrise_str or "PM" in sunrise_str:
            time_part = sunrise_str.replace(" AM", "").replace(" PM", "")
            hours, minutes = map(int, time_part.split(":"))
            if "PM" in sunrise_str and hours != 12:
                hours += 12
            elif "AM" in sunrise_str and hours == 12:
                hours = 0
        else:
            hours, minutes = 6, 0  # Fallback
        
        # Calculate sunrise JD in local time
        sunrise_hour = hours + minutes/60.0
        sunrise_jd = jd + (sunrise_hour) / 24.0
        
        # Convert to DMS format for compatibility
        time_dms = to_dms(sunrise_hour)
        
        return sunrise_jd, time_dms
        
    except Exception as e:
        print(f"Error in sunrise calculation: {e}")
        # Fallback to approximate sunrise
        return jd + 0.25, [6, 0, 0]  # 6 AM fallback

def get_city_coordinates_map() -> Dict[str, Dict[str, float]]:
    """Get full city coordinates mapping"""
    return {
        "bengaluru": {"latitude": 12.9719, "longitude": 77.593},
        "bangalore": {"latitude": 12.9719, "longitude": 77.593},
        "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
        "delhi": {"latitude": 28.6139, "longitude": 77.2090},
        "chennai": {"latitude": 13.0827, "longitude": 80.2707},
        "kolkata": {"latitude": 22.5726, "longitude": 88.3639},
        "hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
        "pune": {"latitude": 18.5204, "longitude": 73.8567},
        "coventry": {"latitude": 52.40656, "longitude": -1.51217},
        "london": {"latitude": 51.5074, "longitude": -0.1278},
        "manchester": {"latitude": 53.4808, "longitude": -2.2426},
        "birmingham": {"latitude": 52.4862, "longitude": -1.8904},
        "new york": {"latitude": 40.7128, "longitude": -74.006},
        "newyork": {"latitude": 40.7128, "longitude": -74.006},
        "miami": {"latitude": 25.7617, "longitude": -80.1918},
        "los angeles": {"latitude": 34.0522, "longitude": -118.2437},
        "chicago": {"latitude": 41.8781, "longitude": -87.6298},
        "lima": {"latitude": -12.0464, "longitude": -77.0428},
        "harare": {"latitude": -17.8292, "longitude": 31.0522},
        "johannesburg": {"latitude": -26.2041, "longitude": 28.0473},
        "cape town": {"latitude": -33.9249, "longitude": 18.4241},
        "canberra": {"latitude": -35.2809, "longitude": 149.13},
        "sydney": {"latitude": -33.8688, "longitude": 151.2093},
        "melbourne": {"latitude": -37.8136, "longitude": 144.9631},
        "brisbane": {"latitude": -27.4698, "longitude": 153.0251},
        "perth": {"latitude": -31.9505, "longitude": 115.8605}
    }

def to_dms(deg: float) -> List[int]:
    """Convert decimal degrees to degrees, minutes, seconds"""
    d = int(deg)
    mins = (deg - d) * 60
    m = int(mins)
    s = int(round((mins - m) * 60))
    return [d, m, s]

def dms_to_datetime_offset(dms_time: List[int], base_jd: float, tz_offset: float) -> datetime:
    """Convert DMS time to datetime with proper timezone handling"""
    try:
        hours, minutes, seconds = dms_time
        
        # Handle negative hours (previous day)
        if hours < 0:
            base_jd -= 1
            hours += 24
        elif hours >= 24:
            base_jd += 1
            hours -= 24
            
        # Calculate the target JD
        target_jd = base_jd + (hours + minutes/60.0 + seconds/3600.0) / 24.0
        
        # Convert to local datetime
        return jd_to_local_datetime_precise(target_jd, "Bengaluru")
        
    except Exception as e:
        print(f"Error converting DMS to datetime: {e}")
        return datetime.now()

def jd_to_local_datetime_precise(jd: float, city: str) -> datetime:
    """Convert Julian Day to precise local datetime"""
    try:
        # Convert JD to Gregorian date
        cal_date = swe.revjul(jd)
        year, month, day, hour_float = cal_date[:4]
        
        hours = int(hour_float)
        minutes = int((hour_float - hours) * 60)
        seconds = int(((hour_float - hours) * 60 - minutes) * 60)
        
        # Handle date overflow
        if hours >= 24:
            day += 1
            hours -= 24
        elif hours < 0:
            day -= 1
            hours += 24
            
        return datetime(int(year), int(month), int(day), hours, minutes, seconds)
        
    except Exception as e:
        print(f"Error in precise JD conversion: {e}")
        return datetime.now()


def calculate_nakshatra(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Nakshatra using exact DrikPanchanga algorithm
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with nakshatra name, start time, and end time
    """
    try:
        # Set Lahiri Ayanamsa
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get city coordinates and timezone
        city_coords = get_city_coordinates(city)
        latitude = city_coords.get('latitude', 12.9719)
        longitude = city_coords.get('longitude', 77.593)
        tz_offset = get_timezone_offset(city, longitude)
        
        # Create place tuple
        place = (latitude, longitude, tz_offset)
        
        # 1. Find time of sunrise (in UTC)
        rise_result = calculate_sunrise_for_panchang(jd, place)
        rise_jd = rise_result[0] - tz_offset / 24  # Convert to UTC
        
        # 2. Swiss Ephemeris gives Sayana, subtract ayanamsa for Nirayana
        offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
        longitudes = [(lunar_longitude(rise_jd + t) - swe.get_ayanamsa_ut(rise_jd + t)) % 360 for t in offsets]
        
        # 3. Today's nakshatra when offset = 0
        # There are 27 Nakshatras spanning 360 degrees
        nak = ceil(longitudes[0] * 27 / 360)
        if nak > 27:
            nak = 1  # Wrap around
        
        # 4. Find end time by 5-point inverse Lagrange interpolation
        y = unwrap_angles(longitudes)
        x = offsets
        approx_end = inverse_lagrange(x, y, nak * 360 / 27)
        ends_hours = (rise_jd - jd + approx_end) * 24 + tz_offset
        
        # 5. Check for skipped nakshatra
        nak_tmrw = ceil(longitudes[-1] * 27 / 360)
        isSkipped = (nak_tmrw - nak) % 27 > 1
        
        # Convert timing to proper format
        end_dt = jd_to_local_datetime_precise(jd + (ends_hours/24), city)
        
        # Calculate start time (previous nakshatra end)
        prev_nak = (nak - 2) % 27 + 1
        prev_approx_end = inverse_lagrange(x, y, prev_nak * 360 / 27)
        start_hours = (rise_jd - jd + prev_approx_end) * 24 + tz_offset
        start_dt = jd_to_local_datetime_precise(jd + (start_hours/24), city)
        
        # Get nakshatra name (1-based to 0-based indexing)
        nakshatra_name = NAKSHATRA_NAMES[(nak - 1) % 27]
        
        result = {
            "name": nakshatra_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
        # Handle skipped nakshatra
        if isSkipped:
            leap_nak = (nak % 27) + 1
            print(f"Skipped nakshatra detected: {NAKSHATRA_NAMES[(leap_nak - 1) % 27]}")
        
        return result
        
    except Exception as e:
        print(f"Error calculating nakshatra: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": "Ashwini",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def calculate_karana(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Karana using simplified reliable algorithm
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with karana name, start time, and end time
    """
    try:
        # Get city coordinates and timezone
        city_coords = get_city_coordinates(city)
        latitude = city_coords.get('latitude', 12.9719)
        longitude = city_coords.get('longitude', 77.593)
        tz_offset = get_timezone_offset(city, longitude)
        
        # Calculate lunar phase (moon - sun longitude)
        moon_long = lunar_longitude(jd)
        sun_long = solar_longitude(jd)
        lunar_phase = (moon_long - sun_long) % 360
        
        # Each karana is 6 degrees (half of tithi)
        # There are 60 karanas in a lunar month (30 tithis × 2)
        karana_number = int(lunar_phase / 6) + 1
        if karana_number > 60:
            karana_number = 1
        
        # Map karana number to name (simplified)
        if karana_number <= 56:
            # Movable karanas (cycle through first 7)
            karana_index = (karana_number - 1) % 7
        else:
            # Fixed karanas (last 4)
            karana_index = 7 + (karana_number - 57)
        
        # Ensure bounds safety
        karana_index = min(karana_index, len(KARANA_NAMES) - 1)
        karana_name = KARANA_NAMES[karana_index]
        
        # Calculate approximate start and end times
        # Each karana lasts about 6 degrees of lunar motion (roughly 12 hours)
        
        # Start: when current karana began
        start_phase = (karana_number - 1) * 6
        degrees_since_start = lunar_phase - start_phase
        if degrees_since_start < 0:
            degrees_since_start += 360
            
        # Estimate time for degrees (moon moves ~13.2 degrees per day)
        hours_since_start = degrees_since_start / 13.2 * 24
        start_jd = jd - hours_since_start / 24
        
        # End: when current karana ends
        end_phase = karana_number * 6
        degrees_to_end = end_phase - lunar_phase
        if degrees_to_end <= 0:
            degrees_to_end += 360
            
        hours_to_end = degrees_to_end / 13.2 * 24
        end_jd = jd + hours_to_end / 24
        
        # Convert to local datetime
        start_dt = jd_to_local_datetime_precise(start_jd, city)
        end_dt = jd_to_local_datetime_precise(end_jd, city)
        
        return {
            "name": karana_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating karana: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": "Bava",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=12)).isoformat()
        }

def calculate_yoga(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Yoga using exact DrikPanchanga algorithm
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with yoga name, start time, and end time
    """
    try:
        # Set Lahiri Ayanamsa
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get city coordinates and timezone
        city_coords = get_city_coordinates(city)
        latitude = city_coords.get('latitude', 12.9719)
        longitude = city_coords.get('longitude', 77.593)
        tz_offset = get_timezone_offset(city, longitude)
        
        # Create place tuple
        place = (latitude, longitude, tz_offset)
        
        # 1. Find time of sunrise (in UTC)
        rise_result = calculate_sunrise_for_panchang(jd, place)
        rise_jd = rise_result[0] - tz_offset / 24  # Convert to UTC
        
        # 2. Find the Nirayana longitudes and add them
        lunar_long = (lunar_longitude(rise_jd) - swe.get_ayanamsa_ut(rise_jd)) % 360
        solar_long = (solar_longitude(rise_jd) - swe.get_ayanamsa_ut(rise_jd)) % 360
        total = (lunar_long + solar_long) % 360
        
        # There are 27 Yogas spanning 360 degrees
        yog = ceil(total * 27 / 360)
        if yog > 27:
            yog = 1  # Wrap around
        
        # 3. Find how many degrees left to be swept
        degrees_left = yog * (360 / 27) - total
        
        # 4. Compute longitudinal sums at intervals from sunrise
        offsets = [0.25, 0.5, 0.75, 1.0]
        lunar_long_diff = [(lunar_longitude(rise_jd + t) - lunar_longitude(rise_jd)) % 360 for t in offsets]
        solar_long_diff = [(solar_longitude(rise_jd + t) - solar_longitude(rise_jd)) % 360 for t in offsets]
        total_motion = [moon + sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff)]
        
        # 5. Find end time by 4-point inverse Lagrange interpolation
        y = total_motion
        x = offsets
        approx_end = inverse_lagrange(x, y, degrees_left)
        ends_hours = (rise_jd + approx_end - jd) * 24 + tz_offset
        
        # 6. Check for skipped yoga
        lunar_long_tmrw = (lunar_longitude(rise_jd + 1) - swe.get_ayanamsa_ut(rise_jd + 1)) % 360
        solar_long_tmrw = (solar_longitude(rise_jd + 1) - swe.get_ayanamsa_ut(rise_jd + 1)) % 360
        total_tmrw = (lunar_long_tmrw + solar_long_tmrw) % 360
        tomorrow = ceil(total_tmrw * 27 / 360)
        isSkipped = (tomorrow - yog) % 27 > 1
        
        # Convert timing to proper format
        end_dt = jd_to_local_datetime_precise(jd + (ends_hours/24), city)
        
        # Calculate start time (previous yoga end)
        prev_yog = (yog - 2) % 27 + 1
        prev_degrees_left = prev_yog * (360 / 27) - total
        prev_approx_end = inverse_lagrange(x, y, prev_degrees_left)
        start_hours = (rise_jd + prev_approx_end - jd) * 24 + tz_offset
        start_dt = jd_to_local_datetime_precise(jd + (start_hours/24), city)
        
        # Get yoga name (1-based to 0-based indexing)
        yoga_name = YOGA_NAMES[(yog - 1) % 27]
        
        result = {
            "name": yoga_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
        # Handle skipped yoga
        if isSkipped:
            leap_yog = (yog % 27) + 1
            print(f"Skipped yoga detected: {YOGA_NAMES[(leap_yog - 1) % 27]}")
        
        return result
        
    except Exception as e:
        print(f"Error calculating yoga: {e}")
        import traceback
        traceback.print_exc()
        return {
            "name": "Vishkambha",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def get_city_coordinates(city: str) -> Dict[str, float]:
    """Get coordinates for supported cities"""
    coordinates = {
        "bengaluru": {"latitude": 12.9719, "longitude": 77.593},
        "bangalore": {"latitude": 12.9719, "longitude": 77.593},
        "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
        "delhi": {"latitude": 28.6139, "longitude": 77.2090},
        "chennai": {"latitude": 13.0827, "longitude": 80.2707},
        "kolkata": {"latitude": 22.5726, "longitude": 88.3639},
        "hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
        "pune": {"latitude": 18.5204, "longitude": 73.8567},
        "coventry": {"latitude": 52.40656, "longitude": -1.51217},
        "london": {"latitude": 51.5074, "longitude": -0.1278},
        "manchester": {"latitude": 53.4808, "longitude": -2.2426},
        "birmingham": {"latitude": 52.4862, "longitude": -1.8904},
        "new york": {"latitude": 40.7128, "longitude": -74.006},
        "newyork": {"latitude": 40.7128, "longitude": -74.006},
        "miami": {"latitude": 25.7617, "longitude": -80.1918},
        "los angeles": {"latitude": 34.0522, "longitude": -118.2437},
        "chicago": {"latitude": 41.8781, "longitude": -87.6298},
        "lima": {"latitude": -12.0464, "longitude": -77.0428},
        "harare": {"latitude": -17.8292, "longitude": 31.0522},
        "johannesburg": {"latitude": -26.2041, "longitude": 28.0473},
        "cape town": {"latitude": -33.9249, "longitude": 18.4241},
        "canberra": {"latitude": -35.2809, "longitude": 149.13},
        "sydney": {"latitude": -33.8688, "longitude": 151.2093},
        "melbourne": {"latitude": -37.8136, "longitude": 144.9631},
        "brisbane": {"latitude": -27.4698, "longitude": 153.0251},
        "perth": {"latitude": -31.9505, "longitude": 115.8605}
    }
    
    city_lower = city.lower().replace(" ", "").replace("-", "")
    return coordinates.get(city_lower, {"latitude": 12.9719, "longitude": 77.593})

def calculate_all_periods_for_hindu_day(
    date: datetime, 
    latitude: float, 
    longitude: float
) -> Dict[str, any]:
    """
    Calculate all periods that overlap with the Hindu day (sunrise to next sunrise).
    
    The Hindu day window is defined as:
    start: sunrise time on the requested date
    end: sunrise time on the next day
    location: Use requested latitude, longitude
    
    For each element (Tithi, Nakshatra, Karana, Yoga):
    - Collect ALL periods that have any time interval overlapping with the Hindu day window
    - Show all valid periods in a list, sorted by start time
    - Do not return entries that end before requested day's sunrise
    
    This matches ProKerala, DrikPanchang, and print Panchangam presentations.
    
    Args:
        date: Date for calculation (local date)
        latitude: Latitude in degrees  
        longitude: Longitude in degrees
        
    Returns:
        Dictionary containing all overlapping periods for tithis, nakshatras, karanas, yogas,
        plus auspicious and inauspicious periods
    """
    try:
        # Use existing fast sunrise calculation
        from app.services.astronomical import calculate_sunrise_sunset
        from app.services.muhurat import (
            calculate_rahu_kalam, calculate_gulika_kalam, calculate_yamaganda_kalam,
            calculate_abhijit_muhurat, calculate_brahma_muhurat, calculate_pradosha_time
        )
        city = "Bengaluru"  # Default city
        
        # Calculate Hindu day window: sunrise to next sunrise
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        next_date = date + timedelta(days=1)
        sunrise_next_str, _ = calculate_sunrise_sunset(next_date, latitude, longitude, city)
        
        # Calculate moonrise and moonset for the date
        from app.services.astronomical import calculate_moonrise_moonset
        moonrise_str, moonset_str = calculate_moonrise_moonset(date, latitude, longitude, city)
        
        def parse_time_to_datetime(date_obj: datetime, time_str: str) -> datetime:
            """Parse time string to datetime object"""
            try:
                if "AM" in time_str or "PM" in time_str:
                    time_part = time_str.replace(" AM", "").replace(" PM", "")
                    hours, minutes = map(int, time_part.split(":"))
                    if "PM" in time_str and hours != 12:
                        hours += 12
                    elif "AM" in time_str and hours == 12:
                        hours = 0
                else:
                    hours, minutes = 6, 10  # Fallback
                
                return date_obj.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            except:
                return date_obj.replace(hour=6, minute=10)
        
        # Define Hindu day window
        hindu_day_start = parse_time_to_datetime(date, sunrise_str)
        hindu_day_end = parse_time_to_datetime(next_date, sunrise_next_str)
        
        # Create ISO format times
        sunrise_iso = f"{hindu_day_start.isoformat()}+05:30"
        sunrise_next_iso = f"{hindu_day_end.isoformat()}+05:30"
        sunset_iso = f"{parse_time_to_datetime(date, sunset_str).isoformat()}+05:30"
        moonrise_iso = f"{parse_time_to_datetime(date, moonrise_str).isoformat()}+05:30"
        moonset_iso = f"{parse_time_to_datetime(date, moonset_str).isoformat()}+05:30"
        
        print(f"Hindu day window: {hindu_day_start} to {hindu_day_end}")
        
        # Calculate Julian Day and use existing optimized functions
        from app.utils.timezone import local_to_utc
        utc_date = local_to_utc(date, city)
        jd = get_julian_day_ut(utc_date)
        
        def format_time_12hour_simple(iso_time_str):
            """Format ISO time to 12-hour format"""
            try:
                dt = datetime.fromisoformat(iso_time_str.replace('Z', '+00:00').replace('+05:30', ''))
                return dt.strftime('%I:%M %p')
            except:
                return "12:00 PM"  # Fallback
        
        def periods_overlap_with_hindu_day(period_start_str: str, period_end_str: str) -> bool:
            """Check if a period overlaps with the Hindu day window"""
            try:
                # Parse period times (remove timezone info for comparison)
                period_start = datetime.fromisoformat(period_start_str.replace('Z', '').replace('+05:30', ''))
                period_end = datetime.fromisoformat(period_end_str.replace('Z', '').replace('+05:30', ''))
                
                # Check for overlap: period_start < hindu_day_end AND period_end > hindu_day_start
                return period_start < hindu_day_end and period_end > hindu_day_start
            except:
                return True  # Include if parsing fails
        
        def get_overlapping_periods(calc_func, jd_range, city):
            """Get all periods that overlap with Hindu day window"""
            all_periods = []
            seen_periods = set()
            
            for test_jd in jd_range:
                try:
                    period_data = calc_func(test_jd, city)
                    
                    # Check if this period overlaps with Hindu day
                    if periods_overlap_with_hindu_day(period_data['start'], period_data['end']):
                        # Create unique key to avoid exact duplicates
                        period_key = f"{period_data['name']}_{period_data['start']}_{period_data['end']}"
                        
                        if period_key not in seen_periods:
                            all_periods.append({
                                'name': period_data['name'],
                                'start': period_data['start'],
                                'end': period_data['end'],
                                'start_formatted': format_time_12hour_simple(period_data['start']),
                                'end_formatted': format_time_12hour_simple(period_data['end'])
                            })
                            seen_periods.add(period_key)
                except Exception as e:
                    print(f"Error calculating period for JD {test_jd}: {e}")
                    continue
            
            # Sort by start time and return
            all_periods.sort(key=lambda x: x['start'])
            return all_periods
        
        # Calculate periods for extended range to catch all overlaps
        # Check 2 days before to 2 days after, but limit karana range to avoid incorrect long periods
        jd_range = [jd - 2, jd - 1, jd, jd + 1, jd + 2]
        jd_range_karana = [jd - 1, jd, jd + 1]  # Smaller range for karanas to avoid calculation errors
        
        # Get overlapping periods for each element type
        tithis = get_overlapping_periods(calculate_tithi, jd_range, city)
        nakshatras = get_overlapping_periods(calculate_nakshatra, jd_range, city)
        karanas = get_overlapping_periods(calculate_karana, jd_range_karana, city)  # Use smaller range
        yogas = get_overlapping_periods(calculate_yoga, jd_range, city)
        
        # Calculate auspicious and inauspicious periods for the Hindu day
        auspicious_periods = []
        inauspicious_periods = []
        
        def format_muhurat_period(muhurat_data, name):
            """Convert muhurat data to consistent format"""
            if not (muhurat_data.get('start') and muhurat_data.get('end')):
                return None
                
            # Parse time strings like "16:30" to create full datetime
            try:
                start_time = muhurat_data['start']  # "16:30"
                end_time = muhurat_data['end']      # "18:00"
                
                # Parse hours and minutes
                start_hour, start_min = map(int, start_time.split(':'))
                end_hour, end_min = map(int, end_time.split(':'))
                
                # Create datetime objects for the requested date
                start_dt = date.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
                end_dt = date.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)
                
                # Handle case where end time is next day
                if end_hour < start_hour:
                    end_dt = end_dt + timedelta(days=1)
                
                return {
                    'name': name,
                    'start': f"{start_dt.isoformat()}+05:30",
                    'end': f"{end_dt.isoformat()}+05:30",
                    'start_formatted': start_dt.strftime('%I:%M %p'),
                    'end_formatted': end_dt.strftime('%I:%M %p')
                }
            except Exception as e:
                print(f"Error formatting {name}: {e}")
                return None
        
        try:
            # Auspicious periods
            abhijit_data = calculate_abhijit_muhurat(date, latitude, longitude, city)
            abhijit_period = format_muhurat_period(abhijit_data, 'Abhijit Muhurat')
            if abhijit_period:
                auspicious_periods.append(abhijit_period)
            
            brahma_data = calculate_brahma_muhurat(date, latitude, longitude, city)
            brahma_period = format_muhurat_period(brahma_data, 'Brahma Muhurat')
            if brahma_period:
                auspicious_periods.append(brahma_period)
            
            pradosha_data = calculate_pradosha_time(date, latitude, longitude, city)
            pradosha_period = format_muhurat_period(pradosha_data, 'Pradosha Time')
            if pradosha_period:
                auspicious_periods.append(pradosha_period)
            
            # Inauspicious periods
            rahu_data = calculate_rahu_kalam(date, latitude, longitude, city)
            rahu_period = format_muhurat_period(rahu_data, 'Rahu Kalam')
            if rahu_period:
                inauspicious_periods.append(rahu_period)
            
            gulika_data = calculate_gulika_kalam(date, latitude, longitude, city)
            gulika_period = format_muhurat_period(gulika_data, 'Gulika Kalam')
            if gulika_period:
                inauspicious_periods.append(gulika_period)
            
            yamaganda_data = calculate_yamaganda_kalam(date, latitude, longitude, city)
            yamaganda_period = format_muhurat_period(yamaganda_data, 'Yamaganda Kalam')
            if yamaganda_period:
                inauspicious_periods.append(yamaganda_period)
        except Exception as e:
            print(f"Error calculating muhurat periods: {e}")
        
        # Ensure we have at least some periods (fallback)
        if not tithis:
            tithi_data = calculate_tithi(jd, city)
            tithis = [{
                'name': tithi_data['name'],
                'start': tithi_data['start'],
                'end': tithi_data['end'],
                'start_formatted': format_time_12hour_simple(tithi_data['start']),
                'end_formatted': format_time_12hour_simple(tithi_data['end'])
            }]
        
        print(f"Found {len(tithis)} Tithis, {len(nakshatras)} Nakshatras, {len(karanas)} Karanas, {len(yogas)} Yogas")
        print(f"Found {len(auspicious_periods)} Auspicious periods, {len(inauspicious_periods)} Inauspicious periods")
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'location': {'latitude': latitude, 'longitude': longitude},
            'sunrise': sunrise_iso,
            'sunset': sunset_iso,
            'moonrise': moonrise_iso,
            'moonset': moonset_iso,
            'sunrise_next': sunrise_next_iso,
            'hindu_day_start': hindu_day_start.isoformat(),
            'hindu_day_end': hindu_day_end.isoformat(),
            'tithis': tithis,
            'nakshatras': nakshatras,
            'karanas': karanas,
            'yogas': yogas,
            'auspicious_periods': auspicious_periods,
            'inauspicious_periods': inauspicious_periods
        }
        
    except Exception as e:
        print(f"Error in periods calculation: {e}")
        import traceback
        traceback.print_exc()
        # Return simple fallback response
        return {
            'date': date.strftime('%Y-%m-%d'),
            'location': {'latitude': latitude, 'longitude': longitude},
            'sunrise': f"{date.replace(hour=6, minute=10).isoformat()}+05:30",
            'sunset': f"{date.replace(hour=18, minute=30).isoformat()}+05:30",
            'moonrise': f"{date.replace(hour=7, minute=0).isoformat()}+05:30",
            'moonset': f"{date.replace(hour=19, minute=0).isoformat()}+05:30",
            'sunrise_next': f"{(date + timedelta(days=1)).replace(hour=6, minute=10).isoformat()}+05:30",
            'tithis': [],
            'nakshatras': [],
            'karanas': [],
            'yogas': [],
            'auspicious_periods': [],
            'inauspicious_periods': []
        }

def parse_sunrise_to_iso(date: datetime, sunrise_str: str, tz_offset: float) -> str:
    """
    Parse sunrise time string to ISO format with timezone
    
    Args:
        date: Base date
        sunrise_str: Sunrise time in "HH:MM AM/PM" format
        tz_offset: Timezone offset in hours
        
    Returns:
        ISO format datetime string with timezone
    """
    try:
        # Parse the time string
        time_part = sunrise_str.replace(" AM", "").replace(" PM", "")
        hours, minutes = map(int, time_part.split(":"))
        
        # Convert to 24-hour format
        if "PM" in sunrise_str and hours != 12:
            hours += 12
        elif "AM" in sunrise_str and hours == 12:
            hours = 0
            
        # Create datetime with timezone
        sunrise_dt = date.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        # Format timezone offset
        tz_hours = int(tz_offset)
        tz_minutes = int((tz_offset - tz_hours) * 60)
        tz_str = f"{tz_hours:+03d}:{tz_minutes:02d}"
        
        return f"{sunrise_dt.isoformat()}{tz_str}"
        
    except Exception as e:
        print(f"Error parsing sunrise time: {e}")
        # Fallback to default
        return f"{date.replace(hour=6, minute=0).isoformat()}+05:30"

def jd_to_local_datetime(jd: float, city: str) -> datetime:
    """Convert Julian Day to local datetime for a specific city"""
    try:
        # Get timezone offset
        city_coords = get_city_coordinates(city)
        longitude = city_coords.get('longitude', 77.593)
        tz_offset = get_timezone_offset(city, longitude)
        
        # Adjust JD to local time
        local_jd = jd + tz_offset/24.0
        
        # Convert to Gregorian calendar
        cal_date = swe.revjul(local_jd)
        year, month, day, hour_float = cal_date[:4]
        
        hours = int(hour_float)
        minutes = int((hour_float - hours) * 60)
        seconds = int(((hour_float - hours) * 60 - minutes) * 60)
        
        return datetime(int(year), int(month), int(day), hours, minutes, seconds)
        
    except Exception as e:
        print(f"Error converting JD to datetime: {e}")
        return datetime.now()
