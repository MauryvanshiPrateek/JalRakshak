"""
Results page — full map + KPIs + timeline + charts + warnings.
Design system: Page 1 light institutional palette.
"""
from __future__ import annotations
import copy
import streamlit as st
from models.simulation_result import SimulationResult
from gis.flood_extent import flood_extent_geojson

_TEAL   = "#256B8E"
_NAVY   = "#17324D"
_GREY   = "#68747D"
_BORDER = "#D7DDE1"
_MUTED  = "#94A3B8"
_AMBER  = "#C98A18"


def render_results(result: SimulationResult) -> None:
    """Render the full results screen in the Page 1 design system."""
    from app.components.map_view import render_map
    from app.components.kpis import render_kpis
    from app.components.charts import render_charts
    from app.components.warnings import render_warnings

    if result.status.value != "completed":
        st.info("Simulation not yet completed.")
        return

    # ── Section header ──────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:4px;">GIS FLOOD PROPAGATION MAP</div>
        <div style="font-size:0.82rem; color:{_GREY}; margin-bottom:12px;">
            Use the <b style="color:{_NAVY};">layer panel</b> (top-right of map) to switch base maps
            and toggle overlays. Use the <b style="color:{_NAVY};">timeline</b> below to animate
            flood propagation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Timeline slider ──────────────────────────────────────────────────────
    time_steps = result.time_steps or [0.0, result.duration_min or 60.0]
    min_t, max_t = time_steps[0], time_steps[-1]

    t_val = st.slider(
        "Timeline — Flood Propagation",
        min_value=float(min_t),
        max_value=float(max_t),
        value=float(max_t),
        step=float((max_t - min_t) / max(len(time_steps) - 1, 1)),
        format="%.0f min",
        key="timeline_slider",
    )

    time_fraction = (t_val - min_t) / (max_t - min_t) if max_t > min_t else 1.0
    time_fraction = max(0.01, min(1.0, time_fraction))

    display_result = copy.copy(result)
    if result.flood_extent_geojson and time_fraction < 1.0:
        bw  = _extract_param(result, "breach_width_m", 30.0)
        bd  = _extract_param(result, "breach_depth_m", 15.0)
        dur = result.duration_min or 60.0
        display_result.flood_extent_geojson = flood_extent_geojson(bw, bd, dur, time_fraction)

    # ── Map header bar ──────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid {_BORDER}; border-top-left-radius:6px;
                    border-top-right-radius:6px; padding:8px 16px; display:flex; align-items:center;
                    justify-content:space-between; font-family:'IBM Plex Mono',monospace;
                    font-size:0.74rem; color:{_NAVY}; margin-bottom:-2px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="display:inline-block; width:8px; height:8px; background:{_TEAL};
                         border-radius:50%;"></span>
            <b>STUDY AREA:</b>&nbsp;Hirakud Reservoir &amp; Mahanadi Basin &middot; Odisha
          </div>
          <div style="color:{_GREY};">LAT: 21.5250&deg; N &middot; LON: 83.8730&deg; E &middot; WGS 84</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Map ─────────────────────────────────────────────────────────────────
    render_map(display_result, time_fraction=time_fraction)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    render_kpis(result)

    # ── Charts header ──────────────────────────────────────────────────────
    st.markdown(
        f"""<div style="border-top:1px solid {_BORDER}; margin:24px 0 12px 0;"></div>
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:12px;">ANALYSIS CHARTS</div>""",
        unsafe_allow_html=True,
    )
    render_charts(result)

    # ── Warnings ────────────────────────────────────────────────────────────
    render_warnings(result)


def _extract_param(result: SimulationResult, key: str, default):
    """Try to extract a scenario param stored on the result object."""
    return getattr(result, key, None) or default
