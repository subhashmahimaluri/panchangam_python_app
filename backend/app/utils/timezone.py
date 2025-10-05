"""
Timezone utility functions for Panchangam calculations
"""
import pytz
from datetime import datetime, timezone
from typing import Dict
from app.utils.constants import CITY_TIMEZONES

def get_timezone_for_city(city: str) -> pytz.BaseTzInfo:
    """
    Get timezone object for a given city
    
    Args:
        city: City name
        
    Returns:
        pytz timezone object
        
    Raises:
        ValueError: If city is not supported
    """
    if city not in CITY_TIMEZONES:
        raise ValueError(f"Timezone not configured for city: {city}")
    
    return pytz.timezone(CITY_TIMEZONES[city])

def utc_to_local(utc_dt: datetime, city: str) -> datetime:
    """
    Convert UTC datetime to local time for given city
    
    Args:
        utc_dt: UTC datetime object
        city: City name
        
    Returns:
        Local datetime object
    """
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    
    local_tz = get_timezone_for_city(city)
    return utc_dt.astimezone(local_tz)

def local_to_utc(local_dt: datetime, city: str) -> datetime:
    """
    Convert local datetime to UTC for given city
    
    Args:
        local_dt: Local datetime object (naive)
        city: City name
        
    Returns:
        UTC datetime object
    """
    local_tz = get_timezone_for_city(city)
    
    # Localize the naive datetime
    localized_dt = local_tz.localize(local_dt)
    
    # Convert to UTC
    return localized_dt.astimezone(timezone.utc)

def format_time_12hour(dt: datetime) -> str:
    """
    Format datetime to 12-hour format string (HH:MM AM/PM)
    
    Args:
        dt: datetime object
        
    Returns:
        Formatted time string
    """
    return dt.strftime("%I:%M %p")

def format_time_24hour(dt: datetime) -> str:
    """
    Format datetime to 24-hour format string (HH:MM)
    
    Args:
        dt: datetime object
        
    Returns:
        Formatted time string
    """
    return dt.strftime("%H:%M")

def get_julian_day_ut(dt: datetime) -> float:
    """
    Convert datetime to Julian Day Number (UT)
    
    Args:
        dt: datetime object in UTC
        
    Returns:
        Julian Day Number
    """
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    
    # Calculate Julian Day Number
    year = dt.year
    month = dt.month
    day = dt.day
    hours = dt.hour + dt.minute/60.0 + dt.second/3600.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    a = int(year / 100)
    b = 2 - a + int(a / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    jd += hours / 24.0
    
    return jd

def julian_day_to_datetime(jd: float, city: str) -> datetime:
    """
    Convert Julian Day Number to datetime in local timezone
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Local datetime object
    """
    # Convert JD to UTC datetime
    jd += 0.5
    z = int(jd)
    f = jd - z
    
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - int(alpha / 4)
    
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    
    day = b - d - int(30.6001 * e)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    
    hours = f * 24
    hour = int(hours)
    minutes = (hours - hour) * 60
    minute = int(minutes)
    seconds = (minutes - minute) * 60
    second = int(seconds)
    
    utc_dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    return utc_to_local(utc_dt, city)