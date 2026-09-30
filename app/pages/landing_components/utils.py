"""
Utility module for safely rendering HTML in Streamlit without triggering Markdown-it code blocks.
"""
from __future__ import annotations
import re
import textwrap
import streamlit as st


def render_html(html_content: str) -> None:
    """
    Renders raw HTML safely in Streamlit.
    Removes HTML comments and collapses blank lines that cause markdown-it
    to mistakenly parse indented HTML tags as <pre><code> blocks.
    """
    clean = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    clean = textwrap.dedent(clean).strip()
    lines = [line for line in clean.splitlines() if line.strip()]
    clean_html = "\n".join(lines)
    st.markdown(clean_html, unsafe_allow_html=True)
