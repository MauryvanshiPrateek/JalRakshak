"""
Header and Navigation Component for JalRakshak Landing Page.
Matches Section 8 of the Master Specification and user screenshot.
Fixed sticky top bar that stays firmly in place upon scrolling.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_header() -> None:
    """
    Render fixed institutional header with semantic navigation and action buttons.
    Stays firmly pinned to the top of the viewport when scrolling.
    """
    render_html(
        """
        <header id="fixed-top-header" style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            height: 68px;
            z-index: 999999;
            background: #FFFFFF;
            border-bottom: 1px solid #D7DDE1;
            box-shadow: 0 1px 4px rgba(23, 50, 77, 0.05);
            display: flex;
            align-items: center;
        ">
            <div style="
                max-width: 1300px;
                width: 100%;
                margin: 0 auto;
                padding: 0 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-sizing: border-box;
            ">
                <a href="#top" style="display: flex; align-items: center; gap: 12px; text-decoration: none;">
                    <svg width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 8L18 5L32 8V12L18 9L4 12V8Z" fill="#17324D"/>
                        <path d="M7 13L18 10.5L29 13V17L18 14.5L7 17V13Z" fill="#256B8E"/>
                        <path d="M10 18L18 16L26 18V22L18 20L10 22V18Z" fill="#2D78A8"/>
                        <path d="M15 23C15 28 12 30 7 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M21 23C21 27 24 29 29 32" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                        <line x1="18" y1="21" x2="18" y2="33" stroke="#256B8E" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #17324D; letter-spacing: 0.03em; line-height: 1.1;">
                            JalRakshak
                        </div>
                        <div style="font-size: 0.72rem; color: #68747D; letter-spacing: 0.04em; font-family: 'IBM Plex Sans', sans-serif;">
                            Dam-Break Flood Simulation &amp; Assessment
                        </div>
                    </div>
                </a>
                <nav style="display: flex; align-items: center; gap: 26px;">
                    <a href="#simulation-preview" style="color: #1E252B; font-size: 0.92rem; font-weight: 500; text-decoration: none; padding: 6px 2px; transition: color 0.15s ease;">
                        Simulation
                    </a>
                    <a href="#history" style="color: #1E252B; font-size: 0.92rem; font-weight: 500; text-decoration: none; padding: 6px 2px; transition: color 0.15s ease;">
                        Dam-Break History
                    </a>
                    <a href="#methodology" style="color: #1E252B; font-size: 0.92rem; font-weight: 500; text-decoration: none; padding: 6px 2px; transition: color 0.15s ease;">
                        Methodology
                    </a>
                    <a href="?action=privacy" target="_self" style="color: #1E252B; font-size: 0.92rem; font-weight: 500; text-decoration: none; padding: 6px 2px; transition: color 0.15s ease;">
                        Privacy &amp; Policy
                    </a>
                    <span style="display: inline-block; width: 1px; height: 20px; background: #D7DDE1; margin: 0 4px;"></span>
                    <a href="?action=signin" target="_self" style="color: #17324D; font-size: 0.86rem; font-weight: 600; text-decoration: none; padding: 6px 14px; border: 1px solid #D7DDE1; border-radius: 6px; background: #FFFFFF; transition: all 0.15s ease;">
                        Sign In
                    </a>
                    <a href="?action=explore" target="_self" style="color: #FFFFFF; font-size: 0.86rem; font-weight: 600; text-decoration: none; padding: 7px 16px; border-radius: 6px; background: #17324D; transition: all 0.15s ease;">
                        Launch Simulation
                    </a>
                </nav>
            </div>
        </header>
        """
    )

