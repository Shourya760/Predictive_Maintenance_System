function Header() {
  return (
    <header className="mb-3 shrink-0 rounded-2xl bg-teal-950 px-4 py-3 text-white shadow-sm sm:px-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-200">
            Predictive maintenance
          </p>
          <h1 className="mt-0.5 text-xl font-bold sm:text-2xl">Machine health check</h1>
        </div>
        <span className="shrink-0 flex gap-1 rounded-full border border-teal-700 bg-teal-900 px-2.5 py-1 text-xs font-medium text-teal-100">
          <p className="text-green-500" >●</p>Model Online
        </span>
      </div>
      <p className="mt-1 text-sm text-teal-100">
        Enter the latest readings to estimate failure risk within 7  days .
      </p>
    </header>
  );
}

export default Header;
