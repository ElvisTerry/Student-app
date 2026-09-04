import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import plotly.graph_objects as go  
import streamlit.components.v1 as components

from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="IA Simulation Pro", layout="wide")



components.html("""
<div style="
    background: linear-gradient(135deg, #ECFEFF, #CFFAFE);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #A5F3FC;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(6,182,212,0.12);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- ICON (Simulation / what-if decision tree) -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#0E7490"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- decision tree / simulation nodes -->
            <circle cx="12" cy="4" r="2"/>
            <circle cx="6" cy="12" r="2"/>
            <circle cx="18" cy="12" r="2"/>
            <circle cx="12" cy="20" r="2"/>

            <!-- connections (scenario branches) -->
            <line x1="12" y1="6" x2="6" y2="10"/>
            <line x1="12" y1="6" x2="18" y2="10"/>
            <line x1="6" y1="14" x2="12" y2="18"/>
            <line x1="18" y1="14" x2="12" y2="18"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#0F172A;
            letter-spacing:-0.4px;
        ">
            Simulation Intelligente (What If Pro)
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#0E7490;
        margin-top:6px;
    ">
        AI Scenario Engine • Predictive Simulation • Decision Modeling
    </div>

</div>
""", height=150)

st.divider()

# =========================
# DATA
# =========================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")
try:
    df = load_data()
except:
    st.error(" Aucune donnée disponible, veuillez remplir le formulaire dans le menu retractable.")
    st.stop()

# =========================
#  TRAIN MODELS PAR FILIERE
# =========================
from sklearn.metrics import mean_absolute_error

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
        # 🔥 prédiction sur dataset (pour MAE)
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

st.markdown("""
 ***Le modèle analyse chaque filiere et prédit en fonction des données collectées et traitées de la filiere de l'étudiant***""")

# =========================
# EXPLICATION PÉDAGOGIQUE
# =========================

st.subheader("📖 Explication du modèle")

st.components.v1.html("""
<style>

/* ===== CONTAINER GLOBAL ===== */
.scroll-wrapper {
    height: 60px;
    overflow: hidden;
    width: 100%;
    position: relative;
}

/* ===== CONTENT ===== */
.scroll-content {
    display: flex;
    flex-direction: column;
    animation: scrollStep 32s infinite;
}

/* ===== LINE ===== */
.line {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    color: #64748B;
    transition: all 0.4s ease;
}

/* ===== ACTIVE LINE ===== */
.line.active {
    font-size: 15px;
    font-weight: 700;
    color:#B22222;
    transform: scale(1.05);
}

/* ===== ANIMATION ===== */
@keyframes scrollStep {

    0%   { transform: translateY(0%); }
    10%  { transform: translateY(0%); }

    12.5% { transform: translateY(-60px); }
    22.5% { transform: translateY(-60px); }

    25%  { transform: translateY(-120px); }
    35%  { transform: translateY(-120px); }

    37.5% { transform: translateY(-180px); }
    47.5% { transform: translateY(-180px); }

    50%  { transform: translateY(-240px); }
    60%  { transform: translateY(-240px); }

    62.5% { transform: translateY(-300px); }
    72.5% { transform: translateY(-300px); }

    75%  { transform: translateY(-360px); }
    85%  { transform: translateY(-360px); }

    87.5% { transform: translateY(-420px); }
    97.5% { transform: translateY(-420px); }

    100% { transform: translateY(0%); }
}

</style>

<div class="scroll-wrapper">
    <div class="scroll-content">

        <div class="line active"> Le modèle analyse et exploite toutes les variables de la filière choisie </div>
        <div class="line"> Ceci étant, les variables exploitées sont entre autres : </div>

        <div class="line">- Habitudes d’étude : heures et régularité</div>

        <div class="line">- Mode de vie : sommeil, téléphone, sport</div>

        <div class="line">- Bien-être : stress, motivation, concentration</div>

        <div class="line">- Profil académique : filière, niveau, sexe, méthode</div>

        <div class="line"> Objectif : </div>

        <div class="line">- prédire la moyenne académique</div> 

        <div class="line">- prédire la réussite ou l’échec</div>


        <div class="line"> Algorithme utilisée : Random Forest (robuste et performant)</div>

    </div>
</div>
""", height=90)
# =========================
# CHOIX FILIERE
# =========================
st.subheader(" Renseigne ton profil")

filiere_input = st.selectbox("📚 Filière", list(models.keys()))
model_data = models[filiere_input]

model = model_data["model"]
features = model_data["features"]
df_fil = model_data["data"]
mae = model_data["mae"]
sexe_input = st.selectbox("👤 Sexe", df_fil["sexe"].unique())
st.divider()
# =========================
# MOYENNE ACTUELLE
# =========================
st.subheader(" Ta situation actuelle")

moyenne_actuelle = st.number_input(
    " Entre ta moyenne actuelle (/20)",
    0.0, 20.0, 10.0
)

# =========================
# INITIALISATION INTELLIGENTE
# =========================
df_fil["diff"] = abs(df_fil["moyenne"] - moyenne_actuelle)
closest = df_fil.sort_values("diff").iloc[0]

# =========================
# INPUT USER
# =========================
st.subheader("🛠️ Adapte à tes nouveaux paramètres d'études")

col1, col2, col3 = st.columns(3)

with col1:
    heures = st.slider("📚 Heures d'étude", 0, 12, int(closest["heures_etude"]))
    sommeil = st.slider("😴 Sommeil", 0, 12, int(closest["sommeil"]))

with col2:
    stress = st.slider("😰 Stress", 1, 10, int(closest["stress"]))
    motivation = st.slider("🔥 Motivation", 1, 10, int(closest["motivation"]))

with col3:
    concentration = st.slider("🧠 Concentration", 1, 10, int(closest["concentration"]))
    telephone = st.slider("📱 Téléphone", 0, 12, int(closest["telephone"]))

# =========================
# FONCTION BUILD INPUT 
# =========================
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

# =========================
# INPUT MODEL
# =========================
input_data = build_input(
    heures, stress, sommeil,
    motivation, concentration, telephone
)

# =========================
# PREDICTION
# =========================
pred = model.predict(input_data)[0]

diff = pred - moyenne_actuelle
percent = (diff / moyenne_actuelle) * 100 if moyenne_actuelle != 0 else 0

# =========================
# RESULTATS
# =========================
st.subheader("🧠 Résultats de simulation")

if st.button("🔍 Voir le résultat"):

    # =========================
    # STYLE KPI CARDS
    # =========================
    st.markdown("""
    <style>

    /* ===== CARD AVEC BORDURE LUMINEUSE ===== */
    .sim-card {
        position: relative;
        background: #1F2937;
        padding: 14px 10px;
        border-radius: 14px;
        text-align: center;
        overflow: hidden;
        transition: 0.3s ease;
    }

    /* 🔥 BORDER GLOW (pseudo-element) */
    .sim-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 14px;
        padding: 1.5px;
        background: linear-gradient(
            135deg,
            #22D3EE,
            #3B82F6,
            #6366F1,
            #22D3EE
        );
        -webkit-mask:
            linear-gradient(#000 0 0) content-box,
            linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }

    /* HOVER EFFECT */
    .sim-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow:
            0 0 15px rgba(34, 211, 238, 0.4),
            0 10px 30px rgba(0,0,0,0.4);
    }

    /* TITRE */
    .sim-title {
        font-size: 12px;
        color: #9CA3AF;
        margin-bottom: 6px;
    }

    /* VALEUR */
    .sim-value {
        font-size: 20px;
        font-weight: 800;
        color: #F9FAFB;
        letter-spacing: -0.3px;
    }

    </style>
    """, unsafe_allow_html=True)
    

    # =========================
    # COULEURS DYNAMIQUES
    # =========================
    pred_color = "#16A34A" if percent >= 0 else "#DC2626"
    current_color = "#EAB308"
    impact_color = "#16A34A" if percent >= 0 else "#DC2626"

    # =========================
    # AFFICHAGE
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="sim-card">
        <div class="sim-title"> Moyenne prédite</div>
        <div class="sim-value" style="color:{pred_color};">
            {round(pred, 2)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="sim-card">
        <div class="sim-title"> Moyenne actuelle</div>
        <div class="sim-value" style="color:{current_color};">
            {round(moyenne_actuelle, 2)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="sim-card">
        <div class="sim-title"> Impact</div>
        <div class="sim-value" style="color:{impact_color};">
            {percent:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader(" Performance du modèle")

    col1, col2 = st.columns(2)

    col1.metric("📉 MAE(Erreur Moyenne)", round(mae, 2))

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
st.subheader("👤 Ton nouveau Profil")

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
    r=[heures, sommeil, 10-stress, motivation, concentration],
    theta=["Étude", "Sommeil", "Anti-stress", "Motivation", "Concentration"],
    fill='toself'
))

st.plotly_chart(radar, use_container_width=True)


st.divider()

# =========================
# RECOMMANDATIONS IA
# =========================

warning = False  # 🔥 AJOUT ICI (IMPORTANT)

if st.button("🚨 Recommandations "):

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
st.subheader(" Diagnostic IA")

if diff > 2:
    st.success(" Très forte amélioration possible")
elif diff > 0:
    st.info(" Amélioration détectée")
elif diff > -2:
    st.warning(" Légère baisse possible")
else:
    st.error(" Forte baisse de performance")

# =========================
# FOOTER
# =========================
st.divider()
