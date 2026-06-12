import { NextRequest, NextResponse } from "next/server";

export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const backendUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const res = await fetch(`${backendUrl}/query/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(60_000),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Request failed";
    const cause = e instanceof Error && (e as any).cause ? String((e as any).cause) : "none";
    const url = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    console.error("Query proxy error:", { message, cause, url });
    return NextResponse.json({ error: message, cause, url }, { status: 500 });
  }
}
