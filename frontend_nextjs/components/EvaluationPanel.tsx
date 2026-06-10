"use client";

import { useEffect, useState } from "react";
import type { EvaluationScores } from "@/types";

interface Props {
  scores: EvaluationScores | null;
  loading: boolean;
  error: string | null;
}

interface GaugeBarProps {
  label: string;
  score: number;
  reasoning: string;
}

const METRICS: { key: keyof Omit<EvaluationScores, "reasoning">; label: string }[] = [
  { key: "sources",   label: "Sources"   },
  { key: "coverage",  label: "Coverage"  },
  { key: "recency",   label: "Recency"   },
  { key: "coherence", label: "Coherence" },
];

function thresholdColor(score: number) {
  if (score >= 80) return { color: "#34d399", glow: "#34d39933" };
  if (score >= 60) return { color: "#f59e0b", glow: "#f59e0b33" };
  return { color: "#ef4444", glow: "#ef444433" };
}

function GaugeBar({ label, score, reasoning }: GaugeBarProps) {
  const [width, setWidth] = useState(0);
  const { color, glow } = thresholdColor(score);

  useEffect(() => {
    const t = setTimeout(() => setWidth(score), 50);
    return () => clearTimeout(t);
  }, [score]);

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-mono text-slate-400 uppercase tracking-widest">{label}</span>
        <span className="text-sm font-mono font-bold" style={{ color }}>{score}</span>
      </div>
      <div
        className="relative h-5 rounded overflow-hidden"
        style={{ background: "#0a0a14", boxShadow: "inset 0 0 0 1px #1e2035" }}
      >
        <div className="absolute inset-0" style={{
          backgroundImage: "repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0px, rgba(255,255,255,0.04) 1px, transparent 1px, transparent 10%)",
          backgroundSize: "10% 100%",
        }} />
        <div className="absolute top-0 bottom-0 w-px bg-white/10" style={{ left: "60%" }} />
        <div className="absolute top-0 bottom-0 w-px bg-white/10" style={{ left: "80%" }} />
        <div
          className="absolute top-0 left-0 h-full rounded transition-all duration-700 ease-out"
          style={{
            width: `${width}%`,
            background: `linear-gradient(90deg, ${color}66, ${color})`,
            boxShadow: `0 0 10px ${glow}`,
          }}
        />
      </div>
      <p className="text-[10px] font-mono text-slate-600 leading-relaxed">{reasoning}</p>
    </div>
  );
}

function SkeletonBar({ label }: { label: string }) {
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-mono text-slate-400 uppercase tracking-widest">{label}</span>
        <span className="text-[11px] font-mono text-slate-600">—</span>
      </div>
      <div
        className="relative h-5 rounded overflow-hidden"
        style={{ background: "#0a0a14", boxShadow: "inset 0 0 0 1px #1e2035" }}
      >
        <div className="absolute inset-0" style={{
          backgroundImage: "repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0px, rgba(255,255,255,0.04) 1px, transparent 1px, transparent 10%)",
          backgroundSize: "10% 100%",
        }} />
        <div className="absolute top-0 bottom-0 w-px bg-white/10" style={{ left: "60%" }} />
        <div className="absolute top-0 bottom-0 w-px bg-white/10" style={{ left: "80%" }} />
      </div>
    </div>
  );
}

export default function EvaluationPanel({ scores, loading, error }: Props) {
  return (
    <div
      className="rounded-xl border border-[#1e2035] overflow-hidden"
      style={{ background: "linear-gradient(180deg, #0d0d18 0%, #080810 100%)" }}
    >
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-[#1e2035]">
        <span className="text-[11px] font-mono uppercase tracking-widest text-slate-500">Evaluation</span>
        <span
          className="text-[10px] font-mono"
          style={{ color: loading ? "#f59e0b" : scores ? "#34d399" : error ? "#ef4444" : "#475569" }}
        >
          {loading ? "● scoring…" : scores ? "● complete" : error ? "● failed" : "○ pending"}
        </span>
      </div>

      <div className="px-4 pb-4 pt-3 space-y-4">
        {loading || !scores
          ? METRICS.map(({ label }) => <SkeletonBar key={label} label={label} />)
          : METRICS.map(({ key, label }) => (
              <GaugeBar
                key={key}
                label={label}
                score={scores[key]}
                reasoning={scores.reasoning[key] ?? ""}
              />
            ))}
        {error && <p className="text-red-400 text-[10px] font-mono pt-1">{error}</p>}
      </div>
    </div>
  );
}
