"use client";

import React from "react";
import { CityOption } from "../types/panchangam";

interface CitySelectorProps {
  cities: CityOption[];
  selectedCity: CityOption;
  onCityChange: (city: CityOption) => void;
}

export default function CitySelector({
  cities,
  selectedCity,
  onCityChange,
}: CitySelectorProps) {
  return (
    <div className="flex flex-col space-y-2">
      <label
        htmlFor="city-select"
        className="text-sm font-medium text-gray-700"
      >
        Select City
      </label>
      <select
        id="city-select"
        value={selectedCity.name}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
          const city = cities.find((c) => c.name === e.target.value);
          if (city) onCityChange(city);
        }}
        className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        {cities.map((city) => (
          <option key={city.name} value={city.name}>
            {city.name}
          </option>
        ))}
      </select>
    </div>
  );
}
