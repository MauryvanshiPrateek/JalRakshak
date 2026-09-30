"""
Scroll-Aligned Simulation Story Component for JalRakshak Landing Page.
Matches Sections 17, 18, 19, 20, 21, 22, and 23 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_story() -> None:
    """
    Render the 5-step simulation story (Reservoir -> Breach -> Wave -> Inundation -> Impact).
    Interactive step selector synchronised with a technical vector map.
    """
    render_html("<div id='story' style='padding-top: 50px;'></div>")
    
    render_html(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 32px auto;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #256B8E; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                02 · SIMULATION PROCESS WALKTHROUGH
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 600; color: #17324D; margin: 0 0 12px 0;">
                The Dam-Break Propagation Cycle
            </h2>
            <p style="font-size: 1.05rem; color: #68747D; line-height: 1.6;">
                Examine how the computational model resolves the transition from impounded reservoir head to catastrophic breach formation and downstream valley inundation.
            </p>
        </div>
        """
    )

    if "story_step" not in st.session_state:
        st.session_state["story_step"] = 1

    # Step selector buttons
    cols = st.columns(5)
    steps_meta = [
        ("01", "The Reservoir"),
        ("02", "Breach Formation"),
        ("03", "Flood Wave"),
        ("04", "Inundation"),
        ("05", "Arrival & Impact"),
    ]
    for idx, (num, title) in enumerate(steps_meta, start=1):
        with cols[idx - 1]:
            is_active = (st.session_state["story_step"] == idx)
            btn_label = f"**{num}** · {title}" if is_active else f"{num} · {title}"
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_label, key=f"btn_step_{idx}", use_container_width=True, type=btn_type):
                st.session_state["story_step"] = idx
                st.rerun()

    active_step = st.session_state["story_step"]

    col_left, col_right = st.columns([4.5, 5.5], gap="large")

    with col_left:
        _render_step_narrative(active_step)

    with col_right:
        _render_step_technical_visual(active_step)


def _render_step_narrative(step: int) -> None:
    """Renders narrative text and technical metrics for the active step."""
    if step == 1:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #256B8E; letter-spacing: 0.08em; margin-bottom: 6px;">
                    STEP 01 — THE RESERVOIR
                </div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #17324D; margin: 0 0 14px 0;">
                    Reservoir Geometry & Hydrostatic Head
                </h3>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.6; margin-bottom: 18px;">
                    "The simulation begins with the representation of the reservoir, dam geometry, terrain and initial hydraulic conditions."
                </p>
                <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 20px;">
                    Digital Elevation Models (DEM) define the storage-elevation curve and valley cross-sections. Water level is configured relative to normal pool level and maximum reservoir capacity.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F8F6; padding: 14px; border-radius: 6px; border: 1px solid #D7DDE1; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">
                    <div><b style="color: #17324D;">Storage:</b> 8,141 MCM</div>
                    <div><b style="color: #17324D;">Dam Height:</b> 60.96 m</div>
                    <div><b style="color: #17324D;">Pool Level:</b> EL 192.0 m</div>
                    <div><b style="color: #17324D;">Tailwater:</b> EL 132.5 m</div>
                </div>
            </div>
            """
        )
    elif step == 2:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #C98A18; letter-spacing: 0.08em; margin-bottom: 6px;">
                    STEP 02 — BREACH FORMATION
                </div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #17324D; margin: 0 0 14px 0;">
                    Breach Development & Outflow Hydrograph
                </h3>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.6; margin-bottom: 18px;">
                    "A breach scenario defines how the dam opening develops and how water is released from the reservoir."
                </p>
                <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 20px;">
                    Parametric models (Froehlich / MacDonald-Langridge-Monopolis) simulate progressive trapezoidal erosion based on structural material, impounded depth, and formation duration.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F8F6; padding: 14px; border-radius: 6px; border: 1px solid #D7DDE1; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">
                    <div><b style="color: #17324D;">Avg Width (B_avg):</b> 45.0 m</div>
                    <div><b style="color: #17324D;">Side Slope (Z):</b> 1.0 H:V</div>
                    <div><b style="color: #17324D;">Formation Time:</b> 1.2 hrs</div>
                    <div><b style="color: #17324D;">Q_peak:</b> 24,800 m³/s</div>
                </div>
            </div>
            """
        )
    elif step == 3:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #256B8E; letter-spacing: 0.08em; margin-bottom: 6px;">
                    STEP 03 — FLOOD-WAVE PROPAGATION
                </div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #17324D; margin: 0 0 14px 0;">
                    Hydrodynamic Wave Routing & Momentum
                </h3>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.6; margin-bottom: 18px;">
                    "The released water propagates through the downstream terrain, producing a changing hydraulic state over time."
                </p>
                <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 20px;">
                    2D non-linear shallow-water conservation equations compute shock wave propagation, channel friction dissipation, and momentum transfer through river bends.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F8F6; padding: 14px; border-radius: 6px; border: 1px solid #D7DDE1; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">
                    <div><b style="color: #17324D;">Peak Wave Velocity:</b> 6.4 m/s</div>
                    <div><b style="color: #17324D;">Governing Eq:</b> 2D SWE</div>
                    <div><b style="color: #17324D;">Manning 'n':</b> 0.035 - 0.065</div>
                    <div><b style="color: #17324D;">Attenuation:</b> 38% / 15 km</div>
                </div>
            </div>
            """
        )
    elif step == 4:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #5FA8D3; letter-spacing: 0.08em; margin-bottom: 6px;">
                    STEP 04 — INUNDATION EXTENT & DEPTH
                </div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #17324D; margin: 0 0 14px 0;">
                    Spatial Inundation & Depth Zoning
                </h3>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.6; margin-bottom: 18px;">
                    "The model can represent the spatial extent of flooding and identify areas affected by different levels of inundation."
                </p>
                <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 20px;">
                    Zoning uses a standardized hydraulic depth scale: 0–0.5 m (wading), 0.5–1.5 m (structural hazard), 1.5–3 m (severe submergence), and >3 m (catastrophic inundation).
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F8F6; padding: 14px; border-radius: 6px; border: 1px solid #D7DDE1; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">
                    <div><b style="color: #17324D;">Total Inundated:</b> 142.8 km²</div>
                    <div><b style="color: #17324D;">Max Depth:</b> 11.4 m</div>
                    <div><b style="color: #17324D;">Settlements:</b> 18 Affected</div>
                    <div><b style="color: #17324D;">Road Inundated:</b> 34.6 km</div>
                </div>
            </div>
            """
        )
    else:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04);">
                <div style="font-size: 0.75rem; font-weight: 700; color: #B8423A; letter-spacing: 0.08em; margin-bottom: 6px;">
                    STEP 05 — ARRIVAL TIME & IMPACT
                </div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: #17324D; margin: 0 0 14px 0;">
                    Lead Time & Emergency Decision Support
                </h3>
                <p style="font-size: 0.95rem; color: #68747D; line-height: 1.6; margin-bottom: 18px;">
                    "Simulation results can be analysed through parameters such as flood depth, velocity, arrival time and inundation extent."
                </p>
                <p style="font-size: 0.9rem; color: #68747D; line-height: 1.6; margin-bottom: 20px;">
                    Isochrones delineate evacuation windows for civil defense, transport corridor cutoffs, and vulnerable facility protection.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F8F6; padding: 14px; border-radius: 6px; border: 1px solid #D7DDE1; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">
                    <div><b style="color: #17324D;">Burla Town:</b> 18 min lead</div>
                    <div><b style="color: #17324D;">Sambalpur:</b> 42 min lead</div>
                    <div><b style="color: #17324D;">NH-53 Cutoff:</b> 35 min</div>
                    <div><b style="color: #17324D;">Risk Level:</b> CRITICAL</div>
                </div>
            </div>
            """
        )


def _render_step_technical_visual(step: int) -> None:
    """Renders visual SVG representation tailored to the selected simulation step."""
    time_labels = ["0.0 h (Steady)", "0.5 h (Breach)", "1.5 h (Propagation)", "3.0 h (Peak)", "6.0 h (Recession)"]
    time_label = time_labels[step - 1]
    overlay_svg = _get_step_svg_overlay(step)
    
    render_html(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(23, 50, 77, 0.04); height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #D7DDE1; padding-bottom: 8px; margin-bottom: 12px;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #17324D; font-family: 'IBM Plex Mono', monospace;">
                    HYDRAULIC STATE DIAGRAM · PHASE 0{step}
                </span>
                <span style="font-size: 0.75rem; color: #256B8E; font-family: 'IBM Plex Mono', monospace;">
                    t = {time_label}
                </span>
            </div>
            <div style="width: 100%; height: 320px; background: #FAF9F5; border: 1px solid #E5E8EB; border-radius: 4px; overflow: hidden; position: relative;">
                <svg width="100%" height="100%" viewBox="0 0 500 320" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <pattern id="stepGrid" width="25" height="25" patternUnits="userSpaceOnUse">
                            <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#ECEFEF" stroke-width="0.8"/>
                        </pattern>
                    </defs>
                    <rect width="500" height="320" fill="url(#stepGrid)"/>
                    <g stroke="#D1D8DE" stroke-width="1" fill="none">
                        <path d="M-10 40 Q 120 60, 180 100 T 320 80 T 510 50"/>
                        <path d="M-10 110 Q 110 130, 180 150 T 330 140 T 510 120"/>
                        <path d="M-10 180 Q 100 200, 180 220 T 340 220 T 510 190"/>
                        <path d="M-10 260 Q 120 280, 200 290 T 350 280 T 510 260"/>
                    </g>
                    <path d="M 0 50 C 60 70, 110 100, 150 120 C 170 135, 175 150, 175 165 C 175 185, 150 205, 110 220 C 70 235, 30 245, 0 260 Z" fill="#2D78A8" opacity="{1.0 if step <= 2 else 0.85}"/>
                    <text x="25" y="160" fill="#FFFFFF" font-family="'IBM Plex Sans', sans-serif" font-size="11" font-weight="600">RESERVOIR</text>
                    <polygon points="170,115 182,120 182,215 170,220" fill="#17324D"/>
                    <path d="M 182 165 C 230 165, 270 190, 310 190 C 360 190, 400 150, 440 150 T 500 160" fill="none" stroke="#2D78A8" stroke-width="12" stroke-linecap="round"/>
                    {overlay_svg}
                </svg>
            </div>
            <div style="margin-top: 10px; display: flex; justify-content: space-between; font-size: 0.75rem; color: #68747D; font-family: 'IBM Plex Mono', monospace;">
                <span>NORTH: ▲ 0°</span>
                <span>DATUM: WGS 84 / UTM 45N</span>
                <span>GRID RESOLUTION: 10 m</span>
            </div>
        </div>
        """
    )


def _get_step_svg_overlay(step: int) -> str:
    """Returns SVG snippet specific to each simulation phase."""
    if step == 1:
        return """
        <line x1="80" y1="120" x2="80" y2="210" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="3,3"/>
        <text x="90" y="150" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="9">HEAD: 60.96 m</text>
        <circle cx="176" cy="165" r="5" fill="#256B8E" stroke="#FFFFFF" stroke-width="1.5"/>
        <text x="195" y="130" fill="#17324D" font-family="'IBM Plex Sans', sans-serif" font-size="10" font-weight="700">DAM CREST EL: 195.0 m</text>
        """
    elif step == 2:
        return """
        <rect x="170" y="153" width="12" height="24" fill="#C98A18"/>
        <line x1="170" y1="153" x2="182" y2="177" stroke="#FFFFFF" stroke-width="1.2"/>
        <line x1="170" y1="177" x2="182" y2="153" stroke="#FFFFFF" stroke-width="1.2"/>
        <text x="192" y="150" fill="#C98A18" font-family="'IBM Plex Mono', monospace" font-size="9.5" font-weight="700">BREACH NOTCH [45 m]</text>
        <path d="M 182 165 L 240 165" stroke="#C98A18" stroke-width="3" stroke-dasharray="4,2"/>
        <polygon points="245,165 237,160 237,170" fill="#C98A18"/>
        <text x="200" y="185" fill="#17324D" font-family="'IBM Plex Mono', monospace" font-size="8.5">Q = 24,800 m³/s</text>
        """
    elif step == 3:
        return """
        <path d="M 182 165 C 220 145, 260 150, 310 150 C 370 150, 410 130, 460 140 T 500 150 L 500 190 C 450 190, 410 220, 350 220 C 290 220, 240 185, 182 175 Z" fill="#5FA8D3" opacity="0.6"/>
        <path d="M 185 165 C 230 165, 270 190, 310 190 C 360 190, 400 150, 440 150" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-dasharray="8,4"/>
        <circle cx="310" cy="190" r="4" fill="#256B8E"/>
        <text x="320" y="194" fill="#17324D" font-family="'IBM Plex Mono', monospace" font-size="9">V_front = 6.4 m/s</text>
        """
    elif step == 4:
        return """
        <path d="M 182 155 C 230 120, 280 130, 340 120 C 420 110, 460 100, 500 110 L 500 230 C 450 250, 400 240, 330 250 C 260 260, 220 200, 182 180 Z" fill="#5FA8D3" opacity="0.7"/>
        <circle cx="280" cy="140" r="4" fill="#17324D"/>
        <text x="290" y="144" fill="#17324D" font-family="'IBM Plex Sans', sans-serif" font-size="9" font-weight="600">Burla (2.8m)</text>
        <circle cx="410" cy="130" r="4" fill="#B8423A"/>
        <text x="420" y="134" fill="#B8423A" font-family="'IBM Plex Sans', sans-serif" font-size="9" font-weight="700">Sambalpur (4.2m)</text>
        <g transform="translate(340, 250)">
            <rect width="145" height="52" fill="#FFFFFF" stroke="#D7DDE1" rx="3" opacity="0.95"/>
            <text x="8" y="12" fill="#17324D" font-family="'IBM Plex Sans', sans-serif" font-size="8" font-weight="700">WATER DEPTH (m)</text>
            <rect x="8" y="18" width="10" height="6" fill="#D2E8F7"/><text x="22" y="24" fill="#1E252B" font-size="7.5">0–0.5m</text>
            <rect x="75" y="18" width="10" height="6" fill="#8AC2E4"/><text x="90" y="24" fill="#1E252B" font-size="7.5">0.5–1.5m</text>
            <rect x="8" y="32" width="10" height="6" fill="#4B95C3"/><text x="22" y="38" fill="#1E252B" font-size="7.5">1.5–3m</text>
            <rect x="75" y="32" width="10" height="6" fill="#17324D"/><text x="90" y="38" fill="#1E252B" font-size="7.5">>3m</text>
        </g>
        """
    else:
        return """
        <path d="M 230 140 C 240 180, 240 210, 230 230" fill="none" stroke="#256B8E" stroke-width="1.8" stroke-dasharray="4,2"/>
        <text x="235" y="135" fill="#256B8E" font-family="'IBM Plex Mono', monospace" font-size="8">15 min</text>
        <path d="M 330 120 C 350 170, 340 220, 320 250" fill="none" stroke="#C98A18" stroke-width="1.8" stroke-dasharray="4,2"/>
        <text x="335" y="115" fill="#C98A18" font-family="'IBM Plex Mono', monospace" font-size="8">30 min</text>
        <path d="M 450 110 C 470 160, 460 210, 440 240" fill="none" stroke="#B8423A" stroke-width="2" stroke-dasharray="4,2"/>
        <text x="455" y="105" fill="#B8423A" font-family="'IBM Plex Mono', monospace" font-size="8" font-weight="700">60 min</text>
        <rect x="380" y="125" width="80" height="30" fill="#FFFFFF" stroke="#B8423A" rx="3" opacity="0.95"/>
        <text x="386" y="138" fill="#B8423A" font-family="'IBM Plex Sans', sans-serif" font-size="8.5" font-weight="700">URBAN IMPACT</text>
        <text x="386" y="149" fill="#17324D" font-family="'IBM Plex Mono', monospace" font-size="7.5">Lead Time: 42 min</text>
        """
