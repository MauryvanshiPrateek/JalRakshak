"""
Interactive Folium map component.

Uses Folium's native LayerControl to provide:
  - Radio buttons for base layers  (Satellite / OpenStreetMap / Topo)
  - Checkboxes  for overlay layers (Place Labels / Flood Extent /
                                    Risk Zones / Settlements / Roads / River)

No Streamlit checkboxes needed — everything lives inside the map panel.
"""
from __future__ import annotations
import streamlit as st

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

from gis.domain import (
    DAM_LAT, DAM_LON, DAM_NAME, STUDY_CENTER_LAT, STUDY_CENTER_LON,
    MAHANADI_CENTRELINE,
)
from models.simulation_result import SimulationResult
from gis.risk import RISK_COLORS


def render_map(
    result: SimulationResult | None,
    time_fraction: float = 1.0,
    height: int = 560,
    key: str | None = None,
    **_kwargs,          # absorb stale show_flood / show_risk / map_style args
) -> None:
    """
    Render the interactive Folium map.

    All layer visibility is controlled inside the Folium LayerControl panel
    (radio buttons for base maps, checkboxes for overlays).
    """
    if not FOLIUM_AVAILABLE:
        st.error("folium / streamlit-folium not installed. "
                 "Run: pip install folium streamlit-folium")
        return

    # ── Base map (tiles=None so we add layers manually) ──────────────────
    m = folium.Map(
        location=[STUDY_CENTER_LAT, STUDY_CENTER_LON],
        zoom_start=10,
        tiles=None,
        control_scale=True,
    )

    # ═══════════════════════════════════════════════════════════════════════
    # BASE LAYERS  (overlay=False  →  radio buttons in LayerControl)
    # ═══════════════════════════════════════════════════════════════════════

    # 1. Esri Satellite  (default — shown first)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="🛰️  Satellite",
        overlay=False,
        control=True,
        show=True,          # active by default
    ).add_to(m)

    # 2. OpenStreetMap
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© OpenStreetMap contributors",
        name="🗺️  OpenStreetMap",
        overlay=False,
        control=True,
        show=False,
    ).add_to(m)

    # 3. Esri World Topo
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Topo Map",
        name="🏔️  Topo Map",
        overlay=False,
        control=True,
        show=False,
    ).add_to(m)

    # ═══════════════════════════════════════════════════════════════════════
    # OVERLAY LAYERS  (overlay=True  →  checkboxes in LayerControl)
    # ═══════════════════════════════════════════════════════════════════════

    # Place Labels (Esri reference)
    folium.TileLayer(
        tiles="https://services.arcgisonline.com/ArcGIS/rest/services/"
              "Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="🏷️  Place Labels",
        overlay=True,
        control=True,
        show=True,
        opacity=0.85,
    ).add_to(m)

    # ── Dam marker (always visible, not in layer control) ─────────────────
    folium.Marker(
        location=[DAM_LAT, DAM_LON],
        popup=folium.Popup(
            f"<b>{DAM_NAME}</b><br>Height: 60.96 m<br>River: Mahanadi<br>"
            f"Storage: 8,141 MCM<br><small>⚠️ Demo location</small>",
            max_width=220,
        ),
        tooltip=DAM_NAME,
        icon=folium.Icon(color="blue", icon="tint", prefix="fa"),
    ).add_to(m)

    # ── River centreline ──────────────────────────────────────────────────
    river_group = folium.FeatureGroup(name="🌊  Mahanadi River", show=True)
    folium.PolyLine(
        locations=[[c[1], c[0]] for c in MAHANADI_CENTRELINE],
        color="#38bdf8",
        weight=3,
        opacity=0.9,
        tooltip="Mahanadi River (approx. centreline — demo)",
        dash_array="8 4",
    ).add_to(river_group)
    river_group.add_to(m)

    # ── Study area bounding box ───────────────────────────────────────────
    folium.Rectangle(
        bounds=[[21.30, 83.70], [21.75, 84.60]],
        color="#475569",
        weight=1,
        fill=False,
        dash_array="6 4",
        tooltip="Study Area Boundary (Demo)",
    ).add_to(m)

    # ── Simulation result layers ──────────────────────────────────────────
    if result and result.status.value == "completed":

        # Flood Extent
        if result.flood_extent_geojson:
            _add_flood_extent(m, result.flood_extent_geojson, time_fraction)

        # Risk Zones
        if result.risk_zones_geojson:
            _add_risk_zones(m, result.risk_zones_geojson)

        # Settlements
        if result.settlements_geojson:
            _add_settlements(m, result.settlements_geojson)

        # Roads
        if result.roads_geojson:
            _add_roads(m, result.roads_geojson)

    # ── Legend (bottom-left, away from LayerControl) ─────────────────────
    _add_legend(m)

    # ── LayerControl — collapsed=False so panel is always open ───────────
    folium.LayerControl(
        position="topright",
        collapsed=False,
    ).add_to(m)

    st_folium(m, use_container_width=True, height=height, returned_objects=[], key=key)


# ---------------------------------------------------------------------------
# Layer helpers
# ---------------------------------------------------------------------------

def _add_flood_extent(m, geojson: dict, time_fraction: float):
    group = folium.FeatureGroup(name="🔵  Flood Extent", show=True)
    folium.GeoJson(
        geojson,
        style_function=lambda _: {
            "fillColor": "#1d4ed8",
            "color": "#60a5fa",
            "weight": 2,
            "fillOpacity": max(0.05, 0.40 * time_fraction),
        },
        tooltip=folium.GeoJsonTooltip(["name", "severity", "data_source"]),
    ).add_to(group)
    group.add_to(m)


def _add_risk_zones(m, geojson: dict):
    def _style(feature):
        color = feature["properties"].get("color", "#94a3b8")
        return {
            "fillColor": color,
            "color": color,
            "weight": 1,
            "fillOpacity": 0.32,
        }
    group = folium.FeatureGroup(name="⚠️  Risk Zones", show=True)
    folium.GeoJson(
        geojson,
        style_function=_style,
        tooltip=folium.GeoJsonTooltip(["risk_level", "description"]),
    ).add_to(group)
    group.add_to(m)


def _add_settlements(m, geojson: dict):
    group = folium.FeatureGroup(name="🏘️  Settlements", show=True)
    for feature in geojson.get("features", []):
        props = feature["properties"]
        lon, lat = feature["geometry"]["coordinates"]
        affected = props.get("affected", False)
        risk = props.get("risk_level", "None")
        color = RISK_COLORS.get(risk, "#94a3b8") if affected else "#64748b"

        folium.CircleMarker(
            location=[lat, lon],
            radius=8 if affected else 4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            weight=2,
            popup=folium.Popup(
                f"<b>{props.get('name', 'Settlement')}</b><br>"
                f"Type: {props.get('type', '—')}<br>"
                f"Population (approx): {props.get('population_approx', '?'):,}<br>"
                f"Affected: {'Yes ⚠️' if affected else 'No ✅'}<br>"
                f"Risk level: <b>{risk}</b><br>"
                f"Est. depth: {props.get('flood_depth_m', 0):.1f} m<br>"
                f"<small style='color:#888'>⚠️ Demo data</small>",
                max_width=210,
            ),
            tooltip=(f"{props.get('name')} — {risk}" if affected
                     else props.get("name")),
        ).add_to(group)
    group.add_to(m)


def _add_roads(m, geojson: dict):
    group = folium.FeatureGroup(name="🛣️  Roads", show=False)
    for feature in geojson.get("features", []):
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        affected = props.get("affected", False)
        risk = props.get("risk_level", "None")
        color = RISK_COLORS.get(risk, "#94a3b8") if affected else "#475569"

        folium.PolyLine(
            locations=[[c[1], c[0]] for c in coords],
            color=color,
            weight=5 if affected else 2,
            opacity=0.95 if affected else 0.55,
            tooltip=f"{props.get('name')} — {'⚠️ AFFECTED' if affected else 'Safe'}",
        ).add_to(group)
    group.add_to(m)


def _add_legend(m):
    legend_html = """
    <div style="
        position: fixed; bottom: 36px; left: 12px; z-index: 1000;
        background: rgba(15,23,42,0.93); border: 1px solid #334155;
        border-radius: 10px; padding: 14px 18px; font-family: Inter, sans-serif;
        font-size: 12px; color: #e2e8f0; min-width: 175px;
        backdrop-filter: blur(10px); box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    ">
        <b style="font-size:13px; color:#38bdf8; letter-spacing:1px;">LEGEND</b><br><br>
        <span style="display:inline-block; background:#1d4ed8; border-radius:3px;
                     width:18px; height:10px; vertical-align:middle;"></span>
        &nbsp;Flood Extent<br><br>
        <span style="color:#ef4444; font-size:14px;">■</span> Critical Risk (&gt;5 m)<br>
        <span style="color:#f97316; font-size:14px;">■</span> High Risk (2–5 m)<br>
        <span style="color:#eab308; font-size:14px;">■</span> Moderate Risk (0.5–2 m)<br>
        <span style="color:#22c55e; font-size:14px;">■</span> Low Risk (&lt;0.5 m)<br><br>
        <span style="color:#38bdf8;">—</span> Mahanadi River<br>
        <span style="color:#60a5fa; font-size:14px;">●</span> Dam Location<br>
        <span style="color:#fb923c; font-size:14px;">●</span> Affected Settlement<br><br>
        <span style="font-size:10px; color:#64748b;">⚠️ DEMO DATA ONLY</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
