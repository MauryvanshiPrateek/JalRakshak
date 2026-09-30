"""
Capabilities Grid Component for JalRakshak Landing Page.
Matches Section 24 & Section 25 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_capabilities() -> None:
    """
    Render 6 restrained engineering capability cards in a 3x2 grid.
    """
    render_html("<div id='capabilities' style='padding-top: 50px;'></div>")

    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 36px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                03 · CORE FUNCTIONALITY
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                Simulation & Analysis Capabilities
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                Engineered for hydraulic engineers, GIS specialists, and water-resource authorities requiring scientifically rigorous hydrodynamic modelling.
            </p>
        </div>
        """
    )

    capabilities = [
        {
            "num": "01",
            "title": "Hydraulic Simulation",
            "desc": "Model dam-break flood propagation under defined scenario conditions and time-varying breach outflow hydrographs.",
            "svg": """<path d="M2 12h20M2 6h20M2 18h20" stroke="#256B8E" stroke-width="2" stroke-linecap="round"/>"""
        },
        {
            "num": "02",
            "title": "Terrain Analysis",
            "desc": "Use high-resolution digital elevation information (DEM) to understand valley confinement and downstream flow paths.",
            "svg": """<path d="M3 20l7-10 5 6 6-9" stroke="#256B8E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 20h18" stroke="#256B8E" stroke-width="2"/>"""
        },
        {
            "num": "03",
            "title": "Inundation Mapping",
            "desc": "Visualize spatial extent and boundaries of flood submergence overlaid with administrative boundaries and settlements.",
            "svg": """<polygon points="1,6 8,2 16,6 23,2 23,18 16,22 8,18 1,22" fill="none" stroke="#256B8E" stroke-width="2"/><line x1="8" y1="2" x2="8" y2="18" stroke="#256B8E" stroke-width="2"/><line x1="16" y1="6" x2="16" y2="22" stroke="#256B8E" stroke-width="2"/>"""
        },
        {
            "num": "04",
            "title": "Flood Depth",
            "desc": "Analyse spatial and temporal variation in water depth to identify high-submergence zones and structural risks.",
            "svg": """<line x1="12" y1="3" x2="12" y2="21" stroke="#256B8E" stroke-width="2"/><polyline points="8,7 12,3 16,7" fill="none" stroke="#256B8E" stroke-width="2"/><polyline points="8,17 12,21 16,17" fill="none" stroke="#256B8E" stroke-width="2"/>"""
        },
        {
            "num": "05",
            "title": "Flow Velocity",
            "desc": "Represent hydraulic velocity vectors across the affected region to assess destructive hydrodynamic shear forces.",
            "svg": """<circle cx="12" cy="12" r="9" fill="none" stroke="#256B8E" stroke-width="2"/><polyline points="12,7 12,12 16,14" fill="none" stroke="#256B8E" stroke-width="2"/>"""
        },
        {
            "num": "06",
            "title": "Arrival Time",
            "desc": "Analyse the time required for the flood wave to reach downstream settlements and transportation infrastructure.",
            "svg": """<circle cx="12" cy="12" r="10" fill="none" stroke="#256B8E" stroke-width="2"/><polyline points="12,6 12,12 14,14" fill="none" stroke="#256B8E" stroke-width="2"/>"""
        },
    ]

    col1, col2, col3 = st.columns(3)
    for idx, cap in enumerate(capabilities):
        target_col = [col1, col2, col3][idx % 3]
        with target_col:
            render_html(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 22px; margin-bottom: 20px; box-shadow: 0 2px 6px rgba(23, 50, 77, 0.03); min-height: 205px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                {cap["svg"]}
                            </svg>
                            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; font-weight: 600; color: #256B8E;">
                                {cap["num"]}
                            </span>
                        </div>
                        <h4 style="font-size: 1.15rem; font-weight: 600; color: #17324D; margin: 0 0 8px 0;">
                            {cap["title"]}
                        </h4>
                        <p style="font-size: 0.9rem; color: #68747D; line-height: 1.55; margin: 0;">
                            {cap["desc"]}
                        </p>
                    </div>
                </div>
                """
            )
