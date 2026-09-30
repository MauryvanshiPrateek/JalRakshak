"""
Charts component — Plotly visualizations for simulation results.
"""
from __future__ import annotations
import streamlit as st

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from models.simulation_result import SimulationResult

_BG_PLT    = "#FFFFFF"
_GRID_COLOR = "#F7F8F6"
_TEXT_COLOR = "#68747D"
_NAVY       = "#17324D"
_TEAL       = "#256B8E"
_TEAL2      = "#2D78A8"
_BORDER     = "#D7DDE1"
_MUTED      = "#94A3B8"
_FONT = "'IBM Plex Sans', 'IBM Plex Mono', sans-serif"


def render_charts(result: SimulationResult | None) -> None:
    """Render time-series and risk breakdown charts."""
    if not PLOTLY_AVAILABLE:
        st.warning("plotly not installed.")
        return

    if result is None or result.status.value != "completed":
        return

    col_a, col_b = st.columns([3, 2])

    with col_a:
        _render_depth_timeseries(result)

    with col_b:
        _render_risk_pie(result)


def _render_depth_timeseries(result: SimulationResult):
    """Flood depth and area over simulation time."""
    if not result.time_steps:
        return

    fig = go.Figure()

    # Depth trace
    fig.add_trace(go.Scatter(
        x=result.time_steps,
        y=result.depth_at_steps,
        mode="lines+markers",
        name="Max Depth (m)",
        line=dict(color=_TEAL, width=2.5),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(37,107,142,0.10)",
        yaxis="y1",
    ))

    # Area trace on secondary axis
    fig.add_trace(go.Scatter(
        x=result.time_steps,
        y=result.area_at_steps,
        mode="lines",
        name="Flooded Area (km\u00b2)",
        line=dict(color=_TEAL2, width=2, dash="dot"),
        yaxis="y2",
    ))

    fig.update_layout(
        title=dict(
            text="Flood Propagation Over Time",
            font=dict(size=13, color=_NAVY, family=_FONT),
        ),
        paper_bgcolor=_BG_PLT,
        plot_bgcolor=_BG_PLT,
        font=dict(color=_TEXT_COLOR, family=_FONT, size=11),
        height=270,
        margin=dict(l=10, r=10, t=45, b=30),
        xaxis=dict(
            title="Time (min)",
            gridcolor=_GRID_COLOR,
            color=_TEXT_COLOR,
            linecolor=_BORDER,
        ),
        yaxis=dict(
            title="Max Depth (m)",
            gridcolor=_GRID_COLOR,
            color=_TEAL,
        ),
        yaxis2=dict(
            title="Flooded Area (km\u00b2)",
            overlaying="y",
            side="right",
            color=_TEAL2,
            gridcolor="rgba(0,0,0,0)",
        ),
        legend=dict(
            bgcolor=_BG_PLT,
            bordercolor=_BORDER,
            borderwidth=1,
            font=dict(size=10),
        ),
        annotations=[
            dict(
                text="Illustrative \u2014 not ANUGA output",
                x=0.01, y=0.01, xref="paper", yref="paper",
                showarrow=False, font=dict(size=9, color=_MUTED),
            )
        ],
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_risk_pie(result: SimulationResult):
    """Risk zone breakdown donut chart."""
    if not result.settlements_geojson:
        return

    # Count settlements per risk level
    counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0, "Safe": 0}
    for f in result.settlements_geojson.get("features", []):
        rl = f["properties"].get("risk_level", "None")
        if rl == "None":
            counts["Safe"] += 1
        elif rl in counts:
            counts[rl] += 1

    labels = list(counts.keys())
    values = list(counts.values())
    colors = ["#C0392B", "#C0710B", "#C98A18", "#5FA8D3", "#94A3B8"]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textfont=dict(size=11, family=_FONT),
        textinfo="label+value",
    ))

    fig.update_layout(
        title=dict(
            text="Settlement Risk Breakdown",
            font=dict(size=13, color=_NAVY, family=_FONT),
        ),
        paper_bgcolor=_BG_PLT,
        font=dict(color=_TEXT_COLOR, family=_FONT, size=11),
        height=270,
        margin=dict(l=10, r=10, t=45, b=10),
        showlegend=False,
        annotations=[dict(
            text=f"<b>{result.affected_settlements or 0}</b><br><span style='font-size:9px'>affected</span>",
            x=0.5, y=0.5, font_size=14, font_color=_NAVY,
            showarrow=False,
        )],
    )

    st.plotly_chart(fig, use_container_width=True)
