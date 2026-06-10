"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  content: string;
}

export default function FinalReport({ content }: Props) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-[#00d4aa44] bg-[#050508] overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#00d4aa44]">
        <span className="font-mono text-xs font-semibold uppercase tracking-widest text-[#00d4aa]">
          📋 Final Report
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-xs font-mono px-3 py-1 rounded-lg border transition-all duration-150"
          style={
            copied
              ? { color: "#00d4aa", borderColor: "#00d4aa", background: "#00d4aa18" }
              : { color: "#64748b", borderColor: "#1e2035", background: "transparent" }
          }
        >
          {copied ? "✓ Copied" : "⎘ Copy"}
        </button>
      </div>

      <div className="p-5 prose prose-invert prose-sm max-w-none max-h-[32rem] overflow-y-auto
        prose-headings:text-[#00d4aa] prose-headings:font-mono
        prose-a:text-sky-400 prose-a:no-underline hover:prose-a:underline
        prose-code:text-emerald-300 prose-code:bg-[#0d1f14] prose-code:px-1 prose-code:rounded
        prose-pre:bg-[#0d1217] prose-pre:border prose-pre:border-[#1e2035]
        prose-strong:text-slate-100
        prose-li:text-slate-300 prose-p:text-slate-300">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  );
}
