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
    page_icon="🎓"
)

# ==========================================================
# STYLE GLOBAL (STYLE LMS MODERNE)
# ==========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background global */
.stApp{
    background:
        radial-gradient(circle at top left,#312E81 0%,transparent 35%),
        radial-gradient(circle at bottom right,#0F172A 0%,transparent 35%),
        linear-gradient(135deg,#F8FAFC,#EEF2FF);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#6366F1;
    border-radius:20px;
}

/* TITRES */
h1,h2,h3{
    color:#0F172A !important;
    font-weight:800 !important;
}

/* Cards modernes */
.glass-card{
    background:rgba(255,255,255,0.82);
    backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.5);
    border-radius:24px;
    padding:22px;
    box-shadow:
        0 10px 35px rgba(15,23,42,.08);
}

/* KPI */
.kpi-card{
    background:linear-gradient(
        135deg,
        rgba(255,255,255,.95),
        rgba(248,250,252,.85)
    );

    border:1px solid rgba(226,232,240,.9);

    border-radius:22px;

    padding:24px 18px;

    text-align:center;

    transition:.3s;

    box-shadow:
        0 8px 30px rgba(15,23,42,.06);
}

.kpi-card:hover{
    transform:translateY(-6px);
    box-shadow:
        0 15px 40px rgba(99,102,241,.18);
}

.kpi-icon{
    font-size:28px;
    margin-bottom:8px;
}

.kpi-number{
    font-size:30px;
    font-weight:900;
    color:#111827;
}

.kpi-label{
    color:#64748B;
    font-size:13px;
}

/* Table */
[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
    border:1px solid #E2E8F0;
    box-shadow:0 10px 30px rgba(0,0,0,.05);
}

/* Alertes */
.stSuccess,
.stInfo,
.stWarning,
.stError{
    border-radius:18px !important;
}

/* Divider */
hr{
    margin-top:35px !important;
    margin-bottom:35px !important;
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
background:
linear-gradient(
135deg,
#0F172A,
#1E1B4B,
#312E81
);

padding:40px;

border-radius:30px;

box-shadow:
0 20px 50px rgba(0,0,0,.25);

position:relative;

overflow:hidden;

border:1px solid rgba(255,255,255,.08);
">

<div style="
position:absolute;
width:300px;
height:300px;
background:rgba(255,255,255,.04);
border-radius:50%;
top:-120px;
right:-80px;
"></div>

<div style="
position:absolute;
width:220px;
height:220px;
background:rgba(99,102,241,.15);
border-radius:50%;
bottom:-100px;
left:-60px;
"></div>

<div style="
display:flex;
align-items:center;
justify-content:center;
gap:20px;
position:relative;
z-index:10;
">

<div style="
font-size:58px;
">
🎓
</div>

<div>

<div style="
font-size:34px;
font-weight:900;
color:white;
letter-spacing:-1px;
">
SmartStudent Analytics
</div>

<div style="
margin-top:8px;
font-size:15px;
color:#CBD5E1;
">
Plateforme intelligente d'analyse des performances académiques
basée sur la Data Science et l'Intelligence Artificielle
</div>

<div style="
margin-top:18px;
display:inline-block;
padding:8px 18px;
border-radius:999px;
background:rgba(99,102,241,.18);
color:#C7D2FE;
font-size:13px;
border:1px solid rgba(255,255,255,.12);
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

.container{
    position:relative;
    height:120px;
}

.objective{

    position:absolute;

    width:100%;

    opacity:0;

    transition:.8s;

    transform:translateY(12px);

    padding:20px;

    border-radius:20px;

    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,.95),
        rgba(248,250,252,.92)
    );

    border:1px solid #E2E8F0;

    box-shadow:
    0 10px 30px rgba(15,23,42,.08);

}

.objective.active{
    opacity:1;
    transform:translateY(0);
}

.title{
    font-size:20px;
    font-weight:800;
    margin-bottom:8px;
}

.desc{
    color:#475569;
    font-size:14px;
}

</style>

<div class="container">

<div class="objective active">
<div class="title" style="color:#2563EB;">
📥 Collecte intelligente des données
</div>

<div class="desc">
Centralisation et structuration des informations étudiantes.
</div>
</div>


<div class="objective">
<div class="title" style="color:#16A34A;">
📈 Analyse comportementale
</div>

<div class="desc">
Étude des performances et des habitudes académiques.
</div>
</div>


<div class="objective">
<div class="title" style="color:#9333EA;">
🧠 Identification des facteurs de réussite
</div>

<div class="desc">
Détection automatique des variables influentes.
</div>
</div>


<div class="objective">
<div class="title" style="color:#DC2626;">
🤖 Prédiction des performances
</div>

<div class="desc">
Utilisation de modèles IA pour anticiper les résultats.
</div>
</div>


<div class="objective">
<div class="title" style="color:#EA580C;">
📑 Rapports intelligents
</div>

<div class="desc">
Génération d'insights décisionnels automatisés.
</div>
</div>

</div>

<script>

let index = 0;

const items =
document.querySelectorAll(".objective");

setInterval(()=>{

items[index].classList.remove("active");

index =
(index + 1) % items.length;

items[index].classList.add("active");

},3000);

</script>

""", height=140)

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================
st.markdown("## 🌍 Indicateurs globaux")

nb_etudiants = len(df)

moyenne_gen = round(
    df['moyenne'].mean(),2
)

stress_moy = round(
    df['stress'].mean(),2
)

heures_moy = round(
    df['heures_etude'].mean(),2
)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">👨‍🎓</div>

        <div class="kpi-number">
        {nb_etudiants}
        </div>

        <div class="kpi-label">
        Étudiants enregistrés
        </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">🎓</div>

        <div class="kpi-number">
        {moyenne_gen}
        </div>

        <div class="kpi-label">
        Moyenne générale
        </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">😰</div>

        <div class="kpi-number">
        {stress_moy}
        </div>

        <div class="kpi-label">
        Stress moyen
        </div>

    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">📚</div>

        <div class="kpi-number">
        {heures_moy}
        </div>

        <div class="kpi-label">
        Heures d'étude moyennes
        </div>

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

        <div style="
        font-size:18px;
        color:#475569;
        font-weight:600;
        ">
        🎯 Taux de réussite
        </div>

        <div style="
        font-size:42px;
        color:#16A34A;
        font-weight:900;
        margin-top:10px;
        ">
        {pass_rate:.1f}%
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">

        <div style="
        font-size:18px;
        color:#475569;
        font-weight:600;
        ">
        ⚠️ Taux d'échec
        </div>

        <div style="
        font-size:42px;
        color:#DC2626;
        font-weight:900;
        margin-top:10px;
        ">
        {fail_rate:.1f}%
        </div>

    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================================
# TOP ETUDIANTS
# ==========================================================
st.markdown("## 🏆 Top 10 des étudiants")

top_students = (
    df
    .sort_values("moyenne", ascending=False)
    .head(10)
)

st.markdown("""
<div class="glass-card">
<h4 style="
margin-top:0;
color:#0F172A;
font-weight:800;
">
🌟 Excellence académique
</h4>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    top_students[
        [
            "nom",
            "age",
            "sexe",
            "filiere",
            "niveau",
            "heures_etude",
            "methode",
            "regularite",
            "sommeil",
            "sport",
            "telephone",
            "stress",
            "concentration",
            "motivation",
            "moyenne",
            "credits"
        ]
    ],
    use_container_width=True,
    height=420
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
    marginal="box"
)

fig_distribution.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)

st.divider()

# ==========================================================
# PERFORMANCE PAR FILIERE
# ==========================================================
st.markdown("## 🏫 Performance moyenne par filière")

mean_by_filiere = (
    df
    .groupby("filiere")["moyenne"]
    .mean()
    .reset_index()
)

fig_filiere = px.bar(
    mean_by_filiere,
    x="filiere",
    y="moyenne",
    title="Moyenne académique selon la filière",
    text_auto=".2f"
)

fig_filiere.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(
    fig_filiere,
    use_container_width=True
)

st.divider()

# ==========================================================
# FACTEURS D'IMPACT
# ==========================================================
st.markdown("## 📈 Facteurs influençant la réussite")

correlation = (
    df
    .select_dtypes(include="number")
    .corr()["moyenne"]
    .sort_values()
)

fig_corr = px.bar(
    correlation,
    title="Corrélation des variables avec la moyenne"
)

fig_corr.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=600
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

st.divider()

# ==========================================================
# HEURES D'ETUDE VS MOYENNE
# ==========================================================
st.markdown("## 📚 Relation entre étude et performance")

fig_scatter = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="filiere",
    size="motivation",
    hover_name="nom",
    title="Heures d'étude et moyenne académique"
)

fig_scatter.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=600
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.divider()

# ==========================================================
# STRESS VS PERFORMANCE
# ==========================================================
st.markdown("## 😰 Impact du stress sur les résultats")

fig_stress = px.box(
    df,
    x="stress",
    y="moyenne",
    title="Influence du niveau de stress"
)

fig_stress.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=550
)

st.plotly_chart(
    fig_stress,
    use_container_width=True
)

st.divider()
# ==========================================================
# PROFIL ETUDIANT IDEAL
# ==========================================================
st.markdown("## 🌟 Profil étudiant idéal")

best_student = (
    df
    .sort_values("moyenne", ascending=False)
    .iloc[0]
)

col1, col2 = st.columns([1, 2])

with col1:

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">

        <div style="font-size:60px;">🏆</div>

        <div style="
        font-size:24px;
        font-weight:900;
        color:#16A34A;
        ">
        {best_student['moyenne']:.2f}/20
        </div>

        <div style="
        color:#64748B;
        margin-top:8px;
        ">
        Meilleure moyenne observée
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="glass-card">

    <h3 style="
    margin-top:0;
    color:#0F172A;
    ">
    👨‍🎓 {best_student['nom']}
    </h3>

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
    recommandations.append(
        (
            "⚠️",
            "#DC2626",
            "Le niveau de stress global est élevé. "
            "Il est conseillé de renforcer l'accompagnement psychologique."
        )
    )

if df["heures_etude"].mean() < 3:
    recommandations.append(
        (
            "📚",
            "#EA580C",
            "Le temps moyen d'étude reste insuffisant. "
            "Des séances de tutorat pourraient être envisagées."
        )
    )

if df["motivation"].mean() > 7:
    recommandations.append(
        (
            "🔥",
            "#16A34A",
            "La motivation générale est excellente et constitue "
            "un levier important de réussite."
        )
    )

if df["sommeil"].mean() < 6:
    recommandations.append(
        (
            "😴",
            "#7C3AED",
            "Le temps de sommeil moyen semble faible. "
            "Une meilleure hygiène de vie pourrait améliorer les performances."
        )
    )

for icon, color, text in recommandations:

    st.markdown(f"""
    <div class="glass-card"
         style="
         border-left:6px solid {color};
         margin-bottom:15px;
         ">

         <div style="
         font-size:16px;
         color:#1E293B;
         font-weight:600;
         ">

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
    background:white;
    border-radius:16px;
    padding:14px 18px;
    margin-bottom:10px;
    border:1px solid #E2E8F0;
    box-shadow:0 4px 12px rgba(0,0,0,.04);
    ">
        {action}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================================
# STATISTIQUES COMPLEMENTAIRES
# ==========================================================
st.markdown("## 📋 Résumé global")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Âge moyen",
        f"{df['age'].mean():.1f} ans"
    )

with col2:

    st.metric(
        "Crédits moyens",
        f"{df['credits'].mean():.1f}"
    )

with col3:

    st.metric(
        "Motivation moyenne",
        f"{df['motivation'].mean():.1f}/10"
    )

st.divider()

# ==========================================================
# FOOTER PREMIUM STYLE LMS
# ==========================================================
components.html("""

<div style="
margin-top:40px;

padding:30px;

border-radius:24px;

background:
linear-gradient(
135deg,
#0F172A,
#1E293B
);

color:white;

text-align:center;

box-shadow:
0 15px 40px rgba(0,0,0,.25);
">

<div style="
font-size:24px;
font-weight:900;
margin-bottom:10px;
">
🎓 SmartStudent Analytics
</div>

<div style="
color:#CBD5E1;
font-size:14px;
max-width:700px;
margin:auto;
line-height:1.8;
">

Plateforme intelligente d'analyse des performances académiques
basée sur la Data Science, la visualisation interactive et
l'intelligence artificielle prédictive.

</div>

<div style="
margin-top:18px;

display:inline-block;

padding:8px 18px;

border-radius:999px;

background:
rgba(99,102,241,.18);

border:
1px solid rgba(255,255,255,.12);

color:#C7D2FE;
">

AI • Data Science • Machine Learning • Analytics

</div>

</div>

""", height=220)

st.info(
    "⬅️ Utilisez le menu latéral pour remplir le formulaire "
    "et naviguer dans l'application."
)