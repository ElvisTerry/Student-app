import streamlit as st
import pandas as pd
import os
import time

# ==========================================================
# CONFIGURATION PAGE
# ==========================================================
st.set_page_config(page_title="SmartStudent Analytics", layout="centered")

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


def form_group(label: str):
    render_html(f'<div class="form-group">{label}</div>')


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

.stApp {{
    background: {BG};
}}

section[data-testid="stSidebar"] {{
    background: #0D0E12;
    border-right: 1px solid {BORDER};
}}

::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 20px; }}

h1, h2, h3 {{
    color: {TEXT_PRIMARY} !important;
}}

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
.app-header .brand {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.app-header .brand-mark {{
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
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
.section-title .label {{
    font-size: 20px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
.section-title .rule {{
    flex: 1;
    height: 1px;
    background: {BORDER};
}}

/* Sous-titres de groupe (à l'intérieur du formulaire) */
.form-group {{
    font-size: 16px;
    font-weight: 600;
    color: {ACCENT};
    margin: 22px 0 10px 0;
}}

/* Carte du formulaire */
[data-testid="stForm"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 24px 26px;
}}

/* Champs de saisie */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {{
    background: {BG};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
.stSlider [data-baseweb="slider"] > div > div {{
    background: {ACCENT} !important;
}}
label, .stMarkdown p {{
    color: {TEXT_PRIMARY} !important;
}}

/* Boutons */
.stButton button,
[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
}}
.stButton button:hover,
[data-testid="stFormSubmitButton"] button:hover {{
    opacity: .9;
}}

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
        <div class="brand-mark">📝</div>
        <div>
            <div class="brand-name">SmartStudent Analytics - Formulaire</div>
            <div class="brand-sub">Data collection, intelligent student profiling system</div>
        </div>
    </div>
</div>
""")

st.divider()
section_title("", "Formulaire de collecte des données étudiants")

DATA_FILE = "data_students.csv"

# =========================
# FORMULAIRE
# =========================
with st.form("student_form"):

    form_group("Identité")

    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")

    form_group("Informations générales")
    age = st.number_input("Âge", min_value=15, max_value=60, step=1)
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])

    filiere = st.selectbox(
        "Filière",
        ["Informatique", "Maths", "Économie", "Droit", "Médecine",
         "Physique", "Chimie", "Biologie", "Histoire", "Géographie",
         "Langue étrangère", "Géologie", "Philosophie", "Architecture", "Énergies renouvelables"]
    )

    niveau = st.selectbox("Niveau", ["L1", "L2", "L3", "Master1", "Master2", "PhD"])

    form_group("Habitudes d'étude")
    heures_etude = st.slider("Heures d'étude par jour", 0, 12, 2)
    methode = st.selectbox("Méthode d'apprentissage", ["Seul(e)", "Groupe"])
    regularite = st.slider("Régularité (1 à 10)", 1, 10, 5)

    form_group("Mode de vie")
    sommeil = st.slider("Heures de sommeil", 0, 12, 6)
    sport = st.selectbox("Activité sportive", ["Oui", "Non"])
    telephone = st.slider("Temps téléphone (heures/jour)", 0, 12, 4)

    form_group("Bien-être")
    stress = st.slider("Stress (1 à 10)", 1, 10, 5)
    concentration = st.slider("Concentration (1 à 10)", 1, 10, 5)
    motivation = st.slider("Motivation (1 à 10)", 1, 10, 5)

    form_group("Résultats")
    moyenne = st.number_input("Moyenne (/20)", 0.0, 20.0, 10.0)
    credits = st.number_input("Crédits validés", 0, 60, 20)

    submit = st.form_submit_button("💾 Enregistrer")

# =========================
# SAUVEGARDE SAFE + MESSAGES TEMPORAIRES
# =========================
if submit:

    nom_complet = f"{prenom} {nom}".strip()

    new_data = pd.DataFrame([{
        "nom": nom_complet,
        "age": age,
        "sexe": sexe,
        "filiere": filiere,
        "niveau": niveau,
        "heures_etude": heures_etude,
        "methode": methode,
        "regularite": regularite,
        "sommeil": sommeil,
        "sport": sport,
        "telephone": telephone,
        "stress": stress,
        "concentration": concentration,
        "motivation": motivation,
        "moyenne": moyenne,
        "credits": credits
    }])

    # =========================
    # COMPATIBILITÉ ANCIENNES DONNÉES
    # =========================
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        df = pd.read_csv(DATA_FILE)

        if "nom" not in df.columns:
            df["nom"] = "Inconnu"

        df = pd.concat([df, new_data], ignore_index=True)

    else:
        df = new_data

    df.to_csv(DATA_FILE, index=False)

    # =========================
    # MESSAGES TEMPORAIRES (2 secondes)
    # =========================
    placeholder = st.empty()

    placeholder.success(" Données enregistrées avec succès, Merci pour votre souscription !")
    time.sleep(2)
    placeholder.empty()

    placeholder2 = st.empty()
    placeholder2.info(" Données ajoutées au système d'analyse,Bonne Navigation et prédiction de vos futures performances ")
    time.sleep(2)
    placeholder2.empty()
