import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components

# ==========================================================
# CONFIGURATION PAGE
# ==========================================================
st.set_page_config(
    page_title="SmartStudent Analytics",
    layout="wide",
    page_icon="🎓",
)

# ==========================================================
# STYLE GLOBAL — THÈME SOMBRE (compatible fond dark de Streamlit)
# ==========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fond global : on garde le dark natif de Streamlit, on ajoute juste
   une légère profondeur avec des halos discrets (plus de fond clair) */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
        radial-gradient(circle at bottom right, rgba(139, 92, 246, 0.10) 0%, transparent 40%),
        #0E1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B0E14, #151923);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #6366F1;
    border-radius: 20px;
}

/* Titres */
h1, h2, h3 {
    color: #F1F5F9 !important;
    font-weight: 800 !important;
}

/* Cards "glass" en version sombre */
.glass-card {
    background: rgba(30, 35, 48, 0.65);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.35);
    color: #E2E8F0;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(30, 35, 48, 0.9), rgba(20, 24, 34, 0.85));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    padding: 24px 18px;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.30);
    border-color: rgba(99, 102, 241, 0.4);
}
.kpi-icon {
    font-size: 28px;
    margin-bottom: 8px;
}
.kpi-number {
    font-size: 30px;
    font-weight: 900;
    color: #F8FAFC;
}
.kpi-label {
    color: #94A3B8;
    font-size: 13px;
}

/* Tableaux */
[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}

/* Alertes Streamlit */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 18px !important;
}

/* Divider */
hr {
    margin-top: 35px !important;
    margin-bottom: 35px !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Texte à l'intérieur des glass-card (titres, paragraphes) */
.glass-card h3, .glass-card h4 {
    color: #F1F5F9 !important;
}
.glass-card p, .glass-card b {
    color: #CBD5E1;
}

</style>
""", unsafe_allow_html=True)


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
# HEADER PREMIUM STYLE LMS
# ==========================================================
components.html("""
<div style="
    background: linear-gradient(135deg, #0F172A, #1E1B4B, #312E81);
    padding: 40px;
    border-radius: 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,.35);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
">
    <div style="
        position: absolute;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,.04);
        border-radius: 50%;
        top: -120px;
        right: -80px;
    "></div>

    <div style="
        position: absolute;
        width: 220px;
        height: 220px;
        background: rgba(99,102,241,.15);
        border-radius: 50%;
        bottom: -100px;
        left: -60px;
    "></div>

    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        position: relative;
        z-index: 10;
    ">
        <div style="font-size: 58px;">🎓</div>

        <div>
            <div style="
                font-size: 34px;
                font-weight: 900;
                color: white;
                letter-spacing: -1px;
            ">
                SmartStudent Analytics
            </div>

            <div style="
                margin-top: 8px;
                font-size: 15px;
                color: #CBD5E1;
            ">
                Plateforme intelligente d'analyse des performances académiques
                basée sur la Data Science et l'Intelligence Artificielle
            </div>

            <div style="
                margin-top: 18px;
                display: inline-block;
                padding: 8px 18px;
                border-radius: 999px;
                background: rgba(99,102,241,.18);
                color: #C7D2FE;
                font-size: 13px;
                border: 1px solid rgba(255,255,255,.12);
            ">
                AI • Machine Learning • Predictive Analytics
            </div>
        </div>
    </div>
</div>
""", height=230)

st.divider()


# ==========================================================
# OBJECTIFS
# ==========================================================
st.markdown("## 🧭 Objectifs du projet")

st.components.v1.html("""
<style>
.container {
    position: relative;
    height: 120px;
}
.objective {
    position: absolute;
    width: 100%;
    opacity: 0;
    transition: .8s;
    transform: translateY(12px);
    padding: 20px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(30,35,48,.92), rgba(20,24,34,.88));
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 10px 30px rgba(0,0,0,.35);
}
.objective.active {
    opacity: 1;
    transform: translateY(0);
}
.title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
}
.desc {
    color: #94A3B8;
    font-size: 14px;
}
</style>

<div class="container">
    <div class="objective active">
        <div class="title" style="color:#60A5FA;">📥 Collecte intelligente des données</div>
        <div class="desc">Centralisation et structuration des informations étudiantes.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#4ADE80;">📈 Analyse comportementale</div>
        <div class="desc">Étude des performances et des habitudes académiques.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#C084FC;">🧠 Identification des facteurs de réussite</div>
        <div class="desc">Détection automatique des variables influentes.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#F87171;">🤖 Prédiction des performances</div>
        <div class="desc">Utilisation de modèles IA pour anticiper les résultats.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#FB923C;">📑 Rapports intelligents</div>
        <div class="desc">Génération d'insights décisionnels automatisés.</div>
    </div>
</div>

<script>
let index = 0;
const items = document.querySelectorAll(".objective");
setInterval(() => {
    items[index].classList.remove("active");
    index = (index + 1) % items.length;
    items[index].classList.add("active");
}, 3000);
</script>
""", height=140)

st.divider()


# ==========================================================
# KPI CARDS
# ==========================================================
st.markdown("## 🌍 Indicateurs globaux")

nb_etudiants = len(df)
moyenne_gen = round(df["moyenne"].mean(), 2)
stress_moy = round(df["stress"].mean(), 2)
heures_moy = round(df["heures_etude"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">👨‍🎓</div>
        <div class="kpi-number">{nb_etudiants}</div>
        <div class="kpi-label">Étudiants enregistrés</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎓</div>
        <div class="kpi-number">{moyenne_gen}</div>
        <div class="kpi-label">Moyenne générale</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">😰</div>
        <div class="kpi-number">{stress_moy}</div>
        <div class="kpi-label">Stress moyen</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📚</div>
        <div class="kpi-number">{heures_moy}</div>
        <div class="kpi-label">Heures d'étude moyennes</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================================
# INSIGHTS INTELLIGENTS
# ==========================================================
st.markdown("## 🧠 Insights automatiques")

best = df.groupby("filiere")["moyenne"].mean().idxmax()
worst = df.groupby("filiere")["moyenne"].mean().idxmin()
stress_high = df.groupby("filiere")["stress"].mean().idxmax()
study_high = df.groupby("filiere")["heures_etude"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()

col1, col2, col3 = st.columns(3)
with col1:
    st.success(f"🏆 Meilleure filière : **{best}**")
with col2:
    st.error(f"📉 Filière la moins performante : **{worst}**")
with col3:
    st.info(f"🏫 Nombre total de filières : **{df['filiere'].nunique()}**")

st.markdown("")

col1, col2, col3 = st.columns(3)
with col1:
    st.warning(f"😰 Filière la plus stressée : **{stress_high}**")
with col2:
    st.info(f"📚 Filière la plus travailleuse : **{study_high}**")
with col3:
    st.success(f"🔥 Filière la plus motivée : **{motivation_high}**")

st.divider()


# ==========================================================
# PERFORMANCE GLOBALE
# ==========================================================
st.markdown("## 📈 Performance académique globale")

pass_rate = (df["moyenne"] >= 10).mean() * 100
fail_rate = 100 - pass_rate

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:18px; color:#94A3B8; font-weight:600;">
            🎯 Taux de réussite
        </div>
        <div style="font-size:42px; color:#4ADE80; font-weight:900; margin-top:10px;">
            {pass_rate:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:18px; color:#94A3B8; font-weight:600;">
            ⚠️ Taux d'échec
        </div>
        <div style="font-size:42px; color:#F87171; font-weight:900; margin-top:10px;">
            {fail_rate:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================================
# TOP ÉTUDIANTS
# ==========================================================
st.markdown("## 🏆 Top 10 des étudiants")

top_students = df.sort_values("moyenne", ascending=False).head(10)

st.markdown("""
<div class="glass-card">
    <h4 style="margin-top:0;">🌟 Excellence académique</h4>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    top_students[[
        "nom", "age", "sexe", "filiere", "niveau", "heures_etude",
        "methode", "regularite", "sommeil", "sport", "telephone",
        "stress", "concentration", "motivation", "moyenne", "credits",
    ]],
    use_container_width=True,
    height=420,
)

st.divider()


# ==========================================================
# DISTRIBUTION DES MOYENNES
# ==========================================================
st.markdown("## 📊 Distribution des performances")

fig_distribution = px.histogram(
    df,
    x="moyenne",
    nbins=20,
    title="Répartition des moyennes étudiantes",
    marginal="box",
)
fig_distribution.update_layout(template="plotly_dark", title_x=0.5, height=500)
st.plotly_chart(fig_distribution, use_container_width=True)

st.divider()


# ==========================================================
# PERFORMANCE PAR FILIÈRE
# ==========================================================
st.markdown("## 🏫 Performance moyenne par filière")

mean_by_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()

fig_filiere = px.bar(
    mean_by_filiere,
    x="filiere",
    y="moyenne",
    title="Moyenne académique selon la filière",
    text_auto=".2f",
)
fig_filiere.update_layout(template="plotly_dark", title_x=0.5, height=500)
st.plotly_chart(fig_filiere, use_container_width=True)

st.divider()


# ==========================================================
# FACTEURS D'IMPACT
# ==========================================================
st.markdown("## 📈 Facteurs influençant la réussite")

correlation = df.select_dtypes(include="number").corr()["moyenne"].sort_values()

fig_corr = px.bar(correlation, title="Corrélation des variables avec la moyenne")
fig_corr.update_layout(template="plotly_dark", title_x=0.5, height=600)
st.plotly_chart(fig_corr, use_container_width=True)

st.divider()


# ==========================================================
# HEURES D'ÉTUDE VS MOYENNE
# ==========================================================
st.markdown("## 📚 Relation entre étude et performance")

fig_scatter = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="filiere",
    size="motivation",
    hover_name="nom",
    title="Heures d'étude et moyenne académique",
)
fig_scatter.update_layout(template="plotly_dark", title_x=0.5, height=600)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()


# ==========================================================
# STRESS VS PERFORMANCE
# ==========================================================
st.markdown("## 😰 Impact du stress sur les résultats")

fig_stress = px.box(df, x="stress", y="moyenne", title="Influence du niveau de stress")
fig_stress.update_layout(template="plotly_dark", title_x=0.5, height=550)
st.plotly_chart(fig_stress, use_container_width=True)

st.divider()


# ==========================================================
# PROFIL ÉTUDIANT IDÉAL
# ==========================================================
st.markdown("## 🌟 Profil étudiant idéal")

best_student = df.sort_values("moyenne", ascending=False).iloc[0]

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:60px;">🏆</div>
        <div style="font-size:24px; font-weight:900; color:#4ADE80;">
            {best_student['moyenne']:.2f}/20
        </div>
        <div style="color:#94A3B8; margin-top:8px;">
            Meilleure moyenne observée
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="margin-top:0;">👨‍🎓 {best_student['nom']}</h3>
        <hr>
        <p><b>📚 Heures d'étude :</b> {best_student['heures_etude']} h/jour</p>
        <p><b>🔥 Motivation :</b> {best_student['motivation']}/10</p>
        <p><b>🧠 Concentration :</b> {best_student['concentration']}/10</p>
        <p><b>😴 Sommeil :</b> {best_student['sommeil']} heures</p>
        <p><b>🏃 Activité sportive :</b> {best_student['sport']}</p>
        <p><b>🎯 Régularité :</b> {best_student['regularite']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================================
# RECOMMANDATIONS IA
# ==========================================================
st.markdown("## 🤖 Assistant d'aide à la décision")

recommandations = []

if df["stress"].mean() > 6:
    recommandations.append((
        "⚠️", "#F87171",
        "Le niveau de stress global est élevé. "
        "Il est conseillé de renforcer l'accompagnement psychologique.",
    ))

if df["heures_etude"].mean() < 3:
    recommandations.append((
        "📚", "#FB923C",
        "Le temps moyen d'étude reste insuffisant. "
        "Des séances de tutorat pourraient être envisagées.",
    ))

if df["motivation"].mean() > 7:
    recommandations.append((
        "🔥", "#4ADE80",
        "La motivation générale est excellente et constitue "
        "un levier important de réussite.",
    ))

if df["sommeil"].mean() < 6:
    recommandations.append((
        "😴", "#A78BFA",
        "Le temps de sommeil moyen semble faible. "
        "Une meilleure hygiène de vie pourrait améliorer les performances.",
    ))

for icon, color, text in recommandations:
    st.markdown(f"""
    <div class="glass-card" style="border-left:6px solid {color}; margin-bottom:15px;">
        <div style="font-size:16px; color:#E2E8F0; font-weight:600;">
            {icon} {text}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================================
# PLAN D'ACTION
# ==========================================================
st.markdown("## 🚀 Plan d'amélioration recommandé")

actions = [
    "📚 Augmenter le temps moyen consacré aux études.",
    "🧠 Développer des stratégies de gestion du stress.",
    "🎯 Renforcer la régularité académique.",
    "😴 Encourager un meilleur équilibre sommeil/travail.",
    "🏃 Favoriser les activités physiques et sportives.",
]

for action in actions:
    st.markdown(f"""
    <div style="
        background: rgba(30,35,48,.75);
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,.08);
        box-shadow: 0 4px 12px rgba(0,0,0,.25);
        color: #E2E8F0;
    ">
        {action}
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================================
# STATISTIQUES COMPLÉMENTAIRES
# ==========================================================
st.markdown("## 📋 Résumé global")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Âge moyen", f"{df['age'].mean():.1f} ans")

with col2:
    st.metric("Crédits moyens", f"{df['credits'].mean():.1f}")

with col3:
    st.metric("Motivation moyenne", f"{df['motivation'].mean():.1f}/10")

st.divider()


# ==========================================================
# FOOTER PREMIUM STYLE LMS
# ==========================================================
components.html("""
<div style="
    margin-top: 40px;
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #0B0E14, #151923);
    color: white;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0,0,0,.35);
    border: 1px solid rgba(255,255,255,.08);
">
    <div style="font-size:24px; font-weight:900; margin-bottom:10px;">
        🎓 SmartStudent Analytics
    </div>

    <div style="color:#94A3B8; font-size:14px; max-width:700px; margin:auto; line-height:1.8;">
        Plateforme intelligente d'analyse des performances académiques
        basée sur la Data Science, la visualisation interactive et
        l'intelligence artificielle prédictive.
    </div>

    <div style="
        margin-top: 18px;
        display: inline-block;
        padding: 8px 18px;
        border-radius: 999px;
        background: rgba(99,102,241,.18);
        border: 1px solid rgba(255,255,255,.12);
        color: #C7D2FE;
    ">
        AI • Data Science • Machine Learning • Analytics
    </div>
</div>
""", height=220)

st.info(
    "⬅️ Utilisez le menu latéral pour remplir le formulaire "
    "et naviguer dans l'application."
)
