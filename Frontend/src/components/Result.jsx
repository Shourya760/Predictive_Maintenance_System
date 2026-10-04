function Result({ result }) {
  return (
    <aside aria-live="polite" className="flex min-h-0 flex-col overflow-hidden bg-slate-50">
      {!result ? (
        <EmptyResult />
      ) : result.error ? (
        <div className="p-5 text-red-800">
          <h2 className="font-bold">Prediction unavailable</h2>
          <p className="mt-1 text-sm">{result.error}</p>
        </div>
      ) : (
        <ResultDetails result={result} />
      )}
    </aside>
  );
}

function EmptyResult() {
  return (
    <div className="flex h-full flex-col justify-center p-6 text-center">
      <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-teal-50 text-2xl">⌁</div>
      <h2 className="mt-4 text-lg font-bold">Your result will appear here</h2>
      <p className="mt-2 text-sm text-slate-500">
        Complete all three steps and run a prediction to see risk and suggested actions.
      </p>
    </div>
  );
}

function ResultDetails({ result }) {
  const failure = result.prediction === 1;
  const probability = (result.failure_probability ?? 0) * 100;

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="border-b border-slate-200 px-5 py-4">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-teal-700">Prediction result</p>
        <h2 className={`mt-1 text-2xl font-bold ${failure ? "text-red-700" : "text-emerald-700"}`}>
          {failure ? "Failure risk detected" : "Machine looks stable"}
        </h2>
        <p className="mt-1 text-sm text-slate-600">{result.message}</p>
        <div className="mt-4 flex items-end justify-between">
          <span className="text-sm text-slate-500">Failure probability</span>
          <strong className="text-3xl tabular-nums">{probability.toFixed(1)}%</strong>
        </div>
        <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100">
          <div
            className={`h-full rounded-full ${failure ? "bg-red-600" : "bg-emerald-600"}`}
            style={{ width: `${Math.max(probability, 2)}%` }}
          />
        </div>
      </div>
      <div className="min-h-0 flex-1 space-y-4 overflow-y-auto px-5 py-4 [scrollbar-color:#0f766e_#f1f5f9] [scrollbar-width:thin] [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:border-2 [&::-webkit-scrollbar-thumb]:border-slate-100 [&::-webkit-scrollbar-thumb]:bg-teal-700 [&::-webkit-scrollbar-track]:bg-slate-100">
        <ResultList
          title="Risk factors"
          empty="No notable sensor risks were found."
          items={result.risk_factors}
          render={(item) => (
            <li key={`${item.sensor}-${item.value}`} className="rounded-lg bg-white px-3 py-2 text-sm">
              <strong>{item.sensor}:</strong> {item.message}{" "}
              <span className="text-slate-500">({item.value})</span>
            </li>
          )}
        />
        <ResultList
          title="Recommended actions"
          empty="No extra actions are required."
          items={result.recommended_actions}
          render={(item) => (
            <li key={item} className="flex gap-2 text-sm text-slate-700">
              <span className="font-bold text-teal-700">•</span>
              <span>{item}</span>
            </li>
          )}
        />
      </div>
    </div>
  );
}

function ResultList({ title, empty, items, render }) {
  return (
    <div>
      <h3 className="text-sm font-bold text-slate-800">{title}</h3>
      {items?.length ? (
        <ul className="mt-2 space-y-2">{items.map(render)}</ul>
      ) : (
        <p className="mt-1 text-sm text-slate-500">{empty}</p>
      )}
    </div>
  );
}

export default Result;
