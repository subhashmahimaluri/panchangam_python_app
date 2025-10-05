// Types for Panchangam API data structures

export interface Location {
  city: string;
  latitude: number;
  longitude: number;
}

export interface PeriodTime {
  name: string;
  start: string; // ISO string format
  end: string; // ISO string format
}

export interface SimpleTime {
  start: string; // "HH:MM" format
  end: string; // "HH:MM" format
}

export interface InauspiciousPeriods {
  rahu: SimpleTime;
  gulika: SimpleTime;
  yamaganda: SimpleTime;
  varjyam: SimpleTime[];
}

export interface AuspiciousPeriods {
  abhijit_muhurat: SimpleTime;
  brahma_muhurat: SimpleTime;
  pradosha_time: SimpleTime;
}

export interface PanchangamData {
  location: Location;
  date: string; // ISO date format (YYYY-MM-DD)
  sunrise: string; // "HH:MM AM/PM" format
  sunset: string; // "HH:MM AM/PM" format
  moonrise: string; // "HH:MM AM/PM" format
  moonset: string; // "HH:MM AM/PM" format
  tithi: PeriodTime;
  nakshatra: PeriodTime;
  karana: PeriodTime;
  yoga: PeriodTime;
  inauspicious_periods: InauspiciousPeriods;
  auspicious_periods: AuspiciousPeriods;
}

export interface PanchangamRequest {
  date: string; // ISO date format (YYYY-MM-DD)
  latitude: number;
  longitude: number;
  city: string;
}

export interface PanchangamResponse extends PanchangamData {}

// New types for the periods API
export interface PeriodDetail {
  name: string;
  start: string; // ISO string format
  end: string; // ISO string format
  start_formatted: string; // "HH:MM AM/PM" format
  end_formatted: string; // "HH:MM AM/PM" format
}

export interface PeriodRequest {
  date: string; // ISO date format (YYYY-MM-DD)
  latitude: number;
  longitude: number;
}

export interface PeriodsResponse {
  date: string; // ISO date format (YYYY-MM-DD)
  location: {
    latitude: number;
    longitude: number;
  };
  sunrise: string; // ISO string format with timezone
  sunset: string; // ISO string format with timezone
  moonrise: string; // ISO string format with timezone
  moonset: string; // ISO string format with timezone
  sunrise_next: string; // ISO string format with timezone
  hindu_day_start?: string; // ISO string format with timezone
  hindu_day_end?: string; // ISO string format with timezone
  tithis: PeriodDetail[];
  nakshatras: PeriodDetail[];
  karanas: PeriodDetail[];
  yogas: PeriodDetail[];
  auspicious_periods?: PeriodDetail[];
  inauspicious_periods?: PeriodDetail[];
}

// City options for the dropdown
export interface CityOption {
  name: string;
  latitude: number;
  longitude: number;
}

export const CITIES: CityOption[] = [
  {
    name: "Bengaluru",
    latitude: 12.9719,
    longitude: 77.593,
  },
  {
    name: "Coventry",
    latitude: 52.40656,
    longitude: -1.51217,
  },
  {
    name: "New York",
    latitude: 40.7128,
    longitude: -74.006,
  },
  {
    name: "Lima",
    latitude: -12.0464,
    longitude: -77.0428,
  },
  {
    name: "Harare",
    latitude: -17.8292,
    longitude: 31.0522,
  },
  {
    name: "Canberra",
    latitude: -35.2809,
    longitude: 149.13,
  },
];

// Error response type
export interface ApiError {
  detail: string;
  error?: string;
}
