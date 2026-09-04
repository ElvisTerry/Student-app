import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Étudiants", layout="wide")



components.html("""
<div style="
    background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #DDD6FE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(139,92,246,0.12);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🧬 + 🔗 ICON (Clustering / ML segmentation) -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#6D28D9"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- cluster nodes -->
            <circle cx="6" cy="7" r="2"/>
            <circle cx="18" cy="7" r="2"/>
            <circle cx="12" cy="18" r="2"/>
            <circle cx="12" cy="11" r="2"/>

            <!-- connections -->
            <line x1="6" y1="7" x2="12" y2="11"/>
            <line x1="18" y1="7" x2="12" y2="11"/>
            <line x1="12" y1="11" x2="12" y2="18"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:22px;
            font-weight:800;
            color:#1E1B4B;
            letter-spacing:-0.4px;
        ">
            Segmentation Intelligente des Étudiants
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#6D28D9;
        margin-top:6px;
    ">
        Machine Learning • K-Means • AI-driven Student Profiling
    </div>

</div>
""", height=150)

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
# FEATURES POUR CLUSTERING
# =========================
features = [
    "moyenne",
    "stress",
    "heures_etude",
    "sommeil",
    "motivation",
    "concentration"
]

X = df[features]

# =========================
# NORMALISATION 
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# KMEANS MODEL
# =========================
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
st.markdown("""
<style>

/* ===== SOFT KPI CARDS ===== */
.card {
    background: linear-gradient(135deg, #9CA3AF, #F8FAFC);
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 6px 4px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

/* icon */
.icon {
    font-size: 12px;
    margin-bottom: 6px;
}

/* KPI number */
.kpi {
    font-size: 12px;
    font-weight: 500;
    color: #0F172A;
}

/* label */
.small {
    font-size: 12.5px;
    color: #64748B;
    margin-top: 4px;
}

/* hover effect (optionnel mais beau) */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
    transition: 0.25s ease;
}
</style>
""", unsafe_allow_html=True)

st.subheader("👤 Répartition des profils")

col1, col2, col3 = st.columns(3)

# valeurs inchangées
perf = (df["profil"] == "🟢 Performants").sum()
moy = (df["profil"] == "🟡 Moyens").sum()
risque = (df["profil"] == "🔴 À risque").sum()


col1.markdown(f"""
<div class="card">
    <div class="icon">🟢</div>
    <div class="kpi">{perf}</div>
    <div class="small">Performants</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
    <div class="icon">🟡</div>
    <div class="kpi">{moy}</div>
    <div class="small">Moyens</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
    <div class="icon">🔴</div>
    <div class="kpi">{risque}</div>
    <div class="small">À risque</div>
</div>
""", unsafe_allow_html=True)

st.divider()
# =========================
# VISUALISATION 2D
# =========================
st.subheader("📉 Visualisation des clusters")

fig = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="profil",
    color_discrete_map={
        "🟢 Performants": "green",
        "🟡 Moyens": "orange",
        "🔴 À risque": "red"
    },
    title="Segmentation des étudiants"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="
    background: #F0FDF4;
    padding:15px;
    border-radius:12px;
    border:1px solid #86EFAC;
    font-size:14px;
    color:#065F46;
">

💡 <b>Interprétation des clusters d’étudiants</b>
<br>
Ce graphique permet de visualiser la répartition des étudiants selon leur <b>temps d’étude</b> et leur <b>performance académique</b>.
<br>

🟢 <b>Performants</b>  
Étudiants avec de bonnes moyennes et généralement un bon volume d’étude  
Profil stable et autonome  
🟡 <b>Moyens</b>  
 Résultats corrects mais variables  
 Peuvent progresser avec plus de régularité ou de concentration  
🔴 <b>À risque</b>  
Faible moyenne malgré parfois un effort  
Nécessitent un accompagnement (méthode de travail, motivation, gestion du stress)  
<br>
📌 <b>Lecture du graphique :</b>  
• Chaque point = un étudiant  
• La couleur indique son profil  

</div>
""", unsafe_allow_html=True)
st.divider()
# =========================
# PROFILS EXPLIQUÉS
# =========================
st.subheader("🧬 Analyse des groupes")

for profil in df["profil"].unique():
    st.markdown(f"### {profil}")

    subset = df[df["profil"] == profil]

    st.write("📊 Moyenne :", round(subset["moyenne"].mean(), 2))
    st.write("😰 Stress moyen:", round(subset["stress"].mean(), 2))
    st.write("📚 Heure d'étude moyenne :", round(subset["heures_etude"].mean(), 2))
    st.write("👥 Effectif :", len(subset))

st.divider()
