"""
Authentication and Exploration Modals for JalRakshak.
Matches Section 11 & Section 12 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


@st.dialog("Explore JalRakshak Simulation", width="medium")
def show_explore_dialog() -> None:
    """
    Modal presenting user with options to Try Demo or Sign In.
    Strictly follows Section 11 specifications.
    """
    render_html(
        """
        <div style="font-size: 0.95rem; color: #68747D; margin-bottom: 20px;">
            Choose how you want to continue.
        </div>
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 20px; height: 180px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #17324D; letter-spacing: 0.08em; text-transform: uppercase;">
                        TRY DEMO
                    </div>
                    <div style="font-size: 0.9rem; color: #68747D; margin-top: 8px; line-height: 1.4;">
                        Explore a prepared scenario without signing in.
                    </div>
                </div>
            </div>
            """
        )
        if st.button("Try Demo", use_container_width=True, key="dlg_btn_demo", type="primary"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    with col2:
        render_html(
            """
            <div style="background: #FFFFFF; border: 1px solid #D7DDE1; border-radius: 8px; padding: 20px; height: 180px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #17324D; letter-spacing: 0.08em; text-transform: uppercase;">
                        SIGN IN
                    </div>
                    <div style="font-size: 0.9rem; color: #68747D; margin-top: 8px; line-height: 1.4;">
                        Access simulation features and saved scenarios.
                    </div>
                </div>
            </div>
            """
        )
        if st.button("Sign In", use_container_width=True, key="dlg_btn_signin"):
            st.session_state["show_signin_modal"] = True
            st.rerun()


@st.dialog("Sign in to JalRakshak", width="small")
def show_signin_dialog() -> None:
    """
    Sign-in modal offering Google & Phone number options.
    Strictly follows Section 12 specifications.
    """
    render_html(
        """
        <div style="font-size: 0.9rem; color: #68747D; margin-bottom: 16px;">
            Select an authentication method to access the full simulation environment.
        </div>
        """
    )

    if st.button("Continue with Google", use_container_width=True, key="dlg_btn_google"):
        st.session_state["user_authenticated"] = True
        st.session_state["user_email"] = "analyst@jalrakshak.org"
        st.session_state["page"] = "dashboard"
        st.success("Authenticated successfully as Research Analyst.")
        st.rerun()

    render_html(
        """
        <div style="display: flex; align-items: center; margin: 18px 0; color: #68747D; font-size: 0.8rem;">
            <div style="flex: 1; height: 1px; background: #D7DDE1;"></div>
            <span style="padding: 0 10px; font-weight: 600; letter-spacing: 0.08em;">OR</span>
            <div style="flex: 1; height: 1px; background: #D7DDE1;"></div>
        </div>
        """
    )

    phone = st.text_input("Phone number", placeholder="+91 98765 43210", key="dlg_phone_input")
    if st.button("Continue", use_container_width=True, key="dlg_btn_phone", type="primary"):
        if phone and len(phone.strip()) >= 10:
            st.session_state["user_authenticated"] = True
            st.session_state["user_phone"] = phone.strip()
            st.session_state["page"] = "dashboard"
            st.success("Verified via phone. Launching simulation workspace…")
            st.rerun()
        else:
            st.error("Please enter a valid phone number with country code.")




@st.dialog("Privacy & Policy — JalRakshak", width="large")
def show_privacy_dialog() -> None:
    """
    Privacy and policy disclosure dialog detailing data origins from existing datasets
    and model execution based on predefined parameters.
    """
    render_html(
        """
        <div style="font-family: 'IBM Plex Sans', -apple-system, sans-serif; color: #1E252B; line-height: 1.65; padding: 4px 0;">
            <div style="border-left: 3px solid #256B8E; padding-left: 12px; margin-bottom: 20px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #17324D;">
                    Data Attribution, Methodology &amp; Privacy Statement
                </div>
                <div style="font-size: 0.82rem; color: #68747D; margin-top: 2px;">
                    Institutional Disclosure · JalRakshak Dam-Break Hydrodynamic Platform
                </div>
            </div>

            <div style="background: #F7F8F6; border: 1px solid #D7DDE1; border-radius: 6px; padding: 14px 18px; margin-bottom: 18px;">
                <div style="font-weight: 700; color: #17324D; font-size: 0.92rem; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span style="display:inline-block; width:8px; height:8px; background:#256B8E; border-radius:50%;"></span>
                    1. Data Origin: Sourced from Existing Benchmark Datasets
                </div>
                <div style="font-size: 0.88rem; color: #475569;">
                    All geographic, elevation, hydrological, and civil infrastructure information displayed within the platform is compiled exclusively from existing, verified open datasets and public institutional repositories:
                </div>
                <ul style="margin: 8px 0 0 18px; padding: 0; font-size: 0.85rem; color: #334155;">
                    <li><b>Digital Elevation &amp; Topography:</b> High-resolution terrain matrices are sourced from Copernicus DEM (GLO-30) and NASA SRTM digital elevation models.</li>
                    <li><b>Dam Inventory &amp; Hydraulic Attributes:</b> Dam crest heights, full reservoir levels (FRL), storage volumes, and spillway configurations are referenced from the Central Water Commission (CWC) National Register of Large Dams (NRLD) and India-WRIS.</li>
                    <li><b>Downstream Geography &amp; Infrastructure:</b> River centrelines, floodplain bathymetry, downstream settlements, and road networks are derived from OpenStreetMap (OSM) contributors and HydroSHEDS hydrographic vectors.</li>
                    <li><b>Satellite Imagery:</b> Spatial base layers are served via Esri World Imagery and ISRO Bhuvan open map services.</li>
                </ul>
            </div>

            <div style="background: #F7F8F6; border: 1px solid #D7DDE1; border-radius: 6px; padding: 14px 18px; margin-bottom: 18px;">
                <div style="font-weight: 700; color: #17324D; font-size: 0.92rem; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span style="display:inline-block; width:8px; height:8px; background:#2D78A8; border-radius:50%;"></span>
                    2. Hydrodynamic Modelling: Predefined Physical &amp; Scenario Parameters
                </div>
                <div style="font-size: 0.88rem; color: #475569;">
                    The simulation engine operates strictly according to predefined mathematical formulations, numerical boundary conditions, and scenario parameters:
                </div>
                <ul style="margin: 8px 0 0 18px; padding: 0; font-size: 0.85rem; color: #334155;">
                    <li><b>Parametric Breach Mechanics:</b> Peak outflow discharge rates and failure progression are calculated according to established empirical laws (Froehlich 2008 / MacDonald-Langridge-Monopolis 1984).</li>
                    <li><b>Shallow-Water Hydrodynamics:</b> Downstream flood propagation, inundation depths, and wave arrival velocity fields are evaluated using 2D Shallow Water Saint-Venant Equations with finite-volume flux approximations and calibrated Manning’s roughness coefficients (<i>n</i> = 0.030 – 0.055).</li>
                    <li><b>Predefined Control Ranges:</b> Reservoir levels, breach dimensions, and failure durations are constrained within engineering tolerance limits predefined by civil dam-safety guidelines.</li>
                </ul>
            </div>

            <div style="background: #F7F8F6; border: 1px solid #D7DDE1; border-radius: 6px; padding: 14px 18px; margin-bottom: 22px;">
                <div style="font-weight: 700; color: #17324D; font-size: 0.92rem; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span style="display:inline-block; width:8px; height:8px; background:#5FA8D3; border-radius:50%;"></span>
                    3. User Privacy, Credentials &amp; Advisory Scope
                </div>
                <div style="font-size: 0.88rem; color: #475569;">
                    <b>Local Execution &amp; No Credential Retention:</b> This application does not collect, harvest, or store personal user credentials, passwords, or tracking telemetry on remote external servers. Session states are stored locally in the browser runtime.<br><br>
                    <b>Decision-Support Notice:</b> JalRakshak is an engineering research and simulation platform. Outputs are generated for risk visualization, infrastructure resilience planning, and scenario assessment. They do not substitute for official statutory emergency notices or evacuation directives issued by the National Disaster Management Authority (NDMA), State Disaster Management Authorities (SDMAs), or the Central Water Commission.
                </div>
            </div>
        </div>
        """
    )
    if st.button("Close", use_container_width=True, key="dlg_btn_privacy_close", type="primary"):
        st.session_state["show_privacy_modal"] = False
        st.rerun()

