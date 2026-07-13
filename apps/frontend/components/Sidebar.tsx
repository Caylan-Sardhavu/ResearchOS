"use client";

import { useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type NotebookEntry = {
  id: string;
  question: string;
  created_at: string;
};

type SidebarProps = {
  onSelectEntry?: (entryId: string) => void;
  refreshKey?: number;
};

const navigationItems = [
  "Home",
  "Director",
  "Agents",
  "Evidence",
  "Notebook",
  "Reports",
];

export default function Sidebar({
  onSelectEntry,
  refreshKey = 0,
}: SidebarProps) {
  const [entries, setEntries] = useState<NotebookEntry[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  useEffect(() => {
    async function loadNotebookHistory() {
      setLoadingHistory(true);

      try {
        const response = await fetch(`${API_URL}/notebook`);

        if (!response.ok) {
          throw new Error("Unable to load notebook history.");
        }

        const data = await response.json();
        setEntries(data.entries ?? []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoadingHistory(false);
      }
    }

    loadNotebookHistory();
  }, [refreshKey]);

  return (
    <aside className="hidden w-72 border-r border-purple-900/40 bg-black/90 p-6 lg:flex lg:flex-col">
      <div className="mb-10 flex items-center gap-3">
        <div className="h-11 w-11 rounded-full bg-gradient-to-br from-purple-500 to-violet-800 shadow-[0_0_35px_rgba(168,85,247,0.9)]" />

        <h1 className="text-2xl font-bold">
          Research<span className="text-purple-500">OS</span>
        </h1>
      </div>

      <nav className="space-y-3 text-slate-300">
        {navigationItems.map((item, index) => (
          <button
            key={item}
            type="button"
            className={`w-full rounded-xl px-4 py-3 text-left transition ${
              index === 0
                ? "border border-purple-500 bg-purple-950/70 text-white shadow-[0_0_25px_rgba(147,51,234,0.35)]"
                : "hover:bg-purple-950/30"
            }`}
          >
            {item}
          </button>
        ))}
      </nav>

      <div className="mt-8 min-h-0 flex-1">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-purple-400">
            Research History
          </p>

          <span className="text-xs text-slate-600">
            {loadingHistory ? "..." : entries.length}
          </span>
        </div>

        <div className="max-h-64 space-y-2 overflow-y-auto pr-1">
          {loadingHistory && (
            <p className="text-sm text-slate-500">
              Loading history...
            </p>
          )}

          {!loadingHistory && entries.length === 0 && (
            <p className="text-sm text-slate-500">
              No saved investigations yet.
            </p>
          )}

          {!loadingHistory &&
            entries.map((entry) => (
              <button
                key={entry.id}
                type="button"
                onClick={() => onSelectEntry?.(entry.id)}
                className="w-full rounded-xl border border-purple-900/30 bg-zinc-950/70 p-3 text-left transition hover:border-purple-700 hover:bg-purple-950/30"
              >
                <p className="line-clamp-2 text-sm font-medium text-slate-200">
                  {entry.question}
                </p>

                <p className="mt-2 text-xs text-slate-600">
                  {new Date(entry.created_at).toLocaleDateString()}
                </p>
              </button>
            ))}
        </div>
      </div>

      <div className="mt-6 rounded-2xl border border-purple-900/40 bg-zinc-950 p-5">
        <p className="mb-3 font-semibold">System Status</p>
        <p className="text-sm text-green-400">● Online</p>
        <p className="mt-3 text-sm text-slate-400">
          Backend ready for investigations.
        </p>
      </div>
    </aside>
  );
}