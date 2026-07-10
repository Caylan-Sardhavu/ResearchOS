"use client";

import { useState } from "react";

type ResultsTabsProps = {
  overview: React.ReactNode;
  agents: React.ReactNode;
  evidence: React.ReactNode;
  gaps: React.ReactNode;
  report: React.ReactNode;
};

const tabs = [
  { id: "overview", label: "Overview" },
  { id: "agents", label: "Agents" },
  { id: "evidence", label: "Evidence" },
  { id: "gaps", label: "Research Gaps" },
  { id: "report", label: "Report" },
];

export default function ResultsTabs({
  overview,
  agents,
  evidence,
  gaps,
  report,
}: ResultsTabsProps) {
  const [activeTab, setActiveTab] = useState("overview");

  const content = {
    overview,
    agents,
    evidence,
    gaps,
    report,
  };

  return (
    <section className="mt-8">
      <div className="mb-6 flex flex-wrap gap-3 rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-3">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              activeTab === tab.id
                ? "bg-purple-700 text-white shadow-[0_0_20px_rgba(147,51,234,0.4)]"
                : "text-slate-400 hover:bg-purple-950/40 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div>{content[activeTab as keyof typeof content]}</div>
    </section>
  );
}