export interface ResearchRequest {
  question: string;
  thread_id: string;
}

export interface ResearchResponse {
  question: string;
  tasks: string[];
  search_results: string[];
  filtered_results: string[];
  final_answer: string;
  iteration_count: number;
  error: string | null;
}

 export interface EvaluationScores {
    sources: number;
    coverage: number;
    recency: number;
    coherence: number;
    reasoning: Record<string, string>;
  }

export type AgentNode = "planner" | "searcher" | "retriever" | "writer";
