import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ResearchReportProps = {
  report: string;
  title?: string;
  badge?: string;
};

export default function ResearchReport({
  report,
  title = "Research Report",
  badge = "Fireworks AI",
}: ResearchReportProps) {
  if (!report.trim()) {
    return (
      <div className="rounded-2xl border border-purple-900/40 bg-zinc-950/80 p-8 text-center">
        <p className="text-slate-400">
          No research report is available.
        </p>
      </div>
    );
  }

  return (
    <article className="overflow-hidden rounded-2xl border border-purple-800/40 bg-zinc-950/90 shadow-[0_0_35px_rgba(147,51,234,0.12)]">
      <header className="border-b border-purple-900/40 bg-gradient-to-r from-purple-950/70 via-zinc-950 to-zinc-950 px-6 py-5 md:px-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-purple-400">
              ResearchOS Investigation
            </p>

            <h2 className="mt-2 text-2xl font-bold text-white">
              {title}
            </h2>
          </div>

          <span className="rounded-full border border-purple-700 bg-purple-950/60 px-3 py-1 text-xs font-semibold text-purple-200">
            {badge}
          </span>
        </div>
      </header>

      <div className="px-6 py-8 md:px-9">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            h1: ({ children }) => (
              <h1 className="mb-7 border-b border-purple-900/40 pb-5 text-3xl font-bold tracking-tight text-white">
                {children}
              </h1>
            ),

            h2: ({ children }) => (
              <div className="mb-5 mt-10 flex items-center gap-3 first:mt-0">
                <span className="h-8 w-1 rounded-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.7)]" />

                <h2 className="text-2xl font-bold text-purple-300">
                  {children}
                </h2>
              </div>
            ),

            h3: ({ children }) => (
              <h3 className="mb-3 mt-7 text-lg font-semibold text-purple-200">
                {children}
              </h3>
            ),

            p: ({ children }) => (
              <p className="mb-5 text-sm leading-8 text-slate-300 md:text-base">
                {children}
              </p>
            ),

            ul: ({ children }) => (
              <ul className="mb-6 space-y-3">
                {children}
              </ul>
            ),

            ol: ({ children }) => (
              <ol className="mb-6 list-decimal space-y-3 pl-6 text-slate-300">
                {children}
              </ol>
            ),

            li: ({ children, ...props }) => (
              <li
                className="ml-5 list-disc pl-1 text-sm leading-7 text-slate-300 md:text-base"
                {...props}
              >
                {children}
              </li>
            ),

            strong: ({ children }) => (
              <strong className="font-semibold text-white">
                {children}
              </strong>
            ),

            blockquote: ({ children }) => (
              <blockquote className="my-6 rounded-r-xl border-l-4 border-purple-500 bg-purple-950/30 px-5 py-4 italic text-purple-100">
                {children}
              </blockquote>
            ),

            table: ({ children }) => (
              <div className="my-8 overflow-x-auto rounded-xl border border-purple-900/40">
                <table className="w-full border-collapse text-left text-sm">
                  {children}
                </table>
              </div>
            ),

            thead: ({ children }) => (
              <thead className="bg-purple-950/70 text-purple-200">
                {children}
              </thead>
            ),

            tbody: ({ children }) => (
              <tbody className="divide-y divide-purple-900/30">
                {children}
              </tbody>
            ),

            tr: ({ children }) => (
              <tr className="transition hover:bg-purple-950/20">
                {children}
              </tr>
            ),

            th: ({ children }) => (
              <th className="px-4 py-3 font-semibold text-purple-200">
                {children}
              </th>
            ),

            td: ({ children }) => (
              <td className="px-4 py-3 align-top leading-6 text-slate-300">
                {children}
              </td>
            ),

            a: ({ children, href }) => (
              <a
                href={href}
                target="_blank"
                rel="noreferrer"
                className="font-semibold text-purple-400 underline decoration-purple-700 underline-offset-4 transition hover:text-purple-300"
              >
                {children}
              </a>
            ),

            code: ({ children }) => (
              <code className="rounded bg-purple-950/70 px-1.5 py-0.5 text-sm text-purple-200">
                {children}
              </code>
            ),

            hr: () => (
              <hr className="my-8 border-purple-900/40" />
            ),
          }}
        >
          {report}
        </ReactMarkdown>
      </div>
    </article>
  );
}