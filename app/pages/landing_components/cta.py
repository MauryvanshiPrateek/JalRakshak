"""
Final Call-to-Action Component for JalRakshak Landing Page.
Matches Section 35 of the Master Specification.
Features solid Deep Navy (#17324D) canvas with no gradients.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_cta() -> None:
    """
    Render Section 35: Final Call-to-Action with primary and secondary engineering buttons.
    """
    render_html("<div style='margin-top: 60px;'></div>")

    render_html(
        """
        <div style="background: #17324D; border-radius: 8px; padding: 48px 32px; text-align: center; box-shadow: 0 4px 16px rgba(23, 50, 77, 0.08); max-width: 1100px; margin: 0 auto;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #5FA8D3; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">
                READY TO RUN SCENARIO ANALYSIS
            </div>
            <h2 style="font-size: 2.5rem; font-weight: 600; color: #FFFFFF; margin: 0 0 16px 0;">
                Explore the Simulation
            </h2>
            <p style="font-size: 1.15rem; color: #D7DDE1; max-width: 680px; margin: 0 auto 32px auto; line-height: 1.6;">
                Define a scenario, run the model, and examine the resulting flood behaviour through an interactive geospatial interface.
            </p>
        </div>
        """
    )

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        btn_cta1, btn_cta2 = st.columns(2)
        with btn_cta1:
            if st.button("Launch Simulation", key="cta_bottom_launch", type="primary", use_container_width=True):
                st.session_state["show_explore_modal"] = True
                st.rerun()
        with btn_cta2:
            render_html(
                """
                <a href="#methodology" style="display: block; text-align: center; padding: 8px 12px; border: 1px solid #17324D; border-radius: 8px; color: #17324D; font-weight: 600; font-size: 0.95rem; text-decoration: none; background: #FFFFFF;">
                    View Methodology
                </a>
                """
            )
