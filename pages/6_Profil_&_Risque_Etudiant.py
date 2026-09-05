import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Profil Étudiant", layout="wide")

# ==========================================================
# PALETTE / TOKENS — identiques à app.py
# ==========================================================
BG = "#0A0B0E"
SURFACE = "#131418"
BORDER = "#22242B"
TEXT_PRIMARY = "#EDEEF0"
TEXT_SECONDARY = "#888B94"
ACCENT = "#6C8EF5"
TEAL = "#3FD7B8"
AMBER = "#F0B457"
CORAL = "#F0716E"
PURPLE = "#B08CF0"


def render_html(html: str):
    """Affiche du HTML sans que Streamlit ne le traite comme un bloc de code
    (chaque ligne est dé-indentée avant envoi à st.markdown)."""
    lines = [line.strip() for line in html.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def section_title(icon: str, label: str):
    render_html(f"""
    <div class="section-title">
        <span class="icon">{icon}</span>
        <span class="label">{label}</span>
        <span class="rule"></span>
    </div>
    """)


def style_polar(fig, height=460, r_range=None):
    polar = dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(gridcolor=BORDER, linecolor=BORDER, color=TEXT_SECONDARY),
        angularaxis=dict(gridcolor=BORDER, linecolor=BORDER, color=TEXT_PRIMARY),
    )
    if r_range is not None:
        polar["radialaxis"]["visible"] = True
        polar["radialaxis"]["range"] = r_range

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SECONDARY, size=13),
        height=height,
        margin=dict(l=30, r=30, t=30, b=30),
        polar=polar,
        showlegend=False,
    )
    fig.update_traces(line=dict(width=3, color=ACCENT), fillcolor="rgba(108,142,245,0.25)")
    return fig


# ==========================================================
# STYLE GLOBAL — même charte que app.py
# ==========================================================
render_html(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    font-size: 20px;
}}

.stApp {{ background: {BG}; }}

section[data-testid="stSidebar"] {{
    background: #0D0E12;
    border-right: 1px solid {BORDER};
}}

::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 20px; }}

h1, h2, h3 {{ color: {TEXT_PRIMARY} !important; }}

/* En-tête */
.app-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 28px;
    border: 1px solid {BORDER};
    border-radius: 14px;
    background: {SURFACE};
    margin-bottom: 8px;
    flex-wrap: wrap;
    gap: 12px;
}}
.app-header .brand {{ display: flex; align-items: center; gap: 14px; }}
.app-header .brand-mark {{
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, {ACCENT}, {TEAL});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}}
.app-header .brand-name {{
    font-size: 25px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    letter-spacing: -0.2px;
}}
.app-header .brand-sub {{
    font-size: 17px;
    color: {TEXT_SECONDARY};
    margin-top: 2px;
}}

/* Titres de section */
.section-title {{
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin: 30px 0 14px 0;
}}
.section-title .icon {{ font-size: 20px; opacity: .9; }}
.section-title .label {{ font-size: 20px; font-weight: 600; color: {TEXT_PRIMARY}; }}
.section-title .rule {{ flex: 1; height: 1px; background: {BORDER}; }}

/* Panel de score de risque */
.risk-panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 4px solid var(--c, {ACCENT});
    border-radius: 12px;
    padding: 20px 22px;
}}
.risk-label {{ font-size: 14px; color: {TEXT_SECONDARY}; }}
.risk-score {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 34px;
    font-weight: 700;
    color: var(--c, {ACCENT});
    margin: 8px 0;
}}
.risk-level {{ font-size: 18px; font-weight: 700; color: var(--c, {ACCENT}); margin-bottom: 6px; }}
.risk-comment {{ font-size: 15px; color: {TEXT_PRIMARY}; }}

/* Widgets */
.stSlider [data-baseweb="slider"] > div > div {{ background: {ACCENT} !important; }}
.stButton button {{
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
}}
.stButton button:hover {{ opacity: .9; }}

.stSuccess, .stInfo, .stWarning, .stError {{ border-radius: 10px !important; }}
hr {{ border-color: {BORDER} !important; margin: 26px 0 !important; }}

</style>
""")


# ==========================================================
# EN-TÊTE
# ==========================================================
render_html("""
<div class="app-header">
    <div class="brand">
        <div class="brand-mark">🧬</div>
        <div>
            <div class="brand-name">Profil Intelligent de l'Étudiant</div>
            <div class="brand-sub">AI-driven Student Profile • Behavioral Analytics • Academic Intelligence</div>
        </div>
    </div>
</div>
""")

DATA_FILE = "data_students.csv"
st.divider()

# =========================
# CHARGEMENT DONNÉES
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


try:
    df = load_data()
except Exception:
    st.error(" Aucune donnée disponible.")
    st.stop()

# =========================
# FORMULAIRE PROFIL
# =========================
section_title("", "Entre tes données et mesure ton risque")

col1, col2 = st.columns(2)

with col1:
    heures_etude = st.slider("Heures d'étude/jour", 0, 12, 3)
    sommeil = st.slider("Heures de sommeil", 0, 12, 6)
    stress = st.slider("Stress (1-10)", 1, 10, 5)

with col2:
    motivation = st.slider("Motivation (1-10)", 1, 10, 5)
    concentration = st.slider("Concentration (1-10)", 1, 10, 5)
    telephone = st.slider("Temps téléphone (h)", 0, 12, 4)

st.divider()

# =========================
# SCORE DE RISQUE
# =========================
section_title("", "Résultat d'analyse")

if st.button("⚠️ Voir ton risque"):

    stress_n = stress / 10
    sommeil_risk = max(0, (7 - sommeil) / 7)
    etude_risk = max(0, (4 - heures_etude) / 4)
    motivation_risk = (10 - motivation) / 10

    score_risque = (
        0.35 * stress_n +
        0.25 * sommeil_risk +
        0.25 * etude_risk +
        0.15 * motivation_risk
    )

    if score_risque < 0.3:
        niveau = "🟢 Faible risque"
        commentaire = "Tu es sur une bonne trajectoire 👍"
        color = TEAL

    elif score_risque < 0.6:
        niveau = "🟠 Risque moyen"
        commentaire = "Attention à ton équilibre travail/repos ⚠️"
        color = AMBER

    else:
        niveau = "🔴 Risque élevé"
        commentaire = "Risque de baisse de performance important"
        color = CORAL

    render_html(f"""
    <div class="risk-panel" style="--c:{color};">
        <div class="risk-label">Score de risque académique</div>
        <div class="risk-score">{round(score_risque, 2)}</div>
        <div class="risk-level">{niveau}</div>
        <div class="risk-comment">{commentaire}</div>
    </div>
    """)

    st.divider()

# =========================
# RADAR
# =========================
section_title("", "Ton profil actuel")

categories = ["Étude", "Sommeil", "Stress", "Motivation"]
values = [heures_etude / 12, sommeil / 12, stress / 10, motivation / 10]

categories += [categories[0]]
values += [values[0]]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', line=dict(width=3)))
st.plotly_chart(style_polar(fig, 460, r_range=[0, 1]), use_container_width=True)

# =========================
# RECOMMANDATIONS AUTOMATIQUES
# =========================
section_title("", "Recommandations personnalisées")

if st.button("💡 Recommandations personnalisées"):
    if sommeil < 6:
        st.info("😴 Essaie de dormir au moins 6h par nuit")

    if heures_etude < 4:
        st.info("📚 Augmente progressivement ton temps d'étude")

    if stress > 7:
        st.info("🧘 Fais des pauses, des distractions et gère ton stress")

    if motivation < 5:
        st.info("🔥 Fixe-toi des objectifs courts et motivants")

    if telephone > 6:
        st.info("📵 Réduis le temps passé sur téléphone")
    else:
        st.info("💪 Allez, nos encouragements")
