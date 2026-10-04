import ReadingField from "./ReadingField";

const fields = [
  { name: "Temperature_C", label: "Temperature", unit: "°C", min: 0, max: 150, step: 0.5, slider: true, warn: 70, critical: 100, bad: "high" },
  { name: "Vibration_mms", label: "Vibration", unit: "mm/s", min: 0, max: 50, step: 0.1, slider: true, warn: 4.5, critical: 11, bad: "high" },
  { name: "Sound_dB", label: "Sound level", unit: "dB", min: 30, max: 140, slider: true, warn: 80, critical: 100, bad: "high" },
  { name: "Power_Consumption_kW", label: "Power draw", unit: "kW", min: 0, max: 300, step: 0.5, slider: true, warn: 100, critical: 200, bad: "high" },
];

function SensorReadings({ data, setValue }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {fields.map((field) => <ReadingField key={field.name} field={field} value={data[field.name]} setValue={setValue} />)}
    </div>
  );
}

export default SensorReadings;
