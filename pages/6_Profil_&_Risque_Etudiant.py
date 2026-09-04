import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Profil Étudiant", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #BAE6FD;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(14,165,233,0.12);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 👤 + 🧠 + 📊 ICON (Smart student profile AI) -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#0EA5E9"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- user head -->
            <circle cx="12" cy="7" r="3"/>

            <!-- body -->
            <path d="M5.5 21c0-4 4-6 6.5-6s6.5 2 6.5 6"/>

            <!-- AI nodes / analytics -->
            <circle cx="5" cy="14" r="1"/>
            <circle cx="19" cy="14" r="1"/>
            <circle cx="12" cy="18" r="1"/>

            <!-- connections -->
            <line x1="5" y1="14" x2="12" y2="18"/>
            <line x1="19" y1="14" x2="12" y2="18"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:20px;
            font-weight:800;
            color:#0F172A;
            letter-spacing:-0.4px;
        ">
            Profil Intelligent de l'Étudiant
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#0369A1;
        margin-top:6px;
    ">
        AI-driven Student Profile • Behavioral Analytics • Academic Intelligence
    </div>

</div>
""", height=150)


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
except:
    st.error(" Aucune donnée disponible.")
    st.stop()

# =========================
# FORMULAIRE PROFIL
# =========================
st.subheader(" Entre tes données et mesure ton risque")

col1, col2 = st.columns(2)

with col1:
    heures_etude = st.slider("📚 Heures d'étude/jour", 0, 12, 3)
    sommeil = st.slider("😴 Heures de sommeil", 0, 12, 6)
    stress = st.slider("😰 Stress (1-10)", 1, 10, 5)

with col2:
    motivation = st.slider("🔥 Motivation (1-10)", 1, 10, 5)
    concentration = st.slider("🧠 Concentration (1-10)", 1, 10, 5)
    telephone = st.slider("📱 Temps téléphone (h)", 0, 12, 4)
st.divider()
# =========================
# SCORE DE RISQUE
# =========================
st.subheader(" Résultat d'analyse")

if st.button("⚠️ Voir ton risque"):

    # Normalisation
    stress_n = stress / 10
    sommeil_risk = max(0, (7 - sommeil) / 7)
    etude_risk = max(0, (4 - heures_etude) / 4)
    motivation_risk = (10 - motivation) / 10

    # SCORE GLOBAL
    score_risque = (
        0.35 * stress_n +
        0.25 * sommeil_risk +
        0.25 * etude_risk +
        0.15 * motivation_risk
    )

    # =========================
    # INTERPRÉTATION
    # =========================
    if score_risque < 0.3:
        niveau = "🟢 Faible risque"
        commentaire = "Tu es sur une bonne trajectoire 👍"
        color = "#16A34A"
        bg = "#ECFDF5"

    elif score_risque < 0.6:
        niveau = "🟠 Risque moyen"
        commentaire = "Attention à ton équilibre travail/repos ⚠️"
        color = "#F59E0B"
        bg = "#FFFBEB"

    else:
        niveau = "🔴 Risque élevé"
        commentaire = "Risque de baisse de performance important "
        color = "#DC2626"
        bg = "#FEF2F2"

    # =========================
    # AFFICHAGE
    # =========================
    st.markdown(f"""
    <div style="font-size:14px; color:#64748B;">
         Score de risque académique
    </div>

    <div style="
        font-size:32px;
        font-weight:800;
        color:{color};
        margin:8px 0;
    ">
        {round(score_risque, 2)}
    </div>

    <div style="
        font-size:18px;
        font-weight:700;
        color:{color};
        margin-bottom:6px;
    ">
        {niveau}
    </div>

    <div style="
        font-size:14px;
        color:#3B82F6;
    ">
        {commentaire}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

import plotly.graph_objects as go

st.subheader("📡Ton Profil actuel")

categories = ["Étude", "Sommeil", "Stress", "Motivation"]
values = [
    heures_etude/12,
    sommeil/12,
    stress/10,
    motivation/10
]

# fermer le cercle
categories += [categories[0]]
values += [values[0]]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    line=dict(width=3),
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    showlegend=False,
    margin=dict(l=30, r=30, t=30, b=30)
)

st.plotly_chart(fig, use_container_width=True)
# =========================
# RECOMMANDATIONS AUTOMATIQUES
# =========================

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
