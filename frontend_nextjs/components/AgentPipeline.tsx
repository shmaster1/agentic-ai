import type { AgentNode } from "@/types";

const NODES: AgentNode[] = ["planner", "searcher", "retriever", "writer"];

const META: Record<AgentNode, { icon: string; label: string }> = {
  planner:   { icon: "⊕", label: "PLANNER" },
  searcher:  { icon: "◎", label: "SEARCHER" },
  retriever: { icon: "⊞", label: "RETRIEVER" },
  writer:    { icon: "✦", label: "WRITER" },
};

const COLORS: Record<AgentNode, { color: string; bg: string; shadow: string }> = {
  planner:   { color: "#f59e0b", bg: "#1a1200", shadow: "0 0 12px #f59e0b44" },
  searcher:  { color: "#38bdf8", bg: "#001a26", shadow: "0 0 12px #38bdf844" },
  retriever: { color: "#a78bfa", bg: "#160d2e", shadow: "0 0 12px #a78bfa44" },
  writer:    { color: "#34d399", bg: "#021a10", shadow: "0 0 12px #34d39944" },
};

interface Props {
  openAgent: AgentNode;
  onSelect: (node: AgentNode) => void;
}

export default function AgentPipeline({ openAgent, onSelect }: Props) {
  return (
    <div className="grid grid-cols-2 gap-2 sm:flex sm:items-center sm:gap-2">
      {NODES.map((node, idx) => {
        const { icon, label } = META[node];
        const colors = COLORS[node];
        const isActive = openAgent === node;
        return (
          <div key={node} className="flex items-center gap-2 flex-1">
            <button
              onClick={() => onSelect(node)}
              className="flex-1 py-2 px-3 rounded-2xl border font-mono transition-all duration-200 cursor-pointer"
              style={
                isActive
                  ? { borderColor: colors.color, background: colors.bg, boxShadow: colors.shadow }
                  : { borderColor: "#1e2035", background: "#111118" }
              }
            >
              <div className="flex items-center justify-between">
                <span
                  className="text-xs font-semibold uppercase tracking-wide"
                  style={{ color: isActive ? colors.color : "#64748b" }}
                >
                  {icon} {label}
                </span>
                <span className="text-[10px]" style={{ color: isActive ? colors.color : "#2a2d45" }}>+</span>
              </div>
              <div className="text-[10px] font-mono mt-0.5 text-left" style={{ color: isActive ? `${colors.color}99` : "#2a2d45" }}>
                idle
              </div>
            </button>
            {idx < NODES.length - 1 && (
              <span className="hidden sm:inline text-[#2a2d45] text-sm shrink-0">→</span>
            )}
          </div>
        );
      })}
    </div>
  );
}
