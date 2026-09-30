"""
Introduction Section Component for JalRakshak Landing Page.
Matches Section 16 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_introduction() -> None:
    """
    Render Section 16: Understanding Dam-Break Flood Behaviour.
    Two columns: Left text; Right technical flow diagram with thin engineering lines.
    """
    render_html("<div id='introduction' style='padding-top: 50px;'></div>")
    
    col_text, col_diagram = st.columns([5, 5], gap="large")

    with col_text:
        render_html(
            """
            <div style="padding-right: 12px;">
                <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                    01 · PHYSICAL PHENOMENA
                </div>
                <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; line-height: 1.2; margin: 0 0 18px 0;">
                    Understanding Dam-Break Flood Behaviour
                </h2>
                <p style="font-size: 1.05rem; color: #68747D; line-height: 1.65; margin-bottom: 16px;">
                    A dam-break event can generate a rapidly propagating flood wave that travels through downstream terrain. The simulation model is designed to represent this propagation and provide spatial and temporal information that can support technical assessment, preparedness, and planning.
                </p>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.65; margin-bottom: 20px;">
                    Unlike conventional rainfall-runoff inundation, catastrophic structural failure releases massive impounded hydraulic head within minutes to hours. Downstream impact depends heavily on breach geometry, valley confinement, topographic friction, and local settlement exposure.
                </p>
                <div style="border-left: 3px solid #256B8E; padding-left: 14px; margin-top: 24px;">
                    <div style="font-size: 0.85rem; font-weight: 600; color: #17324D;">
                        ENGINEERING ASSESSMENT OBJECTIVE
                    </div>
                    <div style="font-size: 0.85rem; color: #68747D; margin-top: 4px;">
                        Quantify hydrodynamic flood arrival time, peak water surface elevation, flow velocities, and critical infrastructure hazard zones.
                    </div>
                </div>
            </div>
            """
        )

    with col_diagram:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #17324D; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 18px;">
                    SYSTEM PROPAGATION PIPELINE
                </div>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #F7F8F6; border: 1px solid #D7DDE1; border-left: 4px solid #2D78A8; border-radius: 4px; padding: 10px 14px;">
                        <div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #17324D;">RESERVOIR</div>
                            <div style="font-size: 0.78rem; color: #68747D;">Impounded storage volume, initial water level (WL), hydrostatic head</div>
                        </div>
                        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #2D78A8;">S_res</span>
                    </div>
                    <div style="text-align: center; color: #256B8E; font-size: 1.1rem; line-height: 1;">↓</div>
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #F7F8F6; border: 1px solid #D7DDE1; border-left: 4px solid #17324D; border-radius: 4px; padding: 10px 14px;">
                        <div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #17324D;">DAM STRUCTURE</div>
                            <div style="font-size: 0.78rem; color: #68747D;">Structural classification (earth-fill, concrete, composite), crest elevation</div>
                        </div>
                        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #17324D;">H_dam</span>
                    </div>
                    <div style="text-align: center; color: #256B8E; font-size: 1.1rem; line-height: 1;">↓</div>
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #F7F8F6; border: 1px solid #D7DDE1; border-left: 4px solid #C98A18; border-radius: 4px; padding: 10px 14px;">
                        <div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #17324D;">BREACH FORMATION</div>
                            <div style="font-size: 0.78rem; color: #68747D;">Trapezoidal notch growth, formation time (t_f), peak discharge (Q_p)</div>
                        </div>
                        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #C98A18;">Q_peak</span>
                    </div>
                    <div style="text-align: center; color: #256B8E; font-size: 1.1rem; line-height: 1;">↓</div>
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #F7F8F6; border: 1px solid #D7DDE1; border-left: 4px solid #5FA8D3; border-radius: 4px; padding: 10px 14px;">
                        <div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #17324D;">FLOOD WAVE</div>
                            <div style="font-size: 0.78rem; color: #68747D;">2D hydrodynamic propagation, shallow-water equations, attenuation</div>
                        </div>
                        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #5FA8D3;">v(x,y,t)</span>
                    </div>
                    <div style="text-align: center; color: #256B8E; font-size: 1.1rem; line-height: 1;">↓</div>
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #F7F8F6; border: 1px solid #D7DDE1; border-left: 4px solid #256B8E; border-radius: 4px; padding: 10px 14px;">
                        <div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #17324D;">DOWNSTREAM TERRAIN</div>
                            <div style="font-size: 0.78rem; color: #68747D;">Topographic confinement, settlement inundation, road network exposure</div>
                        </div>
                        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #256B8E;">Z_dem</span>
                    </div>
                </div>
            </div>
            """
        )
