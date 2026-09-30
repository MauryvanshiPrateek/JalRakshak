"""
Warning panel component — shows affected settlements and risk alerts.
Design system: Page 1 light institutional palette.
"""
from __future__ import annotations
import streamlit as st
from models.simulation_result import SimulationResult

# Page 1 design tokens
_NAVY   = "#17324D"
_TEAL   = "#256B8E"
_TEAL3  = "#5FA8D3"
_GREY   = "#68747D"
_MUTED  = "#94A3B8"
_BORDER = "#D7DDE1"
_BG     = "#F7F8F6"
_WHITE  = "#FFFFFF"
_AMBER  = "#C98A18"

_RISK_CFG = {
    "Critical": {"border": "#C0392B", "bg": "#FDECEA", "text": "#C0392B", "label": "CRITICAL"},
    "High":     {"border": "#C0710B", "bg": "#FEF0E3", "text": "#C0710B", "label": "HIGH"},
    "Moderate": {"border": "#C98A18", "bg": "#FDF6E3", "text": "#C98A18", "label": "MODERATE"},
    "Low":      {"border": _TEAL3,   "bg": "#EAF6FB", "text": _TEAL3,   "label": "LOW"},
}

_WL_CFG = {
    "Critical": {"border": "#C0392B", "bg": "#FDECEA", "text": "#C0392B"},
    "High":     {"border": "#C0710B", "bg": "#FEF0E3", "text": "#C0710B"},
    "Moderate": {"border": "#C98A18", "bg": "#FDF6E3", "text": "#C98A18"},
    "Low":      {"border": _TEAL3,   "bg": "#EAF6FB", "text": _TEAL3},
}


def render_warnings(result: SimulationResult | None) -> None:
    """Render warning panel and affected-locations list in the Page 1 design system."""
    if result is None or result.status.value != "completed":
        return

    wl  = result.warning_level or "Low"
    wlc = _WL_CFG.get(wl, _WL_CFG["Low"])

    st.markdown(
        f"""<div style="border-top:1px solid {_BORDER}; margin:24px 0 16px 0;"></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                    text-transform:uppercase; margin-bottom:12px;">FLOOD RISK ASSESSMENT</div>
        """,
        unsafe_allow_html=True,
    )

    # Main warning banner
    st.markdown(
        f"""
        <div style="background:{wlc['bg']}; border:1px solid {wlc['border']}; border-left:4px solid {wlc['border']};
                    border-radius:8px; padding:14px 20px; margin-bottom:20px;">
            <div style="font-size:0.75rem; font-weight:700; color:{wlc['text']}; letter-spacing:0.06em;
                        text-transform:uppercase; margin-bottom:4px;">{wl.upper()} FLOOD RISK</div>
            <div style="font-size:0.88rem; color:{_NAVY}; font-weight:600; margin-bottom:6px;">
                Scenario: {result.scenario_name or 'Custom'}
            </div>
            <div style="font-size:0.82rem; color:{_GREY}; line-height:1.7;">
                Max water depth:
                <b style="color:{_NAVY};">{result.max_water_depth_m:.1f} m</b>
                &nbsp;|&nbsp;
                Flooded area:
                <b style="color:{_NAVY};">{result.flooded_area_km2:.1f} km&sup2;</b>
                &nbsp;|&nbsp;
                Peak discharge:
                <b style="color:{_NAVY};">{result.peak_discharge_m3s:,.0f} m&sup3;/s</b>
            </div>
            <div style="font-size:0.72rem; color:{_MUTED}; margin-top:8px;">
                {result.data_source_label} &mdash; Not official emergency guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            f"""<div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                            text-transform:uppercase; margin-bottom:10px;">AFFECTED SETTLEMENTS</div>""",
            unsafe_allow_html=True,
        )
        if result.settlements_geojson:
            affected = [
                f for f in result.settlements_geojson.get("features", [])
                if f["properties"].get("affected")
            ]
            order = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3}
            affected.sort(key=lambda f: order.get(f["properties"].get("risk_level", "Low"), 4))

            if affected:
                for f in affected[:10]:
                    p    = f["properties"]
                    risk = p.get("risk_level", "Low")
                    rc   = _RISK_CFG.get(risk, _RISK_CFG["Low"])
                    st.markdown(
                        f"""
                        <div style="background:{_WHITE}; border:1px solid {_BORDER};
                                    border-left:4px solid {rc['border']}; border-radius:6px;
                                    padding:9px 13px; margin-bottom:6px; font-size:0.82rem;">
                            <div style="font-weight:600; color:{_NAVY};">{p.get('name')}</div>
                            <div style="color:{_GREY}; margin-top:2px; font-size:0.76rem;">
                                Est. depth: {p.get('flood_depth_m', 0):.1f} m
                                &nbsp;|&nbsp;
                                Pop. (approx): {p.get('population_approx', 0):,}
                                &nbsp;|&nbsp;
                                <span style="color:{rc['text']}; font-weight:600;">{rc['label']}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                if len(affected) > 10:
                    st.caption(f"…and {len(affected) - 10} more settlements")
            else:
                st.success("No settlements identified in flood zone (demo data).")
        else:
            st.info("No settlement data available.")

    with col2:
        st.markdown(
            f"""<div style="font-size:0.75rem; font-weight:700; color:{_TEAL}; letter-spacing:0.08em;
                            text-transform:uppercase; margin-bottom:10px;">RISK SUMMARY</div>""",
            unsafe_allow_html=True,
        )
        if result.settlements_geojson:
            all_s = result.settlements_geojson.get("features", [])
            total = len(all_s)
            aff   = len([f for f in all_s if f["properties"].get("affected")])
            safe  = total - aff

            for level in ["Critical", "High", "Moderate", "Low"]:
                cnt = len([
                    f for f in all_s
                    if f["properties"].get("affected") and
                    f["properties"].get("risk_level") == level
                ])
                if cnt:
                    rc      = _RISK_CFG[level]
                    bar_pct = int(cnt / total * 100) if total else 0
                    st.markdown(
                        f"""
                        <div style="margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between;
                                        font-size:0.82rem; color:{_NAVY}; margin-bottom:4px;">
                                <span style="font-weight:500;">{level}</span>
                                <span style="font-weight:700; color:{rc['text']};">{cnt}</span>
                            </div>
                            <div style="background:{_BG}; border:1px solid {_BORDER};
                                        border-radius:4px; height:6px;">
                                <div style="background:{rc['border']}; width:{bar_pct}%;
                                            height:6px; border-radius:4px;"></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f"""
                <div style="background:{_WHITE}; border:1px solid {_BORDER}; border-radius:8px;
                            padding:14px; font-size:0.82rem; color:{_GREY}; margin-top:12px; text-align:center;">
                    <div style="font-size:1.4rem; font-weight:700; color:{_NAVY};
                                font-family:'IBM Plex Mono',monospace;">{aff}</div>
                    <div style="margin-top:2px;">of {total} settlements affected</div>
                    <div style="color:#2D7A3A; font-size:0.76rem; margin-top:6px; font-weight:500;">
                        {safe} safe
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
