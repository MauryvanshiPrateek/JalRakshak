"""
Institutional Multi-Column Footer Component for JalRakshak Landing Page.
Matches Sections 36 & 37 of the Master Specification.
"""
from __future__ import annotations
import streamlit as st
from app.pages.landing_components.utils import render_html


def render_footer() -> None:
    """
    Render institutional multi-column footer with disclaimer and navigation references.
    """
    render_html("<div id='privacy' style='margin-top: 60px;'></div>")

    render_html(
        """
        <footer style="background: #1E252B; color: #FFFFFF; padding: 48px 24px 32px 24px; margin: 2rem -1rem -2rem -1rem; border-top: 1px solid #334155;">
            <div style="max-width: 1200px; margin: 0 auto;">
                <div style="display: grid; grid-template-columns: 2.5fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 36px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <svg width="26" height="26" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M4 8L18 5L32 8V12L18 9L4 12V8Z" fill="#5FA8D3"/>
                                <path d="M7 13L18 10.5L29 13V17L18 14.5L7 17V13Z" fill="#256B8E"/>
                                <line x1="18" y1="21" x2="18" y2="33" stroke="#5FA8D3" stroke-width="2.5" stroke-linecap="round"/>
                            </svg>
                            <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.04em;">
                                JalRakshak
                            </span>
                        </div>
                        <p style="font-size: 0.88rem; color: #B9C1C7; line-height: 1.6; margin-bottom: 16px; max-width: 320px;">
                            Dam-break flood inundation modelling, hydrodynamic wave propagation, and geospatial hazard assessment platform for engineers and researchers.
                        </p>
                        <div style="font-size: 0.78rem; color: #64748B; font-family: 'IBM Plex Mono', monospace;">
                            SMART INDIA HACKATHON 2026 · SIH26161
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;">
                            PLATFORM
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.88rem; line-height: 2;">
                            <li><a href="#simulation-preview" style="color: #D7DDE1; text-decoration: none;">Simulation Workspace</a></li>
                            <li><a href="#history" style="color: #D7DDE1; text-decoration: none;">Dam-Break History</a></li>
                            <li><a href="#capabilities" style="color: #D7DDE1; text-decoration: none;">Model Capabilities</a></li>
                            <li><a href="#workflow" style="color: #D7DDE1; text-decoration: none;">Scenario Workflow</a></li>
                        </ul>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;">
                            INFORMATION
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.88rem; line-height: 2;">
                            <li><a href="#methodology" style="color: #D7DDE1; text-decoration: none;">Technical Methodology</a></li>
                            <li><a href="#history" style="color: #D7DDE1; text-decoration: none;">Data Sources & Attribution</a></li>
                            <li><a href="?action=privacy" target="_self" style="color: #D7DDE1; text-decoration: none;">Privacy & Policy</a></li>
                            <li><a href="?action=privacy" target="_self" style="color: #D7DDE1; text-decoration: none;">Terms of Use</a></li>
                        </ul>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;">
                            SUPPORT
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.88rem; line-height: 2;">
                            <li><a href="mailto:support@jalrakshak.org" style="color: #D7DDE1; text-decoration: none;">Technical Inquiries</a></li>
                            <li><a href="#methodology" style="color: #D7DDE1; text-decoration: none;">Documentation</a></li>
                            <li><a href="#top" style="color: #D7DDE1; text-decoration: none;">Back to Top ↑</a></li>
                        </ul>
                    </div>
                </div>
                <div style="border-top: 1px solid #334155; padding-top: 20px; margin-bottom: 20px;">
                    <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.6; max-width: 950px;">
                        <b>DISCLAIMER:</b> Simulation results are dependent on input data, model assumptions and scenario parameters and should be interpreted in accordance with the applicable technical methodology. This platform is a decision-support and technical modelling tool and does not replace official meteorological, hydrological, or emergency advisories issued by national disaster management authorities or water resource departments.
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 0.75rem; color: #64748B;">
                    <div>
                        © 2026 JalRakshak · Dam-Break Flood Simulation & Assessment · All rights reserved.
                    </div>
                    <div style="font-family: 'IBM Plex Mono', monospace;">
                        SYSTEM STATUS: ALL SOLVERS OPERATIONAL
                    </div>
                </div>
            </div>
        </footer>
        """
    )
