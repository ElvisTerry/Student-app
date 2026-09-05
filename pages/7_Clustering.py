import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Étudiants", layout="wide")

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
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def kpi_row(items, cols=3):
    parts = [f'<div class="kpi-row" style="grid-template-columns:repeat({cols},1fr);">']
    for label, value, color in items:
        parts.append(
            f'<div class="kpi">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value" style="color:{color};">{value}</div>'
            f'</div>'
        )
    parts.append("</div>")
    render_html("".join(parts))


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
    background: linear-gradient(135deg, {PURPLE}, {ACCENT});
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

/* KPI */
.kpi-row {{ display: grid; gap: 12px; }}
.kpi {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
}}
.kpi .kpi-label {{ font-size: 15px; color: {TEXT_SECONDARY}; margin-bottom: 8px; }}
.kpi .kpi-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    font-weight: 600;
}}

/* Panel générique */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
    font-size: 15px;
    line-height: 1.7;
}}

/* Fiche de groupe */
.spec-list {{ margin-top: 4px; }}
.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid {BORDER};
    font-size: 16px;
}}
.spec-row:last-child {{ border-bottom: none; }}
.spec-row .k {{ color: {TEXT_SECONDARY}; }}
.spec-row .v {{ color: {TEXT_PRIMARY}; font-family: 'IBM Plex Mono', monospace; }}

[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {BORDER};
}}
.stSuccess, .stInfo, .stWarning, .stError {{ border-radius: 10px !important; }}
hr {{ border-color: {BORDER} !important; margin: 26px 0 !important; }}

@media (max-width: 900px) {{
    .kpi-row {{ grid-template-columns: repeat(2, 1fr) !important; }}
}}
@media (max-width: 520px) {{
    .kpi-row {{ grid-template-columns: 1fr !important; }}
}}

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
            <div class="brand-name">Segmentation Intelligente des Étudiants</div>
            <div class="brand-sub">Machine Learning • K-Means • AI-driven Student Profiling</div>
        </div>
    </div>
</div>
""")

# =========================
# DATA
# =========================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")


try:
    df = load_data()
except Exception:
    st.error(" Aucune donnée disponible, veuillez remplir le formulaire dans le menu rétractable.")
    st.stop()

# =========================
# FEATURES POUR CLUSTERING
# =========================
features = [
    "moyenne", "stress", "heures_etude",
    "sommeil", "motivation", "concentration"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# =========================
# LABELS INTELLIGENTS
# =========================
cluster_map = {}
for c in df["cluster"].unique():
    avg_score = df[df["cluster"] == c]["moyenne"].mean()
    if avg_score >= 13:
        cluster_map[c] = "🟢 Performants"
    elif avg_score >= 10:
        cluster_map[c] = "🟡 Moyens"
    else:
        cluster_map[c] = "🔴 À risque"

df["profil"] = df["cluster"].map(cluster_map)
st.divider()

# =========================
# DISPLAY KPI
# =========================
section_title("", "Répartition des profils")

perf = (df["profil"] == "🟢 Performants").sum()
moy = (df["profil"] == "🟡 Moyens").sum()
risque = (df["profil"] == "🔴 À risque").sum()

kpi_row([
    ("Performants", perf, TEAL),
    ("Moyens", moy, AMBER),
    ("À risque", risque, CORAL),
], cols=3)

st.divider()

# =========================
# VISUALISATION 2D
# =========================
section_title("", "Visualisation des clusters")

fig = px.scatter(
    df, x="heures_etude", y="moyenne", color="profil",
    color_discrete_map={
        "🟢 Performants": TEAL,
        "🟡 Moyens": AMBER,
        "🔴 À risque": CORAL,
    },
    title="Segmentation des étudiants",
)
st.plotly_chart(style_chart(fig, 500), use_container_width=True)

render_html(f"""
<div class="panel" style="border-left:3px solid {TEAL};">
    <b>Interprétation des clusters d'étudiants</b><br>
    Ce graphique permet de visualiser la répartition des étudiants selon leur <b>temps d'étude</b> et leur <b>performance académique</b>.<br><br>
    🟢 <b>Performants</b> - Étudiants avec de bonnes moyennes et généralement un bon volume d'étude. Profil stable et autonome.<br>
    🟡 <b>Moyens</b> - Résultats corrects mais variables. Peuvent progresser avec plus de régularité ou de concentration.<br>
    🔴 <b>À risque</b> - Faible moyenne malgré parfois un effort. Nécessitent un accompagnement (méthode de travail, motivation, gestion du stress).<br><br>
    📌 <b>Lecture du graphique :</b> chaque point représente un étudiant, la couleur indique son profil.
</div>
""")

st.divider()

# =========================
# PROFILS EXPLIQUÉS
# =========================
section_title("", "Analyse des groupes")

for profil in df["profil"].unique():
    subset = df[df["profil"] == profil]

    render_html(f"""
    <div class="panel" style="margin-bottom:14px;">
        <div style="font-size:17px; font-weight:600; margin-bottom:8px;">{profil}</div>
        <div class="spec-list">
            <div class="spec-row"><span class="k">Moyenne</span><span class="v">{round(subset['moyenne'].mean(), 2)}</span></div>
            <div class="spec-row"><span class="k">Stress moyen</span><span class="v">{round(subset['stress'].mean(), 2)}</span></div>
            <div class="spec-row"><span class="k">Heures d'étude moyenne</span><span class="v">{round(subset['heures_etude'].mean(), 2)}</span></div>
            <div class="spec-row"><span class="k">Effectif</span><span class="v">{len(subset)}</span></div>
        </div>
    </div>
    """)

st.divider()
