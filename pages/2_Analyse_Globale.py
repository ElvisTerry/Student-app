import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analyse Globale", layout="wide")

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


def style_heatmap(fig, height=750):
    """Variante de style_chart pour les matrices de corrélation : figure et
    annotations agrandies pour rester lisibles sur toute la largeur du
    conteneur (aspect='auto' + hauteur augmentée)."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SECONDARY, size=14),
        title_font=dict(family="Inter", size=16, color=TEXT_PRIMARY),
        title_x=0.0,
        height=height,
        margin=dict(t=60, l=0, r=0, b=10),
        coloraxis_showscale=False,
    )
    fig.update_xaxes(tickfont=dict(size=13))
    fig.update_yaxes(tickfont=dict(size=13))
    fig.update_traces(textfont_size=12)
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


def reco(tag: str, color: str, text: str):
    render_html(f"""
    <div class="reco" style="--c:{color};">
        <span class="tag">{tag}</span>
        <span>{text}</span>
    </div>
    """)


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
    background: linear-gradient(135deg, {TEAL}, {ACCENT});
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

/* Cartes génériques */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
    font-size: 15px;
    line-height: 1.6;
}}

/* KPI */
.kpi-row {{ display: grid; gap: 12px; }}
.kpi {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 18px;
}}
.kpi .kpi-label {{ font-size: 15px; color: {TEXT_SECONDARY}; margin-bottom: 8px; }}
.kpi .kpi-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    font-weight: 600;
}}

/* Bandeau défilant (interprétation) */
.ticker-wrapper {{ height: 60px; overflow: hidden; width: 100%; position: relative; }}
.ticker-content {{ display: flex; flex-direction: column; animation: scrollLoop 20s linear infinite; }}
.ticker-line {{
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    color: {AMBER};
}}
@keyframes scrollLoop {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-50%); }}
}}

/* Recommandations */
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
    font-size: 15px;
    color: {TEXT_PRIMARY};
    line-height: 1.5;
}}
.reco .tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--c, {ACCENT});
    white-space: nowrap;
    padding-top: 2px;
}}

.prompt-text {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin-top: 10px;
}}

/* Widgets Streamlit */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
.stButton button, .stDownloadButton button {{
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
}}
.stButton button:hover, .stDownloadButton button:hover {{ opacity: .9; }}

[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {BORDER};
}}
.stSuccess, .stInfo, .stWarning, .stError {{ border-radius: 10px !important; }}
hr {{ border-color: {BORDER} !important; margin: 26px 0 !important; }}

@media (max-width: 900px) {{
    .kpi-row {{ grid-template-columns: repeat(2, 1fr) !important; }}
    .app-header {{ flex-wrap: wrap; gap: 12px; }}
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
        <div class="brand-mark">📊</div>
        <div>
            <div class="brand-name">Analyse Globale des Données Étudiantes</div>
            <div class="brand-sub">Exploration complète des tendances, performances et corrélations académiques</div>
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
    st.error("Aucune donnée disponible.")
    st.stop()

numeric_df = df.select_dtypes(include=['int64', 'float64'])
st.divider()

# =========================
# KPIs
# =========================
section_title("", "Indicateurs clés")

kpi_row([
    ("Moyenne générale", round(df["moyenne"].mean(), 2), TEAL),
    ("Stress moyen", round(df["stress"].mean(), 2), CORAL),
    ("Heures d'étude moyenne", round(df["heures_etude"].mean(), 2), AMBER),
], cols=3)

st.divider()

# =========================
# HISTOGRAMMES (inchangé)
# =========================
section_title("", "Distributions des moyennes")

fig_hist = px.histogram(df, x="moyenne", nbins=20, marginal="box")
st.plotly_chart(style_chart(fig_hist, 460), use_container_width=True)

st.divider()

# =========================
# PIE CHARTS
# =========================
section_title("", "Répartitions")

col1, col2 = st.columns(2)

with col1:
    fig4 = px.pie(
        df,
        names="filiere",
        title="Répartition par filière",
        color_discrete_sequence=CHART_COLORWAY,
    )
    fig4.update_layout(height=500)
    st.plotly_chart(style_chart(fig4, 500), use_container_width=True)

with col2:
    fig5 = px.pie(
        df,
        names="sexe",
        title="Répartition par sexe",
        color_discrete_sequence=[AMBER, TEAL],
        hole=0.6,
    )
    fig5.update_layout(height=500)
    st.plotly_chart(style_chart(fig5, 500), use_container_width=True)

st.divider()

# =========================
# CORRELATION
# =========================
section_title("", "Matrice de corrélation")

corr_matrix = numeric_df.corr()

fig6 = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
st.plotly_chart(style_heatmap(fig6, 750), use_container_width=True)

render_html("""
<div class="ticker-wrapper">
    <div class="ticker-content">
        <div class="ticker-line">Interprétation de la matrice de corrélation</div>
        <div class="ticker-line">Analyse des relations entre variables</div>
        <div class="ticker-line">]0,1] = corrélation positive (les variables évoluent dans le même sens)</div>
        <div class="ticker-line">[-1,0[ = corrélation négative (les variables évoluent en sens contraire)</div>
        <div class="ticker-line">0 = pas de relation entre les variables</div>
        <div class="ticker-line">Interprétation de la matrice de corrélation</div>
        <div class="ticker-line">Analyse des relations entre variables</div>
        <div class="ticker-line">]0,1] = corrélation positive (les variables évoluent dans le même sens)</div>
        <div class="ticker-line">[-1,0[ = corrélation négative (les variables évoluent en sens contraire)</div>
        <div class="ticker-line">0 = pas de relation entre les variables</div>
    </div>
</div>
""")

render_html(f"""
<div class="panel" style="border-left:3px solid {AMBER};">
    <b>Lecture du graphique :</b><br>
    • Les couleurs <b>rouges</b> représentent des corrélations positives<br>
    • Les couleurs <b>bleues</b> représentent des corrélations négatives<br>
    • Plus la couleur est intense, plus la relation est forte<br>
    • La relation entre deux variables est d'autant plus forte lorsque leur corrélation tend vers +1 et plus faible lorsqu'elle tend vers -1<br><br>
    Cette analyse permet de détecter rapidement les variables clés comme le <b>temps d'étude</b>, la <b>motivation</b>, le <b>stress</b> ou la <b>concentration</b>.
</div>
""")

st.divider()

# =========================
# RELATIONS IMPORTANTES
# =========================
section_title("", "Relations clés")

fig7 = px.scatter(
    df, x="heures_etude", y="moyenne", color="heures_etude",
    color_continuous_scale="Purples", title="Étude vs Performance", trendline="ols",
)
fig7.update_traces(marker=dict(size=10, opacity=0.7))
st.plotly_chart(style_chart(fig7, 460), use_container_width=True)

fig8 = px.scatter(
    df, x="stress", y="moyenne", color="stress",
    color_continuous_scale="Oranges", title="Stress vs Performance", trendline="ols",
)
fig8.update_traces(marker=dict(size=10, opacity=0.7))
st.plotly_chart(style_chart(fig8, 460), use_container_width=True)

st.divider()

# =========================
# COMPARAISONS
# =========================
section_title("", "Comparaison des filières")

moyenne_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()
fig1 = px.bar(
    moyenne_filiere, x="filiere", y="moyenne", color="filiere",
    title="Moyenne académique par filière", color_discrete_sequence=px.colors.qualitative.Set3,
)
st.plotly_chart(style_chart(fig1, 460), use_container_width=True)

stress_filiere = df.groupby("filiere")["stress"].mean().reset_index()
fig2 = px.bar(
    stress_filiere, x="filiere", y="stress", color="filiere",
    title="Stress moyen par filière", color_discrete_sequence=px.colors.qualitative.Pastel,
)
st.plotly_chart(style_chart(fig2, 460), use_container_width=True)

study_filiere = df.groupby("filiere")["heures_etude"].mean().reset_index()
fig3 = px.bar(
    study_filiere, x="filiere", y="heures_etude", color="filiere",
    title="Heures d'étude moyennes par filière", color_discrete_sequence=px.colors.qualitative.Bold,
)
st.plotly_chart(style_chart(fig3, 460), use_container_width=True)

st.divider()

# =========================
# BOXPLOT
# =========================
section_title("", "Distribution des notes par filière")

fig9 = px.box(
    df, x="filiere", y="moyenne", color="filiere",
    title="Répartition des moyennes par filière", color_discrete_sequence=px.colors.qualitative.Set2,
)
fig9.update_layout(xaxis_tickangle=45)
st.plotly_chart(style_chart(fig9, 480), use_container_width=True)

st.divider()

# ==========================================================
# TENDANCES
# ==========================================================
section_title("", "Tendances globales")

trend = df.groupby("niveau")["moyenne"].mean().reset_index()
fig_trend = px.line(trend, x="niveau", y="moyenne", markers=True, title="Évolution des performances par niveau")
st.plotly_chart(style_chart(fig_trend, 420), use_container_width=True)

st.divider()

# =========================
# ANALYSE INTELLIGENTE
# =========================
section_title("", "Analyse intelligente")

if st.button("🔍 Visualiser"):

    best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
    worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()

    stress_high = df.groupby("filiere")["stress"].mean().idxmax()
    stress_low = df.groupby("filiere")["stress"].mean().idxmin()

    concentration_high = df.groupby("filiere")["concentration"].mean().idxmax()
    motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()
    regularite_high = df.groupby("filiere")["regularite"].mean().idxmax()

    age_high = None
    if "age" in df.columns:
        age_high = df.groupby("filiere")["age"].mean().idxmax()

    reco("TOP", TEAL, f"Filière la plus performante : {best_filiere}")
    reco("BAS", CORAL, f"Filière la moins performante : {worst_filiere}")
    reco("STRESS+", AMBER, f"Filière la plus stressée : {stress_high}")
    reco("STRESS-", TEAL, f"Filière la moins stressée : {stress_low}")
    reco("FOCUS", TEAL, f"Filière la plus concentrée : {concentration_high}")
    reco("MOTIVATION", TEAL, f"Filière la plus motivée : {motivation_high}")
    reco("RÉGULARITÉ", TEAL, f"Filière la plus régulière : {regularite_high}")

    if age_high:
        reco("ÂGE", ACCENT, f"Filière avec étudiants les plus âgés : {age_high}")

st.divider()

# =========================
# EXPORT CSV + AFFICHAGE DONNÉES
# =========================
section_title("", "Export & Visualisation de données")

col1, col2 = st.columns(2)
csv = df.to_csv(index=False).encode("utf-8")

with col1:
    st.download_button(
        label="📥 Télécharger les données CSV",
        data=csv,
        file_name="donnees_etudiants.csv",
        mime="text/csv",
    )

with col2:
    show_data = st.button("👁️ Voir les données brutes")

if show_data:
    section_title("", "Liste complète des étudiants")
    st.dataframe(df, use_container_width=True)

st.divider()

render_html("""
<div class="prompt-text">🤔 Souhaitez-vous visualiser les statistiques par filière ?</div>
""")

st.markdown("<br>", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "show_stats" not in st.session_state:
    st.session_state.show_stats = False

if st.button("🧮 Statistique par filière"):
    st.session_state.show_stats = True

# ===== AFFICHAGE PERSISTANT =====
if st.session_state.show_stats:

    filiere_selected = st.selectbox(
        " Choisir une filière",
        df["filiere"].dropna().unique()
    )

    df_fil = df[df["filiere"] == filiere_selected]

    # =========================
    # KPI FILIERE
    # =========================
    section_title("", f"Indicateurs de la filière - {filiere_selected}")

    kpi_row([
        ("Moyenne", round(df_fil["moyenne"].mean(), 2), TEAL),
        ("Stress", round(df_fil["stress"].mean(), 2), CORAL),
        ("Heures étude", round(df_fil["heures_etude"].mean(), 2), AMBER),
        ("Total étudiants", len(df_fil), ACCENT),
    ], cols=4)

    st.divider()

    # =========================
    # SEMI-CIRCLE SEXE
    # =========================
    section_title("", f"Analyse de la filière - {filiere_selected}")

    sex_counts = df_fil["sexe"].value_counts().reset_index()
    sex_counts.columns = ["sexe", "count"]

    fig_sex = px.pie(
        sex_counts, names="sexe", values="count", hole=0.5,
        title="Répartition du sexe", color_discrete_sequence=[AMBER, TEAL],
    )
    fig_sex.update_traces(textinfo="percent+label")
    fig_sex.update_layout(
        showlegend=True,
        annotations=[dict(text="Sexe", x=0.5, y=0.5, showarrow=False, font=dict(color=TEXT_PRIMARY))],
        margin=dict(t=40, b=0),
    )
    st.plotly_chart(style_chart(fig_sex, 400), use_container_width=True)

    # =========================
    # MATRICE DE CORRELATION
    # =========================
    numeric_df_fil = df_fil.select_dtypes(include=["int64", "float64"])
    fig_corr = px.imshow(
        numeric_df_fil.corr(), text_auto=".2f",
        color_continuous_scale="RdBu", title="Corrélation des variables", aspect="auto",
    )
    st.plotly_chart(style_heatmap(fig_corr, 700), use_container_width=True)

    st.divider()

    # =========================
    # NUAGES DE POINTS FUSIONNÉS
    # =========================
    section_title("", "Relations clés avec la performance")

    df_long = df_fil.melt(
        id_vars=["moyenne"],
        value_vars=["heures_etude", "concentration", "motivation", "regularite"],
        var_name="Variable", value_name="Valeur",
    )
    labels_map = {
        "heures_etude": "Étude",
        "concentration": "Concentration",
        "motivation": "Motivation",
        "regularite": "Régularité",
    }
    df_long["Variable"] = df_long["Variable"].map(labels_map)

    fig = px.scatter(
        df_long, x="Valeur", y="moyenne", facet_col="Variable", facet_col_wrap=2,
        trendline="ols", color="Variable",
        title="Impact des facteurs clés sur la performance académique",
    )
    fig.update_layout(showlegend=False, margin=dict(t=60, l=30, r=30, b=30))
    st.plotly_chart(style_chart(fig, 620), use_container_width=True)

    # =========================
    # ANALYSE PAR NIVEAU
    # =========================
    niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

    section_title("", "Analyse par niveau dans la filière")

    fig1 = px.bar(
        niveau_group, x="niveau", y="moyenne", color="niveau",
        title=f"Moyenne par niveau — {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(style_chart(fig1, 420), use_container_width=True)

    fig2 = px.bar(
        niveau_group, x="niveau", y="stress", color="niveau",
        title=f"Stress par niveau — {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(style_chart(fig2, 420), use_container_width=True)

    fig3 = px.bar(
        niveau_group, x="niveau", y="heures_etude", color="niveau",
        title=f"Heures d'étude par niveau — {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(style_chart(fig3, 420), use_container_width=True)

    # =========================
    # RÉPARTITION NIVEAU (FILTRÉE)
    # =========================
    fig4 = px.pie(
        df_fil, names="niveau",
        title=f"Répartition des niveaux - {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(style_chart(fig4, 460), use_container_width=True)
