import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse Globale", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #A7F3D0;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(16,185,129,0.12);
    font-family: Arial;
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <svg width="40" height="40" viewBox="0 0 24 24"
             fill="none" stroke="#059669" stroke-width="2.5">

            <circle cx="11" cy="11" r="7"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <polyline points="8 11 10 13 14 9"/>

        </svg>

        <div style="
            font-size:20px;
            font-weight:800;
            color:#064E3B;
        ">
            Analyse Globale des Données Étudiantes
        </div>

    </div>

    <div style="
        font-size:14px;
        color:#065F46;
        margin-top:8px;
    ">
        Exploration complète des tendances, performances et corrélations académiques
    </div>

</div>
""", height=180)

# =========================
# DATA
# =========================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")

try:
    df = load_data()
except:
    st.error("Aucune donnée disponible.")
    st.stop()

numeric_df = df.select_dtypes(include=['int64', 'float64'])
st.divider()

# =========================
# KPIs
# =========================
st.markdown("""
<h3 style="color:#92400E;">
🌍  Indicateurs clés
</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("😰 Stress moyen", round(df["stress"].mean(), 2))
col3.metric("📚 Heures d'étude moyenne", round(df["heures_etude"].mean(), 2))

st.divider()

# =========================
#  HISTOGRAMMES (inchangé)
# =========================
st.markdown("""
<h3 style="color:#ffffff;font-size:25px;">
📦 Distributions des moyennes
</h3>
""", unsafe_allow_html=True)

fig_hist = px.histogram(
    df,
    x="moyenne",
    nbins=20,
    marginal="box"
)

st.plotly_chart(fig_hist, use_container_width=True)



st.divider()

# =========================
#  PIE CHARTS 
# =========================
st.markdown("""
<h3 style="color:#059669;">
🔀 Répartitions
</h3>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig4 = px.pie(
        df,
        names="filiere",
        title=" Répartition par filière",
        color_discrete_sequence=["#FF5733", "#FFC300", "#28B463", "#3498DB", "#9B59B6"]
    )

    fig4.update_layout(height=500) 

    st.plotly_chart(fig4, use_container_width=True)

with col2:
    fig5 = px.pie(
        df,
        names="sexe",
        title=" Répartition par sexe",
        color_discrete_sequence=["#FF9F1C", "#2EC4B6"],
        hole=0.6
    )

    fig5.update_layout(height=500) 

    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# =========================
#  CORRELATION 
# =========================
st.markdown("""
<h3 style="color:#92400E;">
🔗Matrice de Corrélation
</h3>
""", unsafe_allow_html=True)

corr_matrix = numeric_df.corr()

fig6 = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="RdBu_r"
)
fig6.update_layout(
    height=550, 
    width=750    
)

st.plotly_chart(fig6, use_container_width=True)

st.components.v1.html("""
<style>

.scroll-wrapper {
    height: 60px;
    overflow: hidden;
    width: 100%;
    position: relative;
}

.scroll-content {
    display: flex;
    flex-direction: column;
    animation: scrollLoop 20s linear infinite;
}

/* lignes */
.line {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #EAB308;
}

/* animation fluide */
@keyframes scrollLoop {
    0%   { transform: translateY(0); }
    100% { transform: translateY(-50%); }
}

</style>

<div class="scroll-wrapper">
    <div class="scroll-content">

        <!-- CONTENU ORIGINAL -->
        <div class="line">Interprétation de la matrice de corrélation</div>
        <div class="line">Analyse des relations entre variables</div>
        <div class="line">]0,1]  = corrélation positive (les variables évoluent dans le même sens)</div>
        <div class="line">[-1,0[ = corrélation négative (les variables evoluent en sens contraire)</div>
        <div class="line">0 = pas de relation entre les variables</div>

        <!-- DUPLICATION (IMPORTANT) -->
        <div class="line">Interprétation de la matrice de corrélation</div>
        <div class="line">Analyse des relations entre variables</div>
        <div class="line">]0,1] = corrélation positive (les variables évoluent dans le même sens)</div>
        <div class="line">[-1,0[ = corrélation négative (les variables evoluent en sens contraire)</div>
        <div class="line">0 = pas de relation entre les variables</div>

    </div>
</div>
""", height=90)
st.markdown("""
<div style="
    background: #FFFBEB;
    padding:15px;
    border-radius:12px;
    border:1px solid #FDE68A;
    font-size:14px;
    color:#92400E;
">

  <b>Lecture du graphique :</b>  
• Les couleurs <b>rouges</b> représentent des corrélations positives  
• Les couleurs <b>bleues</b> représentent des corrélations négatives  
• Plus la couleur est intense, plus la relation est forte  
• Le relation entre deux variables est d'autant plus forte lorsque leur corrélation tend vers +1 et plus faible lorsqu'elle tend vers -1

💡 Cette analyse permet de détecter rapidement les variables clés comme le <b>temps d’étude</b>, la <b>motivation</b>, le <b>stress</b> ou la <b>concentration</b>.

</div>
""", unsafe_allow_html=True)
st.divider()

# =========================
#  RELATIONS IMPORTANTES 
# =========================
st.markdown("""
<h3 style="color:#ffffff;">
🔑 Relations clés
</h3>
""", unsafe_allow_html=True)

fig7 = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="heures_etude",
    color_continuous_scale="Purples",
    title=" Étude vs Performance",
    trendline="ols"
)

fig7.update_traces(marker=dict(size=10, opacity=0.7))
fig7.update_layout(template="plotly_dark")

st.plotly_chart(fig7, use_container_width=True)

fig8 = px.scatter(
    df,
    x="stress",
    y="moyenne",
    color="stress",
    color_continuous_scale="Oranges",
    title=" Stress vs Performance",
    trendline="ols"
)

fig8.update_traces(marker=dict(size=10, opacity=0.7))
fig8.update_layout(template="plotly_dark")

st.plotly_chart(fig8, use_container_width=True)


st.divider()
# =========================
# COMPARAISONS
# =========================
st.subheader("⚖️ Comparaison des filières")

moyenne_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()

fig1 = px.bar(
    moyenne_filiere,
    x="filiere",
    y="moyenne",
    color="filiere",
    title=" Moyenne académique par filière",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)



stress_filiere = df.groupby("filiere")["stress"].mean().reset_index()

fig2 = px.bar(
    stress_filiere,
    x="filiere",
    y="stress",
    color="filiere",
    title=" Stress moyen par filière",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)



study_filiere = df.groupby("filiere")["heures_etude"].mean().reset_index()

fig3 = px.bar(
    study_filiere,
    x="filiere",
    y="heures_etude",
    color="filiere",
    title=" Heures d'étude moyennes par filière",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
# BOXPLOT 
# =========================
st.markdown("""
<h3 style="color:#94A3B8;">
📊 Distribution des notes par filière
</h3>
""", unsafe_allow_html=True)

fig9 = px.box(
    df,
    x="filiere",
    y="moyenne",
    color="filiere",
    title="Répartition des moyennes par filière",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig9.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig9, use_container_width=True)

st.divider()
# ==========================================================
#  TENDANCES
# ==========================================================
st.subheader("📈 Tendances globales")

trend = df.groupby("niveau")["moyenne"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="niveau",
    y="moyenne",
    markers=True,
    title="Évolution des performances par niveau"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()
# =========================
# ANALYSE INTELLIGENTE
# =========================
st.subheader("🔁 Analyse intelligente")
if st.button(" 🔍 Visualiser"):

    # Moyenne
    best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
    worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()

    # Stress
    stress_high = df.groupby("filiere")["stress"].mean().idxmax()
    stress_low = df.groupby("filiere")["stress"].mean().idxmin()

    concentration_high = df.groupby("filiere")["concentration"].mean().idxmax()
    motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()
    regularite_high = df.groupby("filiere")["regularite"].mean().idxmax()

    age_high = None
    credits_high = None

    if "age" in df.columns:
        age_high = df.groupby("filiere")["age"].mean().idxmax()

    if "credits" in df.columns:
        credits_high = df.groupby("filiere")["credits"].mean().idxmax()

    # =========================
    # AFFICHAGE
    # =========================

    st.success(f"🏆 Filière la plus performante : {best_filiere}")
    st.error(f"📉 Filière la moins performante : {worst_filiere}")

    st.warning(f"😰 Filière la plus stressée : {stress_high}")
    st.info(f"😌 Filière la moins stressée : {stress_low}")

    st.success(f"🧠 Filière la plus concentrée : {concentration_high}")
    st.success(f"🔥 Filière la plus motivée : {motivation_high}")
    st.success(f"📅 Filière la plus régulière : {regularite_high}")

    if age_high:
        st.info(f"👴 Filière avec étudiants les plus âgés : {age_high}")

st.divider()
# =========================
# EXPORT CSV + AFFICHAGE DONNÉES (inchangé)
# =========================
st.subheader("📁 Export & Visualisation de données")
col1, col2 = st.columns(2)

csv = df.to_csv(index=False).encode("utf-8")

with col1:
    st.download_button(
        label="📥 Télécharger les données CSV",
        data=csv,
        file_name="donnees_etudiants.csv",
        mime="text/csv"
    )

with col2:
    show_data = st.button("👁️ Voir les données brutes")

if show_data:
    st.subheader("📚 Liste complète des étudiants")

    st.dataframe(
        df,
        use_container_width=True
    )
st.divider()
st.markdown("""
<div style="
    font-size:22px;
    font-weight:700;
    margin-top:10px;
">
🤔 Souhaitez-vous visualiser les statistiques par Filière ?
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "show_stats" not in st.session_state:
    st.session_state.show_stats = False

if st.button("🧮 Statistique par filière"):
    st.session_state.show_stats = True

# ===== AFFICHAGE PERSISTANT =====
if st.session_state.show_stats:
    # =========================
    # FILTRES
    # =========================
    filiere_selected = st.selectbox(
    "📌 Choisir une filière",
    df["filiere"].dropna().unique()
    )

    df_fil = df[df["filiere"] == filiere_selected]


    # =========================
    # KPI FILIERE + SEXE (SEMI CIRCLE)
    # =========================
    st.subheader(f"🌍 Indicateurs de la filiere - {filiere_selected}")

    st.markdown("""
    <style>

    /* ===== ANIMATED KPI CARDS ===== */
    .kpi-card {
        background: linear-gradient(135deg, #9CA3AF, #F8FAFC);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 8px 6px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        transition: all 0.3s ease;
    }

    /* hover effect + glow border */
    .kpi-card:hover {
        transform: translateY(-6px) scale(1.03);
        border: 1px solid #60A5FA;
        box-shadow:
            0 0 10px rgba(96, 165, 250, 0.6),
            0 10px 25px rgba(96, 165, 250, 0.25);
    }

    /* title icon */
    .kpi-icon {
        font-size: 14px;
        margin-bottom: 6px;
    }

    /* value */
    .kpi-value {
        font-size: 16px;
        font-weight: 600;
        color: #0F172A;
    }

    /* label */
    .kpi-label {
        font-size: 12.5px;
        color: #64748B;
        margin-top: 4px;
    }

    </style>
    """, unsafe_allow_html=True)


    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎓</div>
        <div class="kpi-value">{round(df_fil["moyenne"].mean(), 2)}</div>
        <div class="kpi-label">Moyenne</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">😰</div>
        <div class="kpi-value">{round(df_fil["stress"].mean(), 2)}</div>
        <div class="kpi-label">Stress</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📚</div>
        <div class="kpi-value">{round(df_fil["heures_etude"].mean(), 2)}</div>
        <div class="kpi-label">Heures étude</div>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">👨‍🎓</div>
        <div class="kpi-value">{len(df_fil)}</div>
        <div class="kpi-label">Total étudiants</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =========================
    #  SEMI-CIRCLE SEXE
    # =========================
    st.subheader(f"🔬 Analyse de la filiere - {filiere_selected}")

    st.subheader("")

    sex_counts = df_fil["sexe"].value_counts().reset_index()
    sex_counts.columns = ["sexe", "count"]

    fig_sex = px.pie(
        sex_counts,
        names="sexe",
        values="count",
        hole=0.5,
        title=" Répartition du sexe",
        color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
    )

    fig_sex.update_traces(textinfo="percent+label")

    fig_sex.update_layout(
        showlegend=True,
        height=400,
        annotations=[dict(text="Sexe", x=0.5, y=0.5, showarrow=False)],
        margin=dict(t=40, b=0)
    )

    st.plotly_chart(fig_sex, use_container_width=True)



    # =========================
    # MATRICE DE CORRELATION
    # =========================

    numeric_df = df_fil.select_dtypes(include=["int64", "float64"])

    fig_corr = px.imshow(
        numeric_df.corr(),
        text_auto=True,
        color_continuous_scale="RdBu",
        title=" Corrélation des variables"
    )

    st.plotly_chart(fig_corr, use_container_width=True)
    st.divider()
    # =========================
    # NUAGES DE POINTS FUSIONNÉS
    # =========================
    st.subheader("📊 Relations clés avec la performance")

    # transformer les données (format long)
    df_long = df_fil.melt(
        id_vars=["moyenne"],
        value_vars=["heures_etude", "concentration", "motivation", "regularite"],
        var_name="Variable",
        value_name="Valeur"
    )

    # mapping noms propres
    labels_map = {
        "heures_etude": "📚 Étude",
        "concentration": "🧠 Concentration",
        "motivation": "🔥 Motivation",
        "regularite": "📅 Régularité"
    }
    df_long["Variable"] = df_long["Variable"].map(labels_map)

    # création du graphe
    fig = px.scatter(
        df_long,
        x="Valeur",
        y="moyenne",
        facet_col="Variable",
        facet_col_wrap=2,
        trendline="ols",
        color="Variable",
        title=" Impact des facteurs clés sur la performance académique"
    )

    # amélioration visuelle
    fig.update_layout(
        showlegend=False,
        margin=dict(t=60, l=30, r=30, b=30)
    )

    st.plotly_chart(fig, use_container_width=True)


    niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()
    # =========================
    # ANALYSE PAR NIVEAU
    # =========================
    st.subheader("🧠 Analyse par niveau dans la filière")

    fig1 = px.bar(
        niveau_group,
        x="niveau",
        y="moyenne",
        color="niveau",
        title=f"🎓 Moyenne par niveau - {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        niveau_group,
        x="niveau",
        y="stress",
        color="niveau",
        title=f"😰 Stress par niveau - {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(
        niveau_group,
        x="niveau",
        y="heures_etude",
        color="niveau",
        title=f"📚 Heures d'étude par niveau - {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # RÉPARTITION NIVEAU (FILTRÉE)
    # =========================


    fig4 = px.pie(
        df_fil,
        names="niveau",
        title=f"👨‍🎓 Répartition des niveaux - {filiere_selected}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig4, use_container_width=True)


   
    

  

