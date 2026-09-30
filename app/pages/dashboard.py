"""
JalRakshak -- Page 2: Simulation Workspace.

Design System: Identical to Page 1 (landing page).
  - Background: #F7F8F6
  - Primary:    #17324D
  - Accent:     #256B8E
  - Cards:      #FFFFFF, border #D7DDE1
  - Font:       IBM Plex Sans + IBM Plex Mono
  - No emojis as decoration, SVG icons only
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html
from app.components.map_view import render_map
from models.simulation_result import SimulationResult, SimulationStatus
from models.scenario import AVAILABLE_DAMS, Scenario

# ── Design tokens (same as landing page) ─────────────────────────────────
_BG        = "#F7F8F6"
_NAVY      = "#17324D"
_TEAL      = "#256B8E"
_TEAL2     = "#2D78A8"
_TEAL3     = "#5FA8D3"
_GREY      = "#68747D"
_MUTED     = "#94A3B8"
_BORDER    = "#D7DDE1"
_WHITE     = "#FFFFFF"
_CARD_BG   = "#FFFFFF"
_FOOTER_BG = "#1E252B"
_AMBER     = "#C98A18"

# ── Breach preset data ─────────────────────────────────────────────────────
_PRESETS: dict[str, dict] = {
    "small":  {
        "label": "Small",  "tag": "PARTIAL",
        "breach_width_m": 15, "breach_depth_m": 10,
        "formation_time_min": 20, "duration_min": 60,
        "desc": "Partial overtopping breach. Limited downstream extent.",
        "accent": _TEAL3,
    },
    "medium": {
        "label": "Medium", "tag": "SIGNIFICANT",
        "breach_width_m": 40, "breach_depth_m": 22,
        "formation_time_min": 10, "duration_min": 90,
        "desc": "Progressive piping failure. Major inundation risk.",
        "accent": _AMBER,
    },
    "severe": {
        "label": "Severe", "tag": "CATASTROPHIC",
        "breach_width_m": 90, "breach_depth_m": 40,
        "formation_time_min": 5,  "duration_min": 120,
        "desc": "Full structural collapse. Catastrophic outflow.",
        "accent": "#C0392B",
    },
}

# ── SVG icons (no emojis) ─────────────────────────────────────────────────
_SVG_DAM = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 6L12 4L20 6V10L12 8L4 10V6Z" stroke="#256B8E" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M6 11L12 9.5L18 11V14L12 12.5L6 14V11Z" stroke="#256B8E" stroke-width="1.5" stroke-linejoin="round"/>
  <line x1="12" y1="13" x2="12" y2="20" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M8 20C8 20 10 18 12 20C14 18 16 20 16 20" stroke="#5FA8D3" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

_SVG_BREACH = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="6" width="18" height="3" stroke="#256B8E" stroke-width="1.5"/>
  <path d="M3 9L3 18" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M21 9L21 18" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M9 9L7 18" stroke="#C98A18" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M15 9L17 18" stroke="#C98A18" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M9 9L15 9" stroke="#C98A18" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

_SVG_MAP = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <polygon points="1,6 8,2 16,6 23,2 23,18 16,22 8,18 1,22" fill="none" stroke="#256B8E" stroke-width="1.5" stroke-linejoin="round"/>
  <line x1="8" y1="2" x2="8" y2="18" stroke="#256B8E" stroke-width="1.5"/>
  <line x1="16" y1="6" x2="16" y2="22" stroke="#256B8E" stroke-width="1.5"/>
</svg>"""

_SVG_RESULTS = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <polyline points="3,17 7,12 11,14 17,7 21,10" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="3" y1="20" x2="21" y2="20" stroke="#256B8E" stroke-width="1.5"/>
</svg>"""

_SVG_EXPORT = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round"/>
  <polyline points="7,10 12,15 17,10" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="12" y1="15" x2="12" y2="3" stroke="#256B8E" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""


# ── Global CSS override to match Page 1 styling ───────────────────────────
_PAGE2_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
  /* ── Full reset to Page 1 system ── */
  html, body, [class*="css"], .stApp {
    background-color: #F7F8F6 !important;
    color: #1E252B !important;
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
  }
  .main .block-container {
    max-width: 1300px !important;
    padding-top: 80px !important;
    padding-bottom: 2rem !important;
  }
  /* ── Sliders ── */
  .stSlider > div > div > div > div {
    background: #256B8E !important;
  }
  .stSlider label { color: #1E252B !important; font-size: 0.88rem !important; }
  /* ── Selectbox ── */
  .stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D7DDE1 !important;
    color: #1E252B !important;
    border-radius: 6px !important;
  }
  .stSelectbox label { color: #1E252B !important; }
  /* ── Buttons ── */
  .stButton > button {
    font-family: 'IBM Plex Sans', sans-serif !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.15s ease-in-out !important;
  }
  .stButton > button[kind="primary"] {
    background: #17324D !important;
    color: #FFFFFF !important;
    border: 1px solid #17324D !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: #256B8E !important;
    border-color: #256B8E !important;
  }
  .stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #17324D !important;
    border: 1px solid #D7DDE1 !important;
  }
  .stButton > button[kind="secondary"]:hover {
    border-color: #256B8E !important;
    color: #256B8E !important;
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
  /* ── Tabs ── */
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #68747D !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 8px !important;
  }
  .stTabs [aria-selected="true"] {
    color: #17324D !important;
    border-bottom: 2px solid #256B8E !important;
  }
  /* ── Alerts / info ── */
  .stAlert { border-radius: 6px !important; }
  /* ── Progress bar ── */
  .stProgress > div > div > div > div {
    background: #256B8E !important;
  }
  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #F7F8F6; }
  ::-webkit-scrollbar-thumb { background: #D7DDE1; border-radius: 3px; }
  /* ── Folium iframe ── */
  iframe {
    border-radius: 8px !important;
    border: 1px solid #D7DDE1 !important;
  }
  /* ── Dividers ── */
  hr { border-color: #D7DDE1 !important; }
  /* ── Metrics ── */
  [data-testid="stMetric"] label { color: #68747D !important; font-size: 0.78rem !important; }
  [data-testid="stMetricValue"] { color: #17324D !important; font-size: 1.5rem !important; font-weight: 700 !important; }
  /* Section label style */
  .ws2-section-tag {
    font-size: 0.78rem;
    font-weight: 600;
    color: #256B8E;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
</style>
"""


# ── Workspace session state ────────────────────────────────────────────────
def _init_state() -> None:
    defaults = {
        "ws_dam_id":            "hirakud-demo",
        "ws_preset":            None,
        "ws_breach_width":      30,
        "ws_breach_depth":      15,
        "ws_formation_time":    10,
        "ws_duration":          60,
        "ws_reservoir_level":   55,
        "ws_result":            None,
        "ws_time_fraction":     1.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Left configuration panel ──────────────────────────────────────────────
def _render_config_panel() -> None:
    dam_id = st.session_state["ws_dam_id"]
    dam = AVAILABLE_DAMS[dam_id]

    # ── 01 Study Area ──
    render_html(f"""
    <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                text-transform:uppercase; margin-bottom:6px;">01 &mdash; STUDY AREA</div>
    """)

    dam_opts = {v.name: k for k, v in AVAILABLE_DAMS.items()}
    chosen_name = st.selectbox(
        "Select Dam",
        list(dam_opts.keys()),
        key="ws_dam_sel",
        label_visibility="collapsed",
    )
    st.session_state["ws_dam_id"] = dam_opts[chosen_name]
    dam = AVAILABLE_DAMS[st.session_state["ws_dam_id"]]

    render_html(f"""
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-left:4px solid {_TEAL};
                border-radius:6px; padding:14px 16px; margin:8px 0 20px 0;">
      <div style="font-size:0.95rem; font-weight:600; color:{_NAVY}; margin-bottom:8px;">{dam.name}</div>
      <div style="font-size:0.82rem; color:{_GREY}; line-height:1.8;">
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; color:{_TEAL};">LOC</span>&nbsp;
        {dam.location_description}<br>
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; color:{_TEAL};">RIV</span>&nbsp;
        {dam.river}<br>
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; color:{_TEAL};">H</span>&nbsp;&nbsp;&nbsp;
        {dam.height_m} m &nbsp;|&nbsp;
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; color:{_TEAL};">V</span>&nbsp;
        {dam.storage_mcm:,.0f} MCM
      </div>
    </div>
    </div>
    <div style="border-top:1px solid {_BORDER}; margin:20px 0;"></div>
    <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                text-transform:uppercase; margin-bottom:10px;">02 &mdash; PARAMETERS</div>
    """)

    # ── Sliders ──
    st.session_state["ws_breach_width"] = st.slider(
        "Breach Width (m)", min_value=5, max_value=150,
        value=int(st.session_state["ws_breach_width"]), step=5, key="sl_bw",
    )
    st.session_state["ws_breach_depth"] = st.slider(
        "Breach Depth (m)", min_value=2, max_value=int(dam.height_m),
        value=min(int(st.session_state["ws_breach_depth"]), int(dam.height_m)), step=1, key="sl_bd",
    )
    st.session_state["ws_reservoir_level"] = st.slider(
        "Reservoir Level (m)", min_value=10, max_value=int(dam.height_m),
        value=min(int(st.session_state["ws_reservoir_level"]), int(dam.height_m)), step=1, key="sl_rl",
    )
    st.session_state["ws_formation_time"] = st.slider(
        "Formation Time (min)", min_value=1, max_value=60,
        value=int(st.session_state["ws_formation_time"]), step=1, key="sl_ft",
    )
    st.session_state["ws_duration"] = st.slider(
        "Duration (min)", min_value=15, max_value=180,
        value=int(st.session_state["ws_duration"]), step=15, key="sl_dur",
    )

    render_html(f"""<div style="border-top:1px solid {_BORDER}; margin:20px 0;"></div>""")

    with st.expander("View Simulation Assumptions", expanded=False):
        render_html(f"""
        <div style="font-size:0.85rem; color:{_GREY}; line-height:1.7; padding:4px 0;">
          <div style="display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">Breach Shape</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">Rectangular</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">Manning n (channel)</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">0.035</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">Manning n (floodplain)</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">0.060</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">DEM Source</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">Synthetic (demo)</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">CRS</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">EPSG:4326</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 10px;
                        background:{_BG}; border-radius:4px;">
              <span style="color:{_NAVY}; font-weight:500;">Engine</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.78rem;">Phase 1 Mock</span>
            </div>
          </div>
          <div style="margin-top:12px; padding:8px 12px; background:rgba(201,138,24,0.06);
                      border:1px solid rgba(201,138,24,0.3); border-radius:4px;
                      font-size:0.78rem; color:{_AMBER};">
            All outputs are illustrative calculations, not real ANUGA hydrodynamic output.
          </div>
        </div>
        """)


# ── Right panel: scenario summary + run ───────────────────────────────────
def _render_run_panel() -> tuple[bool, Scenario | None]:
    dam_id = st.session_state["ws_dam_id"]
    dam    = AVAILABLE_DAMS[dam_id]
    bw     = st.session_state["ws_breach_width"]
    bd     = st.session_state["ws_breach_depth"]
    rl     = st.session_state["ws_reservoir_level"]
    ft     = st.session_state["ws_formation_time"]
    dur    = st.session_state["ws_duration"]
    preset = st.session_state.get("ws_preset")

    scenario = Scenario(
        dam_id=dam_id,
        breach_width_m=float(bw),
        breach_depth_m=float(bd),
        formation_time_min=float(ft),
        duration_min=float(dur),
        reservoir_level_m=float(rl),
        preset_name=_PRESETS[preset]["label"] if preset else "Custom",
    )
    errors = scenario.validate()

    render_html(f"""
    <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                text-transform:uppercase; margin-bottom:10px;">SCENARIO SUMMARY</div>
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                padding:18px 16px; margin-bottom:16px; box-shadow:0 2px 6px rgba(23,50,77,0.03);">
      <div style="font-size:0.82rem; color:{_GREY}; line-height:2.0;">
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Dam</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">{dam.name[:20]}</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Preset</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">
            {_PRESETS[preset]['label'] if preset else '&mdash; Custom &mdash;'}
          </span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Breach</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">
            {bw} m &times; {bd} m
          </span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Reservoir</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">{rl} m</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Formation</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">{ft} min</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;
                    border-bottom:1px solid {_BG};">
          <span style="color:{_NAVY}; font-weight:500;">Duration</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem;">{dur} min</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:4px 0;">
          <span style="color:{_NAVY}; font-weight:500;">Scenario ID</span>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:{_TEAL};">
            {scenario.scenario_id}
          </span>
        </div>
      </div>
    </div>
    """)

    if errors:
        for e in errors:
            st.error(e)

    run_clicked = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
        key="ws_run_btn",
        disabled=bool(errors),
    )

    # Post-run result summary
    result: SimulationResult | None = st.session_state.get("ws_result")
    if result and result.status == SimulationStatus.COMPLETED:
        wl = result.warning_level or "Low"
        wl_map = {
            "Low":      (_TEAL3,   "#EAF6FB", "LOW RISK"),
            "Moderate": (_AMBER,   "#FDF6E3", "MODERATE RISK"),
            "High":     ("#C0710B", "#FEF0E3", "HIGH RISK"),
            "Critical": ("#C0392B", "#FDECEA", "CRITICAL RISK"),
        }
        wl_col, wl_bg, wl_label = wl_map.get(wl, wl_map["Low"])

        render_html(f"""
        <div style="border-top:1px solid {_BORDER}; margin:20px 0;"></div>
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:10px;">LAST RESULT</div>
        <div style="background:{wl_bg}; border:1px solid {wl_col}; border-radius:8px;
                    padding:12px 16px; margin-bottom:12px;">
          <div style="font-size:0.78rem; font-weight:700; color:{wl_col};
                      letter-spacing:0.06em; margin-bottom:8px;">{wl_label}</div>
          <div style="font-size:0.82rem; color:{_NAVY}; line-height:1.9;">
            <div style="display:flex; justify-content:space-between;">
              <span>Flooded Area</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem; font-weight:600;">
                {result.flooded_area_km2:.1f} km&sup2;</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Max Depth</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem; font-weight:600;">
                {result.max_water_depth_m:.1f} m</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Max Velocity</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem; font-weight:600;">
                {result.max_velocity_mps:.1f} m/s</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Affected Areas</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem; font-weight:600;">
                {result.affected_settlements}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Peak Q</span>
              <span style="font-family:'IBM Plex Mono',monospace; font-size:0.76rem; font-weight:600;">
                {result.peak_discharge_m3s:,.0f} m&sup3;/s</span>
            </div>
          </div>
        </div>
        <div style="font-size:0.72rem; color:{_MUTED}; padding:4px 0;">
          Illustrative calculation &mdash; not real ANUGA output.
        </div>
        """)

    return run_clicked and not errors, scenario


# ── Processing visualiser ──────────────────────────────────────────────────
def _run_with_progress(scenario: Scenario) -> SimulationResult:
    service = st.session_state.get("service")

    render_html(f"""
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                padding:24px 28px; margin-bottom:16px; box-shadow:0 2px 8px rgba(23,50,77,0.04);">
      <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                  text-transform:uppercase; margin-bottom:4px;">PROCESSING</div>
      <div style="font-size:1.0rem; font-weight:600; color:{_NAVY}; margin-bottom:4px;">
        Simulation in Progress
      </div>
      <div style="font-size:0.82rem; color:{_GREY};">
        Scenario ID:
        <span style="font-family:'IBM Plex Mono',monospace; color:{_TEAL};">{scenario.scenario_id}</span>
        &nbsp;&mdash;&nbsp; {AVAILABLE_DAMS[scenario.dam_id].name}
      </div>
    </div>
    """)

    progress_bar   = st.progress(0, text="Initialising...")
    status_ph      = st.empty()
    log_ph         = st.empty()
    logs: list[str] = []

    def _cb(status: SimulationStatus, msg: str, pct: float) -> None:
        logs.append(f"[{status.label()}] {msg}")
        progress_bar.progress(int(pct) / 100, text=f"{status.label()} — {msg}")
        status_ph.markdown(
            f"""
            <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-left:3px solid {_TEAL};
                        border-radius:6px; padding:10px 14px; font-size:0.82rem; color:{_NAVY};">
              <span style="font-weight:600; color:{_TEAL};">{status.label()}</span> &mdash; {msg}
              &nbsp;&nbsp;<span style="float:right; color:{_MUTED}; font-family:'IBM Plex Mono',monospace;">
                {pct:.0f}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        log_ph.code("\n".join(logs[-6:]), language="text")

    return service.submit(scenario, progress_callback=_cb, blocking=True)


# ── Centre panel: map + results ────────────────────────────────────────────
def _render_centre(result: SimulationResult | None) -> None:
    # Map header bar
    mh_left, mh_right = st.columns([5, 1])
    with mh_left:
        render_html(f"""
        <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-top-left-radius:6px;
                    border-top-right-radius:6px; padding:8px 16px; display:flex; align-items:center;
                    justify-content:space-between; font-family:'IBM Plex Mono',monospace;
                    font-size:0.74rem; color:{_NAVY}; margin-bottom:-2px; z-index:2; position:relative;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="display:inline-block; width:8px; height:8px; background:{_TEAL};
                         border-radius:50%;"></span>
            <b>STUDY AREA:</b>&nbsp;Hirakud Reservoir &amp; Mahanadi Basin &middot; Odisha
          </div>
          <div style="color:{_GREY};">LAT: 21.5250&deg; N &middot; LON: 83.8730&deg; E &middot; WGS 84</div>
        </div>
        """)
    with mh_right:
        if result and result.status == SimulationStatus.COMPLETED:
            tf = st.slider(
                "Time", 0.0, 1.0, 1.0, step=0.05, key="ws_tf",
                label_visibility="collapsed",
            )
            st.session_state["ws_time_fraction"] = tf

    # Map
    render_map(
        result=result,
        time_fraction=st.session_state.get("ws_time_fraction", 1.0),
        height=500,
        key="ws_map_main",
    )

    # No-result prompt
    if result is None:
        render_html(f"""
        <div style="background:{_WHITE}; border:1px dashed {_BORDER}; border-radius:8px;
                    padding:20px 24px; margin-top:12px; text-align:center;">
          <div style="font-size:0.92rem; color:{_NAVY}; font-weight:500; margin-bottom:6px;">
            Configure Parameters &amp; Run Simulation
          </div>
          <div style="font-size:0.82rem; color:{_GREY}; max-width:420px; margin:0 auto; line-height:1.6;">
            Use the configuration panel on the left to set breach conditions, then click
            <b>Run Simulation</b> to generate flood inundation layers on this map.
          </div>
        </div>
        """)
        return

    if result.status != SimulationStatus.COMPLETED:
        return

    # ── Warning band ──
    wl     = result.warning_level or "Low"
    wl_map = {
        "Low":      (_TEAL3,   "#EAF6FB"),
        "Moderate": (_AMBER,   "#FDF6E3"),
        "High":     ("#C0710B", "#FEF0E3"),
        "Critical": ("#C0392B", "#FDECEA"),
    }
    wl_col, wl_bg = wl_map.get(wl, wl_map["Low"])

    render_html(f"""
    <div style="background:{wl_bg}; border:1px solid {wl_col}; border-radius:6px;
                padding:10px 16px; margin-top:12px; display:flex; align-items:center;
                justify-content:space-between;">
      <div>
        <span style="font-size:0.75rem; font-weight:700; color:{wl_col}; letter-spacing:0.06em;
                     text-transform:uppercase;">{wl.upper()} FLOOD WARNING</span>
        <span style="font-size:0.78rem; color:{_GREY}; margin-left:12px;">
          Illustrative assessment &mdash; not official emergency guidance
        </span>
      </div>
      <span style="font-size:0.70rem; color:{_AMBER}; font-family:'IBM Plex Mono',monospace;
                   background:rgba(201,138,24,0.08); border:1px solid rgba(201,138,24,0.3);
                   border-radius:4px; padding:2px 8px;">DEMO DATA</span>
    </div>
    """)

    # ── KPI strip ──
    render_html(f"""
    <div style="border-top:1px solid {_BORDER}; margin:20px 0 12px 0;"></div>
    <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                text-transform:uppercase; margin-bottom:12px;">SIMULATION OUTPUTS</div>
    """)

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_items = [
        ("Flooded Area",   f"{result.flooded_area_km2:.1f}",    "km&sup2;",   _TEAL),
        ("Max Depth",      f"{result.max_water_depth_m:.1f}",   "m",          _TEAL2),
        ("Max Velocity",   f"{result.max_velocity_mps:.1f}",    "m/s",        _TEAL2),
        ("Affected Areas", str(result.affected_settlements),    "settlements", _NAVY),
        ("Peak Discharge", f"{result.peak_discharge_m3s:,.0f}", "m&sup3;/s",  _TEAL),
    ]
    for col, (label, value, unit, color) in zip([k1, k2, k3, k4, k5], kpi_items):
        with col:
            render_html(f"""
            <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                        padding:14px 10px; text-align:center;
                        box-shadow:0 2px 6px rgba(23,50,77,0.03);">
              <div style="font-size:1.4rem; font-weight:700; color:{color};
                          font-family:'IBM Plex Mono',monospace; line-height:1.1;">{value}</div>
              <div style="font-size:0.70rem; color:{_MUTED}; margin-top:2px;">{unit}</div>
              <div style="font-size:0.65rem; text-transform:uppercase; letter-spacing:1px;
                          color:{_GREY}; margin-top:4px;">{label}</div>
            </div>
            """)

    # ── Result Tabs ──
    render_html(f"""<div style="border-top:1px solid {_BORDER}; margin:24px 0 0 0;"></div>""")
    t_charts, t_risk, t_export = st.tabs([
        "Flood Propagation Charts",
        "Risk & Exposure Analysis",
        "Export GIS Layers",
    ])

    with t_charts:
        _render_charts_tab(result)

    with t_risk:
        _render_risk_tab(result)

    with t_export:
        _render_export_tab(result)


# ── Charts tab ─────────────────────────────────────────────────────────────
def _render_charts_tab(result: SimulationResult) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.warning("plotly not installed.")
        return

    if not result.time_steps:
        return

    _FONT = "'IBM Plex Sans', sans-serif"
    _BG_PLT = "#FFFFFF"
    _GRID = "#F7F8F6"
    _TEXT = "#68747D"

    col_a, col_b = st.columns([3, 2])

    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=result.time_steps, y=result.depth_at_steps,
            mode="lines+markers", name="Max Depth (m)",
            line=dict(color=_TEAL, width=2.5),
            marker=dict(size=4),
            fill="tozeroy", fillcolor=f"rgba(37,107,142,0.08)",
            yaxis="y1",
        ))
        fig.add_trace(go.Scatter(
            x=result.time_steps, y=result.area_at_steps,
            mode="lines", name="Flooded Area (km²)",
            line=dict(color=_TEAL2, width=2, dash="dot"),
            yaxis="y2",
        ))
        fig.update_layout(
            title=dict(text="Flood Propagation Over Time",
                       font=dict(size=13, color=_NAVY, family=_FONT)),
            paper_bgcolor=_BG_PLT, plot_bgcolor=_BG_PLT,
            font=dict(color=_TEXT, family=_FONT, size=11),
            height=280, margin=dict(l=10, r=10, t=45, b=30),
            xaxis=dict(title="Time (min)", gridcolor=_GRID, color=_TEXT,
                       linecolor=_BORDER, linewidth=1),
            yaxis=dict(title="Max Depth (m)", gridcolor=_GRID, color=_TEAL),
            yaxis2=dict(title="Flooded Area (km²)", overlaying="y", side="right",
                        color=_TEAL2, gridcolor="rgba(0,0,0,0)"),
            legend=dict(bgcolor=_BG_PLT, bordercolor=_BORDER, borderwidth=1,
                        font=dict(size=10)),
            annotations=[dict(
                text="Illustrative calculation — not ANUGA output",
                x=0.01, y=0.01, xref="paper", yref="paper",
                showarrow=False, font=dict(size=9, color=_MUTED),
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if not result.settlements_geojson:
            return
        counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0, "Safe": 0}
        for f in result.settlements_geojson.get("features", []):
            rl = f["properties"].get("risk_level", "None")
            if rl == "None":
                counts["Safe"] += 1
            elif rl in counts:
                counts[rl] += 1

        colors = ["#C0392B", "#C0710B", "#C98A18", _TEAL3, "#94A3B8"]
        fig2 = go.Figure(go.Pie(
            labels=list(counts.keys()),
            values=list(counts.values()),
            hole=0.55,
            marker=dict(colors=colors, line=dict(color=_WHITE, width=2)),
            textfont=dict(size=11, family=_FONT),
            textinfo="label+value",
        ))
        fig2.update_layout(
            title=dict(text="Settlement Risk Breakdown",
                       font=dict(size=13, color=_NAVY, family=_FONT)),
            paper_bgcolor=_BG_PLT,
            font=dict(color=_TEXT, family=_FONT, size=11),
            height=280, margin=dict(l=10, r=10, t=45, b=10),
            showlegend=False,
            annotations=[dict(
                text=f"<b>{result.affected_settlements or 0}</b><br><span style='font-size:9px'>affected</span>",
                x=0.5, y=0.5, font_size=14, font_color=_NAVY, showarrow=False,
            )],
        )
        st.plotly_chart(fig2, use_container_width=True)


# ── Risk tab ───────────────────────────────────────────────────────────────
def _render_risk_tab(result: SimulationResult) -> None:
    if not result.settlements_geojson:
        st.info("No settlement data available.")
        return

    features = result.settlements_geojson.get("features", [])
    affected = [f for f in features if f["properties"].get("affected")]
    safe     = [f for f in features if not f["properties"].get("affected")]

    # Summary row
    render_html(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:20px;">
      <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-top:3px solid #C0392B;
                  border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:700; color:#C0392B;
                    font-family:'IBM Plex Mono',monospace;">{len(affected)}</div>
        <div style="font-size:0.70rem; text-transform:uppercase; letter-spacing:1px;
                    color:{_GREY}; margin-top:4px;">Affected</div>
      </div>
      <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-top:3px solid {_TEAL3};
                  border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:700; color:{_TEAL3};
                    font-family:'IBM Plex Mono',monospace;">{len(safe)}</div>
        <div style="font-size:0.70rem; text-transform:uppercase; letter-spacing:1px;
                    color:{_GREY}; margin-top:4px;">Safe</div>
      </div>
      <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-top:3px solid {_NAVY};
                  border-radius:8px; padding:16px; text-align:center;">
        <div style="font-size:1.8rem; font-weight:700; color:{_NAVY};
                    font-family:'IBM Plex Mono',monospace;">{len(features)}</div>
        <div style="font-size:0.70rem; text-transform:uppercase; letter-spacing:1px;
                    color:{_GREY}; margin-top:4px;">Total Assessed</div>
      </div>
    </div>
    """)

    if affected:
        render_html(f"""
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:10px;">AFFECTED SETTLEMENTS</div>
        """)
        risk_order  = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3}
        risk_colors = {"Critical": "#C0392B", "High": "#C0710B",
                       "Moderate": _AMBER,  "Low": _TEAL3}
        sorted_aff = sorted(affected,
                             key=lambda f: risk_order.get(f["properties"].get("risk_level", "Low"), 99))
        for feat in sorted_aff:
            p  = feat["properties"]
            rl = p.get("risk_level", "Low")
            rc = risk_colors.get(rl, _MUTED)
            render_html(f"""
            <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-left:4px solid {rc};
                        border-radius:6px; padding:10px 14px; margin-bottom:6px;
                        display:flex; align-items:center; gap:12px;">
              <div style="flex:1;">
                <div style="font-size:0.88rem; font-weight:600; color:{_NAVY};">
                  {p.get('name', 'Settlement')}
                </div>
                <div style="font-size:0.76rem; color:{_GREY}; margin-top:2px;">
                  {p.get('type','').title()} &nbsp;&middot;&nbsp;
                  Pop &asymp; {p.get('population_approx', '?'):,} &nbsp;&middot;&nbsp;
                  Depth: {p.get('flood_depth_m', 0):.1f} m
                </div>
              </div>
              <div style="font-size:0.72rem; font-weight:700; color:{rc};
                          letter-spacing:0.06em; text-transform:uppercase;">{rl}</div>
            </div>
            """)

    render_html(f"""
    <div style="margin-top:16px; padding:10px 14px; background:#FDF6E3;
                border:1px solid rgba(201,138,24,0.4); border-radius:6px;
                font-size:0.76rem; color:{_AMBER};">
      <b>Scientific Honesty Notice:</b> All exposure data is derived from illustrative geometric
      calculations on synthetic terrain. Settlement locations are approximate. Do not use these
      outputs for official emergency planning or reporting. <b>DEMO DATA ONLY.</b>
    </div>
    """)


# ── Export tab ─────────────────────────────────────────────────────────────
def _render_export_tab(result: SimulationResult) -> None:
    import json

    render_html(f"""
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                padding:18px 20px; margin-bottom:16px; box-shadow:0 2px 6px rgba(23,50,77,0.03);">
      <div style="font-size:0.9rem; font-weight:600; color:{_NAVY}; margin-bottom:4px;">
        Export Simulation Results
      </div>
      <div style="font-size:0.82rem; color:{_GREY}; line-height:1.55;">
        Download GeoJSON layers for use in QGIS, ArcGIS, or any GIS tool.
        All data is labelled as illustrative &mdash; not production simulation output.
      </div>
    </div>
    """)

    ec1, ec2 = st.columns(2)
    with ec1:
        if result.flood_extent_geojson:
            st.download_button(
                "Download Flood Extent (GeoJSON)",
                data=json.dumps(result.flood_extent_geojson, indent=2),
                file_name=f"jalrakshak_{result.scenario_id}_flood_extent.geojson",
                mime="application/geo+json",
                use_container_width=True, key="dl_flood",
            )
        if result.risk_zones_geojson:
            st.download_button(
                "Download Risk Zones (GeoJSON)",
                data=json.dumps(result.risk_zones_geojson, indent=2),
                file_name=f"jalrakshak_{result.scenario_id}_risk_zones.geojson",
                mime="application/geo+json",
                use_container_width=True, key="dl_risk",
            )
    with ec2:
        if result.settlements_geojson:
            st.download_button(
                "Download Settlements (GeoJSON)",
                data=json.dumps(result.settlements_geojson, indent=2),
                file_name=f"jalrakshak_{result.scenario_id}_settlements.geojson",
                mime="application/geo+json",
                use_container_width=True, key="dl_settle",
            )
        summary = {
            "scenario_id":        result.scenario_id,
            "scenario_name":      result.scenario_name,
            "warning_level":      result.warning_level,
            "flooded_area_km2":   result.flooded_area_km2,
            "max_water_depth_m":  result.max_water_depth_m,
            "max_velocity_mps":   result.max_velocity_mps,
            "peak_discharge_m3s": result.peak_discharge_m3s,
            "affected_settlements": result.affected_settlements,
            "duration_min":       result.duration_min,
            "is_mock":            result.is_mock,
            "data_source_label":  result.data_source_label,
        }
        st.download_button(
            "Download Summary Report (JSON)",
            data=json.dumps(summary, indent=2),
            file_name=f"jalrakshak_{result.scenario_id}_summary.json",
            mime="application/json",
            use_container_width=True, key="dl_summary",
        )

    render_html(f"""
    <div style="margin-top:16px; padding:10px 16px; background:{_WHITE}; border:1px solid {_BORDER};
                border-radius:6px; font-size:0.76rem; color:{_GREY};">
      All GeoJSON exports are RFC 7946 compliant. Coordinates are in WGS84 (EPSG:4326).
      Loadable directly into QGIS, ArcGIS Pro, or any web mapping framework.<br>
      <span style="color:{_AMBER};">All data is for demonstration purposes only.</span>
    </div>
    """)


# ── Main entry ─────────────────────────────────────────────────────────────
def render_dashboard(history: list[SimulationResult]) -> None:  # noqa: ARG001
    """Render Page 2 -- Simulation Workspace, visually matching Page 1."""
    _init_state()

    # Apply Page 1 design system CSS
    render_html(_PAGE2_CSS)

    # ── Workspace header (same visual language as Page 1 header) ──────────
    render_html(f"""
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                padding:20px 28px; margin-bottom:24px;
                box-shadow:0 2px 8px rgba(23,50,77,0.04);
                display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:4px;">02 &mdash; SIMULATION WORKSPACE</div>
        <div style="font-size:1.5rem; font-weight:600; color:{_NAVY}; margin-bottom:4px;
                    letter-spacing:-0.01em;">
          Dam-Break Flood Simulation
        </div>
        <div style="font-size:0.88rem; color:{_GREY};">
          Configure breach conditions &rarr; Run simulation &rarr; Analyse inundation &rarr; Export GIS layers
        </div>
      </div>
      <div style="text-align:right;">
        <div style="display:inline-block; font-size:0.70rem; font-weight:600; color:{_AMBER};
                    background:rgba(201,138,24,0.08); border:1px solid rgba(201,138,24,0.35);
                    border-radius:4px; padding:3px 10px; letter-spacing:0.05em;
                    font-family:'IBM Plex Mono',monospace; margin-bottom:6px;">
          PHASE 1 PROTOTYPE
        </div>
        <div style="font-size:0.72rem; color:{_MUTED}; font-family:'IBM Plex Mono',monospace;">
          SIH 2026 &middot; SIH26161 &middot; Team VisionSix
        </div>
      </div>
    </div>
    """)

    # ── Three-column layout ───────────────────────────────────────────────
    col_left, col_centre, col_right = st.columns([1.6, 4.0, 1.6], gap="medium")

    with col_left:
        _render_config_panel()

    with col_right:
        run_clicked, scenario = _render_run_panel()

    # Handle simulation run (before rendering centre so result is fresh)
    if run_clicked and scenario:
        with col_centre:
            result = _run_with_progress(scenario)
            if result.status == SimulationStatus.COMPLETED:
                st.session_state["ws_result"] = result
                st.session_state["current_result"] = result
                st.success("Simulation complete. Results loaded below.")
            else:
                st.error(f"Simulation failed: {result.status_message}")
            st.rerun()

    with col_centre:
        _render_centre(st.session_state.get("ws_result"))
