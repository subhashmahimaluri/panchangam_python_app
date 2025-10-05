"""
Constants used in Panchangam calculations
"""

# Tithi names (Lunar day names)
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

# Nakshatra names (Star constellation names)
NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Karana names (Half-tithi names)
# There are 60 karanas total:
# 7 movable karanas repeat 8 times (56 total): Bava, Balava, Kaulava, Taitila, Gara, Vanija, Vishti
# 4 fixed karanas (57-60): Shakuni, Chatushpada, Naga, Kimstughno
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti",  # 0-6: movable karanas
    "Shakuni", "Chatushpada", "Naga", "Kimstughno"  # 7-10: fixed karanas
]

# Yoga names (Solar-Lunar combination names)
YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarman", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

# Paksha (Lunar fortnight) prefixes
PAKSHA_NAMES = {
    0: "Shukla Paksha",  # Waxing moon
    1: "Krishna Paksha"  # Waning moon
}

# Swiss Ephemeris planet constants
SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
URANUS = 7
NEPTUNE = 8
PLUTO = 9
MEAN_NODE = 10
TRUE_NODE = 11

# Time zones for cities
CITY_TIMEZONES = {
    "Bengaluru": "Asia/Kolkata",
    "Coventry": "Europe/London",
    "New York": "America/New_York",
    "Lima": "America/Lima",
    "Harare": "Africa/Harare",
    "Canberra": "Australia/Canberra"
}

# Degrees per Nakshatra (360/27)
NAKSHATRA_DEGREES = 13.333333333333334

# Degrees per Tithi (360/30)
TITHI_DEGREES = 12.0

# Standard calculation flags for Swiss Ephemeris
SIDEREAL_FLAG = 256  # SEFLG_SIDEREAL
SPEED_FLAG = 2      # SEFLG_SPEED