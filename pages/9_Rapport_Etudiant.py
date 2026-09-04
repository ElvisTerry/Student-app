import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import streamlit.components.v1 as components

st.set_page_config(page_title="Rapport IA", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #C7D2FE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(79,70,229,0.12);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 📄 + 📊 + 🧠 ICON (AI Report generation) -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#4338CA"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- document -->
            <path d="M7 3h7l3 3v15a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/>
            <path d="M14 3v4h4"/>

            <!-- analytics inside -->
            <line x1="8" y1="14" x2="8" y2="12"/>
            <line x1="11" y1="14" x2="11" y2="10"/>
            <line x1="14" y1="14" x2="14" y2="8"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#1E1B4B;
            letter-spacing:-0.4px;
        ">
            Génération de Rapport Personnel
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#4338CA;
        margin-top:6px;
    ">
        AI-driven Academic Report • Insights • Performance Intelligence
    </div>

</div>
""", height=150)
st.divider()
# =========================
# DATA SAFE LOAD
# =========================
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv("data_students.csv")

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
st.subheader(" Sélection de l'étudiant")

# FILIERE
filiere = st.selectbox(
    " Choisir la filière",
    sorted(df["filiere"].dropna().unique())
)

df_f = df[df["filiere"] == filiere]

# NIVEAU
niveau = st.selectbox(
    " Choisir le niveau",
    sorted(df_f["niveau"].dropna().unique())
)

df_n = df_f[df_f["niveau"] == niveau]

# =========================
# PROTECTION CAS VIDE
# =========================
if df_n.empty:
    st.warning(" Aucun étudiant trouvé pour cette sélection.")
    st.stop()

# =========================
# NOM 
# =========================
df_n = df_n.copy()

# enlever NaN + trier seulement si colonne existe
if "nom" in df_n.columns:
    df_n["nom"] = df_n["nom"].fillna("Inconnu")
    noms = sorted(df_n["nom"].unique())
else:
    noms = ["Inconnu"]

nom = st.selectbox(" Choisir l'étudiant", noms)

student = df_n[df_n["nom"] == nom].iloc[0]

# =========================
# IA RISK SCORE
# =========================
def risk_level(row):
    score = (
        (row.get("stress", 5) * 0.35) +
        ((12 - row.get("heures_etude", 5)) * 0.45) +
        ((row.get("sommeil", 6)) * 0.20)
    )

    if score < 5:
        return "🟢 Faible risque"
    elif score < 8:
        return "🟡 Risque moyen"
    else:
        return "🔴 Risque élevé"

risk = risk_level(student)

# =========================
# PROFIL
# =========================
st.subheader(" Informations de l'étudiant")

st.write("👤 Nom :", student.get("nom", "Inconnu"))
st.write("🎓 Niveau :", student.get("niveau", "N/A"))
st.write("📚 Filière :", student.get("filiere", "N/A"))
st.write("🎓 Moyenne :", student.get("moyenne", 0))
st.write("😰 Niveau de stress (/10) :", student.get("stress", 0))
st.write("📚 Heures d'étude /jour :", student.get("heures_etude", 0))
st.write("😴 Sommeil (h/jour) :", student.get("sommeil", 0))
st.write("📱 Téléphone (h/jour) :", student.get("telephone", 0))
st.divider()
st.subheader("🧠 Diagnostic Intelligent")
st.success(f"Niveau de risque : {risk}")


# =========================
# PDF GENERATION
# =========================
def generate_pdf(student, risk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "RAPPORT INTELLIGENT ETUDIANT")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Nom: {student.get('nom', 'Inconnu')}")
    c.drawString(50, 740, f"Filière: {student.get('filiere', 'N/A')}")
    c.drawString(50, 720, f"Niveau: {student.get('niveau', 'N/A')}")
    c.drawString(50, 700, f"Moyenne: {student.get('moyenne', 0)}")
    c.drawString(50, 680, f"Stress: {student.get('stress', 0)}")
    c.drawString(50, 660, f"Heures étude: {student.get('heures_etude', 0)}")
    c.drawString(50, 640, f"Sommeil: {student.get('sommeil', 0)}")
    c.drawString(50, 620, f"Telephone: {student.get('telephone', 0)}")
    c.drawString(50, 600, f"Risque: {risk}")

    c.drawString(50, 560, "Analyse automatique:")
    c.drawString(50, 540, "- Généré par système IA académique")

    c.save()
    buffer.seek(0)
    return buffer


# =========================
# DOWNLOAD PDF
# =========================
pdf = generate_pdf(student, risk)

st.download_button(
    label="📥 Télécharger le rapport PDF",
    data=pdf,
    file_name=f"rapport_{nom}.pdf",
    mime="application/pdf"
)

# =========================
# FOOTER
# =========================
st.divider()
