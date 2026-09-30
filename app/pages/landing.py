"""
JalRakshak — Page 1: Landing Page Master Coordinator.
Matches Section 7 and the full specification of the Master Prompt.

Order of Sections:
1. Header
2. Hero
3. Introduction
4. Scroll-Aligned Simulation Story
5. Simulation & Analysis Capabilities
6. Simulation Workflow
7. Simulation Preview
8. Historical Dam-Break Events in India
9. Technical Credibility / Methodology
10. Final CTA
11. Footer
"""
from __future__ import annotations
import streamlit as st

from app.pages.landing_components.header import render_header
from app.pages.landing_components.hero import render_hero
from app.pages.landing_components.introduction import render_introduction
from app.pages.landing_components.story import render_story
from app.pages.landing_components.capabilities import render_capabilities
from app.pages.landing_components.workflow import render_workflow
from app.pages.landing_components.preview import render_preview
from app.pages.landing_components.history import render_history
from app.pages.landing_components.methodology import render_methodology
from app.pages.landing_components.cta import render_cta
from app.pages.landing_components.footer import render_footer
from app.pages.landing_components.utils import render_html
from app.pages.landing_components.modals import (
    show_explore_dialog,
    show_signin_dialog,
    show_privacy_dialog,
)


def render_landing() -> None:
    """
    Render the complete Page 1 Landing Page for JalRakshak.
    """
    # ── 0. Inject Global Engineering Typography & Layout Styles ───────────────
    render_html(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
        <style>
            html, body, [class*="css"], .stApp {
                background-color: #F7F8F6 !important;
                color: #1E252B !important;
                font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }
            .main .block-container {
                max-width: 1280px !important;
                padding-top: 88px !important;
                padding-bottom: 2rem !important;
            }
            html {
                scroll-behavior: smooth;
                scroll-padding-top: 84px !important;
            }
            .stButton > button {
                font-family: 'IBM Plex Sans', sans-serif !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                letter-spacing: 0.02em !important;
                transition: all 0.15s ease-in-out !important;
            }
            .stButton > button[kind="primary"] {
                background: #17324D !important;
                color: #FFFFFF !important;
                border: 1px solid #17324D !important;
            }
            .stButton > button[kind="primary"]:hover {
                background: #256B8E !important;
                border-color: #256B8E !important;
                color: #FFFFFF !important;
            }
            .stButton > button[kind="secondary"] {
                background: #FFFFFF !important;
                color: #17324D !important;
                border: 1px solid #D7DDE1 !important;
            }
            .stButton > button[kind="secondary"]:hover {
                background: #F7F8F6 !important;
                border-color: #256B8E !important;
                color: #256B8E !important;
            }
            .stSelectbox div[data-baseweb="select"] {
                background-color: #FFFFFF !important;
                border: 1px solid #D7DDE1 !important;
                color: #1E252B !important;
                border-radius: 6px !important;
            }
            .stTextInput input {
                background-color: #FFFFFF !important;
                border: 1px solid #D7DDE1 !important;
                color: #1E252B !important;
                border-radius: 6px !important;
            }
            .streamlit-expanderHeader {
                background-color: #FFFFFF !important;
                border: 1px solid #D7DDE1 !important;
                border-radius: 6px !important;
                color: #17324D !important;
                font-weight: 600 !important;
            }
            .streamlit-expanderContent {
                background-color: #FFFFFF !important;
                border: 1px solid #D7DDE1 !important;
                border-top: none !important;
                border-bottom-left-radius: 6px !important;
                border-bottom-right-radius: 6px !important;
            }
        </style>
        <div id="top"></div>
        """
    )

    # ── Handle query parameter actions (e.g. ?action=privacy, ?action=signin, ?action=explore) ──
    action = st.query_params.get("action") or st.query_params.get("modal")
    if action:
        if action == "privacy":
            st.session_state["show_privacy_modal"] = True
        elif action == "signin":
            st.session_state["show_signin_modal"] = True
        elif action == "explore":
            st.session_state["show_explore_modal"] = True
        if "action" in st.query_params:
            del st.query_params["action"]
        if "modal" in st.query_params:
            del st.query_params["modal"]

    # ── Modal Check & Render ──────────────────────────────────────────────────
    if st.session_state.get("show_explore_modal", False):
        st.session_state["show_explore_modal"] = False
        show_explore_dialog()

    if st.session_state.get("show_signin_modal", False):
        st.session_state["show_signin_modal"] = False
        show_signin_dialog()

    if st.session_state.get("show_privacy_modal", False):
        st.session_state["show_privacy_modal"] = False
        show_privacy_dialog()

    # ── Page Structure (Exact Section Sequence 1 to 11) ───────────────────────
    # 1. Header
    render_header()

    # 2. Hero
    render_hero()

    # 3. Introduction
    render_introduction()

    # 4. Scroll-Aligned Simulation Story
    render_story()

    # 5. Simulation & Analysis Capabilities
    render_capabilities()

    # 6. Simulation Workflow
    render_workflow()

    # 7. Simulation Preview
    render_preview()

    # 8. Historical Dam-Break Events in India
    render_history()

    # 9. Technical Credibility / Methodology
    render_methodology()

    # 10. Final CTA
    render_cta()

    # 11. Footer
    render_footer()
