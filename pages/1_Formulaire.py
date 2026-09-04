import streamlit as st
import pandas as pd
import os
import time
import streamlit.components.v1 as components
# =========================
# CONFIG
# =========================
st.set_page_config(page_title="SmartStudent Analytics", layout="centered")

components.html("""
<div style="
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 12px;
    font-family: Arial, sans-serif;
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🧠 + 📊 ICON (Brain + Analytics fusion) -->
        <svg width="42" height="42" viewBox="0 0 24 24"
             fill="none"
             stroke="#6366F1"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- brain shape -->
            <path d="M9 3c-2 0-3.5 1.5-3.5 3.5S7 10 7 10"/>
            <path d="M15 3c2 0 3.5 1.5 3.5 3.5S17 10 17 10"/>
            <path d="M7 10c-1.5 0-2.5 1-2.5 2.5S6 15 7 15"/>
            <path d="M17 10c1.5 0 2.5 1 2.5 2.5S18 15 17 15"/>

            <!-- analytics bars -->
            <line x1="9" y1="18" x2="9" y2="14"/>
            <line x1="12" y1="18" x2="12" y2="12"/>
            <line x1="15" y1="18" x2="15" y2="10"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#0F172A;
            letter-spacing:-0.3px;
        ">
            SmartStudent Analytics Forms
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#64748B;
        margin-top:8px;
    ">
        Data collection & intelligent student profiling system
    </div>

</div>
""", height=140)

st.divider()
st.subheader("📑 Formulaire de collecte des données étudiants")

DATA_FILE = "data_students.csv"

# =========================
# FORMULAIRE
# =========================
with st.form("student_form"):

    st.markdown("### 👤 Identité")

    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")

    st.markdown("### 🧾 Informations générales")
    age = st.number_input("Âge", min_value=15, max_value=60, step=1)
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])

    filiere = st.selectbox(
        "Filière",
        ["Informatique", "Maths", "Économie", "Droit", "Médecine",
         "Physique", "Chimie", "Biologie", "Histoire", "Géographie",
         "Langue étrangère", "Géologie", "Philosophie", "Architecture", "Énergies renouvelables"]
    )

    niveau = st.selectbox("Niveau", ["L1", "L2", "L3", "Master1", "Master2", "PhD"])

    st.markdown("### 📚 Habitudes d'étude")
    heures_etude = st.slider("Heures d'étude par jour", 0, 12, 2)
    methode = st.selectbox("Méthode d'apprentissage", ["Seul(e)", "Groupe"])
    regularite = st.slider("Régularité (1 à 10)", 1, 10, 5)

    st.markdown("### 🍎 Mode de vie")
    sommeil = st.slider("Heures de sommeil", 0, 12, 6)
    sport = st.selectbox("Activité sportive", ["Oui", "Non"])
    telephone = st.slider("Temps téléphone (heures/jour)", 0, 12, 4)

    st.markdown("### 😰 Bien-être")
    stress = st.slider("Stress (1 à 10)", 1, 10, 5)
    concentration = st.slider("Concentration (1 à 10)", 1, 10, 5)
    motivation = st.slider("Motivation (1 à 10)", 1, 10, 5)

    st.markdown("### 🎓 Résultats")
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
