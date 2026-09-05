import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Rapport IA", layout="wide")

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
.section-title .label {{ font-size: 20px; font-weight: 600; color: {TEXT_PRIMARY}; }}
.section-title .rule {{ flex: 1; height: 1px; background: {BORDER}; }}

/* Fiche étudiant */
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

.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    color: {TEXT_PRIMARY};
}}

/* Panel diagnostic */
.risk-panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 4px solid var(--c, {ACCENT});
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 17px;
    font-weight: 600;
    color: var(--c, {ACCENT});
}}

/* Widgets */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {SURFACE};
    border: 1px solid {BORDER} !important;
    color: {TEXT_PRIMARY};
    border-radius: 8px;
}}
.stDownloadButton button {{
    background: linear-gradient(135deg, {ACCENT}, {PURPLE});
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
}}
.stDownloadButton button:hover {{ opacity: .9; }}

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
        <div class="brand-mark">📄</div>
        <div>
            <div class="brand-name">Génération de Rapport Personnel</div>
            <div class="brand-sub">AI-driven Academic Report • Insights • Performance Intelligence</div>
        </div>
    </div>
</div>
""")

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
section_title("", "Sélection de l'étudiant")

filiere = st.selectbox("Choisir la filière", sorted(df["filiere"].dropna().unique()))
df_f = df[df["filiere"] == filiere]

niveau = st.selectbox("Choisir le niveau", sorted(df_f["niveau"].dropna().unique()))
df_n = df_f[df_f["niveau"] == niveau]

if df_n.empty:
    st.warning(" Aucun étudiant trouvé pour cette sélection.")
    st.stop()

df_n = df_n.copy()

if "nom" in df_n.columns:
    df_n["nom"] = df_n["nom"].fillna("Inconnu")
    noms = sorted(df_n["nom"].unique())
else:
    noms = ["Inconnu"]

nom = st.selectbox("Choisir l'étudiant", noms)
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
risk_color = TEAL if risk.startswith("🟢") else (AMBER if risk.startswith("🟡") else CORAL)

# =========================
# PROFIL
# =========================
section_title("", "Informations de l'étudiant")

render_html(f"""
<div class="panel">
    <div class="spec-list">
        <div class="spec-row"><span class="k">Nom</span><span class="v">{student.get('nom', 'Inconnu')}</span></div>
        <div class="spec-row"><span class="k">Niveau</span><span class="v">{student.get('niveau', 'N/A')}</span></div>
        <div class="spec-row"><span class="k">Filière</span><span class="v">{student.get('filiere', 'N/A')}</span></div>
        <div class="spec-row"><span class="k">Moyenne</span><span class="v">{student.get('moyenne', 0)}</span></div>
        <div class="spec-row"><span class="k">Niveau de stress (/10)</span><span class="v">{student.get('stress', 0)}</span></div>
        <div class="spec-row"><span class="k">Heures d'étude / jour</span><span class="v">{student.get('heures_etude', 0)}</span></div>
        <div class="spec-row"><span class="k">Sommeil (h/jour)</span><span class="v">{student.get('sommeil', 0)}</span></div>
        <div class="spec-row"><span class="k">Téléphone (h/jour)</span><span class="v">{student.get('telephone', 0)}</span></div>
    </div>
</div>
""")

st.divider()
section_title("", "Diagnostic Intelligent")

render_html(f"""
<div class="risk-panel" style="--c:{risk_color};">
    Niveau de risque : {risk}
</div>
""")


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

st.divider()
st.download_button(
    label="📥 Télécharger le rapport PDF",
    data=pdf,
    file_name=f"rapport_{nom}.pdf",
    mime="application/pdf"
)

st.divider()
