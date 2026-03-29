import uuid
import requests
import streamlit as st
import streamlit.components.v1 as components

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchNexus",
    page_icon="🔬",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        background-color: #0a0a0f;
        color: #e2e8f0;
    }
    .main { background-color: #0a0a0f; }
    h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; }

    /* ── Title block ── */
    .title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.4rem;
        font-weight: 600;
        color: #00d4aa;
        letter-spacing: -0.5px;
        margin-bottom: 0;
        text-align: center;
    }

    /* ── Subtitle Centering Fix ── */
    .subtitle-wrap {
        display: flex; 
        justify-content: center; 
        align-items: center;
        gap: 10px;
        margin-top: 8px;
        margin-bottom: 8rem;
        width: 100%;
    }
    .subtitle-bar {
        width: 3px;
        height: 28px;
        background: linear-gradient(180deg, #00d4aa 0%, #6366f1 100%);
        border-radius: 2px;
        flex-shrink: 0;
    }
    .subtitle-text {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00d4aa 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.4;
    }

    /* ── Agent Buttons (Black/Dark by default) ── */
    .stButton > button {
        background: #111118 !important;
        color: #64748b !important;
        border: 1px solid #1e2035 !important;
        border-radius: 20px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        padding: 5px 14px !important;
    }

    /* ── GO Button (Purple) ── */
    .stButton > button[aria-label="▶ GO"] {
        background: #a855f7 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1.6rem !important;
    }

    /* ── Text Area & Placeholder ── */
    .stTextArea textarea {
        background: #111118 !important;
        border: 1px solid #1e2035 !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* ── Agent Results (White BG, Black Text) ── */
    .agent-panel {
        background: #ffffff !important;
        color: #0a0a0f !important;
        border-radius: 10px;
        border: 1px solid;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
    }
    .agent-panel li { color: #0a0a0f !important; }

    /* ── FINAL REPORT BOX (Inverted: Black BG, White Text) ── */
    .final-box {
        background: #000000 !important; /* Pure Black */
        border: 1px solid #34d399;
        border-radius: 10px;
        padding: 1.6rem;
        margin-top: 1.5rem;
        line-height: 1.8;
        color: #ffffff !important; /* White text */
    }
    .final-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #34d399;
        margin-bottom: 0.8rem;
    }

    /* Selected agent colors (when clicked) */
    button[data-selected="planner"]   { color: #f59e0b !important; border-color: #f59e0b !important; background: #1a1200 !important; }
    button[data-selected="searcher"]  { color: #38bdf8 !important; border-color: #38bdf8 !important; background: #001a26 !important; }
    button[data-selected="retriever"] { color: #a78bfa !important; border-color: #a78bfa !important; background: #160d2e !important; }
    button[data-selected="writer"]    { color: #34d399 !important; border-color: #34d399 !important; background: #021a10 !important; }

    hr { border-color: #1e2035; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)



components.html("""
<script>
(function apply() {
    var btns = window.parent.document.querySelectorAll('button');
    btns.forEach(function(b) {
        // Only target the GO button
        if (b.innerText.includes('▶ GO')) {
            b.style.setProperty('background', '#a855f7', 'important');
            b.style.setProperty('color', '#ffffff', 'important');
            b.style.setProperty('border', 'none', 'important');
        } else {
            // Ensure others stay dark/default if they aren't the GO button
            // unless they are the active agent (handled by the other script)
        }
    });
    setTimeout(apply, 500);
})();
</script>
""", height=0)
# ── Constants ──────────────────────────────────────────────────────────────────

# ── Constants ──────────────────────────────────────────────────────────────────

# ── Constants ──────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000/query/"
NODES = ["planner", "searcher", "retriever", "writer"]

AGENT_META = {
    "planner":   {"icon": "🧠", "label": "Planner",   "desc": "Task Decomposition"},
    "searcher":  {"icon": "🔍", "label": "Searcher",  "desc": "Web Results"},
    "retriever": {"icon": "📊", "label": "Retriever", "desc": "Filtered & Ranked"},
    "writer":    {"icon": "✍️",  "label": "Writer",    "desc": "Final Report"},
}

# ── Session state ──────────────────────────────────────────────────────────────
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "response" not in st.session_state:
    st.session_state.response = None
if "open_agent" not in st.session_state:
    st.session_state.open_agent = "planner"


# ── Helper: pipeline pill buttons ─────────────────────────────────────────────
AGENT_COLORS = {
    "planner":   {"color": "#f59e0b", "bg": "#1a1200", "shadow": "#f59e0b33"},
    "searcher":  {"color": "#38bdf8", "bg": "#001a26", "shadow": "#38bdf833"},
    "retriever": {"color": "#a78bfa", "bg": "#160d2e", "shadow": "#a78bfa33"},
    "writer":    {"color": "#34d399", "bg": "#021a10", "shadow": "#34d39933"},
}

def render_pipeline(open_agent: str | None = "planner"):
    """Render node buttons. The selected one glows in its agent color; rest are gray."""
    cols = st.columns([1, 0.15, 1, 0.15, 1, 0.15, 1])
    col_map = [0, 2, 4, 6]
    for idx, node in enumerate(NODES):
        meta = AGENT_META[node]
        is_open = open_agent == node
        label = f"{meta['icon']} {meta['label']}"
        with cols[col_map[idx]]:
            clicked = st.button(label, key=f"btn_{node}", use_container_width=True)
            if clicked:
                st.session_state.open_agent = None if is_open else node
                st.rerun()
        if idx < len(NODES) - 1:
            with cols[col_map[idx] + 1]:
                st.markdown(
                    '<div style="text-align:center;color:#2a2d45;margin-top:8px;font-size:0.9rem">→</div>',
                    unsafe_allow_html=True
                )

    # JS: style the selected button with its agent color
    if open_agent and open_agent in AGENT_COLORS:
        c = AGENT_COLORS[open_agent]
        agent_label = AGENT_META[open_agent]['label']
        st.markdown(f"""
        <script>
        (function() {{
            var btns = window.parent.document.querySelectorAll('button');
            btns.forEach(function(btn) {{
                if (btn.innerText.toLowerCase().includes("{agent_label.lower()}")) {{
                    btn.style.color = "{c['color']}";
                    btn.style.borderColor = "{c['color']}";
                    btn.style.background = "{c['bg']}";
                    btn.style.boxShadow = "0 0 10px {c['shadow']}";
                }}
            }});
        }})();
        </script>
        """, unsafe_allow_html=True)


# ── Helper: render one agent panel ────────────────────────────────────────────
def render_agent_panel(node: str, items: list[str]):
    meta = AGENT_META[node]
    items_html = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(f"""
    <div class="agent-panel" data-agent="{node}">
        <div class="agent-panel-label">{meta['icon']} {meta['label']} — {meta['desc']}</div>
        <ul>{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)


# ── Layout ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="title" style="text-align:center">ResearchNexus</div>', unsafe_allow_html=True)
st.markdown("""
<div class="subtitle-wrap" style="justify-content:center;width:100%">
    <div class="subtitle-bar"></div>
    <div>
        <span class="subtitle-text">Autonomous · Multi-Agent · Research</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_input, col_results = st.columns([1, 1.6], gap="large")
with col_input:
    st.markdown("<div style='margin-top:0'>", unsafe_allow_html=True)
    question = st.text_area(
        label="Research question",
        placeholder="Ask a research question e.g. what is the impact of AI on jobs?",
        height=20,
        label_visibility="hidden"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    submit = st.button("▶ GO")

    if submit and question.strip():
        st.session_state.response = None
        st.session_state.open_agent = "planner"

        with st.spinner("Running agents..."):
            try:
                res = requests.post(API_URL, json={
                    "question": question.strip(),
                    "thread_id": st.session_state.thread_id
                }, timeout=300)
                res.raise_for_status()
                st.session_state.response = res.json()
            except requests.exceptions.Timeout:
                st.error("Request timed out. The research is taking too long.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the API. Make sure the FastAPI server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif submit and not question.strip():
        st.warning("Please enter a research question.")


# ── Results panel ──────────────────────────────────────────────────────────────
with col_results:
    st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)

    data = st.session_state.response

    if data:
        if data.get("error"):
            st.error(data["error"])
        else:
            render_pipeline(open_agent=st.session_state.open_agent)

            tasks          = data.get("tasks") or data.get("task_list") or data.get("plan") or []
            search_results = data.get("search_results") or data.get("searches") or data.get("web_results") or []
            filtered       = data.get("filtered_results") or data.get("retrieved") or data.get("ranked_results") or []
            final_answer   = data.get("final_answer") or data.get("answer") or data.get("report") or ""

            if isinstance(tasks, str):
                tasks = [t.strip() for t in tasks.split("\n") if t.strip()]
            elif isinstance(tasks, dict):
                tasks = [f"{k}: {v}" for k, v in tasks.items()]
            if isinstance(filtered, str):
                filtered = [r.strip() for r in filtered.split("\n") if r.strip()]

            open_node = st.session_state.open_agent

            if open_node == "planner":
                if tasks:
                    render_agent_panel("planner", tasks)
                else:
                    st.markdown("<p style='color:#94a3b8;font-family:IBM Plex Mono,monospace;font-size:0.8rem'>No task data returned for Planner.</p>", unsafe_allow_html=True)

            elif open_node == "searcher":
                import json as _json
                clean = []
                for r in search_results[:4]:
                    if isinstance(r, dict):
                        title = r.get("title", "")
                        url   = r.get("url", r.get("link", ""))
                        clean.append(f"{title} → {url}" if title else str(r)[:120])
                    elif isinstance(r, str) and r.strip().startswith("{"):
                        try:
                            parsed = _json.loads(r)
                            for item in parsed.get("results", [])[:2]:
                                clean.append(f"{item['title']} → {item['url']}")
                        except Exception:
                            clean.append(r[:120])
                    else:
                        clean.append(str(r)[:120])
                if clean:
                    render_agent_panel("searcher", clean)
                else:
                    st.markdown("<p style='color:#94a3b8;font-family:IBM Plex Mono,monospace;font-size:0.8rem'>No search results returned.</p>", unsafe_allow_html=True)

            elif open_node == "retriever":
                items = [str(r)[:120] for r in filtered[:6]] if filtered else []
                if items:
                    render_agent_panel("retriever", items)
                else:
                    st.markdown("<p style='color:#94a3b8;font-family:IBM Plex Mono,monospace;font-size:0.8rem'>No filtered results returned.</p>", unsafe_allow_html=True)

            elif open_node == "writer":
                if final_answer:
                    render_agent_panel("writer", [s.strip() for s in final_answer.split("\n") if s.strip()][:10])
                else:
                    st.markdown("<p style='color:#94a3b8;font-family:IBM Plex Mono,monospace;font-size:0.8rem'>No writer output returned.</p>", unsafe_allow_html=True)

            if final_answer:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="final-box">
                    <div class="final-label">✦ Final Research Report</div>
                    {final_answer.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <p style='font-family:IBM Plex Mono,monospace;font-size:0.68rem;
            color:#1e2a3a;margin-top:1rem'>
            iterations: {data.get('iteration_count', 0)} &nbsp;·&nbsp;
            thread: {st.session_state.thread_id[:8]}...
            </p>
            """, unsafe_allow_html=True)

    else:
        render_pipeline(open_agent=st.session_state.open_agent)