"use client";

import { PeriodDetail, PeriodsResponse } from "../types/panchangam";

interface PeriodsDisplayProps {
  data: PeriodsResponse;
}

interface PeriodRowProps {
  periods: PeriodDetail[];
  title: string;
  emoji: string;
  colorClass: string;
}

function PeriodRow({ periods, title, emoji, colorClass }: PeriodRowProps) {
  const formatDateRange = (period: PeriodDetail) => {
    const startDate = new Date(period.start);
    const endDate = new Date(period.end);

    const formatDate = (date: Date) => {
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
      });
    };

    const startDateStr = formatDate(startDate);
    const endDateStr = formatDate(endDate);

    return `${startDateStr}, ${period.start_formatted} – ${endDateStr}, ${period.end_formatted}`;
  };

  return (
    <tr className={`border-b border-gray-200 bg-${colorClass}-25`}>
      <td
        className={`px-6 py-4 bg-${colorClass}-100 font-semibold text-${colorClass}-800 border-r border-gray-200 w-1/4 align-top`}
      >
        {emoji} {title}
      </td>
      <td className="px-6 py-4 text-gray-800 font-medium" colSpan={3}>
        <div className="space-y-2">
          {periods.map((period, index) => (
            <div
              key={index}
              className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
            >
              <span
                className={`text-lg font-semibold text-${colorClass}-700 mb-1 sm:mb-0`}
              >
                {period.name}
              </span>
              <span
                className={`text-sm text-gray-600 bg-${colorClass}-50 px-3 py-1 rounded-full`}
              >
                {formatDateRange(period)}
              </span>
            </div>
          ))}
        </div>
      </td>
    </tr>
  );
}

export default function PeriodsDisplay({ data }: PeriodsDisplayProps) {
  const formatDateTime = (dateTimeStr: string) => {
    const date = new Date(dateTimeStr);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "2-digit",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold mb-2">🕉️ Panchangam Periods</h1>
        <p className="text-xl opacity-90">
          {new Date(data.date).toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
        <p className="text-sm opacity-75 mt-2">
          Latitude: {data.location.latitude}°, Longitude:{" "}
          {data.location.longitude}°
        </p>
        <p className="text-sm opacity-75">
          Hindu Day: {formatDateTime(data.sunrise)} to{" "}
          {formatDateTime(data.sunrise_next)}
        </p>
        <div className="grid grid-cols-2 gap-4 mt-3 text-sm opacity-90">
          <div>
            <span className="font-semibold">☀️ Sun:</span>{" "}
            {formatDateTime(data.sunrise)} - {formatDateTime(data.sunset)}
          </div>
          <div>
            <span className="font-semibold">🌙 Moon:</span>{" "}
            {formatDateTime(data.moonrise)} - {formatDateTime(data.moonset)}
          </div>
        </div>
      </div>

      {/* Periods Table */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-4">
          <h2 className="text-xl font-semibold">📅 All Active Periods</h2>
          <p className="text-sm opacity-90 mt-1">
            Multiple periods may be active during the Hindu day (sunrise to next
            sunrise)
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <tbody>
              {/* Tithis */}
              <PeriodRow
                periods={data.tithis}
                title="Tithi"
                emoji="🌙"
                colorClass="orange"
              />

              {/* Nakshatras */}
              <PeriodRow
                periods={data.nakshatras}
                title="Nakshatra"
                emoji="⭐"
                colorClass="green"
              />

              {/* Karanas */}
              <PeriodRow
                periods={data.karanas}
                title="Karana"
                emoji="🔄"
                colorClass="blue"
              />

              {/* Yogas */}
              <PeriodRow
                periods={data.yogas}
                title="Yoga"
                emoji="🧘"
                colorClass="purple"
              />

              {/* Auspicious Periods */}
              {data.auspicious_periods &&
                data.auspicious_periods.length > 0 && (
                  <PeriodRow
                    periods={data.auspicious_periods}
                    title="Auspicious Periods"
                    emoji="✨"
                    colorClass="yellow"
                  />
                )}

              {/* Inauspicious Periods */}
              {data.inauspicious_periods &&
                data.inauspicious_periods.length > 0 && (
                  <PeriodRow
                    periods={data.inauspicious_periods}
                    title="Inauspicious Periods"
                    emoji="⚠️"
                    colorClass="red"
                  />
                )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Info Note */}
      <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
        <div className="flex">
          <div className="ml-3">
            <p className="text-sm text-blue-700">
              <strong>Note:</strong> This view shows all periods that are active
              during the Hindu day. Multiple periods of the same type may
              overlap, which is normal in traditional Panchangam calculations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
