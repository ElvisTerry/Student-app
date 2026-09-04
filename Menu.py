import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================================
# CONFIGURATION PAGE
# ==========================================================
st.set_page_config(
    page_title="SmartStudent Analytics",
    layout="wide",
    page_icon="🎓",
)

# ==========================================================
# PALETTE / TOKENS
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
    """
    Affiche du HTML via st.markdown en évitant le bug classique de Streamlit :
    si une ligne commence par 4 espaces ou plus, le parseur Markdown la
    traite comme un bloc de code et affiche les balises en texte brut au
    lieu de les interpréter. On "dé-indente" donc chaque ligne avant envoi.
    """
    lines = [line.strip() for line in html.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def style_chart(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SECONDARY, size=12),
        title_font=dict(family="Inter", size=14, color=TEXT_PRIMARY),
        title_x=0.0,
        height=height,
        margin=dict(t=50, l=10, r=10, b=10),
        colorway=CHART_COLORWAY,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def section_title(icon: str, label: str):
    render_html(f"""
    <div class="section-title">
        <span class="icon">{icon}</span>
        <span class="label">{label}</span>
        <span class="rule"></span>
    </div>
    """)


# ==========================================================
# STYLE GLOBAL — THÈME SOMBRE, TERMINAL D'ANALYSE
# ==========================================================
render_html(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    font-size : 20 px;
}}

.stApp {{
    background: {BG};
}}

section[data-testid="stSidebar"] {{
    background: #0D0E12;
    border-right: 1px solid {BORDER};
}}

::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 20px; }}

/* Neutralise les gros titres Markdown par défaut de Streamlit */
h1, h2, h3 {{
    color: {TEXT_PRIMARY} !important;
}}

/* En-tête d'application */
.app-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 28px;
    border: 1px solid {BORDER};
    border-radius: 14px;
    background: {SURFACE};
    margin-bottom: 8px;
}}
.app-header .brand {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
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
    font-size: 17px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    letter-spacing: -0.2px;
}}
.app-header .brand-sub {{
    font-size: 12.5px;
    color: {TEXT_SECONDARY};
    margin-top: 2px;
}}
.app-header .status {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    color: {TEAL};
    border: 1px solid {BORDER};
    padding: 6px 12px;
    border-radius: 999px;
    white-space: nowrap;
}}
.app-header .status .dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: {TEAL};
    box-shadow: 0 0 0 3px rgba(63,215,184,.15);
}}

/* Titres de section */
.section-title {{
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin: 30px 0 14px 0;
}}
.section-title .icon {{ font-size: 20px; opacity: .9; }}
.section-title .label {{
    font-size: 20px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
.section-title .rule {{
    flex: 1;
    height: 1px;
    background: {BORDER};
}}

/* Cartes génériques (bordure fine) */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
}}

/* KPI */
.kpi-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}}
.kpi {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px;
}}
.kpi .kpi-label {{
    font-size: 15px;
    color: {TEXT_SECONDARY};
    margin-bottom: 8px;
}}
.kpi .kpi-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
.kpi .kpi-bar {{
    height: 3px;
    border-radius: 3px;
    margin-top: 12px;
    background: {BORDER};
    overflow: hidden;
}}
.kpi .kpi-bar span {{
    display: block;
    height: 100%;
    border-radius: 3px;
}}

/* Bandeau objectifs (séquence 01-05, statique) */
.obj-row {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
}}
.obj {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 2px solid var(--accent, {ACCENT});
    border-radius: 10px;
    padding: 14px 16px;
}}
.obj .obj-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 15px;
    color: {TEXT_SECONDARY};
    margin-bottom: 8px;
}}
.obj .obj-title {{
    font-size: 16px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin-bottom: 6px;
    line-height: 1.3;
}}
.obj .obj-desc {{
    font-size: 15px;
    color: {TEXT_SECONDARY};
    line-height: 1.5;
}}

/* Métriques doubles (réussite / échec) */
.metric-big {{ text-align: left; }}
.metric-big .metric-label {{ font-size: 12.5px; color: {TEXT_SECONDARY}; }}
.metric-big .metric-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 34px;
    font-weight: 600;
    margin-top: 8px;
}}

/* Fiche profil */
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

/* Recommandations & actions */
.reco {{
    display: flex;
    gap: 12px;
    align-items: flex-start;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 3px solid var(--c, {ACCENT});
    border-radius: 10px;
    padding: 13px 16px;
    margin-bottom: 8px;
    font-size: 13px;
    color: {TEXT_PRIMARY};
    line-height: 1.5;
}}
.reco .tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    color: var(--c, {ACCENT});
    white-space: nowrap;
    padding-top: 1px;
}}

.action-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 11px 16px;
    margin-bottom: 8px;
    font-size: 16px;
    color: {TEXT_PRIMARY};
}}
.action-row .idx {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    color: {TEXT_SECONDARY};
    width: 18px;
}}

/* Footer */
.app-footer {{
    margin-top: 36px;
    padding: 16px 4px 4px 4px;
    border-top: 1px solid {BORDER};
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 15px;
    color: {TEXT_SECONDARY};
    flex-wrap: wrap;
    gap: 6px;
}}

/* Table & alertes Streamlit */
[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {BORDER};
}}
.stSuccess, .stInfo, .stWarning, .stError {{ border-radius: 10px !important; }}
hr {{ border-color: {BORDER} !important; margin: 26px 0 !important; }}

/* Responsive : évite le débordement sur mobile */
@media (max-width: 900px) {{
    .kpi-row {{ grid-template-columns: repeat(2, 1fr); }}
    .obj-row {{ grid-template-columns: repeat(2, 1fr); }}
    .app-header {{ flex-wrap: wrap; gap: 12px; }}
}}
@media (max-width: 520px) {{
    .kpi-row {{ grid-template-columns: 1fr; }}
    .obj-row {{ grid-template-columns: 1fr; }}
}}

</style>
""")


# ==========================================================
# CHARGEMENT DONNÉES
# ==========================================================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")


try:
    df = load_data()
except Exception:
    st.error(
        "❌ Aucune donnée disponible. "
        "Veuillez remplir le formulaire dans le menu rétractable."
    )
    st.stop()


# ==========================================================
# EN-TÊTE (une seule fois)
# ==========================================================
render_html("""
<div class="app-header">
    <div class="brand">
        <div class="brand-mark">🎓</div>
        <div>
            <div class="brand-name">SmartStudent Analytics</div>
            <div class="brand-sub">Analyse des performances académiques - Data analysis; IA</div>
        </div>
    </div>
    <div class="status"><span class="dot"></span>Données synchronisées</div>
</div>
""")


# ==========================================================
# OBJECTIFS DU PROJET (bandeau statique en séquence)
# ==========================================================
section_title("🧭", "Objectifs du projet")

objectifs = [
    ("01", "Collecte intelligente des données", "Centralisation et structuration des informations étudiantes.", ACCENT),
    ("02", "Analyse comportementale", "Étude des performances et des habitudes académiques.", TEAL),
    ("03", "Facteurs de réussite", "Détection automatique des variables influentes.", PURPLE),
    ("04", "Prédiction des performances", "Utilisation de modèles IA pour anticiper les résultats.", CORAL),
    ("05", "Rapports intelligents", "Génération d'insights décisionnels automatisés.", AMBER),
]

obj_parts = ['<div class="obj-row">']
for num, title, desc, color in objectifs:
    obj_parts.append(
        f'<div class="obj" style="--accent:{color};">'
        f'<div class="obj-num">{num}</div>'
        f'<div class="obj-title">{title}</div>'
        f'<div class="obj-desc">{desc}</div>'
        f'</div>'
    )
obj_parts.append("</div>")
render_html("".join(obj_parts))


# ==========================================================
# KPI
# ==========================================================
section_title("📊", "Indicateurs globaux")

nb_etudiants = len(df)
moyenne_gen = round(df["moyenne"].mean(), 2)
stress_moy = round(df["stress"].mean(), 2)
heures_moy = round(df["heures_etude"].mean(), 2)

kpis = [
    ("Étudiants enregistrés", f"{nb_etudiants}", ACCENT, 100),
    ("Moyenne générale", f"{moyenne_gen}", TEAL, min(moyenne_gen / 20 * 100, 100)),
    ("Stress moyen", f"{stress_moy}", CORAL, min(stress_moy / 10 * 100, 100)),
    ("Heures d'étude moyennes", f"{heures_moy}", AMBER, min(heures_moy / 8 * 100, 100)),
]

kpi_parts = ['<div class="kpi-row">']
for label, value, color, pct in kpis:
    kpi_parts.append(
        f'<div class="kpi">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-bar"><span style="width:{pct}%; background:{color};"></span></div>'
        f'</div>'
    )
kpi_parts.append("</div>")
render_html("".join(kpi_parts))


# ==========================================================
# INSIGHTS AUTOMATIQUES
# ==========================================================
section_title("🧠", "Insights automatiques")

best = df.groupby("filiere")["moyenne"].mean().idxmax()
worst = df.groupby("filiere")["moyenne"].mean().idxmin()
stress_high = df.groupby("filiere")["stress"].mean().idxmax()
study_high = df.groupby("filiere")["heures_etude"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()

insights = [
    ("Meilleure filière", best, TEAL),
    ("Filière la moins performante", worst, CORAL),
    ("Nombre total de filières", str(df["filiere"].nunique()), ACCENT),
    ("Filière la plus stressée", stress_high, AMBER),
    ("Filière la plus travailleuse", study_high, ACCENT),
    ("Filière la plus motivée", motivation_high, TEAL),
]

cols = st.columns(3)
for i, (label, value, color) in enumerate(insights):
    with cols[i % 3]:
        render_html(f"""
        <div class="panel" style="margin-bottom:12px;">
            <div style="font-size:12px; color:{TEXT_SECONDARY};">{label}</div>
            <div style="font-size:16px; font-weight:600; color:{color}; margin-top:6px;">{value}</div>
        </div>
        """)


# ==========================================================
# PERFORMANCE GLOBALE
# ==========================================================
section_title("📈", "Performance académique globale")

pass_rate = (df["moyenne"] >= 10).mean() * 100
fail_rate = 100 - pass_rate

col1, col2 = st.columns(2)
with col1:
    render_html(f"""
    <div class="panel metric-big">
        <div class="metric-label">Taux de réussite</div>
        <div class="metric-value" style="color:{TEAL};">{pass_rate:.1f}%</div>
    </div>
    """)
with col2:
    render_html(f"""
    <div class="panel metric-big">
        <div class="metric-label">Taux d'échec</div>
        <div class="metric-value" style="color:{CORAL};">{fail_rate:.1f}%</div>
    </div>
    """)


# ==========================================================
# TOP ÉTUDIANTS
# ==========================================================
section_title("🏆", "Top 10 des étudiants")

top_students = df.sort_values("moyenne", ascending=False).head(10)

st.dataframe(
    top_students[[
        "nom", "age", "sexe", "filiere", "niveau", "heures_etude",
        "methode", "regularite", "sommeil", "sport", "telephone",
        "stress", "concentration", "motivation", "moyenne", "credits",
    ]],
    use_container_width=True,
    height=380,
)


# ==========================================================
# DISTRIBUTION DES MOYENNES
# ==========================================================
section_title("📊", "Distribution des performances")

fig_distribution = px.histogram(
    df, x="moyenne", nbins=20,
    title="Répartition des moyennes étudiantes",
    marginal="box",
)
st.plotly_chart(style_chart(fig_distribution, 420), use_container_width=True)


# ==========================================================
# PERFORMANCE PAR FILIÈRE
# ==========================================================
section_title("🏫", "Performance moyenne par filière")

mean_by_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()
fig_filiere = px.bar(
    mean_by_filiere, x="filiere", y="moyenne",
    title="Moyenne académique selon la filière",
    text_auto=".2f",
)
st.plotly_chart(style_chart(fig_filiere, 420), use_container_width=True)


# ==========================================================
# FACTEURS D'IMPACT
# ==========================================================
section_title("📉", "Facteurs influençant la réussite")

correlation = df.select_dtypes(include="number").corr()["moyenne"].sort_values()
fig_corr = px.bar(correlation, title="Corrélation des variables avec la moyenne")
st.plotly_chart(style_chart(fig_corr, 520), use_container_width=True)


# ==========================================================
# HEURES D'ÉTUDE VS MOYENNE
# ==========================================================
section_title("📚", "Relation entre étude et performance")

fig_scatter = px.scatter(
    df, x="heures_etude", y="moyenne", color="filiere", size="motivation",
    hover_name="nom", title="Heures d'étude et moyenne académique",
)
st.plotly_chart(style_chart(fig_scatter, 520), use_container_width=True)


# ==========================================================
# STRESS VS PERFORMANCE
# ==========================================================
section_title("😰", "Impact du stress sur les résultats")

fig_stress = px.box(df, x="stress", y="moyenne", title="Influence du niveau de stress")
st.plotly_chart(style_chart(fig_stress, 460), use_container_width=True)


# ==========================================================
# PROFIL ÉTUDIANT IDÉAL
# ==========================================================
section_title("🌟", "Profil étudiant idéal")

best_student = df.sort_values("moyenne", ascending=False).iloc[0]

col1, col2 = st.columns([1, 2])
with col1:
    render_html(f"""
    <div class="panel" style="text-align:center; height:100%;">
        <div style="font-size:12px; color:{TEXT_SECONDARY};">Meilleure moyenne observée</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:36px; font-weight:600; color:{TEAL}; margin-top:10px;">
            {best_student['moyenne']:.2f}<span style="font-size:16px; color:{TEXT_SECONDARY};">/20</span>
        </div>
    </div>
    """)

with col2:
    render_html(f"""
    <div class="panel">
        <div style="font-size:15px; font-weight:600; margin-bottom:6px;">{best_student['nom']}</div>
        <div class="spec-list">
            <div class="spec-row"><span class="k">Heures d'étude</span><span class="v">{best_student['heures_etude']} h/jour</span></div>
            <div class="spec-row"><span class="k">Motivation</span><span class="v">{best_student['motivation']}/10</span></div>
            <div class="spec-row"><span class="k">Concentration</span><span class="v">{best_student['concentration']}/10</span></div>
            <div class="spec-row"><span class="k">Sommeil</span><span class="v">{best_student['sommeil']} h</span></div>
            <div class="spec-row"><span class="k">Activité sportive</span><span class="v">{best_student['sport']}</span></div>
            <div class="spec-row"><span class="k">Régularité</span><span class="v">{best_student['regularite']}</span></div>
        </div>
    </div>
    """)


# ==========================================================
# RECOMMANDATIONS IA
# ==========================================================
section_title("🤖", "Assistant d'aide à la décision")

recommandations = []

if df["stress"].mean() > 6:
    recommandations.append((
        "ALERTE", CORAL,
        "Le niveau de stress global est élevé. "
        "Il est conseillé de renforcer l'accompagnement psychologique.",
    ))

if df["heures_etude"].mean() < 3:
    recommandations.append((
        "VIGILANCE", AMBER,
        "Le temps moyen d'étude reste insuffisant. "
        "Des séances de tutorat pourraient être envisagées.",
    ))

if df["motivation"].mean() > 7:
    recommandations.append((
        "POSITIF", TEAL,
        "La motivation générale est excellente et constitue "
        "un levier important de réussite.",
    ))

if df["sommeil"].mean() < 6:
    recommandations.append((
        "VIGILANCE", PURPLE,
        "Le temps de sommeil moyen semble faible. "
        "Une meilleure hygiène de vie pourrait améliorer les performances.",
    ))

for tag, color, text in recommandations:
    render_html(f"""
    <div class="reco" style="--c:{color};">
        <span class="tag">{tag}</span>
        <span>{text}</span>
    </div>
    """)





