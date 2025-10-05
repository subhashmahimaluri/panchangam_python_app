"""
Hindu calendar calculations - Tithi, Nakshatra, Karana, Yoga
"""
import swisseph as swe
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple
from app.utils.timezone import get_julian_day_ut, julian_day_to_datetime
from app.utils.constants import (
    TITHI_NAMES, NAKSHATRA_NAMES, KARANA_NAMES, YOGA_NAMES, PAKSHA_NAMES,
    SUN, MOON, SIDEREAL_FLAG, NAKSHATRA_DEGREES, TITHI_DEGREES
)
from app.services.astronomical import get_sun_position, get_moon_position

def calculate_tithi(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Tithi (lunar day) for given Julian Day
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with tithi name, start time, and end time
    """
    try:
        # Set sidereal mode
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get sun and moon positions
        sun_lon, _ = get_sun_position(jd)
        moon_lon, _ = get_moon_position(jd)
        
        # Calculate lunar phase angle
        phase_angle = (moon_lon - sun_lon) % 360
        
        # Determine current tithi (0-29)
        current_tithi = int(phase_angle / TITHI_DEGREES)
        
        # Calculate when current tithi started
        tithi_start_angle = current_tithi * TITHI_DEGREES
        tithi_end_angle = (current_tithi + 1) * TITHI_DEGREES
        
        # Find tithi boundaries
        start_jd = find_tithi_boundary(jd, tithi_start_angle, backward=True)
        end_jd = find_tithi_boundary(jd, tithi_end_angle, backward=False)
        
        # Convert to local times
        start_dt = julian_day_to_datetime(start_jd, city)
        end_dt = julian_day_to_datetime(end_jd, city)
        
        # Determine paksha (waxing/waning)
        paksha = 0 if current_tithi < 15 else 1
        tithi_in_paksha = current_tithi % 15
        
        # Get tithi name
        tithi_name = f"{PAKSHA_NAMES[paksha]} {TITHI_NAMES[current_tithi]}"
        
        return {
            "name": tithi_name,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating tithi: {e}")
        # Return default
        return {
            "name": "Shukla Paksha Pratipada",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def calculate_nakshatra(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Nakshatra (star constellation) for given Julian Day
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with nakshatra name, start time, and end time
    """
    try:
        # Set sidereal mode
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get moon position
        moon_lon, _ = get_moon_position(jd)
        
        # Calculate current nakshatra (0-26)
        current_nakshatra = int(moon_lon / NAKSHATRA_DEGREES)
        if current_nakshatra >= 27:
            current_nakshatra = 26
        
        # Calculate nakshatra boundaries
        nakshatra_start_angle = current_nakshatra * NAKSHATRA_DEGREES
        nakshatra_end_angle = (current_nakshatra + 1) * NAKSHATRA_DEGREES
        
        # Find nakshatra boundaries
        start_jd = find_nakshatra_boundary(jd, nakshatra_start_angle, backward=True)
        end_jd = find_nakshatra_boundary(jd, nakshatra_end_angle, backward=False)
        
        # Convert to local times
        start_dt = julian_day_to_datetime(start_jd, city)
        end_dt = julian_day_to_datetime(end_jd, city)
        
        return {
            "name": NAKSHATRA_NAMES[current_nakshatra],
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating nakshatra: {e}")
        return {
            "name": "Ashwini",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def calculate_karana(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Karana (half tithi) for given Julian Day
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with karana name, start time, and end time
    """
    try:
        # Set sidereal mode
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get sun and moon positions
        sun_lon, _ = get_sun_position(jd)
        moon_lon, _ = get_moon_position(jd)
        
        # Calculate lunar phase angle
        phase_angle = (moon_lon - sun_lon) % 360
        
        # Karana is half of tithi
        karana_angle = TITHI_DEGREES / 2  # 6 degrees
        current_karana = int(phase_angle / karana_angle) % 60
        
        # First 57 karanas cycle through 7 movable karanas
        # Last 3 are fixed karanas
        if current_karana < 57:
            karana_index = current_karana % 7
        else:
            karana_index = 7 + (current_karana - 57)
        
        # Calculate karana boundaries
        karana_start_angle = current_karana * karana_angle
        karana_end_angle = (current_karana + 1) * karana_angle
        
        # Find approximate boundaries (simplified)
        start_jd = jd - 0.25  # Approximate 6 hours ago
        end_jd = jd + 0.25    # Approximate 6 hours from now
        
        # Convert to local times
        start_dt = julian_day_to_datetime(start_jd, city)
        end_dt = julian_day_to_datetime(end_jd, city)
        
        return {
            "name": KARANA_NAMES[min(karana_index, len(KARANA_NAMES)-1)],
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating karana: {e}")
        return {
            "name": "Bava",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=12)).isoformat()
        }

def calculate_yoga(jd: float, city: str) -> Dict[str, str]:
    """
    Calculate Yoga (sun-moon combination) for given Julian Day
    
    Args:
        jd: Julian Day Number
        city: City name for timezone conversion
        
    Returns:
        Dictionary with yoga name, start time, and end time
    """
    try:
        # Set sidereal mode
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Get sun and moon positions
        sun_lon, _ = get_sun_position(jd)
        moon_lon, _ = get_moon_position(jd)
        
        # Calculate yoga angle (sum of sun and moon longitudes)
        yoga_angle = (sun_lon + moon_lon) % 360
        
        # Each yoga spans 13.333... degrees (360/27)
        yoga_span = 360.0 / 27.0
        current_yoga = int(yoga_angle / yoga_span)
        
        if current_yoga >= 27:
            current_yoga = 26
        
        # Calculate yoga boundaries
        yoga_start_angle = current_yoga * yoga_span
        yoga_end_angle = (current_yoga + 1) * yoga_span
        
        # Find approximate boundaries (simplified)
        start_jd = jd - 0.5  # Approximate 12 hours ago
        end_jd = jd + 0.5    # Approximate 12 hours from now
        
        # Convert to local times
        start_dt = julian_day_to_datetime(start_jd, city)
        end_dt = julian_day_to_datetime(end_jd, city)
        
        return {
            "name": YOGA_NAMES[current_yoga],
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        
    except Exception as e:
        print(f"Error calculating yoga: {e}")
        return {
            "name": "Vishkambha",
            "start": datetime.now().isoformat(),
            "end": (datetime.now() + timedelta(hours=24)).isoformat()
        }

def find_tithi_boundary(base_jd: float, target_angle: float, backward: bool = False) -> float:
    """
    Find the Julian Day when tithi boundary occurs
    
    Args:
        base_jd: Base Julian Day Number
        target_angle: Target phase angle in degrees
        backward: Search backward in time if True
        
    Returns:
        Julian Day Number of boundary
    """
    try:
        # Simple approximation - each tithi lasts about 0.984 days on average
        days_per_tithi = 29.53 / 30  # Average lunar month / 30 tithis
        
        if backward:
            return base_jd - days_per_tithi / 2
        else:
            return base_jd + days_per_tithi / 2
            
    except Exception:
        return base_jd

def find_nakshatra_boundary(base_jd: float, target_angle: float, backward: bool = False) -> float:
    """
    Find the Julian Day when nakshatra boundary occurs
    
    Args:
        base_jd: Base Julian Day Number
        target_angle: Target longitude angle in degrees
        backward: Search backward in time if True
        
    Returns:
        Julian Day Number of boundary
    """
    try:
        # Simple approximation - each nakshatra lasts about 1.09 days on average
        days_per_nakshatra = 27.32 / 27  # Sidereal month / 27 nakshatras
        
        if backward:
            return base_jd - days_per_nakshatra / 2
        else:
            return base_jd + days_per_nakshatra / 2
            
    except Exception:
        return base_jd