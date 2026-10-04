import ReadingField from "./ReadingField";

const fields = [
  { name: "Installation_Year", label: "Installation year", unit: "year", min: 1980, max: 2026 },
  { name: "Operational_Hours", label: "Operating hours", unit: "hours", min: 0, max: 200000, step: 500 },
  { name: "Last_Maintenance_Days_Ago", label: "Days since service", unit: "days", min: 0, max: 3000, step: 10 },
  { name: "Maintenance_History_Count", label: "Services completed", unit: "count", min: 0, max: 200 },
  { name: "Failure_History_Count", label: "Past failures", unit: "count", min: 0, max: 200 },
];

function MachineHistory({ data, setValue }) {
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

export default MachineHistory;
