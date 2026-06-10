
  import { NextRequest, NextResponse } from "next/server";

  export async function POST(req: NextRequest) {
    try {
      const body = await req.json();
      const res = await fetch("http://localhost:8000/evaluate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(60_000),
      });
      const data = await res.json();
      return NextResponse.json(data, { status: res.status });
    } catch (e) {
      const message = e instanceof Error ? e.message : "Evaluation failed";
      return NextResponse.json({ error: message }, { status: 500 });
    }
  }
