"use client";

type TimelineStage = {
  id: string;
  label: string;
  description: string;
  icon: string;
};

type InvestigationTimelineProps = {
  activeStage: number;
  completed: boolean;
};

const stages: TimelineStage[] = [
  {
    id: "director",
    label: "Research Director",
    description: "Analyzing the question and assembling the specialist team.",
    icon: "🧠",
  },
  {
    id: "retrieval",
    label: "Evidence Retrieval",
    description: "Searching academic sources for relevant papers.",
    icon: "📚",
  },
  {
    id: "ranking",
    label: "Evidence Ranking",
    description: "Scoring papers by relevance to the research question.",
    icon: "📊",
  },
  {
    id: "analysis",
    label: "Paper Analysis",
    description: "Extracting findings, limitations, and future work.",
    icon: "📝",
  },
  {
    id: "gaps",
    label: "Research Gap Detection",
    description: "Comparing evidence to identify underexplored areas.",
    icon: "🔍",
  },
  {
    id: "report",
    label: "Report Writer",
    description: "Preparing the final structured research report.",
    icon: "📄",
  },
];

export default function InvestigationTimeline({
  activeStage,
  completed,
}: InvestigationTimelineProps) {
  return (
    <section className="rounded-3xl border border-purple-900/50 bg-zinc-950/85 p-6 shadow-[0_0_35px_rgba(147,51,234,0.16)]">
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-purple-400">
            Mission Control
          </p>
          <h2 className="mt-2 text-2xl font-bold text-white">
            Live Investigation
          </h2>
        </div>

        <div className="rounded-full border border-purple-800 bg-purple-950/60 px-4 py-2 text-sm text-purple-200">
          {completed
            ? "Investigation complete"
            : `Stage ${Math.min(activeStage + 1, stages.length)} of ${stages.length}`}
        </div>
      </div>

      <div className="space-y-3">
        {stages.map((stage, index) => {
          const isComplete = completed || index < activeStage;
          const isActive = !completed && index === activeStage;

          return (
            <div
              key={stage.id}
              className={`flex items-start gap-4 rounded-2xl border p-4 transition-all duration-500 ${
                isActive
                  ? "border-purple-500 bg-purple-950/50 shadow-[0_0_24px_rgba(168,85,247,0.22)]"
                  : isComplete
                    ? "border-purple-900/60 bg-purple-950/20"
                    : "border-zinc-800 bg-black/40 opacity-55"
              }`}
            >
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-purple-900 bg-black text-xl">
                {stage.icon}
              </div>

              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="font-semibold text-white">{stage.label}</h3>

                  <span
                    className={`text-sm ${
                      isComplete
                        ? "text-emerald-400"
                        : isActive
                          ? "animate-pulse text-purple-300"
                          : "text-zinc-600"
                    }`}
                  >
                    {isComplete ? "✓ Complete" : isActive ? "Working..." : "Waiting"}
                  </span>
                </div>

                <p className="mt-1 text-sm leading-6 text-slate-400">
                  {stage.description}
                </p>

                {isActive && (
                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-purple-950">
                    <div className="h-full w-1/2 animate-pulse rounded-full bg-gradient-to-r from-purple-600 to-violet-400" />
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}