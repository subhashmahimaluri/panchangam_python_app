"use client";

import { PanchangamData } from "../types/panchangam";

interface PanchangamDisplayProps {
  data: PanchangamData;
}

export default function PanchangamDisplay({ data }: PanchangamDisplayProps) {
  const formatDateTime = (dateTimeStr: string) => {
    const date = new Date(dateTimeStr);
    const monthNames = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];

    const month = monthNames[date.getMonth()];
    const day = String(date.getDate()).padStart(2, "0");
    const hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const ampm = hours >= 12 ? "PM" : "AM";
    const displayHours = hours % 12 || 12;

    return `${month} ${day}, ${String(displayHours).padStart(
      2,
      "0"
    )}:${minutes} ${ampm}`;
  };

  const formatTime = (time: string) => {
    // If already formatted (contains AM/PM), return as is
    if (time.includes("AM") || time.includes("PM")) {
      return time;
    }
    // Otherwise, assume it's in 24-hour format and convert
    const [hours, minutes] = time.split(":");
    const hour24 = parseInt(hours, 10);
    const hour12 = hour24 === 0 ? 12 : hour24 > 12 ? hour24 - 12 : hour24;
    const ampm = hour24 >= 12 ? "PM" : "AM";
    return `${hour12}:${minutes} ${ampm}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold mb-2">
          🕉️ Panchangam for {data.location.city}
        </h1>
        <p className="text-xl opacity-90">
          {new Date(data.date).toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      </div>

      {/* Main Panchangam Table */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-4">
          <h2 className="text-xl font-semibold">📅 Panchangam Details</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <tbody>
              {/* Sun & Moon Times Row */}
              <tr className="border-b border-gray-200">
                <td className="px-6 py-4 bg-yellow-50 font-semibold text-yellow-800 border-r border-gray-200">
                  ☀️ Sunrise
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium border-r border-gray-200">
                  {data.sunrise}
                </td>
                <td className="px-6 py-4 bg-orange-50 font-semibold text-orange-800 border-r border-gray-200">
                  🌅 Sunset
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium">
                  {data.sunset}
                </td>
              </tr>

              <tr className="border-b border-gray-200">
                <td className="px-6 py-4 bg-blue-50 font-semibold text-blue-800 border-r border-gray-200">
                  🌙 Moonrise
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium border-r border-gray-200">
                  {data.moonrise}
                </td>
                <td className="px-6 py-4 bg-purple-50 font-semibold text-purple-800 border-r border-gray-200">
                  🌑 Moonset
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium">
                  {data.moonset}
                </td>
              </tr>

              {/* Tithi */}
              <tr className="border-b border-gray-200 bg-orange-25">
                <td className="px-6 py-4 bg-orange-100 font-semibold text-orange-800 border-r border-gray-200 w-1/4">
                  🌙 Tithi
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium" colSpan={3}>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <span className="text-lg font-semibold text-orange-700 mb-1 sm:mb-0">
                      {data.tithi.name}
                    </span>
                    <span className="text-sm text-gray-600 bg-orange-50 px-3 py-1 rounded-full">
                      {formatDateTime(data.tithi.start)} –{" "}
                      {formatDateTime(data.tithi.end)}
                    </span>
                  </div>
                </td>
              </tr>

              {/* Nakshatra */}
              <tr className="border-b border-gray-200">
                <td className="px-6 py-4 bg-green-100 font-semibold text-green-800 border-r border-gray-200 w-1/4">
                  ⭐ Nakshatra
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium" colSpan={3}>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <span className="text-lg font-semibold text-green-700 mb-1 sm:mb-0">
                      {data.nakshatra.name}
                    </span>
                    <span className="text-sm text-gray-600 bg-green-50 px-3 py-1 rounded-full">
                      {formatDateTime(data.nakshatra.start)} –{" "}
                      {formatDateTime(data.nakshatra.end)}
                    </span>
                  </div>
                </td>
              </tr>

              {/* Karana */}
              <tr className="border-b border-gray-200">
                <td className="px-6 py-4 bg-blue-100 font-semibold text-blue-800 border-r border-gray-200 w-1/4">
                  🔄 Karana
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium" colSpan={3}>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <span className="text-lg font-semibold text-blue-700 mb-1 sm:mb-0">
                      {data.karana.name}
                    </span>
                    <span className="text-sm text-gray-600 bg-blue-50 px-3 py-1 rounded-full">
                      {formatDateTime(data.karana.start)} –{" "}
                      {formatDateTime(data.karana.end)}
                    </span>
                  </div>
                </td>
              </tr>

              {/* Yoga */}
              <tr className="border-b border-gray-200">
                <td className="px-6 py-4 bg-purple-100 font-semibold text-purple-800 border-r border-gray-200 w-1/4">
                  🧘 Yoga
                </td>
                <td className="px-6 py-4 text-gray-800 font-medium" colSpan={3}>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <span className="text-lg font-semibold text-purple-700 mb-1 sm:mb-0">
                      {data.yoga.name}
                    </span>
                    <span className="text-sm text-gray-600 bg-purple-50 px-3 py-1 rounded-full">
                      {formatDateTime(data.yoga.start)} –{" "}
                      {formatDateTime(data.yoga.end)}
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Auspicious & Inauspicious Periods */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Auspicious Periods */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-4">
            <h2 className="text-xl font-semibold">✨ Auspicious Periods</h2>
          </div>
          <div className="p-4">
            <table className="w-full">
              <tbody>
                <tr className="border-b border-gray-200">
                  <td className="py-3 pr-4 font-semibold text-green-800">
                    🌅 Brahma Muhurat
                  </td>
                  <td className="py-3 text-green-600 font-medium">
                    {formatTime(data.auspicious_periods.brahma_muhurat.start)} -{" "}
                    {formatTime(data.auspicious_periods.brahma_muhurat.end)}
                  </td>
                </tr>
                <tr className="border-b border-gray-200">
                  <td className="py-3 pr-4 font-semibold text-green-800">
                    ⚡ Abhijit Muhurat
                  </td>
                  <td className="py-3 text-green-600 font-medium">
                    {formatTime(data.auspicious_periods.abhijit_muhurat.start)}{" "}
                    - {formatTime(data.auspicious_periods.abhijit_muhurat.end)}
                  </td>
                </tr>
                <tr>
                  <td className="py-3 pr-4 font-semibold text-green-800">
                    🌇 Pradosha Time
                  </td>
                  <td className="py-3 text-green-600 font-medium">
                    {formatTime(data.auspicious_periods.pradosha_time.start)} -{" "}
                    {formatTime(data.auspicious_periods.pradosha_time.end)}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Inauspicious Periods */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-red-500 to-pink-500 text-white p-4">
            <h2 className="text-xl font-semibold">⚠️ Inauspicious Periods</h2>
          </div>
          <div className="p-4">
            <table className="w-full">
              <tbody>
                <tr className="border-b border-gray-200">
                  <td className="py-3 pr-4 font-semibold text-red-800">
                    🐍 Rahu Kalam
                  </td>
                  <td className="py-3 text-red-600 font-medium">
                    {formatTime(data.inauspicious_periods.rahu.start)} -{" "}
                    {formatTime(data.inauspicious_periods.rahu.end)}
                  </td>
                </tr>
                <tr className="border-b border-gray-200">
                  <td className="py-3 pr-4 font-semibold text-red-800">
                    🔥 Gulika Kalam
                  </td>
                  <td className="py-3 text-red-600 font-medium">
                    {formatTime(data.inauspicious_periods.gulika.start)} -{" "}
                    {formatTime(data.inauspicious_periods.gulika.end)}
                  </td>
                </tr>
                <tr
                  className={
                    data.inauspicious_periods.varjyam.length > 0
                      ? "border-b border-gray-200"
                      : ""
                  }
                >
                  <td className="py-3 pr-4 font-semibold text-red-800">
                    💀 Yamaganda
                  </td>
                  <td className="py-3 text-red-600 font-medium">
                    {formatTime(data.inauspicious_periods.yamaganda.start)} -{" "}
                    {formatTime(data.inauspicious_periods.yamaganda.end)}
                  </td>
                </tr>
                {data.inauspicious_periods.varjyam.length > 0 && (
                  <tr>
                    <td className="py-3 pr-4 font-semibold text-red-800">
                      ⛔ Varjyam
                    </td>
                    <td className="py-3 text-red-600 font-medium">
                      {data.inauspicious_periods.varjyam.map(
                        (period, index) => (
                          <div key={index}>
                            {formatTime(period.start)} -{" "}
                            {formatTime(period.end)}
                          </div>
                        )
                      )}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
