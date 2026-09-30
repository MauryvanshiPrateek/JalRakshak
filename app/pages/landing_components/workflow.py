"""
Simulation Workflow Component for JalRakshak Landing Page.
Matches Section 26 & Section 27 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_workflow() -> None:
    """
    Render 5-stage sequential process timeline from scenario definition to visualization.
    """
    render_html("<div id='workflow' style='padding-top: 50px;'></div>")

    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 36px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                04 · METHODOLOGICAL PIPELINE
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                From Scenario Definition to Flood Assessment
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                A structured, reproducible computational workflow designed for engineering teams and disaster mitigation planners.
            </p>
        </div>
        """
    )

    steps = [
        {
            "num": "01",
            "phase": "DEFINE",
            "title": "Dam & Reservoir",
            "desc": "Select study area, dam geometry, crest elevation, normal pool level, and impounded volume.",
        },
        {
            "num": "02",
            "phase": "CONFIGURE",
            "title": "Breach Conditions",
            "desc": "Specify failure mode (overtopping/piping), notch width, breach depth, and formation time.",
        },
        {
            "num": "03",
            "phase": "SIMULATE",
            "title": "Hydrodynamic Model",
            "desc": "Run 2D shallow water conservation equations over high-resolution elevation grids.",
        },
        {
            "num": "04",
            "phase": "ANALYSE",
            "title": "Hydraulic Parameters",
            "desc": "Compute spatial depth distribution, maximum velocity, and flood wave arrival isochrones.",
        },
        {
            "num": "05",
            "phase": "VISUALISE",
            "title": "Decision Support",
            "desc": "Inspect interactive geospatial layers, impact tables, risk warnings, and export GIS reports.",
        },
    ]

    cols = st.columns(5)
    for col, s in zip(cols, steps):
        with col:
            render_html(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-top: 4px solid #256B8E; border-radius: 8px; padding: 18px 14px; height: 100%; box-shadow: 0 2px 6px rgba(23, 50, 77, 0.03); display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
                            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 1.25rem; font-weight: 700; color: #17324D;">
                                {s["num"]}
                            </span>
                            <span style="font-size: 0.72rem; font-weight: 700; color: #256B8E; letter-spacing: 0.08em;">
                                {s["phase"]}
                            </span>
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: #17324D; margin-bottom: 6px;">
                            {s["title"]}
                        </div>
                        <div style="font-size: 0.82rem; color: #68747D; line-height: 1.5;">
                            {s["desc"]}
                        </div>
                    </div>
                </div>
                """
            )
