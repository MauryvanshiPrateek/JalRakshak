"""
KPI cards component — flooded area, max depth, velocity, risk summary.
Design system: Page 1 light institutional palette.
"""
from __future__ import annotations
import streamlit as st
from models.simulation_result import SimulationResult

_NAVY   = "#17324D"
_TEAL   = "#256B8E"
_TEAL2  = "#2D78A8"
_TEAL3  = "#5FA8D3"
_GREY   = "#68747D"
_MUTED  = "#94A3B8"
_BORDER = "#D7DDE1"
_BG     = "#F7F8F6"
_WHITE  = "#FFFFFF"
_AMBER  = "#C98A18"

_WL_CFG = {
    "Low":      {"border": _TEAL3,   "bg": "#EAF6FB", "text": _TEAL3,   "label": "LOW FLOOD WARNING"},
    "Moderate": {"border": _AMBER,   "bg": "#FDF6E3", "text": _AMBER,   "label": "MODERATE FLOOD WARNING"},
    "High":     {"border": "#C0710B","bg": "#FEF0E3", "text": "#C0710B","label": "HIGH FLOOD WARNING"},
    "Critical": {"border": "#C0392B","bg": "#FDECEA", "text": "#C0392B","label": "CRITICAL FLOOD WARNING"},
}


def _kpi_card(label: str, value: str, unit: str, color: str = _TEAL) -> str:
    return f"""
    <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-top:3px solid {color};
                border-radius:8px; padding:16px 12px; text-align:center;
                box-shadow:0 2px 6px rgba(23,50,77,0.03);">
        <div style="font-size:1.45rem; font-weight:700; color:{color};
                    font-family:'IBM Plex Mono',monospace; line-height:1.1;">{value}</div>
        <div style="font-size:0.70rem; color:{_MUTED}; margin-top:3px;">{unit}</div>
        <div style="font-size:0.64rem; text-transform:uppercase; letter-spacing:1px;
                    color:{_GREY}; margin-top:5px;">{label}</div>
    </div>
    """


def render_kpis(result: SimulationResult | None) -> None:
    """Render KPI card row in the Page 1 design system."""
    st.markdown(
        f"""<div style="border-top:1px solid {_BORDER}; margin:16px 0 12px 0;"></div>
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:12px;">SIMULATION OUTPUTS</div>""",
        unsafe_allow_html=True,
    )

    if result is None or result.status.value not in ("completed",):
        st.info("Run a simulation to see results here.")
        return

    # Warning level banner
    wl  = result.warning_level or "Low"
    wlc = _WL_CFG.get(wl, _WL_CFG["Low"])
    st.markdown(
        f"""
        <div style="background:{wlc['bg']}; border:1px solid {wlc['border']}; border-left:4px solid {wlc['border']};
                    border-radius:6px; padding:10px 16px; margin-bottom:14px;
                    display:flex; align-items:center; justify-content:space-between;">
            <div>
                <span style="font-size:0.78rem; font-weight:700; color:{wlc['text']};
                             letter-spacing:0.06em; text-transform:uppercase;">{wlc['label']}</span>
                <span style="font-size:0.76rem; color:{_GREY}; margin-left:12px;">
                    Based on illustrative calculation &mdash; not official emergency guidance
                </span>
            </div>
            <span style="font-size:0.70rem; color:{_AMBER}; font-family:'IBM Plex Mono',monospace;
                         background:rgba(201,138,24,0.08); border:1px solid rgba(201,138,24,0.3);
                         border-radius:4px; padding:2px 8px;">DEMO DATA</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    flooded  = f"{result.flooded_area_km2:.1f}"   if result.flooded_area_km2    is not None else "—"
    max_d    = f"{result.max_water_depth_m:.1f}"  if result.max_water_depth_m   is not None else "—"
    max_v    = f"{result.max_velocity_mps:.1f}"   if result.max_velocity_mps    is not None else "—"
    affected = str(result.affected_settlements)   if result.affected_settlements is not None else "—"

    with c1: st.markdown(_kpi_card("Flooded Area",  flooded,  "km&sup2;",    _TEAL),  unsafe_allow_html=True)
    with c2: st.markdown(_kpi_card("Max Depth",     max_d,    "metres",      _TEAL2), unsafe_allow_html=True)
    with c3: st.markdown(_kpi_card("Max Velocity",  max_v,    "m/s",         _TEAL2), unsafe_allow_html=True)
    with c4: st.markdown(_kpi_card("Affected Areas",affected, "settlements", _NAVY),  unsafe_allow_html=True)

    # Discharge footer
    if result.peak_discharge_m3s:
        st.markdown(
            f"""
            <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:6px;
                        padding:8px 14px; font-size:0.80rem; color:{_GREY}; margin-top:8px;">
                <b style="color:{_NAVY};">Peak Breach Discharge:</b>
                {result.peak_discharge_m3s:,.0f} m&sup3;/s
                &nbsp;|&nbsp;
                <b style="color:{_NAVY};">Duration:</b> {result.duration_min:.0f} min
                &nbsp;|&nbsp;
                <span style="font-size:0.72rem; color:{_AMBER};">{result.data_source_label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
