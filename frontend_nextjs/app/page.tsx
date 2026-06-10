"use client";

import { useState, useCallback, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import type { AgentNode, ResearchResponse, EvaluationScores } from "@/types";
import AgentPipeline from "@/components/AgentPipeline";
import AgentPanel from "@/components/AgentPanel";
import FinalReport from "@/components/FinalReport";
import EvaluationPanel from "@/components/EvaluationPanel";

export default function Home() {
  const [threadId] = useState(() => uuidv4());
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<ResearchResponse | null>(null);
  const [openAgent, setOpenAgent] = useState<AgentNode>("planner");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [evalScores, setEvalScores] = useState<EvaluationScores | null>(null);
  const [evalLoading, setEvalLoading] = useState(false);
  const [evalError, setEvalError] = useState<string | null>(null);

  const handleSubmit = useCallback(async () => {
    if (!question.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, thread_id: threadId }),
      });
      const data: ResearchResponse = await res.json();
      if (data.error) setError(data.error);
      else setResponse(data);
    } catch (e) {
      setError("Failed to reach the research backend.");
    } finally {
      setLoading(false);
    }
  }, [question, threadId, loading]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") handleSubmit();
  };


  useEffect(() => {
    if (!response?.final_answer) return;
    setEvalLoading(true);
    setEvalScores(null);
    setEvalError(null);
    fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: response.question,
        sources: response.filtered_results,
        answer: response.final_answer,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) setEvalError(data.error);
        else setEvalScores(data.scores);
      })
      .catch(() => setEvalError("Evaluation failed."))
      .finally(() => setEvalLoading(false));
  }, [response]);


  return (
    <main className="min-h-screen p-8">
      {/* Full-page loader overlay */}
      {loading && (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#0a0a0f]/80 backdrop-blur-sm">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 rounded-full border-2 border-[#1e2035]" />
            <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-[#00d4aa] animate-spin" />
            <div className="absolute inset-2 rounded-full border-2 border-transparent border-t-[#a855f7] animate-spin [animation-duration:1.5s] [animation-direction:reverse]" />
          </div>
          <span className="mt-5 font-mono text-xs tracking-widest text-[#00d4aa]">PROCESSING</span>
        </div>
      )}
      <div className="grid grid-cols-[1fr_1.6fr] gap-8 max-w-7xl mx-auto">

        {/* LEFT — input */}
        <div className="flex flex-col gap-6">

          {/* Title */}
          <div>
            <h1 className="text-3xl font-bold font-mono tracking-tight">
              <span className="text-white">Research</span>
              <span className="bg-gradient-to-r from-[#00d4aa] via-[#a855f7] to-[#38bdf8] bg-clip-text text-transparent">
                Nexus
              </span>
            </h1>
            <p className="mt-2 text-slate-500 text-xs font-mono uppercase tracking-widest">
              Autonomous Multi-Agent Research
            </p>
          </div>

          {/* Input */}
          <div className="flex flex-col gap-2">
            <div className="relative">
              <textarea
                rows={6}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="What would you like to research?"
                className="w-full rounded-xl border border-[#1e2035] bg-[#111118] text-slate-200
                  placeholder:text-slate-600 p-4 pb-7 text-sm font-sans resize-none
                  focus:outline-none focus:border-[#00d4aa] transition-colors"
              />
              <span className="absolute bottom-2 right-3 text-[10px] font-mono text-slate-600">
                {question.length} chars
              </span>
            </div>
            <div className="flex items-center justify-end">
              <button
                onClick={handleSubmit}
                disabled={!question.trim() || loading}
                className="px-6 py-2 rounded-xl bg-[#00d4aa] hover:bg-[#00b894] text-[#0a0a0f]
                  font-mono text-sm font-semibold transition-colors disabled:opacity-40
                  disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? "Running…" : <>GO <span>→</span></>}
              </button>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="rounded-xl border border-red-800 bg-red-950/40 p-4 text-red-400 text-sm font-mono">
              {error}
            </div>
          )}

          {/* Evaluation panel */}
          <EvaluationPanel scores={evalScores} loading={evalLoading} error={evalError} />


        </div>

        {/* RIGHT — results */}
        <div className="flex flex-col gap-5">
          <AgentPipeline openAgent={openAgent} onSelect={setOpenAgent} />
          <AgentPanel agent={openAgent} response={response} />
          {openAgent === "writer" && response?.final_answer && (
            <FinalReport content={response.final_answer} />
          )}
        </div>
      </div>
      <footer className="mt-12 pb-6 text-center font-mono text-[10px] text-slate-600 space-x-4">
        <span>Research <span className="text-slate-400">LLaMA 3.3 70B</span> via Groq</span>
        <span className="text-slate-700">|</span>
        <span>Evaluation <span className="text-slate-400">GPT-4o</span> via OpenAI</span>
      </footer>
    </main>
  );
}
