export default function Hero() {
  return (
    <header className="mb-10">
      {/* Main product title */}
      <h2 className="text-5xl font-extrabold tracking-tight md:text-7xl">
        Research<span className="text-purple-500">OS</span>
      </h2>

      {/* Product positioning */}
      <p className="mt-4 text-xl text-slate-300">
        The Operating System for{" "}
        <span className="text-purple-400">Autonomous Research</span>
      </p>

      {/* Short explanation of the workflow */}
      <p className="mt-4 max-w-2xl text-slate-500">
        Ask a research question. ResearchOS plans the investigation, selects
        specialist agents, retrieves evidence, and generates a structured
        research report.
      </p>
    </header>
  );
}