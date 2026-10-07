import { useState } from "react";

import SensorReadings from "./SensorReadings";
import FluidReadings from "./FluidReadings";
import MachineHistory from "./MachineHistory";
import Result from "./Result";



const initialData = {
  Installation_Year: 2018,
  Operational_Hours: 8500,
  Temperature_C: 82.5,
  Vibration_mms: 4.2,
  Sound_dB: 78,
  Oil_Level_pct: 45,
  Coolant_Level_pct: 60,
  Power_Consumption_kW: 15.2,
  Last_Maintenance_Days_Ago: 120,
  Maintenance_History_Count: 5,
  Failure_History_Count: 2,
  Error_Codes_Last_30_Days: 3,
};

const steps = [
  {
    title: "Sensor readings",
    hint: "Current values from the machine sensors.",
  },
  {
    title: "Fluid readings & alerts",
    hint: "Fluid levels and recent controller alerts.",
  },
  {
    title: "Machine history",
    hint: "Age, usage, service and failure records.",
  },
];

function MachineForm() {
  const [data, setData] = useState(initialData);
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  function setValue(name, value) {
    setData({
      ...data,
      [name]: value === "" ? "" : Number(value),
    });

    setResult(null);
  }


  // API Call
  async function predict() {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/predict`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );
      if (!response.ok) {
        throw new Error("Prediction failed");
      }
      const prediction = await response.json();
      setResult(prediction);
    } catch {
      setResult({
        error: "Could not connect to the prediction server.",
      });
    } finally {
      setLoading(false);
    }
  }

  function showStep() {
    if (step === 0) {
      return (
        <SensorReadings
          data={data}
          setValue={setValue}
        />
      );
    }
    if (step === 1) {
      return (
        <FluidReadings
          data={data}
          setValue={setValue}
        />
      );
    }
    return (
      <MachineHistory
        data={data}
        setValue={setValue}
      />
    );
  }

  return (
    <section className="flex min-h-0 flex-1 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="grid min-h-0 flex-1 grid-rows-[minmax(0,1fr)_minmax(200px,0.8fr)] md:grid-cols-[1.15fr_0.85fr] md:grid-rows-none">

        {/* Form */}

        <div className="flex min-h-0 flex-col border-slate-100 md:border-r">

          {/* Header */}
          <div className="border-b border-slate-100 px-4 py-3">
            <h2 className="text-lg font-bold">
              Machine readings
            </h2>
            <div
              aria-label="Form progress"
              className="mt-3 grid grid-cols-3 gap-2"
            >
              {steps.map((item, index) => (
                <button
                  key={item.title}
                  type="button"
                  onClick={() => setStep(index)}
                  className={`rounded-lg px-2 py-2 text-left text-xs ${index === step
                    ? "bg-teal-700 font-semibold text-white"
                    : index < step
                      ? "bg-teal-50 text-teal-800"
                      : "bg-slate-100 text-slate-500"
                    }`}
                >
                  <span className="block opacity-75">
                    Step {index + 1}
                  </span>
                  <span className="hidden sm:block">
                    {item.title}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Inputs */}
          <div className="flex min-h-0 flex-1 flex-col p-4">
            <h3 className="font-bold text-slate-800">
              {steps[step].title}
            </h3>
            <p className="mt-1 text-sm text-slate-500">
              {steps[step].hint}
            </p>
            <div className="mt-3 min-h-0 flex-1 overflow-y-auto pr-1">
              {showStep()}
            </div>

            {/* Buttons */}
            <div className="mt-3 flex items-center justify-between gap-3 border-t border-slate-100 pt-3">
              <button
                type="button"
                onClick={() => setStep(step - 1)}
                disabled={step === 0}
                className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 disabled:invisible"
              >
                Back
              </button>
              {step === 2 ? (
                <button
                  type="button"
                  onClick={predict}
                  disabled={loading}
                  className="rounded-lg bg-teal-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
                >
                  {loading ? "Analyzing…" : "Run prediction"}
                </button>
              ) : (
                <button
                  type="button"
                  onClick={() => setStep(step + 1)}
                  className="rounded-lg bg-teal-700 px-4 py-2 text-sm font-semibold text-white"
                >
                  Next
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Result */}
        <Result result={result} />

      </div>
    </section>
  );
}

export default MachineForm;