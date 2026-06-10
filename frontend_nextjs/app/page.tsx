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
            <label className="text-xs font-mono uppercase tracking-widest text-slate-500">
              Research Question
            </label>
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
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-slate-600"># + Enter to submit</span>
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

          {/* Status block */}
          <div className="rounded-xl border border-[#1e2035] bg-[#0d0d14] p-4 font-mono text-sm space-y-1">
            {loading ? (
              <div className="flex items-center gap-5 py-1">
                {/* Radar pulse orb */}
                <div className="relative flex items-center justify-center w-8 h-8 shrink-0">
                  <span className="radar-ring absolute inline-flex w-6 h-6 rounded-full border border-[#00d4aa]" />
                  <span className="radar-ring-2 absolute inline-flex w-6 h-6 rounded-full border border-[#00d4aa]" />
                  <span className="radar-ring-3 absolute inline-flex w-6 h-6 rounded-full border border-[#00d4aa]" />
                  <span className="relative w-2 h-2 rounded-full bg-[#00d4aa] shadow-[0_0_8px_#00d4aa]" />
                </div>
                {/* Text + scan bar */}
                <div className="flex flex-col gap-1.5 flex-1 min-w-0">
                  <span className="text-[#00d4aa] font-mono text-sm tracking-widest">RUNNING</span>
                  <div className="relative h-px bg-[#1e2035] overflow-hidden rounded-full">
                    <div className="scan-bar absolute inset-y-0 w-1/4 bg-gradient-to-r from-transparent via-[#00d4aa] to-transparent" />
                  </div>
                </div>
              </div>
            ) : response ? (
              <>
                <div className="text-[#00d4aa]">// COMPLETE</div>
                <div className="text-xs text-slate-400 space-y-1 pt-1">
                  <div>Iterations: <span className="text-slate-100">{response.iteration_count}</span></div>
                  <div>Tasks: <span className="text-slate-100">{response.tasks.length}</span></div>
                  <div>Sources found: <span className="text-slate-100">{response.search_results.length}</span></div>
                  <div>Sources kept: <span className="text-slate-100">{response.filtered_results.length}</span></div>
                </div>
              </>
            ) : (
              <>
                <div className="text-[#00d4aa]">// READY</div>
                <p className="text-slate-600 text-xs">
                  Four agents stand by. Submit a question to dispatch the pipeline.
                </p>
              </>
            )}
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
