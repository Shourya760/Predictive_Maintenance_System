import "./ReadingField.css";

const statusClass = {
  normal:
    "rounded-full border border-green-200 bg-green-50 px-2 py-0.5 text-[11px] font-semibold text-green-700",
  watch:
    "rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-700",
  critical:
    "rounded-full border border-red-200 bg-red-50 px-2 py-0.5 text-[11px] font-semibold text-red-700",
};

function ReadingField({ field, value, setValue }) {
  const { name, label, unit, min, max, step = 1, slider, warn, critical, bad } =
    field;
  const updateValue = (e) => setValue(name, e.target.value);
  const isBad = (threshold) =>
    bad === "low"
      ? Number(value) <= threshold
      : Number(value) >= threshold;
  const status =
    warn === undefined
      ? null
      : isBad(critical)
        ? "critical"
        : isBad(warn)
          ? "watch"
          : "normal";
  const getPoint = (value) => ((value - min) / (max - min)) * 100;
  const sliderStyle =
    warn === undefined
      ? {}
      : {
        background:
          bad === "low"
            ? `linear-gradient(
                  90deg,
                  #dc2626 0% ${getPoint(critical)}%,
                  #f59e0b ${getPoint(critical)}% ${getPoint(warn)}%,
                  #16a34a ${getPoint(warn)}% 100%
                )`
            : `linear-gradient(
                  90deg,
                  #16a34a 0% ${getPoint(warn)}%,
                  #f59e0b ${getPoint(warn)}% ${getPoint(critical)}%,
                  #dc2626 ${getPoint(critical)}% 100%
                )`,
      };

  const statusText = {
    normal: "Normal",
    watch: "Watch",
    critical: "Critical",
  };

  return (
    <label className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm font-medium text-slate-700">
      <span className="mb-2 flex items-center justify-between gap-2">
        <span>{label}</span>

        <span className="flex items-center gap-2">
          <span className="text-xs font-normal text-slate-400">
            {unit}
          </span>

          {status && (
            <span className={statusClass[status]}>
              {statusText[status]}
            </span>
          )}
        </span>
      </span>

      <input
        type="number"
        required
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={updateValue}
        className="min-w-0 w-full rounded-lg border border-slate-300 bg-white px-2 py-2 text-center text-slate-900 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
      />

      {slider && (
        <>
          <input
            type="range"
            aria-label={`${label} slider`}
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={updateValue}
            className="reading-slider mt-3"
            style={sliderStyle}
          />

          <span className="mt-1 flex justify-between text-[11px] font-normal text-slate-400">
            <span>{min}</span>
            <span>{max}</span>
          </span>
        </>
      )}
    </label>
  );
}

export default ReadingField;