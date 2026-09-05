import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

st.set_page_config(page_title="IA Simulation Pro", layout="wide")

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


def style_polar(fig, height=460):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=TEXT_SECONDARY, size=13),
        height=height,
        margin=dict(l=30, r=30, t=30, b=30),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(gridcolor=BORDER, linecolor=BORDER, color=TEXT_SECONDARY),
            angularaxis=dict(gridcolor=BORDER, linecolor=BORDER, color=TEXT_PRIMARY),
        ),
        showlegend=False,
    )
    fig.update_traces(line_color=ACCENT, fillcolor="rgba(108,142,245,0.25)")
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

/* Panel générique */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
    font-size: 16px;
}}

/* Bandeau défilant pas-à-pas (explication du modèle) */
.step-wrapper {{ height: 60px; overflow: hidden; width: 100%; position: relative; }}
.step-content {{ display: flex; flex-direction: column; animation: stepScroll 32s infinite; }}
.step-line {{
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    color: {TEXT_SECONDARY};
    transition: all .4s ease;
}}
.step-line.active {{
    font-size: 15px;
    font-weight: 700;
    color: {ACCENT};
    transform: scale(1.05);
}}
@keyframes stepScroll {{
    0% {{ transform: translateY(0%); }}
    10% {{ transform: translateY(0%); }}
    12.5% {{ transform: translateY(-60px); }}
    22.5% {{ transform: translateY(-60px); }}
    25% {{ transform: translateY(-120px); }}
    35% {{ transform: translateY(-120px); }}
    37.5% {{ transform: translateY(-180px); }}
    47.5% {{ transform: translateY(-180px); }}
    50% {{ transform: translateY(-240px); }}
    60% {{ transform: translateY(-240px); }}
    62.5% {{ transform: translateY(-300px); }}
    72.5% {{ transform: translateY(-300px); }}
    75% {{ transform: translateY(-360px); }}
    85% {{ transform: translateY(-360px); }}
    87.5% {{ transform: translateY(-420px); }}
    97.5% {{ transform: translateY(-420px); }}
    100% {{ transform: translateY(0%); }}
}}

/* Cartes de résultat de simulation */
.sim-card {{
    position: relative;
    background: {SURFACE};
    border: 1px solid {BORDER};
    padding: 16px 12px;
    border-radius: 14px;
    text-align: center;
}}
.sim-title {{ font-size: 13px; color: {TEXT_SECONDARY}; margin-bottom: 8px; }}
.sim-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}

/* Widgets */
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
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
        <div class="brand-mark">🤖</div>
        <div>
            <div class="brand-name">Simulation Intelligente (What If Pro)</div>
            <div class="brand-sub">AI Scenario Engine • Predictive Simulation • Decision Modeling</div>
        </div>
    </div>
</div>
""")

st.divider()

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
# TRAIN MODELS PAR FILIERE
# =========================
@st.cache_resource
def train_models(df):

    models = {}

    for filiere in df["filiere"].dropna().unique():

        df_fil = df[df["filiere"] == filiere].copy()

        if len(df_fil) < 5:
            continue

        df_enc = pd.get_dummies(df_fil, columns=["sexe"], drop_first=True)

        features = [
            "heures_etude", "stress", "sommeil",
            "motivation", "concentration", "telephone"
        ] + [col for col in df_enc.columns if col.startswith("sexe_")]

        X = df_enc[features]
        y = df_enc["moyenne"]

        model = RandomForestRegressor(
            n_estimators=120,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X, y)
        y_pred = model.predict(X)
        mae = mean_absolute_error(y, y_pred)

        models[filiere] = {
            "model": model,
            "features": features,
            "data": df_fil,
            "mae": mae
        }

    return models


models = train_models(df)

render_html("""
<div class="panel">
    <i>Le modèle analyse chaque filière et prédit en fonction des données collectées et traitées de la filière de l'étudiant.</i>
</div>
""")

# =========================
# EXPLICATION PÉDAGOGIQUE
# =========================
section_title("", "Explication du modèle")

render_html("""
<div class="step-wrapper">
    <div class="step-content">
        <div class="step-line active">Le modèle analyse et exploite toutes les variables de la filière choisie</div>
        <div class="step-line">Ceci étant, les variables exploitées sont entre autres :</div>
        <div class="step-line">— Habitudes d'étude : heures et régularité</div>
        <div class="step-line">— Mode de vie : sommeil, téléphone, sport</div>
        <div class="step-line">— Bien-être : stress, motivation, concentration</div>
        <div class="step-line">— Profil académique : filière, niveau, sexe, méthode</div>
        <div class="step-line">Objectif :</div>
        <div class="step-line">— prédire la moyenne académique</div>
        <div class="step-line">— prédire la réussite ou l'échec</div>
        <div class="step-line">Algorithme utilisé : Random Forest (robuste et performant)</div>
    </div>
</div>
""")

# =========================
# CHOIX FILIERE
# =========================
section_title("", "Renseigne ton profil")

filiere_input = st.selectbox("Filière", list(models.keys()))
model_data = models[filiere_input]

model = model_data["model"]
features = model_data["features"]
df_fil = model_data["data"]
mae = model_data["mae"]
sexe_input = st.selectbox("Sexe", df_fil["sexe"].unique())

st.divider()

# =========================
# MOYENNE ACTUELLE
# =========================
section_title("", "Ta situation actuelle")

moyenne_actuelle = st.number_input("Entre ta moyenne actuelle (/20)", 0.0, 20.0, 10.0)

# =========================
# INITIALISATION INTELLIGENTE
# =========================
df_fil["diff"] = abs(df_fil["moyenne"] - moyenne_actuelle)
closest = df_fil.sort_values("diff").iloc[0]

# =========================
# INPUT USER
# =========================
section_title("", "Adapte à tes nouveaux paramètres d'études")

col1, col2, col3 = st.columns(3)

with col1:
    heures = st.slider("Heures d'étude", 0, 12, int(closest["heures_etude"]))
    sommeil = st.slider("Sommeil", 0, 12, int(closest["sommeil"]))

with col2:
    stress = st.slider("Stress", 1, 10, int(closest["stress"]))
    motivation = st.slider("Motivation", 1, 10, int(closest["motivation"]))

with col3:
    concentration = st.slider("Concentration", 1, 10, int(closest["concentration"]))
    telephone = st.slider("Téléphone", 0, 12, int(closest["telephone"]))


def build_input(h, s, sl, m, c, t):
    d = {
        "heures_etude": h,
        "stress": s,
        "sommeil": sl,
        "motivation": m,
        "concentration": c,
        "telephone": t
    }
    for col in features:
        if col.startswith("sexe_"):
            d[col] = 1 if col == f"sexe_{sexe_input}" else 0
    return pd.DataFrame([d])


input_data = build_input(heures, stress, sommeil, motivation, concentration, telephone)

pred = model.predict(input_data)[0]
diff = pred - moyenne_actuelle
percent = (diff / moyenne_actuelle) * 100 if moyenne_actuelle != 0 else 0

# =========================
# RESULTATS
# =========================
section_title("", "Résultats de simulation")

if st.button("🔍 Voir le résultat"):

    pred_color = TEAL if percent >= 0 else CORAL
    current_color = AMBER
    impact_color = TEAL if percent >= 0 else CORAL

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="sim-card">
        <div class="sim-title">Moyenne prédite</div>
        <div class="sim-value" style="color:{pred_color};">{round(pred, 2)}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="sim-card">
        <div class="sim-title">Moyenne actuelle</div>
        <div class="sim-value" style="color:{current_color};">{round(moyenne_actuelle, 2)}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="sim-card">
        <div class="sim-title">Impact</div>
        <div class="sim-value" style="color:{impact_color};">{percent:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    section_title("", "Performance du modèle")

    col1, col2 = st.columns(2)
    col1.metric("MAE (Erreur Moyenne)", round(mae, 2))

    if mae < 1.5:
        col2.success("Modèle très précis")
    elif mae < 3:
        col2.warning("Précision moyenne")
    else:
        col2.error("Modèle peu fiable")

st.divider()

# =========================
# RADAR CHART
# =========================
section_title("", "Ton nouveau profil")

radar = go.Figure()
radar.add_trace(go.Scatterpolar(
    r=[heures, sommeil, 10 - stress, motivation, concentration],
    theta=["Étude", "Sommeil", "Anti-stress", "Motivation", "Concentration"],
    fill='toself'
))
st.plotly_chart(style_polar(radar, 460), use_container_width=True)

st.divider()

# =========================
# RECOMMANDATIONS IA
# =========================
section_title("", "Recommandations")

warning = False

if st.button("🚨 Recommandations"):

    if heures < 4:
        st.warning("📚 Augmente ton temps d'étude")
        warning = True

    if stress > 6:
        st.warning("😰 Réduis ton stress")
        warning = True

    if sommeil < 6:
        st.warning("😴 Dors plus")
        warning = True

    if motivation < 5:
        st.warning("🔥 Travaille ta motivation")
        warning = True

    if concentration < 5:
        st.warning("🧠 Améliore ta concentration")
        warning = True

    if telephone > 6:
        st.warning("📱 Réduis le téléphone")
        warning = True

    if not warning:
        st.success("👏 Bravo, continue dans ta lancée !")

# =========================
# DIAGNOSTIC IA
# =========================
section_title("", "Diagnostic IA")

if diff > 2:
    st.success("Très forte amélioration possible")
elif diff > 0:
    st.info("Amélioration détectée")
elif diff > -2:
    st.warning("Légère baisse possible")
else:
    st.error("Forte baisse de performance")

st.divider()
