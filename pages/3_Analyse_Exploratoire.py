import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Data Explorer PRO", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #C7D2FE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(99,102,241,0.10);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🔍 + 📊 ICON (Data Exploration) -->
        <svg width="40" height="40" viewBox="0 0 24 24"
             fill="none"
             stroke="#4F46E5"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- magnifying glass -->
            <circle cx="11" cy="11" r="7"/>
            <line x1="16.5" y1="16.5" x2="21" y2="21"/>

            <!-- small chart inside -->
            <line x1="8.5" y1="13" x2="8.5" y2="11"/>
            <line x1="11" y1="13" x2="11" y2="9"/>
            <line x1="13.5" y1="13" x2="13.5" y2="7"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#1E1B4B;
            letter-spacing:-0.4px;
        ">
            Analyse Exploratoire
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#4338CA;
        margin-top:6px;
    ">
        Data Exploration • Patterns Detection • Statistical Insights
    </div>

</div>
""", height=150)

st.divider()
# =========================
# LOAD DATA SAFE
# =========================
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv("data_students.csv")

    #  compatibilité colonnes
    if "nom" not in df.columns:
        df["nom"] = "Inconnu"

    if "filiere" not in df.columns:
        df["filiere"] = "Non défini"

    if "niveau" not in df.columns:
        df["niveau"] = "Non défini"

    if "sexe" not in df.columns:
        df["sexe"] = "Non défini"

    return df  # ✅ au bon endroit

# =========================
# EXECUTION
# =========================
try:
    df = load_data()
except:
    st.error("Aucune donnée disponible.")
    st.stop()

# =========================
# UI
# =========================
st.markdown("###  Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    filiere = st.selectbox(
        "📚 Filière",
        ["Toutes"] + sorted(df["filiere"].dropna().unique())
    )

with col2:
    niveau = st.selectbox(
        "🎓 Niveau",
        ["Tous"] + sorted(df["niveau"].dropna().unique())
    )

with col3:
    sexe = st.selectbox(
        "👤 Sexe",
        ["Tous"] + sorted(df["sexe"].dropna().unique())
    )

# =========================
# FILTER DATA
# =========================
df_filtered = df.copy()

if filiere != "Toutes":
    df_filtered = df_filtered[df_filtered["filiere"] == filiere]

if niveau != "Tous":
    df_filtered = df_filtered[df_filtered["niveau"] == niveau]

if sexe != "Tous":
    df_filtered = df_filtered[df_filtered["sexe"] == sexe]


st.markdown("### 👤 Sélectionner l'étudiant")

if len(df_filtered) == 0:
    st.warning("Aucun étudiant trouvé avec ces filtres")
else:
    student_selected = st.selectbox(
        "Choisir un étudiant",
        df_filtered["nom"].unique()
    )

    student_data = df_filtered[df_filtered["nom"] == student_selected]

    st.dataframe(student_data, use_container_width=True)
st.divider()


# =========================
# FILIERE BAR CHART (SAFE)
# =========================
st.markdown("#### 👨‍🎓 Nombre d'étudiants")

filiere_counts = df_filtered["filiere"].value_counts().reset_index()
filiere_counts.columns = ["filiere", "count"]

fig1 = px.bar(
    filiere_counts,
    x="filiere",
    y="count",
    color="filiere",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)
