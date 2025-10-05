"use client";

interface DatePickerProps {
  selectedDate: string;
  onDateChange: (date: string) => void;
}

export default function DatePicker({
  selectedDate,
  onDateChange,
}: DatePickerProps) {
  const today = new Date().toISOString().split("T")[0];

  return (
    <div className="flex flex-col space-y-2">
      <label
        htmlFor="date-picker"
        className="text-sm font-medium text-gray-700"
      >
        Select Date
      </label>
      <input
        id="date-picker"
        type="date"
        value={selectedDate}
        max={today}
        onChange={(e) => onDateChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  );
}
