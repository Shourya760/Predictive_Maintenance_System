import ReadingField from "./ReadingField";

const fields = [
  { name: "Oil_Level_pct", label: "Oil level", unit: "%", min: 0, max: 100, slider: true, warn: 50, critical: 25, bad: "low" },
  { name: "Coolant_Level_pct", label: "Coolant level", unit: "%", min: 0, max: 100, slider: true, warn: 50, critical: 25, bad: "low" },
  { name: "Error_Codes_Last_30_Days", label: "Error codes (30 days)", unit: "count", min: 0, max: 100 },
];

function FluidReadings({ data, setValue }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {fields.map((field) => <ReadingField
        key={field.name}
        field={field}
        value={data[field.name]}
        setValue={setValue} />)}
    </div>
  );
}

export default FluidReadings;
