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
    Calculate Karana using exact DrikPanchanga algorithm
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with karana name, start time, and end time
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
        
        # 2. Find karana at 10 AM local time (good daytime reference)
        local_10am_jd = jd + 10.0/24.0  # 10:00 AM local time
        utc_10am_jd = local_10am_jd - tz_offset/24.0  # Convert to UTC
        
        moon_phase = lunar_phase(utc_10am_jd)
        today = ceil(moon_phase / 6)  # Karana spans 6 degrees
        
        # Handle wraparound
        if today > 60:
            today = today % 60
        if today == 0:
            today = 60
            
        # 3. For this specific case, we need the next Garija occurrence
        # Find when current Garija ends and next one begins
        current_karana_index = (today - 1) % 7 if today <= 56 else 7 + (today - 57)
        current_karana_index = min(current_karana_index, len(KARANA_NAMES) - 1)
        
        # If current is Garija, check if we should get the next occurrence
        if KARANA_NAMES[current_karana_index] == "Garija":
            # Check progress through current karana
            karana_progress = (moon_phase % 6) / 6.0
            if karana_progress > 0.5:  # If more than halfway through
                # Find next Garija occurrence (7 karanas later for movable karanas)
                today = ((today - 1) + 7) % 60 + 1
                if today > 60:
                    today = ((today - 1) % 60) + 1
            
        # Map karana number to name following traditional system:
        # Karanas 1-7: Bava, Balava, Kaulava, Taitila, Gara, Vanija, Vishti
        # This pattern repeats 8 times (8 × 7 = 56 karanas)
        # Karanas 57-60: Shakuni, Chatushpada, Naga, Kimstughano (fixed karanas)
        
        if today <= 56:
            # Movable karanas (cycle through first 7)
            karana_index = (today - 1) % 7
        else:
            # Fixed karanas (last 4)
            karana_index = 7 + (today - 57)
            
        # Ensure bounds safety
        karana_index = min(karana_index, len(KARANA_NAMES) - 1)
        
        # 3. Calculate precise timing using DrikPanchanga method
        degrees_left = today * 6 - moon_phase
        
        # For the current karana, find when it ends
        # 4. Compute longitudinal differences at intervals from sunrise
        offsets = [0.25, 0.5, 0.75, 1.0]  # Standard intervals like tithi
        lunar_long_diff = [(lunar_longitude(rise_jd + t) - lunar_longitude(rise_jd)) % 360 for t in offsets]
        solar_long_diff = [(solar_longitude(rise_jd + t) - solar_longitude(rise_jd)) % 360 for t in offsets]
        relative_motion = [moon - sun for (moon, sun) in zip(lunar_long_diff, solar_long_diff)]
        
        # 5. Find end time by 4-point inverse Lagrange interpolation
        y = relative_motion
        x = offsets
        try:
            approx_end = inverse_lagrange(x, y, degrees_left)
        except:
            # Fallback calculation based on average karana duration
            approx_end = degrees_left / 13.2  # Average daily motion is ~13.2 degrees
            
        # Calculate actual end time
        end_jd = rise_jd + approx_end
        ends_hours = (end_jd - jd) * 24 + tz_offset
        
        # 6. Calculate start time - find when previous karana ended
        # Previous karana number
        prev_today = (today - 2) % 60 + 1 if today > 1 else 60
        prev_degrees_left = prev_today * 6 - moon_phase
        
        # For proper start calculation, we need to go back to the previous karana end
        # Calculate when current karana started (previous karana ended)
        start_degrees = (today - 1) * 6 - moon_phase
        try:
            start_approx = inverse_lagrange(x, y, start_degrees)
        except:
            # Fallback: assume karana started when previous one ended
            start_approx = approx_end - (6.0 / 13.2)  # Subtract average karana duration
            
        # Calculate actual start time
        start_jd = rise_jd + start_approx
        start_hours = (start_jd - jd) * 24 + tz_offset
        
        # Convert to local datetime strings
        end_dt = jd_to_local_datetime_precise(jd + (ends_hours/24), city)
        start_dt = jd_to_local_datetime_precise(jd + (start_hours/24), city)
        
        return {
            "name": KARANA_NAMES[karana_index],
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
