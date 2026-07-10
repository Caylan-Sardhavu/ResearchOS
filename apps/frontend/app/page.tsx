"use client";

import { useState } from "react";

import Hero from "../components/Hero";
import InvestigationTimeline from "../components/InvestigationTimeline";
import ResultsTabs from "../components/ResultsTabs";
import SearchPanel from "../components/SearchPanel";
import Sidebar from "../components/Sidebar";

type Agent = {
  name: string;
  department: string;
  role: string;
  description: string;
};

type Paper = {
  title: string;
  authors: string[];
  summary: string;
  published: string | null;
  url: string;
  pdf_url: string | null;
  source: string;
  relevance_score: number;
};

type ResearchResult = {
  question: string;
  director: {
    complexity: string;
    notebook_matches: string[];
    selected_agents: Agent[];
    notes: string[];
    ai_used: boolean;
  };
  papers_found: number;
  top_papers: Paper[];
  research_gaps: string[];
  report: string;
};

type NotebookEntry = {
  id: string;
  question: string;
  summary: string;
  research_gaps: string[];
  selected_agents: string[];
  paper_titles: string[];
  report: string;
  created_at: string;
};

/**
 * Decorative purple galaxy displayed in the upper-right corner.
 * This uses CSS rather than an image, so it stays sharp and lightweight.
 */
function UniverseVisual() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none absolute right-0 top-0 hidden h-[430px] w-[540px] overflow-hidden lg:block"
    >
      <div className="absolute right-8 top-6 h-80 w-80 rounded-full bg-purple-700/20 blur-3xl" />

      <div className="absolute right-6 top-4 h-[380px] w-[480px] rotate-[-12deg]">
        <div className="absolute left-8 top-24 h-44 w-[420px] rounded-[50%] border border-purple-700/25" />
        <div className="absolute left-20 top-28 h-36 w-[340px] rounded-[50%] border border-violet-500/35" />
        <div className="absolute left-32 top-32 h-28 w-[250px] rounded-[50%] border border-purple-400/45" />
        <div className="absolute left-44 top-36 h-20 w-[160px] rounded-[50%] border border-fuchsia-400/50" />

        <div className="absolute left-[246px] top-[167px] h-5 w-5 rounded-full bg-white shadow-[0_0_12px_rgba(255,255,255,1),0_0_35px_rgba(192,132,252,1),0_0_75px_rgba(126,34,206,1)]" />
        <div className="absolute left-[224px] top-[145px] h-16 w-16 rounded-full bg-purple-500/25 blur-xl" />

        <div className="absolute left-10 top-16 h-1 w-1 rounded-full bg-purple-300 shadow-[0_0_8px_rgba(216,180,254,1)]" />
        <div className="absolute left-24 top-8 h-1.5 w-1.5 rounded-full bg-violet-300 shadow-[0_0_10px_rgba(196,181,253,1)]" />
        <div className="absolute left-44 top-20 h-1 w-1 rounded-full bg-purple-200 shadow-[0_0_8px_rgba(233,213,255,1)]" />
        <div className="absolute right-20 top-16 h-1 w-1 rounded-full bg-fuchsia-300 shadow-[0_0_8px_rgba(240,171,252,1)]" />
        <div className="absolute right-7 top-32 h-1.5 w-1.5 rounded-full bg-purple-300 shadow-[0_0_10px_rgba(216,180,254,1)]" />
        <div className="absolute bottom-24 left-24 h-1 w-1 rounded-full bg-violet-200 shadow-[0_0_8px_rgba(221,214,254,1)]" />
        <div className="absolute bottom-12 left-52 h-1.5 w-1.5 rounded-full bg-purple-300 shadow-[0_0_10px_rgba(216,180,254,1)]" />
        <div className="absolute bottom-20 right-20 h-1 w-1 rounded-full bg-fuchsia-200 shadow-[0_0_8px_rgba(250,232,255,1)]" />

        <div className="absolute left-32 top-[155px] h-2 w-2 rounded-full bg-purple-400 shadow-[0_0_12px_rgba(192,132,252,0.9)]" />
        <div className="absolute right-20 top-[205px] h-2 w-2 rounded-full bg-violet-400 shadow-[0_0_12px_rgba(167,139,250,0.9)]" />
      </div>
    </div>
  );
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [error, setError] = useState("");
  const [activeStage, setActiveStage] = useState(0);
  const [investigationComplete, setInvestigationComplete] = useState(false);

  const [selectedNotebookEntry, setSelectedNotebookEntry] =
    useState<NotebookEntry | null>(null);

  const [loadingNotebookEntry, setLoadingNotebookEntry] = useState(false);

  // Incrementing this value tells Sidebar to reload notebook history.
  const [notebookRefreshKey, setNotebookRefreshKey] = useState(0);

  /**
   * Loads a previously saved investigation from the Research Notebook.
   */
  async function loadNotebookEntry(id: string) {
    setLoadingNotebookEntry(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/notebook/${id}`,
      );

      if (!response.ok) {
        throw new Error("Unable to load notebook entry.");
      }

      const data = (await response.json()) as NotebookEntry;

      if ("error" in data) {
        throw new Error("Notebook entry was not found.");
      }

      setSelectedNotebookEntry(data);
    } catch (err) {
      console.error(err);
      setError("Unable to open the saved investigation.");
    } finally {
      setLoadingNotebookEntry(false);
    }
  }

  /**
   * Runs a new end-to-end ResearchOS investigation.
   */
  async function startResearch() {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);
    setSelectedNotebookEntry(null);
    setActiveStage(0);
    setInvestigationComplete(false);

    const stageDuration = 2200;

    /**
     * Runs the visible timeline independently from the backend request.
     */
    const runTimeline = async () => {
      for (let stage = 1; stage <= 5; stage += 1) {
        await new Promise<void>((resolve) => {
          window.setTimeout(resolve, stageDuration);
        });

        setActiveStage(stage);
      }

      await new Promise<void>((resolve) => {
        window.setTimeout(resolve, stageDuration);
      });
    };

    try {
      const researchRequest = fetch(
        "http://127.0.0.1:8000/research",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question }),
        },
      ).then(async (response) => {
        if (!response.ok) {
          throw new Error("Research request failed.");
        }

        return (await response.json()) as ResearchResult;
      });

      const [data] = await Promise.all([
        researchRequest,
        runTimeline(),
      ]);

      setInvestigationComplete(true);
      setResult(data);

      // Reload the notebook history after the backend saves the investigation.
      setNotebookRefreshKey((current) => current + 1);
    } catch (err) {
      console.error(err);
      setError("Unable to complete the ResearchOS investigation.");
      setInvestigationComplete(false);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <div className="flex min-h-screen">
        <Sidebar
          onSelectEntry={loadNotebookEntry}
          refreshKey={notebookRefreshKey}
        />

        <section className="relative flex-1 overflow-hidden px-6 py-10 lg:px-14">
          <UniverseVisual />

          <div className="absolute bottom-20 left-1/2 h-96 w-96 rounded-full bg-violet-900/20 blur-3xl" />

          <div className="relative z-10 mx-auto max-w-6xl">
            <Hero />

            <SearchPanel
              question={question}
              loading={loading}
              onQuestionChange={setQuestion}
              onStartResearch={startResearch}
            />

            {(loading || investigationComplete) && (
              <div className="mt-8">
                <InvestigationTimeline
                  activeStage={activeStage}
                  completed={investigationComplete}
                />
              </div>
            )}

            {loadingNotebookEntry && (
              <div className="mt-8 rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                <p className="animate-pulse font-semibold text-purple-300">
                  Opening saved investigation...
                </p>
              </div>
            )}

            {error && (
              <div className="mt-8 rounded-xl border border-red-600 bg-red-950/40 p-5 text-red-200">
                {error}
              </div>
            )}

            {selectedNotebookEntry && !loadingNotebookEntry && (
              <section className="mt-8 space-y-6">
                <div className="rounded-3xl border border-purple-700/50 bg-zinc-950/90 p-7 shadow-[0_0_35px_rgba(147,51,234,0.16)]">
                  <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
                    <div>
                      <p className="text-sm font-semibold uppercase tracking-[0.18em] text-purple-400">
                        Research Notebook
                      </p>

                      <h2 className="mt-3 max-w-4xl text-3xl font-bold text-white">
                        {selectedNotebookEntry.question}
                      </h2>

                      <p className="mt-3 text-sm text-slate-500">
                        Saved{" "}
                        {new Date(
                          selectedNotebookEntry.created_at,
                        ).toLocaleString()}
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => setSelectedNotebookEntry(null)}
                      className="shrink-0 rounded-xl border border-purple-800 bg-purple-950/40 px-4 py-3 text-sm font-semibold text-purple-200 transition hover:border-purple-500 hover:bg-purple-900/50"
                    >
                      ← Back to current workspace
                    </button>
                  </div>
                </div>

                <ResultsTabs
                  overview={
                    <div className="space-y-6">
                      <div className="grid gap-4 md:grid-cols-3">
                        <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                          <p className="text-sm text-slate-500">
                            Selected Agents
                          </p>
                          <p className="mt-2 text-2xl font-bold text-purple-300">
                            {selectedNotebookEntry.selected_agents.length}
                          </p>
                        </div>

                        <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                          <p className="text-sm text-slate-500">
                            Papers Referenced
                          </p>
                          <p className="mt-2 text-2xl font-bold text-purple-300">
                            {selectedNotebookEntry.paper_titles.length}
                          </p>
                        </div>

                        <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                          <p className="text-sm text-slate-500">
                            Research Gaps
                          </p>
                          <p className="mt-2 text-2xl font-bold text-purple-300">
                            {selectedNotebookEntry.research_gaps.length}
                          </p>
                        </div>
                      </div>

                      <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                        <h3 className="mb-4 text-2xl font-bold text-purple-400">
                          Investigation Summary
                        </h3>

                        <p className="whitespace-pre-wrap leading-7 text-slate-300">
                          {selectedNotebookEntry.summary}
                        </p>
                      </div>
                    </div>
                  }
                  agents={
                    <div className="grid gap-4 md:grid-cols-2">
                      {selectedNotebookEntry.selected_agents.map(
                        (agent, index) => (
                          <div
                            key={`${index}-${agent}`}
                            className="rounded-2xl border border-purple-900/40 bg-zinc-950 p-5"
                          >
                            <p className="font-semibold text-purple-300">
                              {agent}
                            </p>
                          </div>
                        ),
                      )}
                    </div>
                  }
                  evidence={
                    <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                      <h3 className="mb-4 text-2xl font-bold text-purple-400">
                        Papers Referenced
                      </h3>

                      <div className="space-y-3">
                        {selectedNotebookEntry.paper_titles.map(
                          (title, index) => (
                            <div
                              key={`${index}-${title}`}
                              className="rounded-xl border border-purple-900/30 bg-black/40 p-4 text-slate-300"
                            >
                              {index + 1}. {title}
                            </div>
                          ),
                        )}
                      </div>
                    </div>
                  }
                  gaps={
                    <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                      <h3 className="mb-4 text-2xl font-bold text-purple-400">
                        Research Gaps
                      </h3>

                      <ul className="space-y-3">
                        {selectedNotebookEntry.research_gaps.map(
                          (gap, index) => (
                            <li
                              key={`${index}-${gap}`}
                              className="rounded-xl border border-purple-900/30 bg-black/40 p-4 text-slate-300"
                            >
                              • {gap}
                            </li>
                          ),
                        )}
                      </ul>
                    </div>
                  }
                  report={
                    <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                      <h3 className="mb-4 text-2xl font-bold text-purple-400">
                        Saved Research Report
                      </h3>

                      <pre className="overflow-x-auto whitespace-pre-wrap rounded-xl bg-black/60 p-5 text-sm leading-7 text-slate-300">
                        {selectedNotebookEntry.report}
                      </pre>
                    </div>
                  }
                />
              </section>
            )}

            {result && !selectedNotebookEntry && (
              <ResultsTabs
                overview={
                  <div className="space-y-6">
                    <div className="grid gap-4 md:grid-cols-3">
                      <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                        <p className="text-sm text-slate-500">
                          Complexity
                        </p>
                        <p className="mt-2 text-2xl font-bold capitalize text-purple-300">
                          {result.director.complexity}
                        </p>
                      </div>

                      <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                        <p className="text-sm text-slate-500">
                          Papers Found
                        </p>
                        <p className="mt-2 text-2xl font-bold text-purple-300">
                          {result.papers_found}
                        </p>
                      </div>

                      <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                        <p className="text-sm text-slate-500">
                          AI Used
                        </p>
                        <p className="mt-2 text-2xl font-bold text-purple-300">
                          {result.director.ai_used ? "Yes" : "Fallback"}
                        </p>
                      </div>
                    </div>

                    <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                      <h3 className="mb-4 text-2xl font-bold text-purple-400">
                        Research Director
                      </h3>

                      <div className="space-y-2 text-sm text-slate-300">
                        {result.director.notes.map((note, index) => (
                          <p key={`${index}-${note}`}>✓ {note}</p>
                        ))}
                      </div>

                      {result.director.notebook_matches.length > 0 && (
                        <div className="mt-6">
                          <h4 className="font-semibold text-purple-300">
                            Related Notebook Research
                          </h4>

                          <ul className="mt-3 space-y-2 text-sm text-slate-400">
                            {result.director.notebook_matches.map(
                              (match, index) => (
                                <li key={`${index}-${match}`}>
                                  • {match}
                                </li>
                              ),
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                }
                agents={
                  <div className="grid gap-4 md:grid-cols-2">
                    {result.director.selected_agents.map(
                      (agent, index) => (
                        <div
                          key={`${index}-${agent.name}`}
                          className="rounded-2xl border border-purple-900/40 bg-zinc-950 p-5 shadow-[0_0_20px_rgba(147,51,234,0.08)]"
                        >
                          <h4 className="font-bold text-purple-300">
                            {agent.name}
                          </h4>

                          <p className="text-sm text-slate-500">
                            {agent.department} • {agent.role}
                          </p>

                          <p className="mt-3 text-sm leading-6 text-slate-300">
                            {agent.description}
                          </p>
                        </div>
                      ),
                    )}
                  </div>
                }
                evidence={
                  <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                    <h3 className="mb-4 text-2xl font-bold text-purple-400">
                      Retrieved Evidence
                    </h3>

                    {result.top_papers.length === 0 ? (
                      <p className="text-slate-400">
                        No papers were retrieved for this investigation.
                      </p>
                    ) : (
                      <div className="space-y-4">
                        {result.top_papers.map((paper, index) => (
                          <div
                            key={`${index}-${paper.url}`}
                            className="rounded-xl border border-purple-900/40 bg-black/50 p-5"
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div>
                                <h4 className="font-bold text-purple-300">
                                  {paper.title}
                                </h4>

                                <p className="mt-1 text-sm text-slate-500">
                                  {paper.source} •{" "}
                                  {paper.published
                                    ? paper.published.slice(0, 4)
                                    : "Unknown year"}
                                </p>
                              </div>

                              <div className="shrink-0 rounded-lg bg-purple-950 px-3 py-1 text-sm text-purple-200">
                                Score {paper.relevance_score.toFixed(1)}
                              </div>
                            </div>

                            <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-400">
                              {paper.summary}
                            </p>

                            <a
                              href={paper.url}
                              target="_blank"
                              rel="noreferrer"
                              className="mt-4 inline-block text-sm font-semibold text-purple-400 hover:text-purple-300"
                            >
                              View paper →
                            </a>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                }
                gaps={
                  <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                    <h3 className="mb-4 text-2xl font-bold text-purple-400">
                      Research Gaps
                    </h3>

                    {result.research_gaps.length === 0 ? (
                      <p className="text-slate-400">
                        No research gaps were detected.
                      </p>
                    ) : (
                      <ul className="space-y-3 text-slate-300">
                        {result.research_gaps.map((gap, index) => (
                          <li
                            key={`${index}-${gap}`}
                            className="rounded-xl border border-purple-900/30 bg-black/40 p-4"
                          >
                            • {gap}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                }
                report={
                  <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-6">
                    <h3 className="mb-4 text-2xl font-bold text-purple-400">
                      Research Report
                    </h3>

                    <pre className="overflow-x-auto whitespace-pre-wrap rounded-xl bg-black/60 p-5 text-sm leading-7 text-slate-300">
                      {result.report}
                    </pre>
                  </div>
                }
              />
            )}
          </div>
        </section>
      </div>
    </main>
  );
}