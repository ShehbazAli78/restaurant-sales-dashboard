"""Global CSS injection and small style helpers for the dashboard."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Poppins', sans-serif !important; font-weight: 700 !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2.5rem;
    max-width: 1300px;
}

.gradient-text {
    background: linear-gradient(90deg, #6C5CE7 0%, #00CEC9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-label {
    color: #A29BFE;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.045) 0%, rgba(255,255,255,0.015) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(108, 92, 231, 0.5);
}
.kpi-label {
    color: #8b8fa3;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.kpi-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: #F2F2F7;
    margin-top: 0.15rem;
}
.kpi-icon { font-size: 1.3rem; }

/* Chart container card */
.chart-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1rem 1.1rem 0.4rem 1.1rem;
    margin-bottom: 0.6rem;
}
.chart-title {
    font-weight: 700;
    font-size: 0.98rem;
    margin-bottom: 0.4rem;
    color: #E6E6E6;
}

hr.soft { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 1.6rem 0; }

.insight-box {
    background: rgba(108, 92, 231, 0.08);
    border-left: 3px solid #6C5CE7;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #C9C9DC;
    font-size: 0.9rem;
}

.site-footer {
    text-align: center;
    color: #6b6f80;
    font-size: 0.82rem;
    padding-top: 1.5rem;
}
</style>
"""


def inject_global_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def section_header(label: str, title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-label'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"### {title}")
    if subtitle:
        st.markdown(f"<p style='color:#8b8fa3;margin-top:-0.3rem;'>{subtitle}</p>", unsafe_allow_html=True)


def soft_divider() -> None:
    st.markdown("<hr class='soft'/>", unsafe_allow_html=True)


def kpi_card(label: str, value: str, icon: str = "") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card_start(title: str) -> None:
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{title}</div>", unsafe_allow_html=True)


def chart_card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)
