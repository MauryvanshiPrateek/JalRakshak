from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html
from app.components.map_view import render_map
from simulation.mock_runner import create_instant_demo_result


@st.cache_resource
def _get_hero_demo_result():
    return create_instant_demo_result()


def render_hero() -> None:
    """
    Render Hero section with text, dual CTAs, and interactive Folium GIS simulation visual.
    """
    col_left, col_right = st.columns([4.5, 5.5], gap="large")

    with col_left:
        render_html(
            """
            <div style="padding-top: 18px;">
                <div style="display: inline-block; font-size: 0.8rem; font-weight: 600; color: #256B8E; background: rgba(37, 107, 142, 0.08); border: 1px solid #D7DDE1; border-radius: 4px; padding: 4px 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;">
                    JalRakshak · Hydraulic Engineering &amp; GIS
                </div>
                <h1 style="font-size: 3.4rem; font-weight: 600; line-height: 1.12; color: #17324D; margin: 0 0 16px 0; letter-spacing: -0.01em;">
                    DAM-BREAK<br>FLOOD SIMULATION
                </h1>
                <p style="font-size: 1.15rem; color: #68747D; line-height: 1.6; margin-bottom: 28px; max-width: 520px;">
                    Hydraulic modelling and geospatial analysis for understanding downstream flood propagation and inundation.
                </p>
                <div style="display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #17324D; font-family: 'IBM Plex Mono', monospace;">
                        <span style="display: inline-block; width: 8px; height: 8px; background: #2D78A8; border-radius: 50%;"></span>
                        2D Shallow-Water Solver
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #17324D; font-family: 'IBM Plex Mono', monospace;">
                        <span style="display: inline-block; width: 8px; height: 8px; background: #256B8E; border-radius: 50%;"></span>
                        High-Resolution Topography
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #17324D; font-family: 'IBM Plex Mono', monospace;">
                        <span style="display: inline-block; width: 8px; height: 8px; background: #5FA8D3; border-radius: 50%;"></span>
                        Dynamic Inundation
                    </div>
                </div>
            </div>
            """
        )

        btn_c1, btn_c2 = st.columns([1.2, 1.2])
        with btn_c1:
            if st.button("Explore Simulation", key="hero_cta_explore", type="primary", use_container_width=True):
                st.session_state["show_explore_modal"] = True
                st.rerun()
        with btn_c2:
            render_html(
                """
                <a href="#introduction" style="display: block; text-align: center; padding: 8px 16px; border: 1px solid #17324D; border-radius: 8px; color: #17324D; font-weight: 600; font-size: 0.95rem; text-decoration: none; background: #FFFFFF;">
                    Learn About the Model
                </a>
                """
            )

    with col_right:
        _render_gis_map_panel()


def _render_gis_map_panel() -> None:
    """
    Renders the live interactive Folium satellite map with flood extents,
    risk zones, LayerControl, and legend matching user specifications.
    """
    render_html(
        """
        <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; font-family: 'IBM Plex Mono', monospace; font-size: 0.76rem; color: #17324D; margin-bottom: -10px; z-index: 2; position: relative; box-shadow: 0 1px 3px rgba(23, 50, 77, 0.04);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 8px; height: 8px; background: #256B8E; border-radius: 50%;"></span>
                <b>STUDY AREA:</b> Hirakud Reservoir &amp; Mahanadi Basin · Odisha
            </div>
            <div style="color: #68747D;">
                LAT: 21.5250° N · LON: 83.8730° E · WGS 84
            </div>
        </div>
        """
    )
    demo_result = _get_hero_demo_result()
    render_map(demo_result, height=440, key="hero_interactive_gis_map")

