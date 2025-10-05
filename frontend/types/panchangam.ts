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
];

// Error response type
export interface ApiError {
  detail: string;
  error?: string;
}
