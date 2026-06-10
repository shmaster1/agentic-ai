import type { AgentNode, ResearchResponse } from "@/types";

const HEADER: Record<AgentNode, { icon: string; title: string; subtitle: string; color: string }> = {
  planner:   { icon: "⊕", title: "PLANNER — RESEARCH PLAN",       subtitle: "Decomposes the question into a research plan",    color: "#f59e0b" },
  searcher:  { icon: "◎", title: "SEARCHER — WEB RESULTS",        subtitle: "Retrieves relevant results from the web",          color: "#38bdf8" },
  retriever: { icon: "⊞", title: "RETRIEVER — FILTERED SOURCES",  subtitle: "Ranks and filters sources by relevance",           color: "#a78bfa" },
  writer:    { icon: "✦", title: "WRITER — FINAL REPORT",         subtitle: "Synthesises sources into a structured report",     color: "#34d399" },
};

function linkify(text: string) {
  const urlRe = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRe);
  return parts.map((part, i) =>
    urlRe.test(part) ? (
      <a
        key={i}
        href={part}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sky-400 underline break-all hover:text-sky-300 transition-colors"
      >
        {part}
      </a>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

interface Props {
  agent: AgentNode;
  response: ResearchResponse | null;
}

export default function AgentPanel({ agent, response }: Props) {
  const { icon, title, subtitle, color } = HEADER[agent];

  const items: string[] = response
    ? agent === "planner"
      ? response.tasks
      : agent === "searcher"
      ? response.search_results
      : agent === "retriever"
      ? response.filtered_results
      : []
    : [];

  const isEmpty = !response || items.length === 0;

  return (
    <div className="rounded-xl border border-[#1e2035] bg-[#0d0d14] overflow-hidden">

      {/* Header */}
      <div className="flex items-start gap-3 px-4 py-3 border-b border-[#1e2035]">
        <div
          className="w-7 h-7 rounded-full flex items-center justify-center text-sm shrink-0 mt-0.5"
          style={{ background: `${color}22`, color }}
        >
          {icon}
        </div>
        <div>
          <div className="font-mono text-xs font-semibold uppercase tracking-widest" style={{ color }}>
            {title}
          </div>
          <div className="text-[10px] font-mono text-slate-600 mt-0.5">{subtitle}</div>
        </div>
      </div>

      {/* Body */}
      <div className="p-4 max-h-72 overflow-y-auto">
        {isEmpty ? (
          agent === "writer" && response ? (
            <p className="text-slate-400 text-sm italic">Report generated — see below.</p>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 gap-3 text-slate-600">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" className="opacity-30">
                <circle cx="16" cy="16" r="13" stroke="currentColor" strokeWidth="1.5" />
                <circle cx="16" cy="16" r="5" stroke="currentColor" strokeWidth="1.5" />
                <circle cx="16" cy="16" r="1.5" fill="currentColor" />
              </svg>
              <span className="text-xs font-mono">Run a query to see results.</span>
            </div>
          )
        ) : (
          <ol className="space-y-2">
            {items.map((item, idx) => (
              <li key={idx} className="flex gap-3 text-sm">
                <span
                  className="shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold font-mono mt-0.5"
                  style={{ background: `${color}22`, color }}
                >
                  {idx + 1}
                </span>
                <span className="text-slate-200 leading-relaxed">
                  {agent === "searcher" ? linkify(item) : item}
                </span>
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}
