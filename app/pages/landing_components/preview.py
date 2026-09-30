from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html
from app.components.map_view import render_map
from simulation.mock_runner import create_instant_demo_result


@st.cache_resource
def _get_preview_demo_result():
    return create_instant_demo_result()


def render_preview() -> None:
    """
    Render realistic application preview of the JalRakshak simulation environment with conversion CTA.
    """
    render_html("<div id='simulation-preview' style='padding-top: 50px;'></div>")

    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 36px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                05 · APPLICATION ENVIRONMENT
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                Explore the Simulation Environment
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                Inspect the integrated command dashboard featuring scenario parameter controls, interactive Folium GIS mapping, and time-step hydrodynamic playback.
            </p>
        </div>
        """
    )

    col_preview, col_side = st.columns([7, 3], gap="medium")

    with col_preview:
        render_html(
            """
            <div style="background: #0A1628; border: 1px solid #1E3A5F; border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: -10px; z-index: 2; position: relative;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #B8423A; border-radius: 50%;"></span>
                    <span style="display: inline-block; width: 10px; height: 10px; background: #C98A18; border-radius: 50%;"></span>
                    <span style="display: inline-block; width: 10px; height: 10px; background: #256B8E; border-radius: 50%;"></span>
                    <span style="margin-left: 12px; font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: #94A3B8;">
                        JalRakshak · Simulation Workspace v1.0 [Hirakud Study Area · Severe Breach]
                    </span>
                </div>
                <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #38BDF8;">
                    STATUS: ACTIVE DEMO READY
                </div>
            </div>
            """
        )
        demo_res = _get_preview_demo_result()
        render_map(demo_res, height=460, key="preview_gis_map_component")


    with col_side:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 22px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 6px rgba(23, 50, 77, 0.03);">
                <div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                        INTERACTIVE WORKSPACE
                    </div>
                    <h4 style="font-size: 1.25rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                        Hands-On Hydraulic Simulation
                    </h4>
                    <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 16px;">
                        The full JalRakshak workspace gives you direct control over breach mechanics, parametric inputs, Folium spatial map overlays, and exportable hazard summaries.
                    </p>
                    <ul style="font-size: 0.85rem; color: #17324D; line-height: 1.8; padding-left: 18px; margin: 0 0 20px 0;">
                        <li>Multi-dam study area selection</li>
                        <li>Configurable breach geometry</li>
                        <li>Interactive timeline playback</li>
                        <li>Downstream settlement risk classification</li>
                    </ul>
                </div>
            </div>
            """
        )
        if st.button("Enter Simulation", key="btn_enter_sim_side", type="primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
