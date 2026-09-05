import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Data Explorer PRO", layout="wide")

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

CHART_COLORWAY = [ACCENT, TEAL, AMBER, CORAL, PURPLE, "#5AB7E8"]


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


def style_chart(fig, height=460):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SECONDARY, size=13),
        title_font=dict(family="Inter", size=15, color=TEXT_PRIMARY),
        title_x=0.0,
        height=height,
        margin=dict(t=55, l=10, r=10, b=10),
        colorway=CHART_COLORWAY,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
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
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
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

/* Widgets */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
.stButton button {{
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
}}
.stButton button:hover {{ opacity: .9; }}

[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {BORDER};
}}
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
        <div class="brand-mark">🔍</div>
        <div>
            <div class="brand-name">Analyse Exploratoire</div>
            <div class="brand-sub">Data Exploration • Patterns Detection • Statistical Insights</div>
        </div>
    </div>
</div>
""")

st.divider()

# =========================
# LOAD DATA SAFE
# =========================
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv("data_students.csv")

    if "nom" not in df.columns:
        df["nom"] = "Inconnu"
    if "filiere" not in df.columns:
        df["filiere"] = "Non défini"
    if "niveau" not in df.columns:
        df["niveau"] = "Non défini"
    if "sexe" not in df.columns:
        df["sexe"] = "Non défini"

    return df


try:
    df = load_data()
except Exception:
    st.error("Aucune donnée disponible.")
    st.stop()

# =========================
# UI
# =========================
section_title("", "Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    filiere = st.selectbox(
        "Filière",
        ["Toutes"] + sorted(df["filiere"].dropna().unique())
    )

with col2:
    niveau = st.selectbox(
        "Niveau",
        ["Tous"] + sorted(df["niveau"].dropna().unique())
    )

with col3:
    sexe = st.selectbox(
        "Sexe",
        ["Tous"] + sorted(df["sexe"].dropna().unique())
    )

# =========================
# FILTER DATA
# =========================
df_filtered = df.copy()

if filiere != "Toutes":
    df_filtered = df_filtered[df_filtered["filiere"] == filiere]

if niveau != "Tous":
    df_filtered = df_filtered[df_filtered["niveau"] == niveau]

if sexe != "Tous":
    df_filtered = df_filtered[df_filtered["sexe"] == sexe]


section_title("", "Sélectionner l'étudiant")

if len(df_filtered) == 0:
    st.warning("Aucun étudiant trouvé avec ces filtres")
else:
    student_selected = st.selectbox(
        "Choisir un étudiant",
        df_filtered["nom"].unique()
    )

    student_data = df_filtered[df_filtered["nom"] == student_selected]
    st.dataframe(student_data, use_container_width=True)

st.divider()

# =========================
# FILIERE BAR CHART (SAFE)
# =========================
section_title("", "Nombre d'étudiants")

filiere_counts = df_filtered["filiere"].value_counts().reset_index()
filiere_counts.columns = ["filiere", "count"]

fig1 = px.bar(
    filiere_counts,
    x="filiere",
    y="count",
    color="filiere",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
st.plotly_chart(style_chart(fig1, 460), use_container_width=True)
