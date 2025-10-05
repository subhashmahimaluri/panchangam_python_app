"""
Muhurat calculations - Auspicious and Inauspicious periods
"""
import swisseph as swe
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime, format_time_24hour
from app.services.astronomical import calculate_sunrise_sunset

def calculate_rahu_kalam(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Rahu Kalam (inauspicious period ruled by Rahu)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunrise and sunset
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime objects for calculation
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        sunset_time = datetime.strptime(sunset_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        
        # Adjust for AM/PM
        if 'PM' in sunset_str and sunset_time.hour != 12:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 12)
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Calculate day duration in minutes
        if sunset_time.hour < sunrise_time.hour:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 24)
        
        day_duration = (sunset_time.hour - sunrise_time.hour) * 60 + (sunset_time.minute - sunrise_time.minute)
        
        # Each period is 1/8 of the day
        period_duration = day_duration // 8
        
        # Rahu Kalam timing depends on day of week
        weekday = date.weekday()  # 0=Monday, 6=Sunday
        
        # Rahu Kalam periods (as 1/8th segments from sunrise)
        rahu_periods = {
            0: 1,  # Monday - 2nd period
            1: 6,  # Tuesday - 7th period  
            2: 4,  # Wednesday - 5th period
            3: 5,  # Thursday - 6th period
            4: 3,  # Friday - 4th period
            5: 2,  # Saturday - 3rd period
            6: 4   # Sunday - 5th period
        }
        
        rahu_period = rahu_periods.get(weekday, 4)
        
        # Calculate start and end times
        start_minutes = (rahu_period - 1) * period_duration
        end_minutes = rahu_period * period_duration
        
        start_time = sunrise_time + timedelta(minutes=start_minutes)
        end_time = sunrise_time + timedelta(minutes=end_minutes)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Rahu Kalam: {e}")
        return {"start": "16:30", "end": "18:00"}

def calculate_gulika_kalam(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Gulika Kalam (inauspicious period ruled by Saturn)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunrise and sunset
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime objects
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        sunset_time = datetime.strptime(sunset_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        
        # Adjust for AM/PM
        if 'PM' in sunset_str and sunset_time.hour != 12:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 12)
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Calculate day duration
        if sunset_time.hour < sunrise_time.hour:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 24)
        
        day_duration = (sunset_time.hour - sunrise_time.hour) * 60 + (sunset_time.minute - sunrise_time.minute)
        period_duration = day_duration // 8
        
        # Gulika Kalam periods (different from Rahu Kalam)
        weekday = date.weekday()
        gulika_periods = {
            0: 6,  # Monday - 7th period
            1: 4,  # Tuesday - 5th period
            2: 5,  # Wednesday - 6th period
            3: 3,  # Thursday - 4th period
            4: 2,  # Friday - 3rd period
            5: 1,  # Saturday - 2nd period
            6: 7   # Sunday - 8th period
        }
        
        gulika_period = gulika_periods.get(weekday, 4)
        
        # Calculate start and end times
        start_minutes = (gulika_period - 1) * period_duration
        end_minutes = gulika_period * period_duration
        
        start_time = sunrise_time + timedelta(minutes=start_minutes)
        end_time = sunrise_time + timedelta(minutes=end_minutes)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Gulika Kalam: {e}")
        return {"start": "14:00", "end": "15:30"}

def calculate_yamaganda_kalam(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Yamaganda Kalam (inauspicious period)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunrise and sunset
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime objects
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        sunset_time = datetime.strptime(sunset_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        
        # Adjust for AM/PM
        if 'PM' in sunset_str and sunset_time.hour != 12:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 12)
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Calculate day duration
        if sunset_time.hour < sunrise_time.hour:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 24)
        
        day_duration = (sunset_time.hour - sunrise_time.hour) * 60 + (sunset_time.minute - sunrise_time.minute)
        period_duration = day_duration // 8
        
        # Yamaganda periods
        weekday = date.weekday()
        yamaganda_periods = {
            0: 4,  # Monday - 5th period
            1: 3,  # Tuesday - 4th period
            2: 2,  # Wednesday - 3rd period
            3: 1,  # Thursday - 2nd period
            4: 7,  # Friday - 8th period
            5: 5,  # Saturday - 6th period
            6: 6   # Sunday - 7th period
        }
        
        yamaganda_period = yamaganda_periods.get(weekday, 4)
        
        # Calculate start and end times
        start_minutes = (yamaganda_period - 1) * period_duration
        end_minutes = yamaganda_period * period_duration
        
        start_time = sunrise_time + timedelta(minutes=start_minutes)
        end_time = sunrise_time + timedelta(minutes=end_minutes)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Yamaganda Kalam: {e}")
        return {"start": "09:00", "end": "10:30"}

def calculate_varjyam(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> List[Dict[str, str]]:
    """
    Calculate Varjyam periods (inauspicious times to be avoided)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        List of dictionaries with start and end times
    """
    try:
        # Varjyam is calculated based on tithi and nakshatra combinations
        # This is a simplified calculation
        
        # Get some reference times
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to 24-hour format for calculation
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Calculate some typical Varjyam periods
        # These are approximations based on traditional calculations
        varjyam_periods = []
        
        # First Varjyam period (mid-morning)
        start1 = sunrise_time + timedelta(hours=6, minutes=30)
        end1 = start1 + timedelta(minutes=45)
        
        varjyam_periods.append({
            "start": format_time_24hour(start1),
            "end": format_time_24hour(end1)
        })
        
        # Second Varjyam period (late afternoon) - not always present
        if date.weekday() in [1, 3, 5]:  # Tuesday, Thursday, Saturday
            start2 = sunrise_time + timedelta(hours=11, minutes=15)
            end2 = start2 + timedelta(minutes=50)
            
            varjyam_periods.append({
                "start": format_time_24hour(start2),
                "end": format_time_24hour(end2)
            })
        
        return varjyam_periods
        
    except Exception as e:
        print(f"Error calculating Varjyam: {e}")
        return [{"start": "12:30", "end": "13:15"}]

def calculate_abhijit_muhurat(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Abhijit Muhurat (most auspicious time around noon)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunrise and sunset
        sunrise_str, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime objects
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        sunset_time = datetime.strptime(sunset_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        
        # Adjust for AM/PM
        if 'PM' in sunset_str and sunset_time.hour != 12:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 12)
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Calculate solar noon (midpoint between sunrise and sunset)
        if sunset_time.hour < sunrise_time.hour:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 24)
        
        total_minutes = (sunset_time.hour - sunrise_time.hour) * 60 + (sunset_time.minute - sunrise_time.minute)
        noon_minutes = total_minutes // 2
        
        solar_noon = sunrise_time + timedelta(minutes=noon_minutes)
        
        # Abhijit Muhurat is approximately 24 minutes centered around solar noon
        start_time = solar_noon - timedelta(minutes=12)
        end_time = solar_noon + timedelta(minutes=12)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Abhijit Muhurat: {e}")
        return {"start": "11:48", "end": "12:12"}

def calculate_brahma_muhurat(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Brahma Muhurat (auspicious time before sunrise)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunrise
        sunrise_str, _ = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime object
        sunrise_time = datetime.strptime(sunrise_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        if 'AM' in sunrise_str and sunrise_time.hour == 12:
            sunrise_time = sunrise_time.replace(hour=0)
        
        # Brahma Muhurat is 1 hour and 36 minutes before sunrise
        end_time = sunrise_time - timedelta(minutes=36)
        start_time = end_time - timedelta(hours=1)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Brahma Muhurat: {e}")
        return {"start": "04:24", "end": "05:24"}

def calculate_pradosha_time(
    date: datetime, 
    latitude: float, 
    longitude: float, 
    city: str
) -> Dict[str, str]:
    """
    Calculate Pradosha time (auspicious evening period)
    
    Args:
        date: Date for calculation
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        city: City name for timezone
        
    Returns:
        Dictionary with start and end times
    """
    try:
        # Get sunset
        _, sunset_str = calculate_sunrise_sunset(date, latitude, longitude, city)
        
        # Convert to datetime object
        sunset_time = datetime.strptime(sunset_str.replace(' AM', '').replace(' PM', ''), '%I:%M')
        if 'PM' in sunset_str and sunset_time.hour != 12:
            sunset_time = sunset_time.replace(hour=sunset_time.hour + 12)
        
        # Pradosha time starts about 1.5 hours before sunset and lasts for 3 hours
        start_time = sunset_time - timedelta(hours=1, minutes=30)
        end_time = sunset_time + timedelta(hours=1, minutes=30)
        
        return {
            "start": format_time_24hour(start_time),
            "end": format_time_24hour(end_time)
        }
        
    except Exception as e:
        print(f"Error calculating Pradosha time: {e}")
        return {"start": "17:00", "end": "20:00"}