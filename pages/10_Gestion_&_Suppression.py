import streamlit as st
import pandas as pd
import os
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestion des étudiants", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #FFF1F2, #FFE4E6);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #FECDD3;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(244,63,94,0.10);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🗂️ + ⚙️ ICON (Admin / student management system) -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#9F1239"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- folder / database -->
            <path d="M3 7h6l2 2h10v10a2 2 0 0 1-2 2H3z"/>

            <!-- settings gear -->
            <circle cx="17" cy="15" r="2"/>
            <path d="M17 11v2"/>
            <path d="M17 17v2"/>
            <path d="M15 15h2"/>
            <path d="M19 15h2"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#881337;
            letter-spacing:-0.4px;
        ">
            Gestion des étudiants
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#9F1239;
        margin-top:6px;
    ">
        Admin Panel • Data Control • Student Records Management
    </div>

</div>
""", height=150)

st.divider()

DATA_FILE = "data_students.csv"

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv(DATA_FILE)

    if "nom" not in df.columns:
        df["nom"] = "Inconnu"

    if "filiere" not in df.columns:
        df["filiere"] = "Non défini"

    if "niveau" not in df.columns:
        df["niveau"] = "Non défini"

    return df

try:
    df = load_data()
except Exception as e:
    st.error("❌ Erreur lors du chargement des données")
    st.caption(f"Détail : {e}")
    st.stop()

# =========================
# FILTRES
# =========================
st.subheader("📌 Sélection de l'étudiant")

filiere = st.selectbox(
    " Choisir la filière",
    sorted(df["filiere"].dropna().unique())
)

df_f = df[df["filiere"] == filiere]

niveau = st.selectbox(
    " Choisir le niveau",
    sorted(df_f["niveau"].dropna().unique())
)

df_n = df_f[df_f["niveau"] == niveau]

if df_n.empty:
    st.warning(" Aucun étudiant trouvé.")
    st.stop()

df_n = df_n.copy()
df_n["nom"] = df_n["nom"].fillna("Inconnu")
df_n = df_n.sort_values("nom")

nom = st.selectbox(" Choisir l'étudiant", df_n["nom"].unique())

student = df_n[df_n["nom"] == nom].iloc[0]

# =========================
# PROFIL
# =========================
st.subheader("📄 Informations étudiant")

st.write("👤 Nom :", student["nom"])
st.write("🎓 Niveau :", student["niveau"])
st.write("📚 Filière :", student["filiere"])

# =========================
# CONFIRMATION
# =========================
st.subheader("⚠️ Confirmation")

confirm = st.checkbox("Je confirme vouloir supprimer cet étudiant")

if confirm:
    if st.button("🗑️ Supprimer définitivement"):

        try:
        
            st.cache_data.clear()

        
            df_new = df[df["nom"] != nom]

            
            temp_file = "temp_students.csv"
            df_new.to_csv(temp_file, index=False)

        
            os.replace(temp_file, DATA_FILE)

            st.success(" Étudiant supprimé avec succès")

            time.sleep(1)
            st.rerun()

        except PermissionError:
            st.error(" Erreur : le fichier est ouvert ailleurs (Excel ?). Ferme-le puis réessaie.")

        except Exception as e:
            st.error(f" Erreur inattendue : {e}")

# =========================
# FOOTER
# =========================
st.divider()
st.info(" Suppression sécurisée avec gestion d'erreur avancée")
