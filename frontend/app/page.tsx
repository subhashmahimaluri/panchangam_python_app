"use client";
"use client";

import { useEffect, useState } from "react";
import CitySelector from "../components/CitySelector";
import DatePicker from "../components/DatePicker";
import PanchangamDisplay from "../components/PanchangamDisplay";
import { CITIES, CityOption, PanchangamData } from "../types/panchangam";
import {
  checkApiHealth,
  fetchPanchangamData,
  fetchSupportedCities,
} from "../utils/api";

export default function HomePage() {
  const [panchangamData, setPanchangamData] = useState<PanchangamData | null>(
    null
  );
  const [cities, setCities] = useState<CityOption[]>(CITIES); // Initialize with default cities
  const [selectedCity, setSelectedCity] = useState<CityOption>(CITIES[0]); // Default to Bengaluru
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split("T")[0] // Today's date in YYYY-MM-DD format
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiHealthy, setApiHealthy] = useState<boolean>(false);

  // Check API health and load cities on component mount
  useEffect(() => {
    const initializeApp = async () => {
      const healthy = await checkApiHealth();
      setApiHealthy(healthy);

      if (healthy) {
        try {
          const citiesResponse = await fetchSupportedCities();
          if (citiesResponse?.cities && Array.isArray(citiesResponse.cities)) {
            const cityOptions: CityOption[] = citiesResponse.cities.map(
              (city: any) => ({
                name: city.name,
                latitude: city.latitude,
                longitude: city.longitude,
              })
            );
            setCities(cityOptions);
            // Update selected city if it's not in the new list
            if (!cityOptions.find((c) => c.name === selectedCity.name)) {
              setSelectedCity(cityOptions[0]);
            }
          }
        } catch (error) {
          console.error(
            "Failed to load cities from backend, using default cities:",
            error
          );
          // Keep using default CITIES array
        }
      }
    };

    initializeApp();
  }, []);

  // Fetch Panchangam data when city or date changes
  useEffect(() => {
    if (apiHealthy) {
      fetchData();
    }
  }, [selectedCity, selectedDate, apiHealthy]);

  const fetchData = async () => {
    if (!selectedCity || !selectedDate) return;

    setLoading(true);
    setError(null);

    try {
      const data = await fetchPanchangamData({
        date: selectedDate,
        latitude: selectedCity.latitude,
        longitude: selectedCity.longitude,
        city: selectedCity.name,
      });
      setPanchangamData(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to fetch Panchangam data"
      );
      console.error("Error fetching Panchangam data:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!apiHealthy) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50 p-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-orange-800 mb-8">
            🕉️ Panchangam Calendar
          </h1>
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <strong>Backend API is not available!</strong>
            <p className="mt-2">
              Please ensure the backend server is running on
              http://localhost:8000
            </p>
            <p className="text-sm mt-1">
              Run:{" "}
              <code className="bg-red-200 px-1 rounded">
                cd backend && python run_server.py
              </code>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-yellow-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-orange-800 mb-2">
            🕉️ Panchangam Calendar
          </h1>
          <p className="text-orange-600">
            Daily Hindu Calendar with Astronomical Calculations
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-center">
            <div className="flex flex-col">
              <label className="text-sm font-medium text-gray-700 mb-1">
                Select City
              </label>
              <CitySelector
                cities={cities}
                selectedCity={selectedCity}
                onCityChange={setSelectedCity}
              />
            </div>
            <div className="flex flex-col">
              <label className="text-sm font-medium text-gray-700 mb-1">
                Select Date
              </label>
              <DatePicker
                selectedDate={selectedDate}
                onDateChange={setSelectedDate}
              />
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600"></div>
            <p className="mt-2 text-orange-600">Loading Panchangam data...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Panchangam Data */}
        {panchangamData && !loading && (
          <PanchangamDisplay data={panchangamData} />
        )}
      </div>
    </div>
  );
}
