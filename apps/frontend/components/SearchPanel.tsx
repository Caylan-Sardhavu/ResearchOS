"use client";

type SearchPanelProps = {
  question: string;
  loading: boolean;
  onQuestionChange: (value: string) => void;
  onStartResearch: () => void;
};

export default function SearchPanel({
  question,
  loading,
  onQuestionChange,
  onStartResearch,
}: SearchPanelProps) {
  return (
    <section className="rounded-3xl border border-purple-500/70 bg-zinc-950/80 p-8 shadow-[0_0_45px_rgba(147,51,234,0.28)] backdrop-blur">
      <h3 className="mb-5 text-2xl font-bold text-purple-300">
        ✦ What would you like to research?
      </h3>

      <textarea
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        placeholder="E.g., Find research gaps in AMD GPU performance optimization for LLM inference..."
        className="h-40 w-full resize-none rounded-2xl border border-purple-900 bg-black/70 p-5 text-slate-100 outline-none placeholder:text-slate-500 focus:border-purple-500"
      />

      <div className="mt-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-wrap gap-3">
          <div className="rounded-xl border border-purple-900/70 bg-black/60 px-5 py-3 text-sm text-slate-300">
            🧠 AI Director
          </div>

          <div className="rounded-xl border border-purple-900/70 bg-black/60 px-5 py-3 text-sm text-slate-300">
            📚 Evidence Retrieval
          </div>

          <div className="rounded-xl border border-purple-900/70 bg-black/60 px-5 py-3 text-sm text-slate-300">
            🧾 Report Writer
          </div>
        </div>

        <button
          type="button"
          onClick={onStartResearch}
          disabled={loading}
          className="rounded-xl bg-gradient-to-r from-purple-700 to-violet-500 px-8 py-4 font-bold shadow-[0_0_30px_rgba(147,51,234,0.6)] transition hover:from-purple-600 hover:to-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Researching..." : "🚀 Start Research →"}
        </button>
      </div>
    </section>
  );
}