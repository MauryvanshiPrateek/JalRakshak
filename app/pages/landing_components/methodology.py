"""
Technical Credibility & Methodology Component for JalRakshak Landing Page.
Matches Section 33 & Section 34 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_methodology() -> None:
    """
    Render Section 33 & 34: Engineering Architecture and Hydrodynamic Methodology.
    """
    render_html("<div id='methodology' style='padding-top: 50px;'></div>")

    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 36px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                07 · SCIENTIFIC FRAMEWORK
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                A Technical Approach to Flood Simulation
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                Rigorous numerical formulation combining parametric breach initiation models with 2D non-linear shallow water conservation equations over geospatial elevation rasters.
            </p>
        </div>
        """
    )

    # 4-Stage Architecture Diagram
    cols = st.columns(4)
    stages = [
        {
            "tag": "STAGE 01",
            "title": "INPUT DATA",
            "items": [
                "Digital Elevation Model (DEM)",
                "Reservoir storage & pool level",
                "Dam height & structural type",
                "Breach geometry (width/depth)",
                "Embankment formation duration"
            ],
            "accent": "#2D78A8"
        },
        {
            "tag": "STAGE 02",
            "title": "HYDRAULIC MODEL",
            "items": [
                "2D Shallow Water Equations (SWE)",
                "Conservation of mass (∂h/∂t)",
                "Conservation of momentum (x, y)",
                "Friction slope (Manning's n)",
                "Discharge hydrograph Q(t)"
            ],
            "accent": "#17324D"
        },
        {
            "tag": "STAGE 03",
            "title": "SPATIAL ANALYSIS",
            "items": [
                "Topographic valley confinement",
                "Floodplain boundary delineation",
                "Settlement vulnerability overlay",
                "Highway corridor cutoff points",
                "Critical facility exposure"
            ],
            "accent": "#256B8E"
        },
        {
            "tag": "STAGE 04",
            "title": "OUTPUTS",
            "items": [
                "Spatial water depth grid (m)",
                "Flow velocity vectors (m/s)",
                "Arrival isochrones (lead time)",
                "Inundation polygon (GeoJSON)",
                "Hazard categorization metrics"
            ],
            "accent": "#5FA8D3"
        },
    ]

    for col, s in zip(cols, stages):
        with col:
            items_html = "".join([f"<li style='margin-bottom: 6px;'>{it}</li>" for it in s["items"]])
            render_html(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-top: 4px solid {s['accent']}; border-radius: 8px; padding: 20px 16px; height: 100%; box-shadow: 0 2px 6px rgba(23, 50, 77, 0.03);">
                    <div style="font-size: 0.72rem; font-weight: 700; color: {s['accent']}; letter-spacing: 0.08em; margin-bottom: 4px;">
                        {s['tag']}
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #17324D; margin-bottom: 14px;">
                        {s['title']}
                    </div>
                    <ul style="font-size: 0.85rem; color: #68747D; line-height: 1.5; padding-left: 16px; margin: 0;">
                        {items_html}
                    </ul>
                </div>
                """
            )

    render_html("<div style='margin-top: 24px;'></div>")

    # Detailed expandable methodology
    with st.expander("📘 View Mathematical Methodology & Governing Equations"):
        st.markdown(
            """
            #### 1. Governing Hydrodynamic Equations
            The 2D depth-averaged shallow water equations govern the conservation of fluid mass and momentum across arbitrary topography:

            $$\\frac{\\partial h}{\\partial t} + \\frac{\\partial (hu)}{\\partial x} + \\frac{\\partial (hv)}{\\partial y} = 0$$

            $$\\frac{\\partial (hu)}{\\partial t} + \\frac{\\partial}{\\partial x}\\left(hu^2 + \\frac{1}{2}gh^2\\right) + \\frac{\\partial (huv)}{\\partial y} = -gh\\frac{\\partial z_b}{\\partial x} - gh S_{fx}$$

            $$\\frac{\\partial (hv)}{\\partial t} + \\frac{\\partial (huv)}{\\partial x} + \\frac{\\partial}{\\partial y}\\left(hv^2 + \\frac{1}{2}gh^2\\right) = -gh\\frac{\\partial z_b}{\\partial y} - gh S_{fy}$$

            Where:
            * $h$: Water depth $(m)$
            * $u, v$: Velocity components in the Cartesian $x$ and $y$ directions $(m/s)$
            * $g$: Gravitational acceleration $(9.81 m/s^2)$
            * $z_b$: Bed elevation from DEM $(m)$
            * $S_{fx}, S_{fy}$: Friction slopes determined by Manning's roughness equation:
              $$S_{fx} = \\frac{n^2 u \\sqrt{u^2 + v^2}}{h^{4/3}}, \\quad S_{fy} = \\frac{n^2 v \\sqrt{u^2 + v^2}}{h^{4/3}}$$

            #### 2. Dam Breach Initiation Formula
            Peak breach discharge ($Q_p$) is calculated using the Froehlich (1995) empirical formulation for earthen and composite structures:
            $$Q_p = 0.607 \\cdot V_w^{0.295} \\cdot h_w^{1.24}$$
            Where $V_w$ is the volume of impounded water above breach bottom $(m^3)$ and $h_w$ is hydraulic height of water above breach invert $(m)$.

            *Disclaimer: Simulation outputs reflect mathematical approximations based on user-specified boundary conditions and DEM spatial resolution.*
            """
        )
