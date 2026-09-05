import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Gestion des étudiants", layout="wide")

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
    background: linear-gradient(135deg, {CORAL}, {PURPLE});
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

/* Fiche étudiant */
.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
}}
.spec-list {{ margin-top: 4px; }}
.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid {BORDER};
    font-size: 16px;
}}
.spec-row:last-child {{ border-bottom: none; }}
.spec-row .k {{ color: {TEXT_SECONDARY}; }}
.spec-row .v {{ color: {TEXT_PRIMARY}; font-family: 'IBM Plex Mono', monospace; }}

/* Zone de danger */
.danger-panel {{
    background: {SURFACE};
    border: 1px solid {CORAL};
    border-left: 4px solid {CORAL};
    border-radius: 12px;
    padding: 18px 20px;
}}
.danger-panel .danger-label {{
    font-size: 14px;
    color: {CORAL};
    font-weight: 600;
    margin-bottom: 4px;
}}

/* Widgets */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
.stCheckbox label p {{ color: {TEXT_PRIMARY} !important; }}

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
        <div class="brand-mark">🗂️</div>
        <div>
            <div class="brand-name">Gestion des étudiants</div>
            <div class="brand-sub">Admin Panel • Data Control • Student Records Management</div>
        </div>
    </div>
</div>
""")

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
section_title("", "Sélection de l'étudiant")

filiere = st.selectbox("Choisir la filière", sorted(df["filiere"].dropna().unique()))
df_f = df[df["filiere"] == filiere]

niveau = st.selectbox("Choisir le niveau", sorted(df_f["niveau"].dropna().unique()))
df_n = df_f[df_f["niveau"] == niveau]

if df_n.empty:
    st.warning(" Aucun étudiant trouvé.")
    st.stop()

df_n = df_n.copy()
df_n["nom"] = df_n["nom"].fillna("Inconnu")
df_n = df_n.sort_values("nom")

nom = st.selectbox("Choisir l'étudiant", df_n["nom"].unique())
student = df_n[df_n["nom"] == nom].iloc[0]

# =========================
# PROFIL
# =========================
section_title("", "Informations étudiant")

render_html(f"""
<div class="panel">
    <div class="spec-list">
        <div class="spec-row"><span class="k">Nom</span><span class="v">{student['nom']}</span></div>
        <div class="spec-row"><span class="k">Niveau</span><span class="v">{student['niveau']}</span></div>
        <div class="spec-row"><span class="k">Filière</span><span class="v">{student['filiere']}</span></div>
    </div>
</div>
""")

st.divider()

# =========================
# CONFIRMATION
# =========================
section_title("", "Confirmation")

render_html("""
<div class="danger-panel">
    <div class="danger-label">⚠️ Zone sensible</div>
    <div>Cette action est irréversible.</div>
</div>
""")

st.markdown("<br>", unsafe_allow_html=True)
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

