"""
Sidebar component — scenario configuration controls.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import yaml
from models.scenario import Scenario, AVAILABLE_DAMS


def _load_presets() -> dict:
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config", "scenarios.yaml"
    )
    try:
        with open(config_path) as f:
            return yaml.safe_load(f).get("scenarios", {})
    except Exception:
        return {}


def render_sidebar() -> tuple[Scenario | None, bool]:
    """
    Render the left-panel scenario configuration.

    Returns
    -------
    scenario : Scenario | None
        The configured scenario, or None if not yet submitted.
    run_clicked : bool
        True if the user clicked 'Run Simulation'.
    """
    presets = _load_presets()

    with st.sidebar:
        # Header
        st.markdown(
            """
            <div style="padding: 8px 0 16px 0;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
                    <svg width="26" height="26" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 8L18 5L32 8V12L18 9L4 12V8Z" fill="#17324D"/>
                        <path d="M7 13L18 10.5L29 13V17L18 14.5L7 17V13Z" fill="#256B8E"/>
                        <path d="M10 18L18 16L26 18V22L18 20L10 22V18Z" fill="#2D78A8"/>
                        <path d="M15 23C15 28 12 30 7 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M21 23C21 27 24 29 29 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                        <line x1="18" y1="21" x2="18" y2="33" stroke="#256B8E" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#17324D; letter-spacing:0.03em; line-height:1.1;">JalRakshak</div>
                        <div style="font-size:0.68rem; color:#68747D; letter-spacing:0.04em; font-family:'IBM Plex Sans',sans-serif;">Dam-Break Flood Analysis</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Dam Selection ────────────────────────────────────────────────
        st.markdown("#### 🏔️ Study Area")
        dam_options = {v.name: k for k, v in AVAILABLE_DAMS.items()}
        selected_dam_name = st.selectbox(
            "Select Dam",
            list(dam_options.keys()),
            help="Demo study area. More dams can be added as datasets become available.",
        )
        dam_id = dam_options[selected_dam_name]
        dam = AVAILABLE_DAMS[dam_id]

        st.markdown(
            f"""
            <div style="background:#1e293b; border-radius:8px; padding:10px 14px;
                        border-left:3px solid #38bdf8; font-size:0.82rem; color:#cbd5e1; margin-bottom:8px;">
                📍 {dam.location_description}<br>
                🌊 {dam.river}<br>
                ⬆️ Height: {dam.height_m} m &nbsp;|&nbsp; Storage: {dam.storage_mcm:,.0f} MCM
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Preset Buttons ────────────────────────────────────────────────
        st.markdown("#### ⚡ Breach Presets")
        preset_cols = st.columns(3)
        chosen_preset = st.session_state.get("chosen_preset", None)

        preset_styles = {
            "small":  ("🟢", "Small"),
            "medium": ("🟡", "Medium"),
            "severe": ("🔴", "Severe"),
        }

        for col, (key, (icon, label)) in zip(preset_cols, preset_styles.items()):
            with col:
                if st.button(f"{icon}\n{label}", key=f"preset_{key}", use_container_width=True):
                    st.session_state["chosen_preset"] = key

        st.markdown("---")

        # ── Parameter Inputs ──────────────────────────────────────────────
        st.markdown("#### 🔧 Breach Parameters")

        preset_data = presets.get(st.session_state.get("chosen_preset", ""), {})

        breach_width = st.slider(
            "Breach Width (m)",
            min_value=5, max_value=150,
            value=int(preset_data.get("breach_width_m", 30)),
            step=5,
            help="Horizontal width of the breach opening in the dam wall.",
        )
        breach_depth = st.slider(
            "Breach Depth (m)",
            min_value=2, max_value=int(dam.height_m),
            value=min(int(preset_data.get("breach_depth_m", 15)), int(dam.height_m)),
            step=1,
            help="Vertical depth of the breach from the dam crest.",
        )
        reservoir_level = st.slider(
            "Reservoir Water Level (m)",
            min_value=10, max_value=int(dam.height_m),
            value=min(55, int(dam.height_m)),
            step=1,
            help="Water level in the reservoir above the dam base at time of breach.",
        )
        formation_time = st.slider(
            "Breach Formation Time (min)",
            min_value=1, max_value=60,
            value=int(preset_data.get("formation_time_min", 10)),
            step=1,
            help="Time for the breach to reach full dimensions.",
        )
        duration = st.slider(
            "Simulation Duration (min)",
            min_value=15, max_value=180,
            value=int(preset_data.get("duration_min", 60)),
            step=15,
            help="How long to simulate flood propagation.",
        )

        st.markdown("---")

        # ── Assumptions box ───────────────────────────────────────────────
        with st.expander("📋 Simulation Assumptions", expanded=False):
            st.markdown(
                """
                - Model: Illustrative weir-based calculation (Phase 1 mock)
                - Manning roughness: 0.035 (channel) / 0.06 (floodplain)
                - DEM: Synthetic terrain — not real survey data
                - CRS: EPSG:4326 (WGS84)
                - Downstream boundary: Free outflow (assumed)
                - Breach shape: Rectangular (simplified)
                - ⚠️ All outputs are DEMO DATA only
                """
            )

        st.markdown("---")

        # ── Run Button ────────────────────────────────────────────────────
        run_clicked = st.button(
            "▶  RUN SIMULATION",
            type="primary",
            use_container_width=True,
            key="run_simulation_btn",
        )

        scenario = Scenario(
            dam_id=dam_id,
            breach_width_m=float(breach_width),
            breach_depth_m=float(breach_depth),
            formation_time_min=float(formation_time),
            duration_min=float(duration),
            reservoir_level_m=float(reservoir_level),
            preset_name=st.session_state.get("chosen_preset", "Custom").title()
            if st.session_state.get("chosen_preset")
            else "Custom",
        )

        # Validation preview
        errors = scenario.validate()
        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")

        st.markdown(
            """
            <div style="font-size:0.7rem; color:#475569; text-align:center; padding-top:8px;">
                JalRakshak v0.1 · SIH 2026 · Team VisionSix
            </div>
            """,
            unsafe_allow_html=True,
        )

    return scenario, run_clicked and not errors
