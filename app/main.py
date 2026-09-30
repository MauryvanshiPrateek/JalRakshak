"""
JalRakshak — Main Streamlit Application Entry Point

Run with:
    streamlit run app/main.py

from the project root directory.
"""
from __future__ import annotations
import sys
import os

# ── Path setup (allow running from project root) ──────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st

# ── Page configuration ────────────────────────────────────────────────────
st.set_page_config(
    page_title="JalRakshak | Dam Break Flood Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**JalRakshak** — Dam Break Inundation Modelling & Flood Risk Visualization Platform\n\n"
            "Smart India Hackathon 2026 · SIH26161 · Team VisionSix\n\n"
            "⚠️ This is a prototype for demonstration purposes only."
        ),
    },
)

# ── Global CSS (Page 1 design system — light institutional) ──────────────
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        /* ── Global font & background (Page 1 system) ── */
        html, body, [class*="css"], .stApp {
            font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: #F7F8F6 !important;
            color: #1E252B !important;
        }
        /* ── Hide Streamlit chrome ── */
        header[data-testid="stHeader"] { display: none !important; }
        #MainMenu { display: none !important; }
        footer { display: none !important; }
        /* ── Hide sidebar globally on all pages ── */
        section[data-testid="stSidebar"] { display: none !important; }
        .block-container { padding-top: 0.6rem !important; padding-bottom: 2rem; }
        .stApp > div:first-child { padding-top: 0 !important; }
        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #D7DDE1;
        }
        section[data-testid="stSidebar"] * { color: #1E252B !important; }
        /* ── Metrics ── */
        [data-testid="stMetric"] label { color: #68747D !important; font-size: 0.75rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; color: #17324D !important; }
        /* ── Buttons ── */
        .stButton > button {
            font-family: 'IBM Plex Sans', sans-serif !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.15s ease-in-out !important;
        }
        .stButton > button[kind="primary"] {
            background: #17324D !important;
            color: #FFFFFF !important;
            border: 1px solid #17324D !important;
        }
        .stButton > button[kind="primary"]:hover { background: #256B8E !important; border-color: #256B8E !important; }
        .stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #17324D !important;
            border: 1px solid #D7DDE1 !important;
        }
        .stButton > button[kind="secondary"]:hover { border-color: #256B8E !important; color: #256B8E !important; }
        /* ── Sliders ── */
        .stSlider > div > div > div > div { background: #256B8E !important; }
        /* ── Selectbox ── */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
            border: 1px solid #D7DDE1 !important;
            color: #1E252B !important;
            border-radius: 6px !important;
        }
        /* ── Expander ── */
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            border: 1px solid #D7DDE1 !important;
            border-radius: 6px !important;
            color: #17324D !important;
            font-weight: 600 !important;
        }
        .streamlit-expanderContent {
            background-color: #FFFFFF !important;
            border: 1px solid #D7DDE1 !important;
            border-top: none !important;
            border-bottom-left-radius: 6px !important;
            border-bottom-right-radius: 6px !important;
        }
        /* ── Progress ── */
        .stProgress > div > div > div > div { background: #256B8E !important; }
        /* ── Tabs ── */
        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: #68747D !important;
            border-bottom: 2px solid transparent !important;
            font-weight: 500 !important;
        }
        .stTabs [aria-selected="true"] { color: #17324D !important; border-bottom: 2px solid #256B8E !important; }
        /* ── Alerts ── */
        .stAlert { border-radius: 6px !important; }
        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #F7F8F6; }
        ::-webkit-scrollbar-thumb { background: #D7DDE1; border-radius: 3px; }
        /* ── Folium map ── */
        iframe { border-radius: 8px !important; border: 1px solid #D7DDE1 !important; }
        /* ── Dividers ── */
        hr { border-color: #D7DDE1 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Import components ──────────────────────────────────────────────────────
from app.components.sidebar import render_sidebar
from app.pages.dashboard import render_dashboard
from app.pages.landing import render_landing
from app.pages.results import render_results
from simulation.simulation_service import SimulationService
from models.simulation_result import SimulationStatus

# ── Query params routing bridge ───────────────────────────────────────────
if "page" in st.query_params:
    qp = st.query_params["page"]
    if qp in ["landing", "dashboard", "results"]:
        st.session_state["page"] = qp
    del st.query_params["page"]

if "modal" in st.query_params:
    if st.query_params["modal"] == "explore":
        st.session_state["show_explore_modal"] = True
    elif st.query_params["modal"] == "signin":
        st.session_state["show_signin_modal"] = True
    del st.query_params["modal"]

# ── Session state initialisation ──────────────────────────────────────────
if "service" not in st.session_state:
    st.session_state["service"] = SimulationService()
if "current_result" not in st.session_state:
    st.session_state["current_result"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

service: SimulationService = st.session_state["service"]

# ── Top navigation bar (Rendered for Simulation & Results workspace) ──────
if st.session_state.get("page") != "landing":
    # Institutional nav bar matching Page 1 header design language
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([4, 1.6, 2.2, 1.6])

    with nav_col1:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:10px; padding:4px 0 8px 0;">
                <svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 8L18 5L32 8V12L18 9L4 12V8Z" fill="#17324D"/>
                    <path d="M7 13L18 10.5L29 13V17L18 14.5L7 17V13Z" fill="#256B8E"/>
                    <path d="M10 18L18 16L26 18V22L18 20L10 22V18Z" fill="#2D78A8"/>
                    <path d="M15 23C15 28 12 30 7 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                    <path d="M21 23C21 27 24 29 29 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="18" y1="21" x2="18" y2="33" stroke="#256B8E" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                <div>
                    <div style="font-size:1.05rem; font-weight:700; color:#17324D; letter-spacing:0.03em; line-height:1.1;">JalRakshak</div>
                    <div style="font-size:0.70rem; color:#68747D; letter-spacing:0.04em; font-family:'IBM Plex Sans',sans-serif;">Simulation Workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav_col2:
        if st.button("Home", use_container_width=True, key="nav_home", type="secondary"):
            st.session_state["page"] = "landing"
            st.rerun()

    with nav_col3:
        if st.button("Simulation Workspace", use_container_width=True, key="nav_sim", type="secondary"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    with nav_col4:
        result = st.session_state.get("current_result")
        if result and result.status == SimulationStatus.COMPLETED:
            if st.button("View Results", use_container_width=True, key="nav_results", type="secondary"):
                st.session_state["page"] = "results"
                st.rerun()
        else:
            st.button("View Results", use_container_width=True, key="nav_results_dis", disabled=True)

    st.markdown(
        "<hr style='margin:0 0 12px 0; border-color:#D7DDE1;'>",
        unsafe_allow_html=True,
    )

# ── Sidebar (disabled — hidden globally via CSS) ──────────────────────────
# All controls are embedded directly in the Simulation Workspace page.
scenario, run_clicked = None, False


# ── Page Routing ──────────────────────────────────────────────────────────
if st.session_state["page"] == "landing":
    render_landing()

elif st.session_state["page"] == "running" and scenario:

    st.markdown("### ⚙️ Running Simulation…")
    progress_bar = st.progress(0, text="Initialising…")
    status_box = st.empty()
    log_box = st.empty()

    logs = []

    def _callback(status, msg, pct):
        logs.append(f"[{status.label()}] {msg}")
        progress_bar.progress(pct / 100, text=f"**{status.label()}** — {msg}")
        status_box.markdown(
            f"""
            <div style="background:#1e293b; border-radius:8px; padding:10px 16px;
                        border-left:4px solid #38bdf8; color:#94a3b8; font-size:0.85rem;">
                <b style="color:#38bdf8;">{status.label()}</b> — {msg}
            </div>
            """,
            unsafe_allow_html=True,
        )
        log_box.code("\n".join(logs[-6:]), language="text")

    result = service.submit(scenario, progress_callback=_callback, blocking=True)
    st.session_state["current_result"] = result

    if result.status == SimulationStatus.COMPLETED:
        st.success("✅ Simulation complete! Switching to results…")
        import time; time.sleep(0.8)
        st.session_state["page"] = "results"
        st.rerun()
    else:
        st.error(f"❌ Simulation failed: {result.status_message}")
        st.session_state["page"] = "dashboard"

elif st.session_state["page"] == "results":
    result = st.session_state.get("current_result")
    if result:
        render_results(result)
    else:
        st.info("No results available. Run a simulation first.")
        st.session_state["page"] = "dashboard"

else:
    # Dashboard / Simulation Workspace (Page 2)
    render_dashboard(service.get_history())
