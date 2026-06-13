"""
╔══════════════════════════════════════════════════════════════════════╗
║              FCOT ChemSafe — Chemical Compatibility Checker         ║
║     Gabungan terbaik: UI modern + database reaksi lengkap + GHS     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import datetime
from collections import defaultdict

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FCOT ChemSafe",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (tema dark modern dari app_4)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --card:      #1a2236;
    --border:    #2a3650;
    --accent-f:  #ff6b35;
    --accent-c:  #4ecdc4;
    --accent-o:  #ffe66d;
    --accent-t:  #a29bfe;
    --text:      #e2e8f0;
    --muted:     #8892a4;
    --green:     #00d084;
    --red:       #ff4757;
    --yellow:    #f59e0b;
    --radius:    14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; }

/* HERO */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content:''; position:absolute; top:-40%; right:-10%;
    width:400px; height:400px;
    background:radial-gradient(circle, rgba(78,205,196,0.12) 0%, transparent 70%);
    pointer-events:none;
}
.hero-title {
    font-family:'Syne',sans-serif;
    font-size:2.6rem; font-weight:800; margin:0 0 6px;
    background:linear-gradient(90deg,#4ecdc4,#a29bfe,#ff6b35);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero-sub { color:var(--muted); font-size:1rem; margin:0; }

/* STAT CARDS */
.stat-grid { display:flex; gap:16px; margin-bottom:24px; flex-wrap:wrap; }
.stat-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:var(--radius); padding:18px 22px;
    flex:1; min-width:130px; position:relative; overflow:hidden;
}
.stat-card::before {
    content:''; position:absolute; top:0; left:0;
    width:4px; height:100%; border-radius:4px 0 0 4px;
}
.stat-card.f::before{background:var(--accent-f);}
.stat-card.c::before{background:var(--accent-c);}
.stat-card.o::before{background:var(--accent-o);}
.stat-card.t::before{background:var(--accent-t);}
.stat-card.g::before{background:#38bdf8;}
.stat-num{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;margin:0;}
.stat-label{color:var(--muted);font-size:0.82rem;margin:4px 0 0;}

/* RESULT BOX */
.result-danger {
    background:linear-gradient(135deg,#450a0a,#7f1d1d);
    border:2px solid #ef4444; border-radius:var(--radius);
    padding:1.5rem; margin:1rem 0;
    box-shadow:0 4px 20px rgba(239,68,68,0.3);
}
.result-warning {
    background:linear-gradient(135deg,#431407,#78350f);
    border:2px solid #f59e0b; border-radius:var(--radius);
    padding:1.5rem; margin:1rem 0;
    box-shadow:0 4px 20px rgba(245,158,11,0.3);
}
.result-safe {
    background:linear-gradient(135deg,#052e16,#14532d);
    border:2px solid #22c55e; border-radius:var(--radius);
    padding:1.5rem; margin:1rem 0;
    box-shadow:0 4px 20px rgba(34,197,94,0.3);
}
.result-title{font-size:1.5rem;font-weight:700;color:#fff;margin:0 0 0.4rem;}
.result-sub{color:rgba(255,255,255,0.75);font-size:0.9rem;}

/* FCOT BADGE */
.fcot-badge {
    display:inline-block; padding:4px 12px; border-radius:20px;
    font-size:0.78rem; font-weight:700;
    font-family:'Space Mono',monospace; letter-spacing:1px; margin:2px 4px;
}
.badge-F{background:rgba(255,107,53,0.15);color:var(--accent-f);border:1px solid rgba(255,107,53,0.3);}
.badge-C{background:rgba(78,205,196,0.15);color:var(--accent-c);border:1px solid rgba(78,205,196,0.3);}
.badge-O{background:rgba(255,230,109,0.15);color:var(--accent-o);border:1px solid rgba(255,230,109,0.3);}
.badge-T{background:rgba(162,155,254,0.15);color:var(--accent-t);border:1px solid rgba(162,155,254,0.3);}
.fcot-grid{display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.5rem 0;}

/* GHS */
.ghs-container{display:flex;flex-wrap:wrap;gap:0.6rem;margin:0.5rem 0;}
.ghs-badge{
    background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
    border-radius:10px;padding:0.4rem 0.8rem;
    font-size:0.8rem;color:#e2e8f0;display:flex;align-items:center;gap:0.4rem;
}

/* CHEM CARD */
.chem-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:var(--radius); padding:16px 20px; margin:6px 0;
    transition:border-color 0.2s;
}
.chem-card:hover{border-color:#4ecdc4;}
.chem-name{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;}

/* INFO BOX */
.info-strip {
    background:rgba(78,205,196,0.08); border-left:3px solid var(--accent-c);
    border-radius:0 8px 8px 0; padding:12px 16px; margin:10px 0;
    font-size:0.9rem; color:var(--text);
}
.info-box{
    background:rgba(30,58,138,0.2);border-left:4px solid #3b82f6;
    border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin:0.5rem 0;color:#e2e8f0;
}
.info-box h4{color:#93c5fd;margin:0 0 0.4rem;font-size:0.9rem;}
.info-box p{margin:0;font-size:0.88rem;line-height:1.6;}

/* THEORY BOX */
.theory-box{
    background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.3);
    border-radius:14px;padding:1.2rem;margin:0.6rem 0;
}
.theory-title{font-size:1rem;font-weight:700;color:#a5b4fc;margin-bottom:0.5rem;}

/* FAV / HISTORY CARD */
.fav-card{
    background:var(--card);border:1px solid var(--border);
    border-radius:var(--radius);padding:14px 18px;margin:6px 0;
    display:flex;align-items:center;gap:12px;
}
.fav-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.fav-dot.ok{background:var(--green);}
.fav-dot.no{background:var(--red);}
.fav-dot.warn{background:var(--yellow);}

.history-item{
    background:rgba(15,23,42,0.5);border:1px solid rgba(148,163,184,0.15);
    border-radius:10px;padding:0.75rem 1rem;margin:0.4rem 0;
    display:flex;justify-content:space-between;align-items:center;
}
.history-chem{font-size:0.9rem;color:#cbd5e1;font-weight:600;}
.history-time{font-size:0.75rem;color:#475569;}

/* METRIC ROW */
.metric-row{display:flex;gap:1rem;margin:1rem 0;}
.metric-card{
    flex:1;background:rgba(15,23,42,0.6);
    border:1px solid rgba(148,163,184,0.15);border-radius:12px;
    padding:1rem;text-align:center;
}
.metric-num{font-size:2rem;font-weight:800;color:#38bdf8;}
.metric-label{font-size:0.75rem;color:#64748b;text-transform:uppercase;letter-spacing:1px;}

/* NAV LABEL */
.nav-label{
    font-family:'Syne',sans-serif;font-size:0.7rem;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;color:var(--muted);
    margin:18px 0 6px;padding-left:4px;
}

/* selectbox override */
div[data-baseweb="select"] > div {
    background:var(--card) !important;
    border-color:var(--border) !important;
    color:var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "custom_chemicals" not in st.session_state:
    st.session_state.custom_chemicals = {}

# ─────────────────────────────────────────────
#  DATABASE BAHAN KIMIA (lengkap dari app_3)
# ─────────────────────────────────────────────
CHEMICALS = {
    # ── ASAM ──
    "Asam Sulfat (H₂SO₄)": {
        "formula":"H₂SO₄","cas":"7664-93-9","fcot":["C"],
        "ghs":["GHS05","GHS07"],"description":"Asam kuat, sangat korosif. Digunakan dalam industri kimia.",
        "class":"Asam Kuat","ph":"< 1",
        "hazard":"Sangat korosif terhadap kulit dan mata. Reaksi eksotermik dengan air.",
        "storage":"Wadah HDPE, jauh dari basa, logam, dan bahan organik.",
        "first_aid":"Siram dengan air mengalir 15–20 menit. Segera ke dokter.","group":"Asam",
    },
    "Asam Klorida (HCl)": {
        "formula":"HCl","cas":"7647-01-0","fcot":["C","T"],
        "ghs":["GHS05","GHS07"],"description":"Asam kuat, asap putih mengiritasi saluran pernapasan.",
        "class":"Asam Kuat","ph":"< 1",
        "hazard":"Korosif; uap sangat mengiritasi. Bereaksi dengan logam menghasilkan H₂.",
        "storage":"Ventilasi baik, terpisah dari basa dan oksidator.",
        "first_aid":"Pindahkan ke udara segar. Bilas mata/kulit dengan air.","group":"Asam",
    },
    "Asam Nitrat (HNO₃)": {
        "formula":"HNO₃","cas":"7697-37-2","fcot":["C","O"],
        "ghs":["GHS03","GHS05","GHS07"],"description":"Asam kuat sekaligus oksidator kuat. Warna kuning jika terkontaminasi NO₂.",
        "class":"Asam Kuat / Oksidator","ph":"< 1",
        "hazard":"Korosif + oksidator. Dapat menyebabkan kebakaran jika kontak bahan organik.",
        "storage":"Wadah kaca/HDPE, jauh dari reduktor dan bahan mudah terbakar.",
        "first_aid":"Bilas dengan air banyak. Cari bantuan medis segera.","group":"Asam",
    },
    "Asam Asetat (CH₃COOH)": {
        "formula":"CH₃COOH","cas":"64-19-7","fcot":["F","C"],
        "ghs":["GHS02","GHS05"],"description":"Asam lemah, bau tajam seperti cuka. Mudah terbakar pada konsentrasi tinggi.",
        "class":"Asam Lemah","ph":"2.4 (1M)",
        "hazard":"Mudah terbakar, titik nyala 39°C. Korosif pada konsentrasi tinggi.",
        "storage":"Jauh dari panas, api, dan oksidator kuat.",
        "first_aid":"Bilas dengan air. Ventilasi area jika tumpah.","group":"Asam",
    },
    "Asam Fosfat (H₃PO₄)": {
        "formula":"H₃PO₄","cas":"7664-38-2","fcot":["C"],
        "ghs":["GHS05"],"description":"Asam sedang, digunakan dalam pupuk dan food-grade.",
        "class":"Asam Sedang","ph":"1.5 (1M)",
        "hazard":"Korosif. Kurang berbahaya dibanding H₂SO₄ atau HNO₃.",
        "storage":"Wadah plastik, jauh dari basa kuat.",
        "first_aid":"Bilas kulit/mata dengan air mengalir.","group":"Asam",
    },
    "Asam Fluorida (HF)": {
        "formula":"HF","cas":"7664-39-3","fcot":["C","T"],
        "ghs":["GHS05","GHS06","GHS07"],"description":"Sangat toksik dan korosif. Menembus kulit dan merusak tulang.",
        "class":"Asam Sangat Berbahaya","ph":"< 1",
        "hazard":"Korosif dan sangat toksik. Dapat menembus jaringan ke tulang (hipokalsemia).",
        "storage":"Wadah polietilen khusus, lemari asam, jauh dari kaca.",
        "first_aid":"DARURAT: Gel kalsium glukonat topikal. Segera ke UGD.","group":"Asam",
    },
    # ── BASA ──
    "Natrium Hidroksida (NaOH)": {
        "formula":"NaOH","cas":"1310-73-2","fcot":["C"],
        "ghs":["GHS05"],"description":"Basa kuat (kaustik soda). Sangat higroskopis, eksoterm dengan air.",
        "class":"Basa Kuat","ph":"> 13",
        "hazard":"Sangat korosif terhadap kulit, mata, dan jaringan. Reaksi keras dengan asam.",
        "storage":"Wadah tertutup rapat, jauh dari asam dan logam aktif.",
        "first_aid":"Bilas dengan air mengalir minimal 20 menit. Ke dokter.","group":"Basa",
    },
    "Kalium Hidroksida (KOH)": {
        "formula":"KOH","cas":"1310-58-3","fcot":["C"],
        "ghs":["GHS05"],"description":"Basa kuat mirip NaOH, lebih larut, digunakan dalam baterai alkali.",
        "class":"Basa Kuat","ph":"> 13",
        "hazard":"Korosif sangat kuat. Eksotermis dengan air dan asam.",
        "storage":"Wadah kedap udara, jauh dari asam, kelembaban rendah.",
        "first_aid":"Bilas dengan air minimal 15 menit. Cari bantuan medis.","group":"Basa",
    },
    "Amonia (NH₃)": {
        "formula":"NH₃","cas":"7664-41-7","fcot":["T","C"],
        "ghs":["GHS04","GHS06","GHS05"],"description":"Gas/larutan basa, bau menyengat. Digunakan dalam pupuk dan refrigeran.",
        "class":"Basa Lemah","ph":"11.6 (1M)",
        "hazard":"Uap toksik, mengiritasi saluran napas. Gas bertekanan.",
        "storage":"Ventilasi baik, jauh dari klorin dan asam kuat.",
        "first_aid":"Pindahkan ke udara segar. Bilas mata/kulit dengan air.","group":"Basa",
    },
    "Kalsium Hidroksida (Ca(OH)₂)": {
        "formula":"Ca(OH)₂","cas":"1305-62-0","fcot":["C"],
        "ghs":["GHS05","GHS07"],"description":"Basa sedang (kapur padam). Digunakan dalam konstruksi dan pengolahan air.",
        "class":"Basa Sedang","ph":"12.4",
        "hazard":"Korosif, debu mengiritasi mata dan saluran pernapasan.",
        "storage":"Wadah tertutup, jauh dari asam dan CO₂.",
        "first_aid":"Bilas dengan air. Gunakan masker jika terhirup debu.","group":"Basa",
    },
    # ── PELARUT / ORGANIK ──
    "Etanol (C₂H₅OH)": {
        "formula":"C₂H₅OH","cas":"64-17-5","fcot":["F"],
        "ghs":["GHS02"],"description":"Pelarut umum, mudah terbakar. Digunakan dalam laboratorium dan farmasi.",
        "class":"Pelarut Organik","ph":"7 (netral)",
        "hazard":"Sangat mudah terbakar, titik nyala 13°C. Uap berat.",
        "storage":"Wadah tertutup, jauh dari api dan oksidator.",
        "first_aid":"Pindahkan ke udara segar. Bilas kulit.","group":"Pelarut",
    },
    "Metanol (CH₃OH)": {
        "formula":"CH₃OH","cas":"67-56-1","fcot":["F","T"],
        "ghs":["GHS02","GHS06","GHS08"],"description":"Pelarut organik sangat toksik. Konsumsi menyebabkan kebutaan/kematian.",
        "class":"Pelarut Organik Toksik","ph":"7 (netral)",
        "hazard":"Mudah terbakar + sangat toksik. Merusak saraf optik.",
        "storage":"Wadah gelap tertutup, ventilasi baik, jauh dari api.",
        "first_aid":"SEGERA ke dokter. Hindari paparan berulang.","group":"Pelarut",
    },
    "Aseton (C₃H₆O)": {
        "formula":"(CH₃)₂CO","cas":"67-64-1","fcot":["F"],
        "ghs":["GHS02","GHS07"],"description":"Pelarut ketone sangat mudah terbakar. Digunakan pembersih laboratorium.",
        "class":"Pelarut Organik","ph":"7 (netral)",
        "hazard":"Titik nyala -20°C, sangat mudah terbakar. Uap mengiritasi.",
        "storage":"Jauh dari nyala api dan oksidator. Ventilasi baik.",
        "first_aid":"Pindahkan ke udara segar. Bilas kulit dengan air.","group":"Pelarut",
    },
    "Kloroform (CHCl₃)": {
        "formula":"CHCl₃","cas":"67-66-3","fcot":["T"],
        "ghs":["GHS06","GHS08"],"description":"Pelarut organik halogen. Karsinogenik dan neurotoksik.",
        "class":"Pelarut Halogen","ph":"7 (netral)",
        "hazard":"Karsinogenik, hepatotoksik, neurotoksik. Jangan hirup uapnya.",
        "storage":"Wadah gelap, stabil dengan inhibitor. Jauh dari cahaya.",
        "first_aid":"Pindahkan ke udara segar. Pantau fungsi hati. Ke dokter.","group":"Pelarut",
    },
    "Benzena (C₆H₆)": {
        "formula":"C₆H₆","cas":"71-43-2","fcot":["F","T"],
        "ghs":["GHS02","GHS06","GHS08"],"description":"Pelarut aromatik. Karsinogenik (leukemia). Dilarang penggunaan umum.",
        "class":"Pelarut Aromatik Berbahaya","ph":"7 (netral)",
        "hazard":"Karsinogenik kelas 1A. Mudah terbakar. Paparan kronik → leukemia.",
        "storage":"Kabinet khusus, ventilasi tinggi, jauh dari api.",
        "first_aid":"DARURAT. Segera ke dokter. Pemantauan darah berkala.","group":"Pelarut",
    },
    "Toluena (C₇H₈)": {
        "formula":"C₇H₈","cas":"108-88-3","fcot":["F","T"],
        "ghs":["GHS02","GHS06","GHS08"],"description":"Pelarut aromatik, alternatif benzena. Neurotoksik pada paparan tinggi.",
        "class":"Pelarut Aromatik","ph":"7 (netral)",
        "hazard":"Mudah terbakar + neurotoksik.",
        "storage":"Wadah tertutup, jauh dari api dan oksidator.",
        "first_aid":"Udara segar, bilas kulit. Pantau kondisi neurologis.","group":"Pelarut",
    },
    "Isopropanol (IPA)": {
        "formula":"C₃H₇OH","cas":"67-63-0","fcot":["F"],
        "ghs":["GHS02","GHS07"],"description":"Alkohol isopropil, desinfektan umum.",
        "class":"Pelarut Organik","ph":"7 (netral)",
        "hazard":"Mudah terbakar. Dapat menyebabkan pusing pada paparan uap tinggi.",
        "storage":"Jauh dari api dan panas. Wadah tertutup.",
        "first_aid":"Udara segar. Bilas kulit.","group":"Pelarut",
    },
    "Dietil Eter (C₄H₁₀O)": {
        "formula":"C₄H₁₀O","cas":"60-29-7","fcot":["F"],
        "ghs":["GHS02","GHS07"],"description":"Pelarut anestesi, sangat volatil dan mudah terbakar.",
        "class":"Pelarut Organik","ph":"7 (netral)",
        "hazard":"Sangat mudah terbakar. Dapat membentuk peroksida eksplosif saat disimpan lama.",
        "storage":"Wadah gelap, suhu rendah, jauh dari api. Periksa peroksida secara berkala.",
        "first_aid":"Udara segar, bilas kulit.","group":"Pelarut",
    },
    "Heksana (C₆H₁₄)": {
        "formula":"C₆H₁₄","cas":"110-54-3","fcot":["F","T"],
        "ghs":["GHS02","GHS06","GHS08"],"description":"Pelarut nonpolar, titik nyala -22°C. Neurotoksik kronik.",
        "class":"Pelarut Alifatik","ph":"7 (netral)",
        "hazard":"Sangat mudah terbakar + neurotoksik kronik (neuropati perifer).",
        "storage":"Jauh dari api, ventilasi baik.",
        "first_aid":"Udara segar, bilas. Pantau gejala neurologis.","group":"Pelarut",
    },
    "Diklorometana (CH₂Cl₂)": {
        "formula":"CH₂Cl₂","cas":"75-09-2","fcot":["T"],
        "ghs":["GHS06","GHS08"],"description":"Pelarut klorinasi umum. Dicurigai karsinogenik, membentuk CO dalam tubuh.",
        "class":"Pelarut Halogen","ph":"7 (netral)",
        "hazard":"Karsinogenik dicurigai. Metabolisme ke CO di tubuh → bahaya jantung.",
        "storage":"Wadah tertutup, ventilasi baik, jauh dari api.",
        "first_aid":"Udara segar, pantau fungsi jantung dan hati.","group":"Pelarut",
    },
    # ── OKSIDATOR ──
    "Kalium Permanganat (KMnO₄)": {
        "formula":"KMnO₄","cas":"7722-64-7","fcot":["O","T"],
        "ghs":["GHS03","GHS07","GHS09"],"description":"Oksidator kuat, warna ungu tua. Digunakan dalam analisis dan desinfektan.",
        "class":"Oksidator Kuat","ph":"7–8 (larutan)",
        "hazard":"Oksidator kuat; api jika kontak bahan organik/reduktor. Korosif.",
        "storage":"Jauh dari bahan organik, reduktor, dan panas.",
        "first_aid":"Bilas dengan air. Jangan campurkan tanpa perhitungan.","group":"Oksidator",
    },
    "Hidrogen Peroksida (H₂O₂)": {
        "formula":"H₂O₂","cas":"7722-84-1","fcot":["O","C"],
        "ghs":["GHS03","GHS05","GHS07"],"description":"Oksidator, antiseptik. Berbahaya pada konsentrasi tinggi (>30%).",
        "class":"Oksidator","ph":"4–5 (3% larutan)",
        "hazard":"Oksidator. Konsentrasi tinggi = korosif + eksplosif jika terkontaminasi.",
        "storage":"Wadah gelap, sejuk, jauh dari logam berat (katalis).",
        "first_aid":"Bilas dengan air. Hindari pakaian yang terkena H₂O₂ pekat.","group":"Oksidator",
    },
    "Kalium Dikromat (K₂Cr₂O₇)": {
        "formula":"K₂Cr₂O₇","cas":"7778-50-9","fcot":["O","T"],
        "ghs":["GHS03","GHS06","GHS08","GHS09"],"description":"Oksidator kuat, karsinogenik (Cr⁶⁺). Digunakan dalam analisis dan galvanoteknik.",
        "class":"Oksidator / Karsinogenik","ph":"3–4 (larutan)",
        "hazard":"Karsinogenik kelas 1A (Cr VI). Oksidator kuat. Toksik terhadap lingkungan.",
        "storage":"Wadah tertutup, jauh dari reduktor dan bahan organik.",
        "first_aid":"Bilas dengan air. Pantau ginjal dan paru. Segera ke dokter.","group":"Oksidator",
    },
    "Natrium Hipoklorit (NaOCl)": {
        "formula":"NaOCl","cas":"7681-52-9","fcot":["O","C"],
        "ghs":["GHS03","GHS05","GHS07","GHS09"],"description":"Oksidator/disinfektan, larutan pemutih. Melepas Cl₂ saat bereaksi dengan asam.",
        "class":"Oksidator / Disinfektan","ph":"11–12",
        "hazard":"Melepas gas Cl₂ dengan asam. Korosif. Berbahaya bagi lingkungan perairan.",
        "storage":"Wadah gelap, sejuk, TIDAK dicampur dengan asam atau amonia.",
        "first_aid":"Bilas mata/kulit. Pindahkan dari paparan gas. Ke dokter.","group":"Oksidator",
    },
    # ── GAS / HALOGEN ──
    "Gas Klorin (Cl₂)": {
        "formula":"Cl₂","cas":"7782-50-5","fcot":["O","T","C"],
        "ghs":["GHS03","GHS06","GHS05","GHS04"],"description":"Gas kuning kehijauan, sangat toksik. Digunakan dalam klorinasi air.",
        "class":"Gas Toksik / Oksidator","ph":"—",
        "hazard":"Gas toksik, penyebab kerusakan paru parah. Oksidator kuat.",
        "storage":"Silinder bertekanan, ventilasi sangat baik, jauh dari reduktor.",
        "first_aid":"Evakuasi segera. Oksigen murni. Panggil HAZMAT.","group":"Gas",
    },
    # ── GARAM & LAIN-LAIN ──
    "Natrium Klorida (NaCl)": {
        "formula":"NaCl","cas":"7647-14-5","fcot":[],
        "ghs":[],"description":"Garam dapur. Relatif tidak berbahaya dalam kondisi normal.",
        "class":"Garam Inert","ph":"7 (netral)",
        "hazard":"Minimal. Iritasi ringan jika terhirup debu dalam jumlah besar.",
        "storage":"Wadah tertutup, tempat kering.",
        "first_aid":"Bilas dengan air jika terkena mata.","group":"Garam",
    },
    "Natrium Bikarbonat (NaHCO₃)": {
        "formula":"NaHCO₃","cas":"144-55-8","fcot":[],
        "ghs":[],"description":"Baking soda. Basa lemah, digunakan menetralkan asam ringan.",
        "class":"Basa Sangat Lemah","ph":"8.3",
        "hazard":"Sangat rendah. Aman untuk penanganan umum.",
        "storage":"Wadah tertutup, kering.",
        "first_aid":"Bilas jika mengenai mata.","group":"Garam",
    },
    "Tembaga(II) Sulfat (CuSO₄)": {
        "formula":"CuSO₄","cas":"7758-99-8","fcot":["T"],
        "ghs":["GHS07","GHS09"],"description":"Garam tembaga biru. Fungisida dan reagen analitik.",
        "class":"Garam Logam Berat","ph":"3–4",
        "hazard":"Toksik bagi organisme air. Iritan kulit dan mata.",
        "storage":"Wadah tertutup, jauh dari sistem perairan.",
        "first_aid":"Bilas mata/kulit. Ke dokter jika tertelan.","group":"Garam",
    },
    "Formaldehida (HCHO)": {
        "formula":"HCHO","cas":"50-00-0","fcot":["T","F"],
        "ghs":["GHS02","GHS06","GHS08"],"description":"Karsinogen, iritan kuat, fiksatif jaringan.",
        "class":"Aldehida Toksik","ph":"—",
        "hazard":"Karsinogenik. Iritasi kuat pada mata, hidung, tenggorokan.",
        "storage":"Wadah tertutup, ventilasi, jauh dari api dan panas.",
        "first_aid":"Udara segar, bilas dengan air minimal 15 menit. Ke dokter.","group":"Lain-lain",
    },
    "Merkuri (Hg)": {
        "formula":"Hg","cas":"7439-97-6","fcot":["T"],
        "ghs":["GHS06","GHS08","GHS09"],"description":"Logam berat neurotoksik, uap berbahaya.",
        "class":"Logam Berat Toksik","ph":"—",
        "hazard":"Neurotoksik. Uap merkuri sangat berbahaya meski tidak terlihat.",
        "storage":"Wadah kedap, ventilasi tinggi, suhu rendah.",
        "first_aid":"Evakuasi area. Panggil HAZMAT. Jangan bersihkan dengan vacuum biasa.","group":"Logam",
    },
    "Sianida (KCN)": {
        "formula":"KCN","cas":"151-50-8","fcot":["T"],
        "ghs":["GHS06"],"description":"Sangat beracun, inhibitor enzim sitokrom c oksidase.",
        "class":"Toksik Sangat Berbahaya","ph":"11 (larutan)",
        "hazard":"Toksik akut. Gas HCN terbentuk dengan asam – mematikan.",
        "storage":"Lemari terkunci, jauh dari asam, ventilasi sangat baik.",
        "first_aid":"DARURAT: antidot hidroksokobalamin. Panggil 119 segera.","group":"Lain-lain",
    },
    "Arsenik Trioksida (As₂O₃)": {
        "formula":"As₂O₃","cas":"1327-53-3","fcot":["T"],
        "ghs":["GHS06","GHS08","GHS09"],"description":"Karsinogen klas 1, sangat toksik.",
        "class":"Senyawa Arsenik","ph":"—",
        "hazard":"Karsinogenik. Toksik akut. Bahaya lingkungan tinggi.",
        "storage":"Lemari terkunci, terpisah dari reduktor.",
        "first_aid":"DARURAT segera ke dokter.","group":"Lain-lain",
    },
    "Karbontetraklorida (CCl₄)": {
        "formula":"CCl₄","cas":"56-23-5","fcot":["T"],
        "ghs":["GHS06","GHS08"],"description":"Hepatotoksik & nefrotoksik, deplesi ozon.",
        "class":"Pelarut Halogen Toksik","ph":"7 (netral)",
        "hazard":"Hepatotoksik dan nefrotoksik kuat. Deplesi lapisan ozon.",
        "storage":"Wadah tertutup, ventilasi, jauh dari cahaya dan panas.",
        "first_aid":"Udara segar, pantau fungsi hati dan ginjal.","group":"Pelarut",
    },
    "Natrium (Na)": {
        "formula":"Na","cas":"7440-23-5","fcot":["F","C"],
        "ghs":["GHS02","GHS05"],"description":"Logam alkali reaktif, bereaksi keras dengan air.",
        "class":"Logam Alkali","ph":"—",
        "hazard":"Bereaksi eksplosif dengan air. Sangat mudah terbakar.",
        "storage":"Disimpan dalam minyak mineral, jauh dari air dan udara lembab.",
        "first_aid":"Jangan gunakan air. Padamkan dengan dry sand atau dry powder.","group":"Logam",
    },
    "Air/H₂O": {
        "formula":"H₂O","cas":"7732-18-5","fcot":[],
        "ghs":[],"description":"Pelarut universal. Aman dalam kondisi normal namun reaktif dengan logam aktif.",
        "class":"Pelarut Universal","ph":"7",
        "hazard":"Umumnya aman. Bereaksi keras dengan logam alkali.",
        "storage":"Wadah bersih, jauh dari logam alkali dan karbida.",
        "first_aid":"—","group":"Lain-lain",
    },
    "Kalsium Karbid (CaC₂)": {
        "formula":"CaC₂","cas":"75-20-7","fcot":["F"],
        "ghs":["GHS02","GHS07"],"description":"Bereaksi dengan air menghasilkan gas asetilena yang sangat mudah terbakar.",
        "class":"Senyawa Karbida","ph":"—",
        "hazard":"Menghasilkan C₂H₂ eksplosif dengan air.",
        "storage":"Wadah kering kedap udara. JAUHKAN dari air.",
        "first_aid":"Pindahkan dari area. Ventilasi. Jangan gunakan air.","group":"Lain-lain",
    },
}

# ─────────────────────────────────────────────
#  GHS LOOKUP
# ─────────────────────────────────────────────
GHS_INFO = {
    "GHS01":("💥","GHS01","Eksplosif"),
    "GHS02":("🔥","GHS02","Mudah Terbakar"),
    "GHS03":("⬆️🔥","GHS03","Oksidator"),
    "GHS04":("🔵","GHS04","Gas Bertekanan"),
    "GHS05":("🧪","GHS05","Korosif"),
    "GHS06":("☠️","GHS06","Toksik Akut"),
    "GHS07":("❗","GHS07","Bahaya/Iritan"),
    "GHS08":("⚠️","GHS08","Bahaya Kesehatan"),
    "GHS09":("🌿❌","GHS09","Bahaya Lingkungan"),
}

# ─────────────────────────────────────────────
#  DATABASE KOMPATIBILITAS PENYIMPANAN
#  Fokus: apakah dua bahan AMAN DISIMPAN BERDEKATAN
#  Ref: NFPA 49/430, OSHA 29 CFR 1910, COSHH, GHS Purple Book
# ─────────────────────────────────────────────
def _pair(a, b):
    return tuple(sorted([a, b]))

COMPAT_DB = {
    _pair("Asam Sulfat (H₂SO₄)","Natrium Hidroksida (NaOH)"): {
        "status":"DANGER","short":"Netralisasi Sangat Eksotermik – Semburan Korosif!",
        "reason":"H₂SO₄ (asam kuat) + NaOH (basa kuat) → panas sangat besar, dapat mendidihkan larutan dan menyemburkan cairan korosif.",
        "why_danger":"Panas yang dihasilkan (ΔH ≈ -57 kJ/mol) dapat mendidihkan larutan, menyemburkan cairan korosif ke wajah/tubuh. Risiko luka bakar kimia parah.",
        "reaction":"H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O  (+Panas besar)",
        "products":["Na₂SO₄","H₂O","Panas"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Kedua reaktan sangat korosif, panas reaksi berbahaya.",
    },
    _pair("Asam Klorida (HCl)","Natrium Hidroksida (NaOH)"): {
        "status":"DANGER","short":"Reaksi Netralisasi Sangat Eksotermik",
        "reason":"Asam kuat + basa kuat menghasilkan panas intens disertai semburan cairan korosif.",
        "why_danger":"Panas yang sangat besar dapat menyebabkan semburan larutan garam panas. Uap HCl juga berbahaya.",
        "reaction":"HCl + NaOH → NaCl + H₂O  (+Panas)",
        "products":["NaCl","H₂O","Panas"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Kedua zat korosif, panas reaksi berbahaya.",
    },
    _pair("Asam Nitrat (HNO₃)","Etanol (C₂H₅OH)"): {
        "status":"DANGER","short":"Reaksi Oksidasi – Risiko Kebakaran/Ledakan",
        "reason":"HNO₃ oksidator kuat + etanol reduktor mudah terbakar → panas intens, gas NO₂ toksik, berisiko ledakan.",
        "why_danger":"Campuran dapat menyala atau meledak secara spontan. Gas NO₂ sangat toksik.",
        "reaction":"HNO₃ + C₂H₅OH → (oksidasi) + NO₂↑ + H₂O + Panas",
        "products":["CO₂","H₂O","NO₂ (toksik)","Panas"],"fcot_involved":["F","O","C"],
        "theory":"Flammable (F) + Oxidator (O) + Corrosive (C): Bahan bakar + oksidator = bahaya kebakaran/ledakan.",
    },
    _pair("Asam Nitrat (HNO₃)","Aseton (C₃H₆O)"): {
        "status":"DANGER","short":"Oksidasi Eksplosif",
        "reason":"HNO₃ pekat + aseton membentuk campuran eksplosif dan senyawa nitro sensitif.",
        "why_danger":"Aseton dapat teroksidasi ke produk eksplosif. Panas reaksi memicu ledakan mendadak.",
        "reaction":"HNO₃ + (CH₃)₂CO → Produk nitro eksplosif + panas",
        "products":["Senyawa nitro eksplosif","CO₂","H₂O"],"fcot_involved":["F","O"],
        "theory":"Flammable (F) + Oxidator (O): Pelarut mudah terbakar + oksidator kuat = eksplosif.",
    },
    _pair("Kalium Permanganat (KMnO₄)","Asam Sulfat (H₂SO₄)"): {
        "status":"DANGER","short":"Oksidator + Asam Kuat – Campuran Eksplosif",
        "reason":"Menghasilkan campuran pengoksidasi sangat kuat (Mn₂O₇) yang dapat memicu kebakaran/ledakan spontan dengan bahan organik.",
        "why_danger":"Mn₂O₇ yang terbentuk adalah cairan eksplosif yang sangat berbahaya.",
        "reaction":"2KMnO₄ + H₂SO₄ → K₂SO₄ + 2HMnO₄ → (Mn₂O₇ + H₂O)",
        "products":["Mn₂O₇ (eksplosif)","K₂SO₄"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Campuran oksidator kuat dan asam pekat = sangat berbahaya.",
    },
    _pair("Natrium Hipoklorit (NaOCl)","Asam Klorida (HCl)"): {
        "status":"DANGER","short":"Gas Klorin Toksik Terbentuk!",
        "reason":"Pemutih (NaOCl) + asam (HCl) → gas Cl₂ yang sangat toksik dan korosif dilepaskan.",
        "why_danger":"Gas klorin menyebabkan kerusakan paru yang parah bahkan pada konsentrasi rendah. Kecelakaan laboratorium yang sering terjadi.",
        "reaction":"NaOCl + 2HCl → NaCl + H₂O + Cl₂↑",
        "products":["Cl₂ (GAS TOKSIK!)","NaCl","H₂O"],"fcot_involved":["O","T","C"],
        "theory":"Toxic (T) + Oxidator (O): Menghasilkan gas beracun yang sangat berbahaya.",
    },
    _pair("Natrium Hipoklorit (NaOCl)","Amonia (NH₃)"): {
        "status":"DANGER","short":"Gas Kloramin Toksik Terbentuk!",
        "reason":"Pemutih + amonia membentuk kloramin (NH₂Cl, NHCl₂, NCl₃) yang sangat toksik.",
        "why_danger":"Kloramin menyebabkan iritasi paru berat, edema paru, dan kematian. NCl₃ juga eksplosif.",
        "reaction":"NH₃ + NaOCl → NH₂Cl + NaOH / NHCl₂ / NCl₃",
        "products":["Kloramin (sangat toksik)","NaOH"],"fcot_involved":["T","O"],
        "theory":"Toxic (T) + Oxidator (O): Menghasilkan senyawa beracun berbahaya.",
    },
    _pair("Benzena (C₆H₆)","Asam Nitrat (HNO₃)"): {
        "status":"DANGER","short":"Reaksi Nitrasi – Produk Eksplosif",
        "reason":"Campuran nitrasi membentuk nitrobenzena dan dinitrobenzena yang eksplosif.",
        "why_danger":"Reaksi eksotermik. Dinitrobenzena dapat meledak.",
        "reaction":"C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O",
        "products":["Nitrobenzena (toksik)","Dinitrobenzena (eksplosif)","H₂O"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Reaksi nitrasi berbahaya.",
    },
    _pair("Asam Fluorida (HF)","Natrium Hidroksida (NaOH)"): {
        "status":"DANGER","short":"Netralisasi + Risiko HF Residual",
        "reason":"HF sangat berbahaya; netralisasi tidak sempurna menyisakan HF bebas yang masih toksik.",
        "why_danger":"HF dapat menembus kulit tanpa sensasi awal. Bahaya terlambat disadari.",
        "reaction":"HF + NaOH → NaF + H₂O",
        "products":["NaF (relatif aman)","H₂O","Panas"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): HF ekstrem berbahaya, penanganan memerlukan keahlian khusus.",
    },
    _pair("Kalium Dikromat (K₂Cr₂O₇)","Etanol (C₂H₅OH)"): {
        "status":"DANGER","short":"Oksidator Karsinogenik + Reduktor",
        "reason":"K₂Cr₂O₇ mengoksidasi etanol; menghasilkan senyawa kromium karsinogenik dan aldehida.",
        "why_danger":"Paparan produk reaksi (Cr³⁺ dan asetaldehida) bersifat karsinogenik dan toksik.",
        "reaction":"K₂Cr₂O₇ + C₂H₅OH + H₂SO₄ → Cr₂(SO₄)₃ + CH₃CHO + K₂SO₄ + H₂O",
        "products":["Kromium(III) sulfat","Asetaldehida (toksik)"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidator karsinogenik bereaksi dengan reduktor.",
    },
    _pair("Natrium (Na)","Air/H₂O"): {
        "status":"DANGER","short":"Reaksi Eksplosif dengan Air",
        "reason":"Natrium bereaksi sangat keras dengan air menghasilkan H₂ dan NaOH disertai ledakan dan api.",
        "why_danger":"Reaksi tak bisa dihentikan setelah dimulai. Gas H₂ langsung terbakar dari panas reaksi.",
        "reaction":"2Na + 2H₂O → 2NaOH + H₂↑ + Panas (dapat meledak)",
        "products":["NaOH (korosif)","H₂ (terbakar/meledak)","Panas besar"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Logam alkali + air = reaksi eksplosif.",
    },
    _pair("Kalsium Karbid (CaC₂)","Air/H₂O"): {
        "status":"DANGER","short":"Gas Asetilena Eksplosif",
        "reason":"CaC₂ + H₂O → gas asetilena (C₂H₂) yang sangat mudah terbakar dan eksplosif.",
        "why_danger":"Gas asetilena memiliki rentang ledakan lebar (2.5–100% di udara). Terbentuk dalam jumlah besar secara cepat.",
        "reaction":"CaC₂ + 2H₂O → Ca(OH)₂ + C₂H₂↑",
        "products":["Ca(OH)₂","C₂H₂ (Gas asetilena – sangat mudah terbakar!)"],"fcot_involved":["F"],
        "theory":"Flammable (F): Menghasilkan gas sangat mudah terbakar dengan rentang ledakan lebar.",
    },
    _pair("Asam Sulfat (H₂SO₄)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Dua Asam Kuat – Tidak Bereaksi tapi Keduanya Korosif",
        "reason":"H₂SO₄ dan HCl tidak bereaksi berbahaya, namun campuran dua asam kuat ini sangat korosif.",
        "why_caution":"Tidak ada reaksi berbahaya, namun campuran ini lebih korosif dari masing-masing. H₂SO₄ pekat dapat memfasilitasi penguapan HCl.",
        "reaction":"Tidak ada reaksi signifikan antar keduanya",
        "products":["Campuran asam kuat"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Keduanya sangat korosif, hati-hati dalam penanganan.",
    },
    _pair("Etanol (C₂H₅OH)","Hidrogen Peroksida (H₂O₂)"): {
        "status":"CAUTION","short":"Oksidator + Bahan Mudah Terbakar",
        "reason":"H₂O₂ adalah oksidator sedang; etanol adalah bahan mudah terbakar. Dalam kondisi panas atau konsentrasi tinggi dapat bereaksi.",
        "why_caution":"Konsentrasi tinggi H₂O₂ (>30%) dapat mengoksidasi etanol. Hindari panas.",
        "reaction":"C₂H₅OH + H₂O₂ → CH₃CHO + H₂O (jika H₂O₂ pekat)",
        "products":["Asetaldehida (toksik)","H₂O"],"fcot_involved":["F","O"],
        "theory":"Flammable (F) + Oxidator (O): Bahan bakar + oksidator harus diwaspadai.",
    },
    _pair("Asam Asetat (CH₃COOH)","Hidrogen Peroksida (H₂O₂)"): {
        "status":"CAUTION","short":"Membentuk Asam Peraseat – Oksidator Kuat",
        "reason":"Asam asetat + H₂O₂ membentuk asam peraseat (CH₃CO₃H), oksidator kuat yang korosif.",
        "why_caution":"Asam peraseat sangat korosif dan oksidatif. Digunakan disinfektan, namun perlu SOP ketat.",
        "reaction":"CH₃COOH + H₂O₂ ⇌ CH₃CO₃H + H₂O",
        "products":["Asam Peraseat (oksidator kuat, korosif)"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Produk peraseat oksidator berbahaya.",
    },
    _pair("Amonia (NH₃)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Asap Putih Ammonium Klorida",
        "reason":"Uap NH₃ + HCl bereaksi membentuk asap putih NH₄Cl. Reaksi eksotermik, uap awal berbahaya.",
        "why_caution":"Kedua zat toksik/korosif dalam fase gas. Asap NH₄Cl mengiritasi saluran napas.",
        "reaction":"NH₃(g) + HCl(g) → NH₄Cl(s) ↑ (asap putih)",
        "products":["NH₄Cl (Ammonium Klorida)"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Reaktan berbahaya, produk lebih aman, namun prosesnya perlu hati-hati.",
    },
    _pair("Kalium Permanganat (KMnO₄)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Gas Klorin dan Oksidasi Kuat",
        "reason":"KMnO₄ + HCl → melepas gas Cl₂. Hanya dalam lemari asam dengan pengawasan ketat.",
        "why_caution":"Gas Cl₂ yang terbentuk sangat toksik. Hanya lakukan dalam lemari asam.",
        "reaction":"2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂↑ + 8H₂O",
        "products":["Cl₂ (gas toksik)","MnCl₂","KCl"],"fcot_involved":["O","T","C"],
        "theory":"Oxidator (O) + Toxic (T) + Corrosive (C): Menghasilkan gas beracun.",
    },
    _pair("Metanol (CH₃OH)","Asam Sulfat (H₂SO₄)"): {
        "status":"CAUTION","short":"Esterifikasi – Perlu Kontrol Suhu",
        "reason":"H₂SO₄ mengkatalisis reaksi; dimetil sulfat yang mungkin terbentuk sangat toksik.",
        "why_caution":"Dimetil sulfat sangat toksik dan karsinogenik. Perlu kontrol suhu dan ventilasi.",
        "reaction":"2CH₃OH + H₂SO₄ → (CH₃)₂SO₄ + 2H₂O (pada suhu tinggi)",
        "products":["Dimetil sulfat (sangat toksik!)","H₂O"],"fcot_involved":["F","C","T"],
        "theory":"Flammable (F) + Corrosive (C) + Toxic (T): Produk reaksi sangat berbahaya.",
    },
    _pair("Kloroform (CHCl₃)","Aseton (C₃H₆O)"): {
        "status":"CAUTION","short":"Potensi Pembentukan Kloroaseton jika Ada Basa",
        "reason":"Dalam kondisi normal digunakan untuk ekstraksi. Namun dengan basa kuat dapat membentuk kloroaseton berbahaya.",
        "why_caution":"Jika ada basa kuat (NaOH) → reaksi haloform membentuk kloroaseton toksik. Hindari pencampuran dengan basa.",
        "reaction":"CHCl₃ + Aseton + NaOH → Kloroaseton + produk lain",
        "products":["Kloroaseton (lakrimator/toksik) jika ada basa"],"fcot_involved":["T"],
        "theory":"Toxic (T): Campuran berpotensi membentuk produk berbahaya dalam kondisi tertentu.",
    },
    _pair("Natrium Bikarbonat (NaHCO₃)","Asam Sulfat (H₂SO₄)"): {
        "status":"CAUTION","short":"Netralisasi – Gas CO₂ Terbentuk",
        "reason":"Asam + bikarbonat → CO₂ dalam jumlah besar. Dalam wadah tertutup dapat meledak karena tekanan gas.",
        "why_caution":"Pastikan wadah tidak tertutup rapat saat mencampurkan. Gas CO₂ dapat menggantikan oksigen di ruang tertutup.",
        "reaction":"2NaHCO₃ + H₂SO₄ → Na₂SO₄ + 2H₂O + 2CO₂↑",
        "products":["Na₂SO₄","H₂O","CO₂ (gas)"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Asam kuat bereaksi dengan garam karbonat melepas gas CO₂.",
    },
    _pair("Natrium Klorida (NaCl)","Natrium Bikarbonat (NaHCO₃)"): {
        "status":"SAFE","short":"Dua Garam Netral – Aman Disimpan Bersama",
        "reason":"NaCl dan NaHCO₃ tidak bereaksi satu sama lain dan keduanya bersifat relatif inert.",
        "why_safe":"Tidak ada reaksi kimia signifikan antara keduanya. Profil bahaya rendah. Aman disimpan di lokasi yang sama.",
        "reaction":"Tidak ada reaksi",
        "products":["—"],"fcot_involved":[],
        "theory":"Tidak ada FCOT yang relevan. Keduanya inert satu sama lain.",
    },
    _pair("Etanol (C₂H₅OH)","Aseton (C₃H₆O)"): {
        "status":"SAFE","short":"Dua Pelarut Organik – Miscible, Tidak Bereaksi",
        "reason":"Etanol dan aseton saling larut sempurna tanpa reaksi kimia. Digunakan campuran dalam pembersih laboratorium.",
        "why_safe":"Tidak ada reaksi kimia antara keduanya. Keduanya pelarut polar. Aman dicampurkan untuk keperluan pembersihan.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut organik"],"fcot_involved":["F"],
        "theory":"Flammable (F): Keduanya mudah terbakar, hati-hati dari api/panas. Tapi tidak reaktif satu sama lain.",
    },
    _pair("Asam Fosfat (H₃PO₄)","Natrium Bikarbonat (NaHCO₃)"): {
        "status":"SAFE","short":"Netralisasi Terkontrol – Produk Aman",
        "reason":"H₃PO₄ (asam lemah-sedang) + NaHCO₃ (basa lemah) → garam fosfat + CO₂ + air. Reaksi terkontrol.",
        "why_safe":"Asam fosfat jauh lebih lemah dari H₂SO₄. Reaksi terkontrol dengan CO₂ pelan-pelan. Produk aman.",
        "reaction":"H₃PO₄ + 3NaHCO₃ → Na₃PO₄ + 3H₂O + 3CO₂↑",
        "products":["Na₃PO₄","H₂O","CO₂"],"fcot_involved":["C"],
        "theory":"Corrosive (C) ringan: H₃PO₄ agak korosif, tapi reaksi relatif aman.",
    },
    _pair("Kalsium Hidroksida (Ca(OH)₂)","Asam Fosfat (H₃PO₄)"): {
        "status":"SAFE","short":"Pembentukan Kalsium Fosfat – Reaksi Terkontrol",
        "reason":"Basa sedang + asam sedang → kalsium fosfat yang tidak larut dan air.",
        "why_safe":"Reaksi netralisasi terkontrol. Produk kalsium fosfat adalah komponen pupuk. Tidak ada gas berbahaya.",
        "reaction":"3Ca(OH)₂ + 2H₃PO₄ → Ca₃(PO₄)₂↓ + 6H₂O",
        "products":["Ca₃(PO₄)₂ (endapan aman)","H₂O"],"fcot_involved":[],
        "theory":"Corrosive (C) lemah: Keduanya sedikit korosif, tapi reaksinya aman dan produknya inert.",
    },
    # ── TAMBAHAN PASANGAN LENGKAP ──
    _pair("Asam Sulfat (H₂SO₄)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Campuran Sangat Oksidatif – Potensi Ledakan",
        "reason":"H₂SO₄ pekat + KMnO₄ membentuk Mn₂O₇ yang sangat tidak stabil dan eksplosif.",
        "why_danger":"Mn₂O₇ (diasam mangan) adalah cairan eksplosif yang dapat menyala secara spontan dengan bahan organik. Reaksi tak terkendali.",
        "reaction":"2KMnO₄ + H₂SO₄ → K₂SO₄ + 2HMnO₄ → Mn₂O₇ + H₂O",
        "products":["Mn₂O₇ (eksplosif)","K₂SO₄"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Pembentukan senyawa oksidator ekstrem.",
    },
    _pair("Asam Sulfat (H₂SO₄)","Etanol (C₂H₅OH)"): {
        "status":"DANGER","short":"Dehidrasi & Oksidasi – Panas Intens + Gas Berbahaya",
        "reason":"H₂SO₄ pekat mendehidrasi etanol menghasilkan dietil eter atau etilena. Reaksi sangat eksotermik, risiko kebakaran.",
        "why_danger":"Panas reaksi dapat menyulut uap etanol. Pada suhu tinggi membentuk gas etilena yang mudah terbakar.",
        "reaction":"C₂H₅OH + H₂SO₄(pekat) → C₂H₄↑ + H₂O + SO₂ (panas tinggi)",
        "products":["Etilena (gas mudah terbakar)","H₂O","Panas"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Asam kuat mendehidrasi pelarut mudah terbakar, risiko kebakaran.",
    },
    _pair("Asam Sulfat (H₂SO₄)","Aseton (C₃H₆O)"): {
        "status":"DANGER","short":"Oksidasi Aseton – Reaksi Eksotermik Berbahaya",
        "reason":"H₂SO₄ pekat bereaksi dengan aseton menghasilkan panas besar dan produk oksidasi berbahaya.",
        "why_danger":"Reaksi sangat eksotermik dapat menyulut uap aseton. Produk tidak stabil dapat terbentuk.",
        "reaction":"(CH₃)₂CO + H₂SO₄ → produk oksidasi + CO₂ + H₂O + panas",
        "products":["Produk oksidasi campuran","CO₂","Panas besar"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Asam kuat + pelarut mudah terbakar = risiko kebakaran/ledakan.",
    },
    _pair("Asam Sulfat (H₂SO₄)","Amonia (NH₃)"): {
        "status":"DANGER","short":"Netralisasi Eksotermik + Asap Amonium Sulfat",
        "reason":"Asam kuat + basa volatil menghasilkan panas besar dan asap ammonium sulfat yang mengiritasi.",
        "why_danger":"Reaksi sangat eksotermik. Uap NH₃ yang bereaksi membentuk kabut amonium sulfat berbahaya untuk pernapasan.",
        "reaction":"H₂SO₄ + 2NH₃ → (NH₄)₂SO₄ + Panas besar",
        "products":["(NH₄)₂SO₄","Panas besar","Asap iritan"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Asam kuat + basa volatil toksik = reaksi berbahaya.",
    },
    _pair("Asam Sulfat (H₂SO₄)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Gas Klorin Toksik + Asam Kuat",
        "reason":"Asam kuat menguraikan NaOCl melepaskan gas Cl₂ yang sangat toksik.",
        "why_danger":"Gas klorin sangat toksik meski dalam jumlah kecil. Dapat menyebabkan edema paru dan kematian.",
        "reaction":"H₂SO₄ + NaOCl → NaHSO₄ + HOCl → Cl₂↑ + H₂O",
        "products":["Cl₂ (GAS TOKSIK!)","NaHSO₄"],"fcot_involved":["O","T","C"],
        "theory":"Toxic (T) + Oxidator (O): Asam menguraikan oksidator hipoklorit melepas gas beracun.",
    },
    _pair("Asam Klorida (HCl)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Gas Klorin Toksik Terbentuk",
        "reason":"KMnO₄ mengoksidasi HCl melepaskan gas Cl₂ yang sangat toksik.",
        "why_danger":"Gas klorin sangat korosif pada saluran napas. Wajib dilakukan dalam lemari asam.",
        "reaction":"2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂↑ + 8H₂O",
        "products":["Cl₂ (gas toksik)","MnCl₂","KCl"],"fcot_involved":["O","T","C"],
        "theory":"Oxidator (O) + Toxic (T): Oksidator kuat bereaksi dengan asam melepas gas halogen beracun.",
    },
    _pair("Asam Klorida (HCl)","Kalium Hidroksida (KOH)"): {
        "status":"DANGER","short":"Netralisasi Sangat Eksotermik",
        "reason":"Asam kuat + basa kuat → panas besar, risiko semburan cairan korosif.",
        "why_danger":"Reaksi netralisasi menghasilkan panas tinggi yang dapat mendidihkan larutan dan menyemburkan cairan korosif.",
        "reaction":"HCl + KOH → KCl + H₂O + Panas",
        "products":["KCl","H₂O","Panas besar"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Dua zat sangat korosif bereaksi menghasilkan panas berbahaya.",
    },
    _pair("Asam Klorida (HCl)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Asap Putih Amonium Klorida – Iritan Pernapasan",
        "reason":"Uap HCl + NH₃ bereaksi membentuk asap putih NH₄Cl yang mengiritasi.",
        "why_caution":"Asap NH₄Cl mengiritasi saluran pernapasan. Kedua reaktan toksik/korosif dalam fase gas.",
        "reaction":"HCl(g) + NH₃(g) → NH₄Cl(s) asap putih",
        "products":["NH₄Cl (asap iritan)"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Uap reaktan berbahaya; produk lebih aman namun prosesnya perlu ventilasi.",
    },
    _pair("Asam Klorida (HCl)","Kalsium Hidroksida (Ca(OH)₂)"): {
        "status":"DANGER","short":"Netralisasi Eksotermik Asam Kuat + Basa",
        "reason":"HCl (asam kuat) + Ca(OH)₂ (basa sedang) → panas signifikan dan produk korosif.",
        "why_danger":"Reaksi eksotermik dan kedua zat sangat korosif. Uap HCl berbahaya jika terhirup.",
        "reaction":"2HCl + Ca(OH)₂ → CaCl₂ + 2H₂O + Panas",
        "products":["CaCl₂","H₂O","Panas"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Asam kuat + basa = reaksi netralisasi berbahaya.",
    },
    _pair("Asam Nitrat (HNO₃)","Natrium Hidroksida (NaOH)"): {
        "status":"DANGER","short":"Netralisasi Eksotermik + Oksidator Kuat",
        "reason":"HNO₃ adalah asam kuat sekaligus oksidator; reaksi dengan NaOH sangat eksotermik.",
        "why_danger":"Panas besar dapat mendidihkan larutan. Sifat oksidatif HNO₃ menambah risiko.",
        "reaction":"HNO₃ + NaOH → NaNO₃ + H₂O + Panas",
        "products":["NaNO₃","H₂O","Panas besar"],"fcot_involved":["C","O"],
        "theory":"Corrosive (C) + Oxidator (O): Asam oksidatif kuat + basa kuat = reaksi berbahaya.",
    },
    _pair("Asam Nitrat (HNO₃)","Amonia (NH₃)"): {
        "status":"DANGER","short":"Ammonium Nitrat – Potensi Ledakan",
        "reason":"HNO₃ + NH₃ membentuk amonium nitrat (NH₄NO₃) yang merupakan bahan peledak.",
        "why_danger":"Amonium nitrat adalah bahan peledak kuat. Campuran ini sangat berbahaya dan berpotensi meledak.",
        "reaction":"HNO₃ + NH₃ → NH₄NO₃ (amonium nitrat – EKSPLOSIF)",
        "products":["NH₄NO₃ (eksplosif!)"],"fcot_involved":["O","C","T"],
        "theory":"Oxidator (O) + Corrosive (C): Produk amonium nitrat adalah bahan peledak berbahaya.",
    },
    _pair("Asam Nitrat (HNO₃)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Dua Oksidator Kuat + Asam – Sangat Berbahaya",
        "reason":"Dua oksidator kuat bercampur dengan asam kuat, menghasilkan campuran sangat reaktif dan gas toksik.",
        "why_danger":"Dapat menghasilkan gas klorin dan nitrogen dioksida yang keduanya sangat toksik.",
        "reaction":"HNO₃ + NaOCl → NaNO₃ + HOCl → Cl₂↑ + gas NOₓ",
        "products":["Cl₂ (toksik)","NOₓ (toksik)"],"fcot_involved":["O","C","T"],
        "theory":"Oxidator (O) + Corrosive (C) + Toxic (T): Kombinasi oksidator-asam berbahaya.",
    },
    _pair("Asam Nitrat (HNO₃)","Kalium Hidroksida (KOH)"): {
        "status":"DANGER","short":"Netralisasi Sangat Eksotermik – Oksidator + Basa Kuat",
        "reason":"Asam kuat oksidatif + basa kuat menghasilkan panas besar dan risiko semburan.",
        "why_danger":"Panas besar + sifat oksidatif HNO₃ + kaustisitas KOH = sangat berbahaya.",
        "reaction":"HNO₃ + KOH → KNO₃ + H₂O + Panas",
        "products":["KNO₃","H₂O","Panas besar"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Asam oksidator kuat bereaksi dengan basa kuat.",
    },
    _pair("Asam Nitrat (HNO₃)","Kalsium Hidroksida (Ca(OH)₂)"): {
        "status":"DANGER","short":"Netralisasi Eksotermik + Sifat Oksidatif",
        "reason":"Asam oksidatif kuat + basa → panas, risiko semburan cairan korosif.",
        "why_danger":"Reaksi eksotermik disertai sifat oksidatif HNO₃ meningkatkan risiko kebakaran jika ada bahan organik.",
        "reaction":"2HNO₃ + Ca(OH)₂ → Ca(NO₃)₂ + 2H₂O + Panas",
        "products":["Ca(NO₃)₂","H₂O","Panas"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Asam oksidatif + basa = reaksi berbahaya.",
    },
    _pair("Asam Asetat (CH₃COOH)","Natrium Hidroksida (NaOH)"): {
        "status":"CAUTION","short":"Netralisasi Terkontrol – Asam Lemah + Basa Kuat",
        "reason":"Asam lemah + basa kuat menghasilkan natrium asetat dan air. Reaksi lebih terkontrol dibanding asam kuat.",
        "why_caution":"NaOH tetap sangat korosif. Reaksi eksotermik lebih ringan, namun tetap perlu APD dan hati-hati.",
        "reaction":"CH₃COOH + NaOH → CH₃COONa + H₂O + Panas ringan",
        "products":["CH₃COONa (natrium asetat)","H₂O"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Asam lemah + basa kuat, reaksi lebih aman namun NaOH tetap korosif.",
    },
    _pair("Asam Asetat (CH₃COOH)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Kuat – Risiko Kebakaran",
        "reason":"KMnO₄ mengoksidasi asam asetat dengan kuat; reaksi dapat menyulut pembakaran.",
        "why_danger":"Asam asetat mudah terbakar (titik nyala 39°C) dan KMnO₄ oksidator kuat. Kombinasi berbahaya.",
        "reaction":"CH₃COOH + KMnO₄ → CO₂ + H₂O + MnO₂ + panas",
        "products":["CO₂","H₂O","MnO₂","Panas besar"],"fcot_involved":["F","O","C"],
        "theory":"Flammable (F) + Oxidator (O): Bahan mudah terbakar + oksidator kuat = risiko kebakaran.",
    },
    _pair("Asam Asetat (CH₃COOH)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Pembentukan Amonium Asetat – Asap Iritan",
        "reason":"Asam asetat + amonia membentuk amonium asetat disertai asap yang mengiritasi.",
        "why_caution":"Uap amonia dan asam asetat mengiritasi pernapasan. Reaksi lebih aman dari asam kuat + basa kuat.",
        "reaction":"CH₃COOH + NH₃ → CH₃COONH₄",
        "products":["CH₃COONH₄ (amonium asetat)"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Uap reaktan mengiritasi; produk relatif aman.",
    },
    _pair("Asam Fosfat (H₃PO₄)","Natrium Hidroksida (NaOH)"): {
        "status":"CAUTION","short":"Netralisasi Terkontrol – Produk Aman",
        "reason":"Asam sedang + basa kuat → natrium fosfat dan air. Reaksi moderat.",
        "why_caution":"NaOH sangat korosif. Reaksi lebih terkontrol dari asam kuat namun tetap perlu kehati-hatian.",
        "reaction":"H₃PO₄ + 3NaOH → Na₃PO₄ + 3H₂O + Panas",
        "products":["Na₃PO₄","H₂O"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Asam sedang + basa kuat, reaksi terkontrol namun tetap berbahaya.",
    },
    _pair("Asam Fosfat (H₃PO₄)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Pembentukan Amonium Fosfat – Asap Ringan",
        "reason":"H₃PO₄ + NH₃ membentuk amonium fosfat (pupuk). Reaksi moderat dengan asap ringan.",
        "why_caution":"Uap amonia mengiritasi. Produk amonium fosfat relatif aman (digunakan sebagai pupuk).",
        "reaction":"H₃PO₄ + 3NH₃ → (NH₄)₃PO₄",
        "products":["(NH₄)₃PO₄ (amonium fosfat)"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Asap amonia iritan; produk akhir aman.",
    },
    _pair("Asam Fluorida (HF)","Kalium Hidroksida (KOH)"): {
        "status":"DANGER","short":"HF + Basa Kuat – Sangat Berbahaya",
        "reason":"HF sangat berbahaya; netralisasi dengan KOH kuat menghasilkan panas dan fluorida.",
        "why_danger":"HF dapat menembus kulit; KOH sangat korosif. Penanganan HF memerlukan keahlian khusus dan gel kalsium glukonat.",
        "reaction":"HF + KOH → KF + H₂O + Panas",
        "products":["KF","H₂O","Panas"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): HF ekstrem berbahaya, kombinasi dengan basa kuat perlu kehati-hatian luar biasa.",
    },
    _pair("Asam Fluorida (HF)","Amonia (NH₃)"): {
        "status":"DANGER","short":"HF + Gas Toksik – Sangat Berbahaya",
        "reason":"HF sangat toksik; bercampur dengan amonia toksik menghasilkan ammonium fluorida dan risiko paparan ganda.",
        "why_danger":"Kedua zat sangat toksik dan korosif. HF dapat menembus kulit tanpa terasa.",
        "reaction":"HF + NH₃ → NH₄F",
        "products":["NH₄F (fluorida toksik)"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Dua zat sangat berbahaya; hindari kontak.",
    },
    _pair("Natrium Hidroksida (NaOH)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Basa Kuat + Oksidator Kuat",
        "reason":"NaOH dapat mempercepat dekomposisi KMnO₄, melepas oksigen dan mangane oksida.",
        "why_danger":"Dekomposisi KMnO₄ yang dipercepat dapat melepas O₂ dan panas, risiko kebakaran dengan bahan organik.",
        "reaction":"4KMnO₄ + 4KOH → 4K₂MnO₄ + O₂↑ + 2H₂O",
        "products":["K₂MnO₄","O₂ (gas)","H₂O"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Basa mempercepat dekomposisi oksidator.",
    },
    _pair("Natrium Hidroksida (NaOH)","Natrium Hipoklorit (NaOCl)"): {
        "status":"SAFE","short":"Stabilitasi Larutan Hipoklorit",
        "reason":"NaOH dalam larutan hipoklorit justru menstabilkannya dan mencegah dekomposisi.",
        "why_safe":"Produk komersial pemutih mengandung NaOH sebagai stabilizer. Kombinasi ini aman dan sengaja digunakan industri.",
        "reaction":"NaOH + NaOCl → larutan stabil (tidak ada reaksi tambahan)",
        "products":["Larutan hipoklorit yang stabil"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Basa menstabilkan hipoklorit. Tidak ada reaksi berbahaya.",
    },
    _pair("Natrium Hidroksida (NaOH)","Kalsium Hidroksida (Ca(OH)₂)"): {
        "status":"SAFE","short":"Dua Basa Kuat – Tidak Saling Bereaksi",
        "reason":"Dua basa kuat tidak bereaksi satu sama lain secara berbahaya.",
        "why_safe":"Tidak ada reaksi kimia signifikan antara NaOH dan Ca(OH)₂. Keduanya basa, aman disimpan bersamaan dalam lemari alkali.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran basa"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Sesama basa korosif, tidak bereaksi satu sama lain.",
    },
    _pair("Kalium Hidroksida (KOH)","Natrium Hipoklorit (NaOCl)"): {
        "status":"SAFE","short":"Basa + Hipoklorit – Stabil",
        "reason":"KOH menstabilkan larutan hipoklorit, mirip dengan efek NaOH.",
        "why_safe":"Basa alkali menstabilkan hipoklorit. Tidak ada produk berbahaya terbentuk.",
        "reaction":"KOH + NaOCl → larutan stabil",
        "products":["Larutan stabil"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Basa menstabilkan oksidator hipoklorit.",
    },
    _pair("Kalium Hidroksida (KOH)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Dua Basa – Uap Amonia Tetap Berbahaya",
        "reason":"KOH dan NH₃ keduanya basa. Tidak bereaksi berbahaya, namun uap amonia tetap toksik.",
        "why_caution":"Tidak ada reaksi kimia berbahaya, tetapi uap NH₃ mengiritasi. KOH sangat korosif. Ventilasi baik diperlukan.",
        "reaction":"Tidak ada reaksi signifikan",
        "products":["—"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Uap amonia berbahaya meski tidak bereaksi dengan KOH.",
    },
    _pair("Kalium Hidroksida (KOH)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Basa Kuat Mempercepat Dekomposisi Oksidator",
        "reason":"KOH dapat mempercepat dekomposisi KMnO₄ melepas oksigen dan panas.",
        "why_danger":"O₂ yang dilepas dapat memicu kebakaran dengan bahan organik di sekitarnya.",
        "reaction":"4KMnO₄ + 4KOH → 4K₂MnO₄ + O₂↑ + 2H₂O",
        "products":["K₂MnO₄","O₂ (gas)","Panas"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Basa kuat tidak boleh berdekatan dengan oksidator kuat.",
    },
    _pair("Amonia (NH₃)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Gas Kloramin Mematikan",
        "reason":"NH₃ + NaOCl → kloramin (NH₂Cl, NHCl₂, NCl₃) yang sangat toksik.",
        "why_danger":"Kloramin menyebabkan edema paru dan kematian. Reaksi umum penyebab kecelakaan di rumah tangga (campur pemutih + pembersih amonia).",
        "reaction":"NH₃ + NaOCl → NH₂Cl + NaOH (kloramin terbentuk)",
        "products":["Kloramin (sangat toksik)","NaOH"],"fcot_involved":["T","O"],
        "theory":"Toxic (T) + Oxidator (O): Gas kloramin sangat berbahaya bagi pernapasan.",
    },
    _pair("Amonia (NH₃)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Amonia – Gas Nitrogen Oksida Toksik",
        "reason":"KMnO₄ mengoksidasi amonia menghasilkan nitrogen oksida (NOₓ) yang sangat toksik.",
        "why_danger":"Gas NOₓ sangat toksik bagi paru-paru. Reaksi dapat terjadi secara eksplosif.",
        "reaction":"NH₃ + KMnO₄ → NOₓ↑ + MnO₂ + H₂O + K₂O",
        "products":["NOₓ (sangat toksik)","MnO₂"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidator kuat mengoksidasi amonia menghasilkan gas beracun.",
    },
    _pair("Amonia (NH₃)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Pelarut Mudah Terbakar + Gas Toksik",
        "reason":"Tidak bereaksi langsung, namun uap amonia dan etanol keduanya berbahaya dalam ruang tertutup.",
        "why_caution":"Uap amonia toksik; etanol mudah terbakar. Bersama dalam ruang tertutup meningkatkan risiko ledakan atau keracunan.",
        "reaction":"Tidak ada reaksi kimia signifikan",
        "products":["—"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Uap campuran berbahaya; butuh ventilasi baik.",
    },
    _pair("Etanol (C₂H₅OH)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Pembentukan Kloroetanol + Kloroform – Toksik",
        "reason":"Etanol + NaOCl dapat membentuk kloroetanol dan kloroform yang keduanya toksik.",
        "why_danger":"Kloroform (CHCl₃) bersifat karsinogenik dan narkotika. Reaksi dapat menghasilkan campuran berbahaya.",
        "reaction":"C₂H₅OH + NaOCl → CHCl₃ + produk klorinasi lain",
        "products":["Kloroform (karsinogenik)","Kloroetanol (toksik)"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Oksidator mengklorinasi pelarut menghasilkan produk toksik.",
    },
    _pair("Etanol (C₂H₅OH)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Kuat – Risiko Kebakaran/Ledakan",
        "reason":"KMnO₄ mengoksidasi etanol dengan kuat. Reaksi eksotermik dapat menyulut pembakaran.",
        "why_danger":"Campuran KMnO₄ + etanol dapat terbakar secara spontan. Sering digunakan sebagai demonstrasi reaksi penyalaan.",
        "reaction":"C₂H₅OH + KMnO₄ → CH₃CHO + CO₂ + MnO₂ + panas",
        "products":["Asetaldehida (toksik)","CO₂","MnO₂","Panas/Api"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O): Oksidator kuat + pelarut mudah terbakar = kebakaran spontan.",
    },
    _pair("Etanol (C₂H₅OH)","Aseton (C₃H₆O)"): {
        "status":"SAFE","short":"Dua Pelarut Organik Mudah Terbakar – Larut Sempurna",
        "reason":"Etanol dan aseton saling larut sempurna tanpa reaksi kimia. Campuran umum dalam pembersih laboratorium.",
        "why_safe":"Tidak ada reaksi kimia. Digunakan secara rutin sebagai campuran pembersih. Yang perlu diperhatikan hanyalah sifat mudah terbakarnya.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut organik"],"fcot_involved":["F"],
        "theory":"Flammable (F): Keduanya mudah terbakar, jauhkan dari api. Tidak reaktif satu sama lain.",
    },
    _pair("Metanol (CH₃OH)","Etanol (C₂H₅OH)"): {
        "status":"SAFE","short":"Dua Alkohol – Larut, Tidak Bereaksi",
        "reason":"Metanol dan etanol larut sempurna satu sama lain tanpa reaksi kimia berbahaya.",
        "why_safe":"Tidak ada reaksi. Namun metanol SANGAT TOKSIK jika tertelan/terhirup. Pisahkan label dengan jelas.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran alkohol"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Tidak bereaksi, namun metanol toksik harus diberi label jelas.",
    },
    _pair("Metanol (CH₃OH)","Aseton (C₃H₆O)"): {
        "status":"SAFE","short":"Dua Pelarut Organik – Larut, Tidak Bereaksi",
        "reason":"Metanol dan aseton larut sempurna tanpa reaksi kimia.",
        "why_safe":"Tidak ada reaksi. Keduanya mudah terbakar dan metanol toksik; ventilasi baik dan jauhkan dari api.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Mudah terbakar, metanol toksik; tidak saling bereaksi.",
    },
    _pair("Metanol (CH₃OH)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Klorinasi Metanol – Produk Toksik",
        "reason":"Metanol + hipoklorit dapat membentuk kloroform dan produk klorinasi lain yang toksik.",
        "why_danger":"Kloroform bersifat karsinogenik. Metanol sendiri sangat toksik. Kombinasi berbahaya.",
        "reaction":"CH₃OH + NaOCl → CHCl₃ + produk klorinasi",
        "products":["Kloroform (karsinogenik)","Produk klorinasi toksik"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Oksidator mengklorinasi alkohol toksik.",
    },
    _pair("Metanol (CH₃OH)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Metanol – Formaldehida Karsinogenik",
        "reason":"KMnO₄ mengoksidasi metanol menjadi formaldehida yang karsinogenik.",
        "why_danger":"Formaldehida adalah karsinogen kelas 1 dan sangat iritan. Reaksi eksotermik dapat menyulut api.",
        "reaction":"CH₃OH + KMnO₄ → HCHO + MnO₂ + H₂O + panas",
        "products":["Formaldehida (HCHO, karsinogenik)","MnO₂"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Oksidasi menghasilkan produk karsinogenik.",
    },
    _pair("Aseton (C₃H₆O)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Reaksi Haloform – Kloroform Terbentuk",
        "reason":"Aseton + hipoklorit bereaksi melalui reaksi haloform menghasilkan kloroform.",
        "why_danger":"Kloroform bersifat karsinogenik dan narkotika. Reaksi terjadi pada suhu kamar.",
        "reaction":"(CH₃)₂CO + 3NaOCl → CHCl₃ + CH₃COONa + 2NaOH",
        "products":["Kloroform CHCl₃ (karsinogenik)","NaOH"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O): Reaksi haloform menghasilkan produk toksik.",
    },
    _pair("Aseton (C₃H₆O)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Kuat – Kebakaran/Ledakan",
        "reason":"KMnO₄ mengoksidasi aseton kuat; reaksi eksotermik dapat menyulut pembakaran spontan.",
        "why_danger":"Campuran KMnO₄ + aseton berisiko terbakar spontan. Aseton titik nyala -20°C.",
        "reaction":"(CH₃)₂CO + KMnO₄ → CH₃COOH + CO₂ + MnO₂ + panas",
        "products":["Asam asetat","CO₂","MnO₂","Panas/Api"],"fcot_involved":["F","O"],
        "theory":"Flammable (F) + Oxidator (O): Oksidator kuat + pelarut mudah terbakar = sangat berbahaya.",
    },
    _pair("Aseton (C₃H₆O)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Kondensasi Aldol – Produk Sedikit Berbahaya",
        "reason":"Aseton + amonia dapat membentuk diacetone amine dalam kondisi tertentu. Uap keduanya iritan.",
        "why_caution":"Tidak ada reaksi spontan pada suhu kamar. Uap campuran mengiritasi. Ventilasi diperlukan.",
        "reaction":"(CH₃)₂CO + NH₃ → diacetone amine (kondisi tertentu)",
        "products":["Diacetone amine (iritan)"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Uap campuran iritan; tidak bereaksi hebat pada suhu kamar.",
    },
    _pair("Kloroform (CHCl₃)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Oksidasi Kloroform – Gas Fosgen Terbentuk",
        "reason":"Hipoklorit dapat mengoksidasi kloroform menghasilkan fosgen (COCl₂) yang sangat toksik.",
        "why_danger":"Fosgen adalah gas perang kimia, sangat toksik. Bahkan konsentrasi rendah berbahaya.",
        "reaction":"CHCl₃ + NaOCl → COCl₂↑ (fosgen) + NaCl + HCl",
        "products":["Fosgen COCl₂ (GAS PERANG – MEMATIKAN)","NaCl","HCl"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidasi kloroform menghasilkan fosgen yang mematikan.",
    },
    _pair("Benzena (C₆H₆)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Klorinasi Benzena – Produk Toksik Karsinogen",
        "reason":"Hipoklorit mengklorinasi benzena menghasilkan klorobenzena dan produk klorinasi lain yang toksik.",
        "why_danger":"Klorobenzena dan diklorobenzena bersifat toksik dan karsinogenik. Benzena sendiri karsinogen kelas 1.",
        "reaction":"C₆H₆ + NaOCl → C₆H₅Cl + produk klorinasi lain",
        "products":["Klorobenzena (toksik)","Produk klorinasi karsinogenik"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Klorinasi hidrokarbon aromatik menghasilkan produk berbahaya.",
    },
    _pair("Benzena (C₆H₆)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Dua Pelarut Mudah Terbakar – Toksisitas Tinggi",
        "reason":"Benzena dan etanol larut sempurna. Tidak bereaksi, namun campuran tetap sangat mudah terbakar dan toksik.",
        "why_caution":"Benzena karsinogen kelas 1. Campuran sangat mudah terbakar. Ventilasi lemari asam wajib.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut mudah terbakar"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Keduanya mudah terbakar; benzena sangat karsinogenik.",
    },
    _pair("Benzena (C₆H₆)","Aseton (C₃H₆O)"): {
        "status":"CAUTION","short":"Dua Pelarut Mudah Terbakar – Campuran Berbahaya",
        "reason":"Benzena dan aseton larut sempurna. Tidak bereaksi, namun campuran sangat mudah terbakar.",
        "why_caution":"Campuran memiliki titik nyala sangat rendah. Benzena karsinogen. Jauhkan dari semua sumber api.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Campuran pelarut mudah terbakar dengan benzena karsinogenik.",
    },
    _pair("Benzena (C₆H₆)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Benzena – Panas Intens + Api",
        "reason":"KMnO₄ mengoksidasi benzena dengan sangat kuat, melepas panas intens dan risiko kebakaran/ledakan.",
        "why_danger":"Benzena mudah terbakar + oksidator kuat. Campuran dapat menyulut api spontan.",
        "reaction":"C₆H₆ + KMnO₄ → CO₂ + H₂O + MnO₂ + panas/api",
        "products":["CO₂","H₂O","MnO₂","Panas/Api"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O): Oksidator kuat dengan hidrokarbon aromatik = sangat berbahaya.",
    },
    _pair("Hidrogen Peroksida (H₂O₂)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Dua Oksidator Kuat – Reaksi Eksplosif",
        "reason":"KMnO₄ mengkatalisis dekomposisi H₂O₂ dengan sangat cepat menghasilkan O₂ berlebih dan panas.",
        "why_danger":"Dekomposisi H₂O₂ sangat cepat → pelepasan O₂ masif → kebakaran/ledakan dengan bahan organik.",
        "reaction":"2H₂O₂ + KMnO₄ (katalis) → 2H₂O + O₂↑ (sangat cepat)",
        "products":["O₂ (masif, cepat)","H₂O","Panas"],"fcot_involved":["O"],
        "theory":"Oxidator (O): Dua oksidator saling berinteraksi menghasilkan gas O₂ masif.",
    },
    _pair("Hidrogen Peroksida (H₂O₂)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Dua Oksidator – Dekomposisi Cepat + Gas O₂",
        "reason":"Campuran dua oksidator menghasilkan dekomposisi cepat dengan pelepasan O₂ dan panas.",
        "why_danger":"O₂ yang dilepas mendukung pembakaran. Reaksi tidak terkendali dapat menyebabkan ledakan wadah.",
        "reaction":"H₂O₂ + NaOCl → NaCl + H₂O + O₂↑ + panas",
        "products":["O₂ (gas)","NaCl","H₂O","Panas"],"fcot_involved":["O"],
        "theory":"Oxidator (O): Dua oksidator bereaksi menghasilkan oksigen masif dan panas.",
    },
    _pair("Hidrogen Peroksida (H₂O₂)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Oksidator + Basa Toksik – Perlu Kehati-hatian",
        "reason":"H₂O₂ dapat mengoksidasi amonia dalam kondisi tertentu. Amonia mempercepat dekomposisi H₂O₂.",
        "why_caution":"Amonia mempercepat dekomposisi H₂O₂ menghasilkan O₂. Uap NH₃ toksik. Ventilasi baik diperlukan.",
        "reaction":"NH₃ + H₂O₂ → N₂ + H₂O (kondisi tertentu) atau dekomposisi",
        "products":["O₂","H₂O","N₂"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): H₂O₂ oksidator; amonia toksik dan mempercepat dekomposisi.",
    },
    _pair("Kalium Permanganat (KMnO₄)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Dua Oksidator Kuat – Sangat Berbahaya",
        "reason":"Dua oksidator kuat bersama menghasilkan campuran sangat reaktif dengan pelepasan O₂ dan klorin.",
        "why_danger":"Gas klorin dan oksigen berlebih dapat menyebabkan kebakaran/ledakan dengan bahan organik apapun.",
        "reaction":"KMnO₄ + NaOCl → reaksi oksidatif kompleks + Cl₂↑ + O₂",
        "products":["Cl₂ (toksik)","O₂","Produk mangan"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Dua oksidator kuat tidak boleh dicampurkan.",
    },
    _pair("Kalium Dikromat (K₂Cr₂O₇)","Natrium Hidroksida (NaOH)"): {
        "status":"CAUTION","short":"Konversi ke Kromat – Perlu Kehati-hatian",
        "reason":"K₂Cr₂O₇ + NaOH → natrium kromat (Na₂CrO₄). Perubahan warna jingga ke kuning.",
        "why_caution":"Semua senyawa krom(VI) karsinogenik. NaOH korosif. Produk natrium kromat tetap berbahaya.",
        "reaction":"K₂Cr₂O₇ + 2NaOH → 2Na₂CrO₄ + K₂O + H₂O",
        "products":["Na₂CrO₄ (karsinogenik)","K₂O"],"fcot_involved":["O","T","C"],
        "theory":"Oxidator (O) + Toxic (T) + Corrosive (C): Produk senyawa krom karsinogenik.",
    },
    _pair("Kalium Dikromat (K₂Cr₂O₇)","Asam Klorida (HCl)"): {
        "status":"DANGER","short":"Gas Klorin + Oksidator Kuat",
        "reason":"K₂Cr₂O₇ + HCl → gas klorin (Cl₂) yang sangat toksik dan larutan asam kromat.",
        "why_danger":"Gas Cl₂ sangat toksik. Senyawa krom(VI) karsinogenik. Wajib dalam lemari asam.",
        "reaction":"K₂Cr₂O₇ + 14HCl → 2CrCl₃ + 2KCl + 3Cl₂↑ + 7H₂O",
        "products":["Cl₂ (gas toksik)","CrCl₃","KCl"],"fcot_involved":["O","T","C"],
        "theory":"Oxidator (O) + Toxic (T): Menghasilkan gas klorin berbahaya.",
    },
    _pair("Natrium (Na)","Etanol (C₂H₅OH)"): {
        "status":"DANGER","short":"Logam Alkali + Alkohol – Reaksi Keras + H₂",
        "reason":"Natrium bereaksi dengan etanol menghasilkan natrium etoksida dan gas H₂ mudah terbakar.",
        "why_danger":"Gas H₂ dapat terbakar/meledak. Reaksi menghasilkan panas signifikan. Wadah dapat pecah karena tekanan gas.",
        "reaction":"2Na + 2C₂H₅OH → 2C₂H₅ONa + H₂↑",
        "products":["Natrium etoksida (korosif)","H₂ (mudah terbakar)"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Logam alkali bereaksi keras dengan alkohol menghasilkan gas hidrogen.",
    },
    _pair("Natrium (Na)","Asam Klorida (HCl)"): {
        "status":"DANGER","short":"Logam Alkali + Asam Kuat – Eksplosif",
        "reason":"Na bereaksi sangat keras dengan HCl menghasilkan H₂ dan NaCl, disertai panas besar.",
        "why_danger":"Reaksi sangat eksotermik dan cepat. Gas H₂ yang terbentuk langsung terbakar dari panas reaksi.",
        "reaction":"2Na + 2HCl → 2NaCl + H₂↑ + Panas besar",
        "products":["NaCl","H₂ (eksplosif)","Panas besar"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Logam alkali + asam kuat = reaksi eksplosif.",
    },
    _pair("Natrium (Na)","Aseton (C₃H₆O)"): {
        "status":"DANGER","short":"Logam Alkali + Keton – Reaksi Keras",
        "reason":"Na bereaksi dengan aseton menghasilkan enolat natrium dan gas H₂. Reaksi eksotermik.",
        "why_danger":"Gas H₂ mudah terbakar. Panas reaksi dapat menyulut uap aseton (titik nyala -20°C).",
        "reaction":"Na + (CH₃)₂CO → NaOCH(CH₃)₂ + H₂↑ (sebagian)",
        "products":["Natrium isopropoksida","H₂ (mudah terbakar)"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Logam alkali bereaksi dengan pelarut polar mudah terbakar.",
    },
    _pair("Kalsium Karbid (CaC₂)","Asam Klorida (HCl)"): {
        "status":"DANGER","short":"Asetilena + Asam Kuat – Sangat Eksplosif",
        "reason":"CaC₂ + HCl menghasilkan gas asetilena dan kalsium klorida. Asetilena sangat mudah meledak.",
        "why_danger":"Gas asetilena rentang ledakan sangat lebar (2.5–100% udara). Lebih reaktif dari CaC₂ + air.",
        "reaction":"CaC₂ + 2HCl → CaCl₂ + C₂H₂↑",
        "products":["C₂H₂ (asetilena, sangat eksplosif)","CaCl₂"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Menghasilkan gas asetilena yang sangat mudah meledak.",
    },
    _pair("Kalsium Karbid (CaC₂)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"CaC₂ + Amonia Cair – Hindari Kontak",
        "reason":"CaC₂ dapat bereaksi dengan amonia cair, namun reaksi relatif lambat. Kedua zat berbahaya.",
        "why_caution":"NH₃ cair dengan CaC₂ dapat menghasilkan kalsium amida dan asetilena. Ventilasi baik diperlukan.",
        "reaction":"CaC₂ + 2NH₃ → Ca(NH₂)₂ + C₂H₂↑ (NH₃ cair)",
        "products":["Kalsium amida","C₂H₂ (asetilena)"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Menghasilkan asetilena mudah terbakar; amonia toksik.",
    },
    _pair("Sianida (KCN)","Natrium Hidroksida (NaOH)"): {
        "status":"SAFE","short":"Basa Menstabilkan KCN – Aman Disimpan Bersama",
        "reason":"NaOH menstabilkan KCN dan mencegah pembentukan HCN. Industri sering menyimpan KCN dalam suasana basa.",
        "why_safe":"Lingkungan basa mencegah hidrolisis KCN menjadi HCN. Praktik standar industri galvanik.",
        "reaction":"Tidak ada reaksi; NaOH menstabilkan larutan KCN",
        "products":["KCN stabil dalam basa"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Basa menstabilkan sianida – ini adalah prosedur standar keselamatan.",
    },
    _pair("Sianida (KCN)","Kalium Hidroksida (KOH)"): {
        "status":"SAFE","short":"Basa Menstabilkan KCN",
        "reason":"KOH menstabilkan KCN mencegah pembentukan HCN, sama seperti NaOH.",
        "why_safe":"Lingkungan basa wajib untuk penyimpanan KCN. Aman dalam kondisi ini.",
        "reaction":"Tidak ada reaksi berbahaya",
        "products":["KCN stabil"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Basa diperlukan untuk stabilisasi sianida.",
    },
    _pair("Sianida (KCN)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Sianida + Pelarut – Hindari Asam",
        "reason":"KCN larut dalam etanol. Tidak ada reaksi langsung, namun jika ada sedikit asam HCN terbentuk.",
        "why_caution":"Etanol dapat melarutkan KCN. Dalam lingkungan asam sekecil apapun, HCN mematikan terbentuk. Ventilasi ketat.",
        "reaction":"KCN + C₂H₅OH → larutan (tidak ada reaksi langsung tanpa asam)",
        "products":["Larutan KCN dalam etanol"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): KCN larut dalam etanol; bahaya HCN jika ada asam.",
    },
    _pair("Merkuri (Hg)","Asam Nitrat (HNO₃)"): {
        "status":"DANGER","short":"Merkuri + Asam Oksidatif – Gas NOₓ Toksik",
        "reason":"HNO₃ melarutkan merkuri menghasilkan merkuri nitrat dan gas NOₓ yang toksik.",
        "why_danger":"Gas NOₓ sangat toksik. Merkuri terlarut lebih mudah terserap tubuh. Reaksi di lemari asam wajib.",
        "reaction":"3Hg + 8HNO₃(encer) → 3Hg(NO₃)₂ + 2NO↑ + 4H₂O",
        "products":["Hg(NO₃)₂ (sangat toksik)","NO (toksik)","NOₓ"],"fcot_involved":["O","T","C"],
        "theory":"Oxidator (O) + Toxic (T): Asam oksidatif melarutkan logam berat menghasilkan senyawa toksik.",
    },
    _pair("Merkuri (Hg)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Merkuri + Asam – Reaksi Lambat tapi Berbahaya",
        "reason":"Hg bereaksi lambat dengan HCl menghasilkan merkuri(I) klorida (kalomel) yang toksik.",
        "why_caution":"Kalomel (Hg₂Cl₂) toksik. Uap merkuri sangat berbahaya. Wajib ventilasi dan lemari asam.",
        "reaction":"2Hg + 2HCl → Hg₂Cl₂ + H₂↑ (lambat)",
        "products":["Hg₂Cl₂ (kalomel, toksik)","H₂"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Logam berat + asam menghasilkan garam merkuri berbahaya.",
    },
    _pair("Arsenik Trioksida (As₂O₃)","Natrium Hidroksida (NaOH)"): {
        "status":"CAUTION","short":"Arsenik + Basa – Arsenat Lebih Larut",
        "reason":"NaOH bereaksi dengan As₂O₃ membentuk natrium arsenat yang lebih larut dalam air.",
        "why_caution":"Produk natrium arsenat lebih larut → lebih mudah terserap tubuh. Sangat toksik dan karsinogenik.",
        "reaction":"As₂O₃ + 6NaOH → 2Na₃AsO₄ + 3H₂O",
        "products":["Na₃AsO₄ (arsenat, sangat toksik)","H₂O"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Basa meningkatkan kelarutan arsenik, meningkatkan risiko paparan.",
    },
    _pair("Arsenik Trioksida (As₂O₃)","Asam Klorida (HCl)"): {
        "status":"DANGER","short":"Arsenik + Asam – AsCl₃ Volatil Toksik",
        "reason":"As₂O₃ + HCl → arsenik triklorida (AsCl₃) yang mudah menguap dan sangat toksik.",
        "why_danger":"AsCl₃ mudah menguap pada suhu kamar dan sangat toksik. Uap dapat menyebabkan keracunan akut.",
        "reaction":"As₂O₃ + 6HCl → 2AsCl₃ + 3H₂O",
        "products":["AsCl₃ (sangat toksik, volatil)","H₂O"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Menghasilkan senyawa arsenik volatil yang mematikan.",
    },
    _pair("Formaldehida (HCHO)","Natrium Hipoklorit (NaOCl)"): {
        "status":"DANGER","short":"Oksidasi Formaldehida – Asam Format + Gas Berbahaya",
        "reason":"NaOCl mengoksidasi formaldehida menghasilkan asam format dan gas klorin dalam kondisi asam.",
        "why_danger":"Formaldehida karsinogen + hipoklorit oksidator kuat. Produk sampingan toksik dapat terbentuk.",
        "reaction":"HCHO + NaOCl → HCOOH + NaCl (atau produk klorinasi lain)",
        "products":["Asam format","NaCl","Produk klorinasi toksik"],"fcot_involved":["F","O","T"],
        "theory":"Flammable (F) + Oxidator (O) + Toxic (T): Karsinogen mudah terbakar + oksidator = berbahaya.",
    },
    _pair("Formaldehida (HCHO)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Pembentukan Bis(klorometil) Eter – Karsinogen Ekstrem",
        "reason":"Formaldehida + HCl → bis(klorometil) eter (BCME) yang merupakan karsinogen kelas 1 paling kuat.",
        "why_caution":"BCME adalah karsinogen sangat kuat. Hindari campuran ini sepenuhnya. Lemari asam wajib.",
        "reaction":"2HCHO + 2HCl → ClCH₂OCH₂Cl + H₂O (BCME, karsinogen ekstrem)",
        "products":["Bis(klorometil) eter BCME (karsinogen kelas 1 ekstrem)"],"fcot_involved":["F","T","C"],
        "theory":"Flammable (F) + Toxic (T): Reaksi menghasilkan karsinogen paling berbahaya. Hindari!",
    },
    _pair("Formaldehida (HCHO)","Amonia (NH₃)"): {
        "status":"CAUTION","short":"Pembentukan Hexamethylenetetramine",
        "reason":"Formaldehida + amonia → heksametilentetramin (urotropin). Reaksi cepat, menghasilkan gas iritan.",
        "why_caution":"Reaksi menghasilkan panas. Uap formaldehida karsinogenik. Uap amonia toksik. Ventilasi ketat.",
        "reaction":"6HCHO + 4NH₃ → (CH₂)₆N₄ + 6H₂O",
        "products":["Heksametilentetramin (HMT)","H₂O"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Uap reaktan berbahaya; produk HMT relatif aman.",
    },
    _pair("Karbontetraklorida (CCl₄)","Natrium (Na)"): {
        "status":"DANGER","short":"Logam Alkali + Pelarut Klor – EKSPLOSIF",
        "reason":"Na bereaksi dengan CCl₄ secara eksplosif menghasilkan NaCl dan karbon.",
        "why_danger":"Reaksi SANGAT eksotermik, dapat meledak. Jangan pernah mencampurkan CCl₄ dengan logam alkali.",
        "reaction":"4Na + CCl₄ → 4NaCl + C + Ledakan!",
        "products":["NaCl","C (karbon)","Panas ledakan"],"fcot_involved":["F","T","C"],
        "theory":"Toxic (T) + Corrosive (C): Logam alkali + pelarut berhalogen = LEDAKAN.",
    },
    _pair("Karbontetraklorida (CCl₄)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Campuran Toksik – Saling Melarutkan",
        "reason":"CCl₄ dan etanol larut sempurna. Tidak ada reaksi, namun campuran meningkatkan toksisitas hepatik.",
        "why_caution":"CCl₄ hepatotoksik; etanol memperparah toksisitas hati. Campuran lebih berbahaya dari masing-masing.",
        "reaction":"Tidak ada reaksi kimia",
        "products":["Campuran toksik"],"fcot_involved":["F","T"],
        "theory":"Toxic (T) + Flammable (F): Campuran meningkatkan toksisitas hati. Hindari paparan.",
    },
    _pair("Natrium Klorida (NaCl)","Asam Sulfat (H₂SO₄)"): {
        "status":"CAUTION","short":"Pembentukan HCl Gas – Iritan Pernapasan",
        "reason":"NaCl + H₂SO₄ pekat → HCl gas dan NaHSO₄/Na₂SO₄. Gas HCl mengiritasi.",
        "why_caution":"Gas HCl terbentuk pada suhu tinggi. Metode klasik pembuatan HCl di laboratorium.",
        "reaction":"NaCl + H₂SO₄(pekat) → NaHSO₄ + HCl↑",
        "products":["HCl (gas iritan)","NaHSO₄"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C): Asam kuat bereaksi dengan garam klorida menghasilkan gas HCl.",
    },
    _pair("Natrium Klorida (NaCl)","Asam Klorida (HCl)"): {
        "status":"SAFE","short":"Garam + Asam Sumbernya – Tidak Bereaksi Signifikan",
        "reason":"NaCl dan HCl tidak bereaksi lebih lanjut dalam larutan. Penambahan NaCl ke HCl tidak berbahaya.",
        "why_safe":"Tidak ada reaksi kimia berbahaya. HCl tetap korosif; NaCl inert.",
        "reaction":"Tidak ada reaksi",
        "products":["Larutan NaCl dalam HCl"],"fcot_involved":["C"],
        "theory":"Corrosive (C): HCl korosif; NaCl inert. Tidak ada produk berbahaya baru.",
    },
    _pair("Natrium Bikarbonat (NaHCO₃)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Netralisasi – Gas CO₂ dalam Wadah Tertutup",
        "reason":"NaHCO₃ + HCl → NaCl + CO₂ + H₂O. Produksi CO₂ cepat berbahaya di wadah tertutup.",
        "why_caution":"CO₂ berlebih dapat meledakkan wadah tertutup. Di ruang terbuka reaksi ini relatif aman.",
        "reaction":"NaHCO₃ + HCl → NaCl + H₂O + CO₂↑",
        "products":["NaCl","H₂O","CO₂ (gas)"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Asam kuat + bikarbonat → CO₂ cepat; wadah harus terbuka.",
    },
    _pair("Natrium Bikarbonat (NaHCO₃)","Amonia (NH₃)"): {
        "status":"SAFE","short":"Dua Basa Lemah – Tidak Bereaksi Berbahaya",
        "reason":"NaHCO₃ dan NH₃ keduanya basa lemah. Tidak ada reaksi berbahaya antara keduanya.",
        "why_safe":"Tidak ada reaksi kimia signifikan. Keduanya basa lemah dengan profil bahaya rendah.",
        "reaction":"Tidak ada reaksi signifikan",
        "products":["—"],"fcot_involved":["T"],
        "theory":"Toxic (T) ringan: NH₃ iritan; NaHCO₃ aman. Tidak ada reaksi berbahaya.",
    },
    _pair("Air/H₂O","Asam Sulfat (H₂SO₄)"): {
        "status":"DANGER","short":"JANGAN Tuang Air ke H₂SO₄ Pekat!",
        "reason":"H₂SO₄ pekat + air sangat eksotermik. Harus selalu H₂SO₄ dituang ke air (bukan sebaliknya).",
        "why_danger":"Menuang air ke H₂SO₄ pekat menyebabkan semburan cairan korosif mendidih. Prosedur: ASAM ke AIR.",
        "reaction":"H₂SO₄(l) + H₂O → H₂SO₄(aq) + Panas besar (bila air dituang ke asam pekat!)",
        "products":["H₂SO₄ encer","Panas besar (bisa mendidihkan dan menyemburkan)"],"fcot_involved":["C"],
        "theory":"Corrosive (C): Hidrasi H₂SO₄ pekat sangat eksotermik. Selalu tuang asam ke air, bukan sebaliknya.",
    },
    _pair("Air/H₂O","Asam Klorida (HCl)"): {
        "status":"SAFE","short":"Pelarutan HCl – Aman dengan Prosedur Benar",
        "reason":"Air + HCl membentuk larutan asam klorida. Reaksi moderat, jauh lebih aman dari H₂SO₄.",
        "why_safe":"HCl gas larut dalam air menghasilkan asam klorida. Prosedur standar laboratorium.",
        "reaction":"HCl(g) + H₂O → H₃O⁺ + Cl⁻",
        "products":["Larutan HCl (asam klorida)"],"fcot_involved":["C"],
        "theory":"Corrosive (C): HCl larut dalam air; produk asam klorida korosif namun tidak berbahaya secara prosedur.",
    },
    _pair("Air/H₂O","Amonia (NH₃)"): {
        "status":"SAFE","short":"Pelarutan Amonia – Larutan Amoniak",
        "reason":"NH₃ larut dalam air membentuk larutan amonia (amoniak). Prosedur standar.",
        "why_safe":"Reaksi biasa untuk membuat larutan amonia. NH₃(aq) masih korosif dan berbahaya namun prosedurnya aman.",
        "reaction":"NH₃ + H₂O ⇌ NH₄OH ⇌ NH₄⁺ + OH⁻",
        "products":["NH₄OH (larutan amonia)"],"fcot_involved":["T","C"],
        "theory":"Toxic (T) + Corrosive (C): Pelarutan amonia dalam air adalah prosedur normal.",
    },
    _pair("Air/H₂O","Etanol (C₂H₅OH)"): {
        "status":"SAFE","short":"Larut Sempurna – Tidak Berbahaya",
        "reason":"Air dan etanol larut sempurna dalam segala perbandingan tanpa reaksi kimia.",
        "why_safe":"Tidak ada reaksi. Produk adalah campuran air-etanol (seperti minuman beralkohol atau antiseptik).",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran air-etanol"],"fcot_involved":["F"],
        "theory":"Flammable (F): Campuran tetap mudah terbakar tergantung konsentrasi etanol.",
    },
    _pair("Air/H₂O","Natrium Hipoklorit (NaOCl)"): {
        "status":"SAFE","short":"Pengenceran Hipoklorit – Normal",
        "reason":"Air mengencerkan NaOCl membentuk larutan pemutih lebih encer. Prosedur standar.",
        "why_safe":"Pengenceran dengan air adalah cara normal penggunaan pemutih. Tidak ada reaksi berbahaya.",
        "reaction":"NaOCl(pekat) + H₂O → larutan lebih encer",
        "products":["Larutan NaOCl encer"],"fcot_involved":["O"],
        "theory":"Oxidator (O): Pengenceran dengan air aman untuk hipoklorit.",
    },
    _pair("Natrium Hipoklorit (NaOCl)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Dua Oksidator Kuat – Sangat Berbahaya",
        "reason":"NaOCl dan KMnO₄ adalah dua oksidator kuat. Campuran tidak stabil dan sangat reaktif.",
        "why_danger":"Campuran dua oksidator kuat dapat menghasilkan reaksi tak terkendali dengan pelepasan O₂, Cl₂, dan panas.",
        "reaction":"NaOCl + KMnO₄ → reaksi oksidatif kompleks, gas toksik",
        "products":["Cl₂ (toksik)","O₂","Senyawa mangan"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O): Dua oksidator kuat tidak boleh dicampurkan.",
    },
    _pair("Natrium Bikarbonat (NaHCO₃)","Natrium Hidroksida (NaOH)"): {
        "status":"SAFE","short":"Dua Basa – Tidak Bereaksi Berbahaya",
        "reason":"NaHCO₃ (basa lemah) dan NaOH (basa kuat) tidak bereaksi secara berbahaya satu sama lain.",
        "why_safe":"Tidak ada reaksi berbahaya. NaOH tetap korosif namun tidak menimbulkan produk baru berbahaya.",
        "reaction":"Tidak ada reaksi signifikan",
        "products":["Campuran basa"],"fcot_involved":["C"],
        "theory":"Corrosive (C): NaOH korosif; NaHCO₃ aman. Tidak ada reaksi berbahaya.",
    },
    _pair("Hidrogen Peroksida (H₂O₂)","Aseton (C₃H₆O)"): {
        "status":"DANGER","short":"Pembentukan Aseton Peroksida – BAHAN PELEDAK PRIMER",
        "reason":"H₂O₂ + aseton dalam kondisi asam membentuk aseton peroksida (TATP/DADP) yang merupakan bahan peledak primer.",
        "why_danger":"Aseton peroksida sangat eksplosif dan tidak stabil. Sering digunakan sebagai bahan peledak teroris. SANGAT BERBAHAYA.",
        "reaction":"(CH₃)₂CO + H₂O₂ → aseton peroksida (TATP/DADP) (kondisi asam)",
        "products":["Aseton peroksida TATP (EKSPLOSIF PRIMER SANGAT BERBAHAYA)"],"fcot_involved":["F","O"],
        "theory":"Flammable (F) + Oxidator (O): Produk aseton peroksida adalah bahan peledak primer ekstrem.",
    },
    _pair("Hidrogen Peroksida (H₂O₂)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Oksidator + Bahan Mudah Terbakar",
        "reason":"H₂O₂ dapat mengoksidasi etanol dalam kondisi tertentu. Pada konsentrasi tinggi berbahaya.",
        "why_caution":"H₂O₂ >30% + etanol dapat bereaksi menghasilkan produk oksidasi. Hindari campuran dengan H₂O₂ pekat.",
        "reaction":"C₂H₅OH + H₂O₂ → CH₃CHO + H₂O (H₂O₂ pekat)",
        "products":["Asetaldehida (toksik)","H₂O"],"fcot_involved":["F","O"],
        "theory":"Flammable (F) + Oxidator (O): Oksidator dengan bahan mudah terbakar; hindari H₂O₂ pekat.",
    },
    _pair("Asam Asetat (CH₃COOH)","Aseton (C₃H₆O)"): {
        "status":"SAFE","short":"Dua Pelarut Organik – Larut, Tidak Bereaksi",
        "reason":"Asam asetat dan aseton larut sempurna tanpa reaksi kimia berbahaya.",
        "why_safe":"Campuran ini digunakan dalam berbagai aplikasi laboratorium. Tidak ada reaksi berbahaya.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut organik"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C) ringan: Campuran mudah terbakar; asam asetat sedikit korosif.",
    },
    _pair("Asam Asetat (CH₃COOH)","Etanol (C₂H₅OH)"): {
        "status":"SAFE","short":"Pelarut + Asam Lemah – Esterifikasi Lambat",
        "reason":"Asam asetat + etanol dapat membentuk etil asetat (ester) dengan katalis asam kuat pada suhu tinggi.",
        "why_safe":"Tanpa katalis dan pada suhu kamar, reaksi sangat lambat. Campuran digunakan dalam berbagai produk.",
        "reaction":"CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O (katalis asam, panas tinggi)",
        "products":["Etil asetat (pelarut, berbau harum)","H₂O"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C) ringan: Reaksi esterifikasi lambat. Produk etil asetat mudah terbakar.",
    },
    _pair("Kloroform (CHCl₃)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Campuran Pelarut Toksik + Mudah Terbakar",
        "reason":"Kloroform dan etanol larut sempurna. Tidak bereaksi, namun campuran meningkatkan efek narkotika.",
        "why_caution":"Kloroform bersifat narkotika dan karsinogenik. Etanol meningkatkan penyerapan. Lemari asam wajib.",
        "reaction":"Tidak ada reaksi kimia",
        "products":["Campuran toksik-pelarut"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Pelarut toksik karsinogenik; kombinasi meningkatkan risiko paparan.",
    },
    _pair("Kloroform (CHCl₃)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Oksidasi Kloroform – Gas Fosgen Terbentuk",
        "reason":"KMnO₄ mengoksidasi kloroform menghasilkan fosgen (COCl₂) yang sangat mematikan.",
        "why_danger":"Fosgen adalah gas perang kimia. Sangat toksik bahkan pada konsentrasi sangat rendah.",
        "reaction":"CHCl₃ + KMnO₄ → COCl₂↑ (fosgen) + produk mangan",
        "products":["Fosgen COCl₂ (GAS PERANG – MEMATIKAN)","MnO₂"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidasi kloroform menghasilkan fosgen mematikan.",
    },
    _pair("Benzena (C₆H₆)","Metanol (CH₃OH)"): {
        "status":"CAUTION","short":"Dua Pelarut Organik Sangat Berbahaya",
        "reason":"Benzena dan metanol larut sempurna. Tidak bereaksi, namun keduanya sangat toksik/karsinogenik.",
        "why_caution":"Benzena karsinogen kelas 1; metanol menyebabkan kebutaan/kematian. Ventilasi ketat dan APD wajib.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut toksik"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Dua pelarut sangat berbahaya; lemari asam wajib.",
    },
    _pair("Karbontetraklorida (CCl₄)","Aseton (C₃H₆O)"): {
        "status":"CAUTION","short":"Campuran Pelarut Toksik",
        "reason":"CCl₄ dan aseton larut sempurna. Tidak bereaksi, namun CCl₄ sangat hepatotoksik.",
        "why_caution":"Campuran pelarut ini digunakan dalam ekstraksi. CCl₄ sangat toksik bagi hati. Ventilasi wajib.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran pelarut"],"fcot_involved":["T","F"],
        "theory":"Toxic (T) + Flammable (F): CCl₄ hepatotoksik; aseton mudah terbakar. Ventilasi ketat.",
    },
    _pair("Karbontetraklorida (CCl₄)","Natrium Hipoklorit (NaOCl)"): {
        "status":"CAUTION","short":"Pelarut Klor + Oksidator – Stabil tapi Toksik",
        "reason":"Tidak ada reaksi langsung signifikan, namun keduanya mengandung klor dan berbahaya.",
        "why_caution":"CCl₄ sangat toksik dan karsinogenik. NaOCl oksidator. Gabungan bahaya toksik tinggi.",
        "reaction":"Tidak ada reaksi signifikan pada suhu kamar",
        "products":["—"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Keduanya berbahaya; tidak ada reaksi langsung namun hindari kombinasi.",
    },
    _pair("Merkuri (Hg)","Natrium (Na)"): {
        "status":"DANGER","short":"Amalgam Natrium + Risiko Ledakan",
        "reason":"Na bereaksi dengan Hg membentuk amalgam natrium. Reaksi keras dengan air sesudahnya.",
        "why_danger":"Amalgam Na-Hg bereaksi sangat keras dengan air menghasilkan H₂ dan NaOH. Paparan merkuri berbahaya.",
        "reaction":"Na + Hg → Na-Hg (amalgam) → reaksi hebat dengan air",
        "products":["Amalgam Na-Hg (reaktif dengan air)","Uap Hg"],"fcot_involved":["F","T","C"],
        "theory":"Flammable (F) + Toxic (T) + Corrosive (C): Logam alkali + merkuri = amalgam sangat berbahaya.",
    },
    _pair("Merkuri (Hg)","Etanol (C₂H₅OH)"): {
        "status":"CAUTION","short":"Merkuri Terlarut + Pelarut Organik",
        "reason":"Merkuri tidak larut dalam etanol murni. Namun campuran meningkatkan risiko paparan uap merkuri.",
        "why_caution":"Uap merkuri sangat berbahaya. Etanol dapat meningkatkan penguapan. Ventilasi ketat wajib.",
        "reaction":"Tidak ada reaksi kimia signifikan",
        "products":["Campuran dengan uap Hg meningkat"],"fcot_involved":["F","T"],
        "theory":"Flammable (F) + Toxic (T): Uap merkuri sangat neurotoksik; ventilasi ketat.",
    },
    _pair("Asam Fosfat (H₃PO₄)","Kalium Permanganat (KMnO₄)"): {
        "status":"CAUTION","short":"Asam + Oksidator – Perlu Pengawasan",
        "reason":"H₃PO₄ tidak bereaksi hebat dengan KMnO₄, namun dapat menurunkan pH dan mempercepat oksidasi.",
        "why_caution":"Asam mempengaruhi aktivitas KMnO₄. Ventilasi dan pengawasan diperlukan.",
        "reaction":"Tidak ada reaksi langsung signifikan; asam mempengaruhi reduksi permanganat",
        "products":["MnO₂ (dalam kondisi tertentu)"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Asam + oksidator perlu pengawasan.",
    },
    _pair("Asam Fluorida (HF)","Asam Klorida (HCl)"): {
        "status":"CAUTION","short":"Dua Asam Kuat – HF Sangat Berbahaya",
        "reason":"HF dan HCl keduanya asam kuat korosif. Tidak bereaksi satu sama lain, namun HF jauh lebih berbahaya.",
        "why_caution":"HF dapat menembus kulit tanpa rasa sakit awal, menyebabkan hipokalsemia dan kematian mendadak.",
        "reaction":"Tidak ada reaksi signifikan antar keduanya",
        "products":["Campuran asam korosif"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): HF jauh lebih berbahaya dari asam lain. APD khusus HF wajib.",
    },
    _pair("Asam Fluorida (HF)","Asam Sulfat (H₂SO₄)"): {
        "status":"CAUTION","short":"Dua Asam Kuat – HF Sangat Berbahaya",
        "reason":"HF dan H₂SO₄ tidak bereaksi satu sama lain secara langsung, namun keduanya sangat korosif.",
        "why_caution":"HF menembus kulit; H₂SO₄ pekat sangat eksotermik dengan air. Penanganan memerlukan APD khusus.",
        "reaction":"Tidak ada reaksi signifikan",
        "products":["Campuran asam korosif kuat"],"fcot_involved":["C","T"],
        "theory":"Corrosive (C) + Toxic (T): Dua asam berbahaya; penanganan terpisah wajib.",
    },
    _pair("Kalsium Hidroksida (Ca(OH)₂)","Natrium Hipoklorit (NaOCl)"): {
        "status":"SAFE","short":"Basa + Hipoklorit – Stabil (Kaporit)",
        "reason":"Ca(OH)₂ + NaOCl adalah dasar pembuatan kaporit (kalsium hipoklorit) untuk air minum.",
        "why_safe":"Kombinasi ini sengaja digunakan dalam pengolahan air. Basa menstabilkan hipoklorit.",
        "reaction":"Ca(OH)₂ + 2NaOCl → Ca(OCl)₂ + 2NaOH",
        "products":["Ca(OCl)₂ (kaporit)","NaOH"],"fcot_involved":["C","O"],
        "theory":"Corrosive (C) + Oxidator (O): Basa + hipoklorit = kaporit, prosedur standar pengolahan air.",
    },
    _pair("Kalsium Hidroksida (Ca(OH)₂)","Kalium Permanganat (KMnO₄)"): {
        "status":"CAUTION","short":"Basa + Oksidator Kuat – Perlu Kehati-hatian",
        "reason":"Basa dapat mempercepat dekomposisi KMnO₄ melepas oksigen.",
        "why_caution":"Pelepasan O₂ dari dekomposisi KMnO₄ dapat memicu kebakaran dengan bahan organik.",
        "reaction":"4KMnO₄ + 4Ca(OH)₂ → 4CaMnO₄ + O₂ + 4KOH (parsial)",
        "products":["O₂ (gas)","Senyawa mangan"],"fcot_involved":["O","C"],
        "theory":"Oxidator (O) + Corrosive (C): Basa + oksidator perlu pengawasan.",
    },
    _pair("Kalsium Karbid (CaC₂)","Natrium Hidroksida (NaOH)"): {
        "status":"CAUTION","short":"Karbid + Basa Kuat – Asetilena Lambat",
        "reason":"NaOH berair bereaksi dengan CaC₂ menghasilkan asetilena, lebih lambat dari air murni.",
        "why_caution":"Gas asetilena tetap terbentuk dan mudah meledak. NaOH korosif.",
        "reaction":"CaC₂ + 2NaOH(aq) → Ca(OH)₂ + C₂H₂↑ (dengan air)",
        "products":["C₂H₂ (asetilena mudah terbakar)","Ca(OH)₂"],"fcot_involved":["F","C"],
        "theory":"Flammable (F) + Corrosive (C): Basa kuat berair bereaksi dengan karbid menghasilkan asetilena.",
    },
    _pair("Natrium Klorida (NaCl)","Natrium Hidroksida (NaOH)"): {
        "status":"SAFE","short":"Garam Netral + Basa – Tidak Bereaksi",
        "reason":"NaCl tidak bereaksi dengan NaOH. Campuran digunakan dalam berbagai proses industri.",
        "why_safe":"Tidak ada reaksi kimia berbahaya. NaOH tetap korosif namun tidak menimbulkan produk baru berbahaya.",
        "reaction":"Tidak ada reaksi",
        "products":["Campuran larutan"],"fcot_involved":["C"],
        "theory":"Corrosive (C): NaOH korosif; NaCl inert. Tidak ada produk berbahaya baru.",
    },
    _pair("Arsenik Trioksida (As₂O₃)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Arsenik + Oksidator Kuat – Sangat Berbahaya",
        "reason":"KMnO₄ mengoksidasi As₂O₃ menghasilkan arsenik pentaoksida yang lebih larut dan lebih toksik.",
        "why_danger":"As₂O₅ lebih toksik dan lebih larut air. Kombinasi dua zat berbahaya dalam laboratorium.",
        "reaction":"As₂O₃ + KMnO₄ → As₂O₅ + MnO₂ (kondisi asam)",
        "products":["As₂O₅ (arsenik pentaoksida, lebih toksik)","MnO₂"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidasi arsenik menghasilkan produk lebih toksik.",
    },
    _pair("Sianida (KCN)","Kalium Permanganat (KMnO₄)"): {
        "status":"DANGER","short":"Sianida + Oksidator Kuat – Produk Toksik",
        "reason":"KMnO₄ mengoksidasi CN⁻ menghasilkan sianat (OCN⁻) dan produk oksidasi lain. Reaksi tidak terkontrol.",
        "why_danger":"Reaksi tidak terkontrol dapat melepas HCN dalam kondisi asam. Dua zat sangat berbahaya.",
        "reaction":"KCN + KMnO₄ → KOCN + MnO₂ (kondisi tertentu, bisa melepas HCN)",
        "products":["KOCN (sianat)","MnO₂","Risiko HCN"],"fcot_involved":["O","T"],
        "theory":"Oxidator (O) + Toxic (T): Oksidator kuat + sianida = sangat berbahaya.",
    },
}

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def badge_html(letter):
    labels = {"F":"FLAMMABLE","C":"CORROSIVE","O":"OXIDIZING","T":"TOXIC"}
    return f'<span class="fcot-badge badge-{letter}">{labels.get(letter,letter)}</span>'

def chem_badges(name):
    data = CHEMICALS.get(name) or st.session_state.custom_chemicals.get(name, {})
    return "".join(badge_html(l) for l in data.get("fcot",[]))

def fcot_html(codes):
    fcot_data = {
        "F":("F","Flammable","badge-F"),
        "C":("C","Corrosive","badge-C"),
        "O":("O","Oxidator","badge-O"),
        "T":("T","Toxic","badge-T"),
    }
    badges = ""
    for code in codes:
        if code in fcot_data:
            c, label, cls = fcot_data[code]
            badges += f'<span class="fcot-badge {cls}">{c} – {label}</span>'
    return f'<div class="fcot-grid">{badges}</div>' if badges else "<i style='color:#8892a4'>Tidak ada klasifikasi FCOT</i>"

def ghs_html(ghs_codes):
    badges = ""
    for code in ghs_codes:
        if code in GHS_INFO:
            emoji, label, desc = GHS_INFO[code]
            badges += f'<span class="ghs-badge">{emoji} {label}: {desc}</span>'
    return f'<div class="ghs-container">{badges}</div>' if badges else ""

def lookup_compatibility(chem1, chem2):
    key = _pair(chem1, chem2)
    return COMPAT_DB.get(key, None)

def heuristic_compat(chem1, chem2):
    ci1 = CHEMICALS.get(chem1) or st.session_state.custom_chemicals.get(chem1, {})
    ci2 = CHEMICALS.get(chem2) or st.session_state.custom_chemicals.get(chem2, {})
    fcot1 = set(ci1.get("fcot",[]))
    fcot2 = set(ci2.get("fcot",[]))
    g1 = ci1.get("group","")
    g2 = ci2.get("group","")
    all_f = fcot1 | fcot2

    # Storage-based logic (sifat bahan, bukan reaksi)
    # F + O: tidak boleh satu ruangan (kebakaran/ledakan jika ada kebocoran)
    if "F" in fcot1 and "O" in fcot2 or "F" in fcot2 and "O" in fcot1:
        return "DANGER", "⚠️ Flammable & Oksidator tidak boleh disimpan berdekatan. Jika terjadi kebocoran, uap flammable + oksidator dapat memicu kebakaran/ledakan spontan tanpa sumber api eksternal."
    # Asam + Basa: tidak boleh satu lemari
    is_acid1 = g1 == "Asam" or "asam" in ci1.get("class","").lower()
    is_acid2 = g2 == "Asam" or "asam" in ci2.get("class","").lower()
    is_base1 = g1 == "Basa" or "basa" in ci1.get("class","").lower()
    is_base2 = g2 == "Basa" or "basa" in ci2.get("class","").lower()
    if (is_acid1 and is_base2) or (is_acid2 and is_base1):
        return "DANGER", "⚠️ Asam & Basa tidak boleh disimpan dalam satu lemari. Kebocoran dapat menyebabkan reaksi netralisasi eksotermik dan semburan cairan korosif."
    # Basa + O
    if ("O" in fcot1 and is_base2) or ("O" in fcot2 and is_base1):
        return "DANGER", "⚠️ Oksidator & Basa Kuat tidak boleh disimpan berdekatan. Dapat mempercepat dekomposisi oksidator dan melepas O₂ serta panas."
    # C + C (both corrosive but different acid/base) — caught above
    # F + C-Asam: perlu hati-hati
    if "F" in all_f and "C" in all_f:
        if is_acid1 or is_acid2:
            return "CAUTION", "Flammable + Asam Korosif perlu jarak penyimpanan. Asam dapat merusak wadah logam bahan flammable, memicu kebocoran uap yang mudah terbakar."
    # T in combination
    if "T" in all_f and ("C" in all_f or "O" in all_f):
        # KCN + Asam is a special case for DANGER
        if ("KCN" in chem1 or "KCN" in chem2 or "Sianida" in chem1 or "Sianida" in chem2) and (is_acid1 or is_acid2):
            return "DANGER", "🚨 KRITIS: Sianida + Asam menghasilkan gas HCN yang mematikan. Harus disimpan terpisah ruangan."
        return "CAUTION", "Toksik berdekatan dengan korosif/oksidator memerlukan evaluasi SDS. Pastikan wadah bebas kebocoran dan ventilasi memadai."
    if "T" in all_f:
        return "CAUTION", "Bahan toksik harus disimpan di lemari terkunci (poison cabinet). Pastikan tidak berdekatan dengan bahan yang dapat membebaskan gas toksiknya."
    if "C" in all_f:
        return "CAUTION", "Setidaknya satu bahan bersifat korosif. Gunakan secondary containment (baki), pastikan lemari tahan korosi, dan APD lengkap saat penanganan."
    return "SAFE", "Tidak ada kombinasi FCOT kritis untuk penyimpanan yang terdeteksi. Tetap gunakan wadah yang tepat dan patuhi SDS masing-masing bahan."

def add_to_history(chem1, chem2, status):
    entry = {"chem1":chem1,"chem2":chem2,"status":status,
             "time":datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
    if st.session_state.history and st.session_state.history[0].get("chem1")==chem1 and st.session_state.history[0].get("chem2")==chem2:
        return
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]

def status_color(s):
    return {"DANGER":"#ef4444","CAUTION":"#f59e0b","SAFE":"#22c55e"}.get(s,"#94a3b8")
def status_emoji(s):
    return {"DANGER":"🔴","CAUTION":"🟡","SAFE":"🟢"}.get(s,"⚪")
def status_label(s):
    return {"DANGER":"BERBAHAYA","CAUTION":"HATI-HATI","SAFE":"AMAN"}.get(s,"TIDAK DIKETAHUI")
def status_dot(s):
    return {"DANGER":"no","CAUTION":"warn","SAFE":"ok"}.get(s,"")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 8px;'>
      <span style='font-size:2.6rem;'>⚗️</span><br>
      <span style='font-family:Syne,sans-serif;font-weight:800;font-size:1.25rem;
                   background:linear-gradient(90deg,#4ecdc4,#a29bfe);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        FCOT ChemSafe
      </span><br>
      <span style='color:#8892a4;font-size:0.75rem;'>Chemical Storage Safety v2</span>
    </div>
    <hr style='border-color:rgba(42,54,80,0.6);'>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Menu Utama</div>', unsafe_allow_html=True)
    menu = st.radio(
        "Pilih Halaman",
        ["🏠 Dashboard","🔬 Cek Kompatibilitas","🗺️ Matrix Penyimpanan","📚 Database Bahan","📖 Materi FCOT","⭐ Favorit","🕐 Riwayat","📋 Panduan"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:rgba(42,54,80,0.6);'>", unsafe_allow_html=True)
    total_checks = len(st.session_state.history)
    danger_c = sum(1 for h in st.session_state.history if h["status"]=="DANGER")
    all_db = {**CHEMICALS, **st.session_state.custom_chemicals}
    st.markdown(f"""
    <div style='font-size:0.75rem;color:#475569;text-align:center;line-height:1.8;'>
        Total Pengecekan: <b style='color:#38bdf8'>{total_checks}</b><br>
        Bahaya Terdeteksi: <b style='color:#ef4444'>{danger_c}</b><br>
        Database: <b style='color:#22c55e'>{len(all_db)}</b> bahan kimia
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">⚗️ FCOT ChemSafe</div>
  <p class="hero-sub">Kompatibilitas Penyimpanan FCOT · Matrix Asam & Basa · Standar GHS Internasional</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  PAGE: DASHBOARD
# ═══════════════════════════════════════════
if menu == "🏠 Dashboard":
    all_db_local = {**CHEMICALS, **st.session_state.custom_chemicals}
    n_f = sum(1 for v in all_db_local.values() if "F" in v.get("fcot",[]))
    n_c = sum(1 for v in all_db_local.values() if "C" in v.get("fcot",[]))
    n_o = sum(1 for v in all_db_local.values() if "O" in v.get("fcot",[]))
    n_t = sum(1 for v in all_db_local.values() if "T" in v.get("fcot",[]))

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card f"><p class="stat-num" style="color:var(--accent-f)">🔥 {n_f}</p><p class="stat-label">Flammable</p></div>
      <div class="stat-card c"><p class="stat-num" style="color:var(--accent-c)">🧪 {n_c}</p><p class="stat-label">Corrosive</p></div>
      <div class="stat-card o"><p class="stat-num" style="color:var(--accent-o)">💥 {n_o}</p><p class="stat-label">Oxidizing</p></div>
      <div class="stat-card t"><p class="stat-num" style="color:var(--accent-t)">☠️ {n_t}</p><p class="stat-label">Toxic</p></div>
      <div class="stat-card g"><p class="stat-num" style="color:#38bdf8">{len(all_db_local)}</p><p class="stat-label">Total Bahan</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-strip">
    ⚗️ <strong>FCOT ChemSafe</strong> membantu teknisi K3, petugas laboratorium, dan mahasiswa untuk menentukan keamanan penyimpanan bahan kimia berdasarkan teori FCOT dan standar GHS internasional.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🔍 Cari Bahan Kimia")
        q = st.text_input("", placeholder="Ketik nama atau rumus kimia...", label_visibility="collapsed")
        filtered = {n:d for n,d in all_db_local.items() if not q or q.lower() in n.lower() or q.lower() in d.get("formula","").lower()}
        shown = list(filtered.items())[:8]
        for name, data in shown:
            st.markdown(f"""
            <div class="chem-card">
              <div class="chem-name">{name}</div>
              <div style='color:#8892a4;font-size:0.8rem;margin:3px 0 6px;'>{data.get('desc',data.get('description',''))}</div>
              {fcot_html(data.get('fcot',[]))}
              <span style='font-family:Space Mono,monospace;font-size:0.7rem;color:#8892a4;'>CAS: {data.get('cas','—')}</span>
            </div>
            """, unsafe_allow_html=True)
        if len(filtered) > 8:
            st.markdown(f"<div style='color:#8892a4;font-size:0.82rem;text-align:center;'>… dan {len(filtered)-8} bahan lainnya di Database</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("### 📋 Matriks Kompatibilitas FCOT (Penyimpanan)")
        st.markdown("""
        <div style='overflow-x:auto;'>
        <table style='width:100%;border-collapse:collapse;font-size:0.82rem;font-family:Space Mono,monospace;'>
          <thead>
            <tr>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#8892a4;'>Sifat</th>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#ff6b35;'>🔥 F</th>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#4ecdc4;'>🧪 C-Asam</th>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#4ecdc4;'>🧪 C-Basa</th>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#ffe66d;'>💥 O</th>
              <th style='background:#1a2236;padding:10px 8px;border:1px solid #2a3650;color:#a29bfe;'>☠️ T</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style='background:#1a2236;padding:8px;border:1px solid #2a3650;color:#ff6b35;font-weight:700;'>🔥 Flammable</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
            </tr>
            <tr>
              <td style='background:#1a2236;padding:8px;border:1px solid #2a3650;color:#4ecdc4;font-weight:700;'>🧪 Asam</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
            </tr>
            <tr>
              <td style='background:#1a2236;padding:8px;border:1px solid #2a3650;color:#4ecdc4;font-weight:700;'>🧪 Basa</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
            </tr>
            <tr>
              <td style='background:#1a2236;padding:8px;border:1px solid #2a3650;color:#ffe66d;font-weight:700;'>💥 Oxidator</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(239,68,68,0.2);padding:8px;border:1px solid #2a3650;text-align:center;color:#ef4444;'>❌</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
            </tr>
            <tr>
              <td style='background:#1a2236;padding:8px;border:1px solid #2a3650;color:#a29bfe;font-weight:700;'>☠️ Toxic</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(245,158,11,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#f59e0b;'>⚠️</td>
              <td style='background:rgba(34,197,94,0.15);padding:8px;border:1px solid #2a3650;text-align:center;color:#22c55e;'>✅</td>
            </tr>
          </tbody>
        </table>
        </div>
        <div style='font-size:0.78rem;color:#8892a4;margin-top:8px;'>
        ✅ Aman disimpan berdekatan &nbsp;|&nbsp; ❌ Harus terpisah (risiko kebakaran/gas toksik) &nbsp;|&nbsp; ⚠️ Perlu evaluasi & jarak aman
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚡ Akses Cepat")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔬 Cek Kompatibilitas", use_container_width=True):
                st.session_state["_nav"] = "🔬 Cek Kompatibilitas"
                st.rerun()
        with c2:
            if st.button("🗺️ Matrix Penyimpanan", use_container_width=True):
                st.session_state["_nav"] = "🗺️ Matrix Penyimpanan"
                st.rerun()

# ═══════════════════════════════════════════
#  PAGE: CEK KOMPATIBILITAS
# ═══════════════════════════════════════════
elif menu == "🔬 Cek Kompatibilitas":
    st.markdown("## 🔬 Cek Kompatibilitas Penyimpanan")
    st.markdown("""
    <div class="info-strip">
      Pilih <strong>dua bahan kimia</strong> untuk mengecek apakah aman, harus berhati-hati, atau berbahaya saat <strong>disimpan berdekatan</strong> (berdasarkan sifat FCOT — bukan hasil reaksi kimia). Untuk detail reaksi, lihat hasil di bawah.
    </div>
    """, unsafe_allow_html=True)

    all_db2 = {**CHEMICALS, **st.session_state.custom_chemicals}
    chem_names = sorted(all_db2.keys())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧪 Bahan Kimia 1")
        chem1 = st.selectbox("Bahan 1", chem_names, key="chem1_sel", label_visibility="collapsed")
        ci1 = all_db2.get(chem1, {})
        st.markdown(f"""
        <div class="chem-card">
          <div class="chem-name">{chem1}</div>
          <div style='color:#8892a4;font-size:0.82rem;margin:3px 0 6px;'>{ci1.get('description','—')}</div>
          {fcot_html(ci1.get('fcot',[]))}
          {ghs_html(ci1.get('ghs',[]))}
          <div style='font-size:0.75rem;color:#8892a4;margin-top:4px;'>CAS: {ci1.get('cas','—')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🧪 Bahan Kimia 2")
        default_idx = min(8, len(chem_names)-1)
        chem2 = st.selectbox("Bahan 2", chem_names, key="chem2_sel", index=default_idx, label_visibility="collapsed")
        ci2 = all_db2.get(chem2, {})
        st.markdown(f"""
        <div class="chem-card">
          <div class="chem-name">{chem2}</div>
          <div style='color:#8892a4;font-size:0.82rem;margin:3px 0 6px;'>{ci2.get('description','—')}</div>
          {fcot_html(ci2.get('fcot',[]))}
          {ghs_html(ci2.get('ghs',[]))}
          <div style='font-size:0.75rem;color:#8892a4;margin-top:4px;'>CAS: {ci2.get('cas','—')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([2, 1.2, 1])
    with col_b1:
        check_btn = st.button("⚡ CEK KOMPATIBILITAS", type="primary", use_container_width=True)
    with col_b2:
        fav_btn = st.button("⭐ Simpan ke Favorit", use_container_width=True)
    with col_b3:
        clear_btn = st.button("🔄 Reset", use_container_width=True)

    if chem1 == chem2:
        st.warning("⚠️ Pilih dua bahan kimia yang **berbeda** untuk dicek.")
    else:
        if fav_btn:
            fav_entry = {"chem1":chem1,"chem2":chem2}
            if fav_entry not in st.session_state.favorites:
                st.session_state.favorites.append(fav_entry)
                st.toast("⭐ Pasangan disimpan ke Favorit!", icon="✅")
            else:
                st.toast("Pasangan ini sudah ada di Favorit.", icon="ℹ️")

        if check_btn:
            result = lookup_compatibility(chem1, chem2)

            if result is None:
                auto_status, auto_reason = heuristic_compat(chem1, chem2)
                add_to_history(chem1, chem2, auto_status)
                box_class = {"DANGER":"result-danger","CAUTION":"result-warning","SAFE":"result-safe"}[auto_status]
                em = status_emoji(auto_status)
                lbl = status_label(auto_status)

                st.markdown(f"""
                <div class="{box_class}">
                    <div class="result-title">{em} STATUS: {lbl}</div>
                    <div class="result-sub">⚠️ Pasangan ini belum ada di database lengkap. Hasil berdasarkan analisis FCOT otomatis.</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="info-box"><h4>📊 Analisis FCOT Otomatis</h4><p>{auto_reason}</p></div>
                """, unsafe_allow_html=True)
                all_ghs = list(set(ci1.get("ghs",[]) + ci2.get("ghs",[])))
                if all_ghs:
                    st.markdown("**🏷️ Simbol Bahaya GHS Gabungan:**")
                    st.markdown(ghs_html(all_ghs), unsafe_allow_html=True)
                st.info("💡 Untuk keakuratan lebih tinggi, konsultasikan SDS (Safety Data Sheet) masing-masing bahan.")

            else:
                status = result["status"]
                add_to_history(chem1, chem2, status)
                box_class = {"DANGER":"result-danger","CAUTION":"result-warning","SAFE":"result-safe"}[status]
                em = status_emoji(status)
                lbl = status_label(status)

                st.markdown(f"""
                <div class="{box_class}">
                    <div class="result-title">{em} STATUS: {lbl}</div>
                    <div class="result-sub">{result['short']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="info-box"><h4>📋 Ringkasan</h4><p>{result['reason']}</p></div>
                """, unsafe_allow_html=True)

                # Status-specific explanation
                if status == "DANGER" and result.get("why_danger"):
                    st.markdown(f"""
                    <div style='background:rgba(239,68,68,0.1);border-left:4px solid #ef4444;
                         border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin:0.5rem 0;'>
                        <h4 style='color:#fca5a5;margin:0 0 0.4rem;'>🚨 Mengapa BERBAHAYA?</h4>
                        <p style='color:#e2e8f0;font-size:0.88rem;line-height:1.6;margin:0'>{result['why_danger']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                if status == "SAFE" and result.get("why_safe"):
                    st.markdown(f"""
                    <div style='background:rgba(34,197,94,0.1);border-left:4px solid #22c55e;
                         border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin:0.5rem 0;'>
                        <h4 style='color:#86efac;margin:0 0 0.4rem;'>✅ Mengapa AMAN?</h4>
                        <p style='color:#e2e8f0;font-size:0.88rem;line-height:1.6;margin:0'>{result['why_safe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                if status == "CAUTION" and result.get("why_caution"):
                    st.markdown(f"""
                    <div style='background:rgba(245,158,11,0.1);border-left:4px solid #f59e0b;
                         border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin:0.5rem 0;'>
                        <h4 style='color:#fde68a;margin:0 0 0.4rem;'>⚠️ Mengapa Harus HATI-HATI?</h4>
                        <p style='color:#e2e8f0;font-size:0.88rem;line-height:1.6;margin:0'>{result['why_caution']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Detail teknis
                st.markdown("---")
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.markdown("**⚗️ Reaksi Kimia:**")
                    st.code(result.get("reaction","—"), language=None)
                    st.markdown("**🏭 Produk yang Terbentuk:**")
                    for p in result.get("products",[]):
                        dot = "🔴" if any(w in p.lower() for w in ["toksik","eksplosif","gas","berbahaya","korosif","ledak"]) else "🟢"
                        st.markdown(f"{dot} {p}")
                with col_r2:
                    st.markdown("**🔬 Klasifikasi FCOT Terlibat:**")
                    st.markdown(fcot_html(result.get("fcot_involved",[])), unsafe_allow_html=True)
                    st.markdown("**📖 Analisis Teori FCOT:**")
                    st.markdown(f"""
                    <div class="theory-box">
                        <p style='color:#c7d2fe;font-size:0.85rem;margin:0'>{result.get('theory','—')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # GHS & First Aid
                all_ghs = list(set(ci1.get("ghs",[]) + ci2.get("ghs",[])))
                if all_ghs:
                    st.markdown("**🏷️ Simbol Bahaya GHS:**")
                    st.markdown(ghs_html(all_ghs), unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("**🩺 Pertolongan Pertama & Penyimpanan:**")
                col_fa1, col_fa2 = st.columns(2)
                with col_fa1:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4>🧪 {chem1.split('(')[0].strip()}</h4>
                        <p><b>P3K:</b> {ci1.get('first_aid','—')}<br><b>Simpan:</b> {ci1.get('storage','—')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_fa2:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4>🧪 {chem2.split('(')[0].strip()}</h4>
                        <p><b>P3K:</b> {ci2.get('first_aid','—')}<br><b>Simpan:</b> {ci2.get('storage','—')}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # Tambah bahan kustom
    st.markdown("---")
    with st.expander("➕ Tambah Bahan Kimia Kustom ke Database"):
        st.markdown("Tambahkan bahan kimia yang belum ada untuk digunakan dalam pengecekan.")
        cc1, cc2 = st.columns(2)
        with cc1:
            custom_name = st.text_input("Nama Bahan Kimia", placeholder="Contoh: Anilin (C₆H₅NH₂)")
            custom_formula = st.text_input("Rumus Kimia", placeholder="C₆H₅NH₂")
            custom_cas = st.text_input("Nomor CAS", placeholder="62-53-3")
            custom_desc = st.text_area("Deskripsi singkat", placeholder="Amina aromatik, karsinogenik...")
        with cc2:
            custom_fcot = st.multiselect("Klasifikasi FCOT", ["F – Flammable","C – Corrosive","O – Oxidator","T – Toxic"])
            custom_ghs = st.multiselect("Simbol GHS", list(GHS_INFO.keys()),
                                        format_func=lambda x: f"{GHS_INFO[x][0]} {x}: {GHS_INFO[x][2]}")
            custom_hazard = st.text_area("Bahaya utama", placeholder="Karsinogenik, hepatotoksik...")
            custom_storage = st.text_input("Cara penyimpanan", placeholder="Wadah tertutup, ventilasi baik")
        if st.button("💾 Simpan Bahan Kustom", type="primary"):
            if custom_name and custom_formula:
                fcot_codes = [x.split(" – ")[0] for x in custom_fcot]
                st.session_state.custom_chemicals[custom_name] = {
                    "formula":custom_formula,"cas":custom_cas or "—","fcot":fcot_codes,
                    "ghs":custom_ghs,"description":custom_desc or "—","class":"Kustom","ph":"—",
                    "hazard":custom_hazard or "—","storage":custom_storage or "—",
                    "first_aid":"Konsultasikan SDS bahan.","group":"Kustom",
                }
                st.success(f"✅ **{custom_name}** berhasil ditambahkan!")
                st.rerun()
            else:
                st.error("Nama dan rumus kimia wajib diisi.")

# ═══════════════════════════════════════════
#  PAGE: MATRIX PENYIMPANAN
# ═══════════════════════════════════════════
elif menu == "🗺️ Matrix Penyimpanan":
    st.markdown("## 🗺️ Matrix Kompatibilitas Penyimpanan FCOT")
    st.markdown("""
    <div class="info-strip">
    📦 Matrix ini menunjukkan <strong>kompatibilitas penyimpanan</strong> bahan kimia berdasarkan sifat FCOT (Flammable, Corrosive, Oxidizing, Toxic).
    Penilaian berdasarkan <strong>risiko kebocoran, penguapan, dan kontak tidak sengaja saat penyimpanan</strong> — bukan reaksi langsung.
    </div>
    """, unsafe_allow_html=True)

    # ── STORAGE COMPATIBILITY MATRIX DATA ──
    # Rows = bahan yang disimpan, Cols = bahan yang berdekatan
    # Asam dan Basa dipisah karena risikonya berbeda
    # Status: SAFE / CAUTION / DANGER
    # Basis: NFPA 49, OSHA 29 CFR 1910.106, COSHH UK, standar OSHA Storage

    STORAGE_RULES = {
        # (sifat_bahan, sifat_tetangga): (status, alasan_singkat)
        ("F","F"):   ("SAFE",   "Sesama flammable boleh satu lemari tahan api khusus flammable cabinet"),
        ("F","C-A"): ("CAUTION","Asam korosif dapat merusak wadah logam flammable → risiko kebocoran uap mudah terbakar"),
        ("F","C-B"): ("SAFE",   "Basa korosif tidak memicu ignitasi langsung; pisahkan secara fisik dalam lemari yang sama"),
        ("F","O"):   ("DANGER", "Oksidator + flammable = risiko kebakaran/ledakan spontan jika ada kebocoran uap"),
        ("F","T"):   ("CAUTION","Toxic dapat meningkatkan risiko paparan saat kebocoran uap flammable; butuh ventilasi ekstra"),
        ("C-A","F"): ("CAUTION","Uap asam + uap pelarut mudah terbakar di ruang tertutup berpotensi menghasilkan campuran berbahaya"),
        ("C-A","C-A"):("SAFE",  "Sesama asam korosif boleh disimpan satu lemari (acid cabinet); pisahkan asam oksidatif dan non-oksidatif"),
        ("C-A","C-B"):("DANGER","Asam + basa kuat → jika terjadi kebocoran, netralisasi eksotermik kuat, semburan korosif, gas toksik"),
        ("C-A","O"):  ("CAUTION","Asam oksidatif (HNO₃) pisahkan dari asam biasa; asam non-oksidatif + oksidator solid perlu jarak"),
        ("C-A","T"):  ("CAUTION","Beberapa asam dapat membebaskan gas toksik dari senyawa toksik padat (mis. KCN + asam → HCN)"),
        ("C-B","F"):  ("SAFE",   "Basa kuat tidak memicu kebakaran; simpan terpisah secara fisik dari flammable cabinet"),
        ("C-B","C-A"):("DANGER","Basa + asam kuat → reaksi netralisasi eksotermik hebat jika tumpah bersama"),
        ("C-B","C-B"):("SAFE",  "Sesama basa korosif aman satu lemari (alkali cabinet); hindari campuran dengan logam aktif"),
        ("C-B","O"):  ("DANGER","Basa kuat + oksidator kuat (mis. NaOH + NaOCl pekat) dapat melepas gas O₂ dan panas"),
        ("C-B","T"):  ("CAUTION","Basa dapat menguraikan beberapa senyawa toksik; ventilasi baik, monitor secara berkala"),
        ("O","F"):    ("DANGER","KRITIS: Oksidator tidak boleh satu ruangan dengan flammable; risiko kebakaran/ledakan"),
        ("O","C-A"):  ("CAUTION","Asam oksidatif satu kategori dengan oksidator solid; pisahkan oksidator pekat dari asam biasa"),
        ("O","C-B"):  ("DANGER","Oksidator kuat + basa kuat → dekomposisi oksidator dipercepat, pelepasan O₂, panas"),
        ("O","O"):    ("CAUTION","Sesama oksidator umumnya aman, tapi pisahkan oksidator organik dari anorganik"),
        ("O","T"):    ("CAUTION","Oksidator dapat mengoksidasi senyawa toksik menghasilkan produk lebih berbahaya; evaluasi SDS"),
        ("T","F"):    ("CAUTION","Toxic mudah terbakar (mis. benzena, metanol) simpan di flammable cabinet; label ganda F+T"),
        ("T","C-A"):  ("CAUTION","Asam dapat bereaksi dengan beberapa toksik (mis. sianida → HCN); WAJIB pisahkan sianida dari asam"),
        ("T","C-B"):  ("CAUTION","Basa dapat menguraikan beberapa toksik; pantau stabilitas produk toksik"),
        ("T","O"):    ("CAUTION","Oksidator + toksik organik dapat membentuk produk toksik baru; evaluasi SDS"),
        ("T","T"):    ("SAFE",   "Sesama toksik aman satu lemari terkunci (poison cabinet); pisahkan berdasarkan rute paparan"),
    }

    # Tambahkan data sub-kelompok asam ke setiap bahan
    def get_storage_class(name, data):
        """Tentukan kelas penyimpanan bahan berdasarkan FCOT dan group."""
        fcot = set(data.get("fcot", []))
        group = data.get("group", "")
        classes = []
        if "F" in fcot:
            classes.append("F")
        if "C" in fcot:
            if group == "Asam" or "asam" in data.get("class","").lower():
                classes.append("C-A")
            elif group == "Basa" or "basa" in data.get("class","").lower():
                classes.append("C-B")
            else:
                # Default: cek pH
                ph_str = data.get("ph","7")
                try:
                    ph_val = float(ph_str.replace("<","").replace(">","").strip().split("(")[0].strip())
                    classes.append("C-A" if ph_val < 7 else "C-B")
                except:
                    classes.append("C-A")  # default asam jika tidak jelas
        if "O" in fcot:
            classes.append("O")
        if "T" in fcot:
            classes.append("T")
        return classes if classes else ["NETRAL"]

    def storage_compat(classes1, classes2):
        """Cek kompatibilitas penyimpanan dua bahan berdasarkan kelas FCOT-storage."""
        if not classes1 or not classes2 or classes1==["NETRAL"] or classes2==["NETRAL"]:
            return "SAFE", "Bahan inert/netral aman disimpan bersama hampir semua bahan."
        worst = "SAFE"
        reason = ""
        for c1 in classes1:
            for c2 in classes2:
                rule = STORAGE_RULES.get((c1, c2))
                if rule:
                    s, r = rule
                    if s == "DANGER":
                        worst = "DANGER"
                        reason = r
                    elif s == "CAUTION" and worst != "DANGER":
                        worst = "CAUTION"
                        reason = r
                    elif s == "SAFE" and worst == "SAFE" and not reason:
                        reason = r
        if not reason:
            reason = "Tidak ada aturan spesifik; konsultasikan SDS."
        return worst, reason

    # ── TAB UTAMA ──
    tab_matrix, tab_asam, tab_basa, tab_panduan_simpan = st.tabs([
        "📊 Matrix FCOT Lengkap",
        "🧪 Matrix Asam",
        "🔵 Matrix Basa",
        "📖 Panduan Penyimpanan"
    ])

    # Helper warna cell
    def cell_style(status):
        if status == "DANGER":
            return "background:rgba(239,68,68,0.25);color:#fca5a5;font-weight:700;"
        elif status == "CAUTION":
            return "background:rgba(245,158,11,0.2);color:#fde68a;font-weight:600;"
        else:
            return "background:rgba(34,197,94,0.15);color:#86efac;"

    def cell_icon(status):
        return {"DANGER":"❌","CAUTION":"⚠️","SAFE":"✅"}.get(status,"—")

    with tab_matrix:
        st.markdown("### 📊 Matrix Kompatibilitas Penyimpanan FCOT (Asam & Basa Dipisah)")
        st.markdown("""
        <div style='font-size:0.82rem;color:#8892a4;margin-bottom:12px;'>
        Baris = bahan yang akan disimpan &nbsp;|&nbsp; Kolom = bahan tetangga di rak/lemari yang sama.<br>
        <strong style='color:#4ecdc4'>C-A = Corrosive Asam</strong> &nbsp;|&nbsp; <strong style='color:#4ecdc4'>C-B = Corrosive Basa</strong>
        </div>
        """, unsafe_allow_html=True)

        # 6 kategori: F, C-A, C-B, O, T, NETRAL
        cats = [("F","🔥 Flammable","#ff6b35"),("C-A","🧪 Asam Korosif","#4ecdc4"),
                ("C-B","🔵 Basa Korosif","#38bdf8"),("O","💥 Oksidator","#ffe66d"),
                ("T","☠️ Toksik","#a29bfe"),("NETRAL","⚪ Inert/Netral","#8892a4")]

        # Build header
        header_cells = "<th style='background:#111827;padding:10px 6px;border:1px solid #2a3650;color:#8892a4;min-width:90px;font-size:0.75rem;'>Simpan ↓ / Dekat →</th>"
        for code, label, color in cats:
            header_cells += f"<th style='background:#111827;padding:8px 4px;border:1px solid #2a3650;color:{color};font-size:0.72rem;text-align:center;min-width:90px;'>{label}</th>"

        rows_html = ""
        for row_code, row_label, row_color in cats:
            row_html = f"<td style='background:#1a2236;padding:8px 10px;border:1px solid #2a3650;color:{row_color};font-weight:700;font-size:0.75rem;white-space:nowrap;'>{row_label}</td>"
            for col_code, col_label, col_color in cats:
                if row_code == col_code:
                    # Same category diagonal
                    s, r = storage_compat([row_code], [col_code])
                else:
                    s, r = storage_compat([row_code], [col_code])
                row_html += f"<td style='{cell_style(s)}padding:8px 4px;border:1px solid #2a3650;text-align:center;font-size:1rem;' title='{r}'>{cell_icon(s)}</td>"
            rows_html += f"<tr>{row_html}</tr>"

        st.markdown(f"""
        <div style='overflow-x:auto;margin:8px 0;'>
        <table style='border-collapse:collapse;width:100%;'>
          <thead><tr>{header_cells}</tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        <div style='font-size:0.8rem;color:#8892a4;margin-top:10px;display:flex;gap:20px;flex-wrap:wrap;'>
          <span>❌ <span style='color:#ef4444'>BAHAYA</span> – Harus terpisah ruangan/lemari berbeda</span>
          <span>⚠️ <span style='color:#f59e0b'>HATI-HATI</span> – Jarak aman, monitor, SDS wajib diperiksa</span>
          <span>✅ <span style='color:#22c55e'>AMAN</span> – Dapat satu lemari khusus golongannya</span>
        </div>
        """, unsafe_allow_html=True)

        # Penjelasan aturan utama
        st.markdown("---")
        st.markdown("### 🔑 Aturan Pemisahan Penyimpanan Utama")
        rules_cols = st.columns(3)
        with rules_cols[0]:
            st.markdown("""
            <div class="result-danger" style='padding:1rem;'>
            <div style='font-weight:700;color:#fca5a5;margin-bottom:8px;'>❌ WAJIB TERPISAH</div>
            <ul style='color:#e2e8f0;font-size:0.82rem;margin:0;padding-left:16px;line-height:2;'>
              <li>Flammable ↔ Oksidator</li>
              <li>Asam Kuat ↔ Basa Kuat</li>
              <li>Basa Kuat ↔ Oksidator</li>
              <li>Sianida/KCN ↔ Asam apapun</li>
              <li>HF ↔ Basa kuat (tanpa SOP)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        with rules_cols[1]:
            st.markdown("""
            <div class="result-warning" style='padding:1rem;'>
            <div style='font-weight:700;color:#fde68a;margin-bottom:8px;'>⚠️ PERLU EVALUASI</div>
            <ul style='color:#e2e8f0;font-size:0.82rem;margin:0;padding-left:16px;line-height:2;'>
              <li>Flammable ↔ Asam Korosif</li>
              <li>Oksidator ↔ Asam Korosif</li>
              <li>Toksik ↔ semua golongan</li>
              <li>Oksidator organik ↔ anorganik</li>
              <li>Flammable+Toksik (label ganda)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        with rules_cols[2]:
            st.markdown("""
            <div class="result-safe" style='padding:1rem;'>
            <div style='font-weight:700;color:#86efac;margin-bottom:8px;'>✅ SATU LEMARI (khusus)</div>
            <ul style='color:#e2e8f0;font-size:0.82rem;margin:0;padding-left:16px;line-height:2;'>
              <li>Sesama Flammable → <em>flammable cabinet</em></li>
              <li>Sesama Asam → <em>acid cabinet</em></li>
              <li>Sesama Basa → <em>alkali cabinet</em></li>
              <li>Sesama Toksik → <em>poison cabinet</em> (kunci)</li>
              <li>Inert/Netral ↔ hampir semua</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_asam:
        st.markdown("### 🧪 Matrix Penyimpanan: Fokus Bahan ASAM")
        st.markdown("""
        <div class="info-strip">Asam dipisahkan menjadi dua sub-tipe: <strong>Asam Oksidatif</strong> (HNO₃, H₂SO₄ pekat) yang memiliki sifat O sekaligus C, dan <strong>Asam Non-Oksidatif</strong> (HCl, H₃PO₄). Keduanya tetap tidak boleh disimpan bersama Basa Kuat.</div>
        """, unsafe_allow_html=True)

        all_acids = {n: d for n, d in CHEMICALS.items() if d.get("group") == "Asam"}
        all_bases = {n: d for n, d in CHEMICALS.items() if d.get("group") == "Basa"}
        all_oxid  = {n: d for n, d in CHEMICALS.items() if d.get("group") == "Oksidator"}
        all_solv  = {n: d for n, d in CHEMICALS.items() if d.get("group") == "Pelarut" and "F" in d.get("fcot",[])}

        acid_names = list(all_acids.keys())
        compare_groups = [
            ("🧪 Asam Lain", acid_names),
            ("🔵 Basa Kuat/Sedang", list(all_bases.keys())),
            ("💥 Oksidator", list(all_oxid.keys())),
            ("🔥 Flammable Pelarut", list(all_solv.keys())[:5]),
        ]

        # Build matrix header
        col_labels_flat = []
        for grp_label, grp_names in compare_groups:
            for n in grp_names:
                col_labels_flat.append((grp_label, n))

        header_html = "<th style='background:#111827;padding:8px 6px;border:1px solid #2a3650;color:#8892a4;font-size:0.72rem;min-width:80px;'>Asam ↓ / Simpan dekat →</th>"
        prev_grp = None
        for grp, n in col_labels_flat:
            grp_color = {"🧪 Asam Lain":"#4ecdc4","🔵 Basa Kuat/Sedang":"#38bdf8","💥 Oksidator":"#ffe66d","🔥 Flammable Pelarut":"#ff6b35"}.get(grp,"#8892a4")
            short = n.split("(")[0].strip()[:14]
            border_left = "border-left:3px solid " + grp_color + ";" if grp != prev_grp else ""
            header_html += f"<th style='background:#111827;padding:6px 4px;border:1px solid #2a3650;{border_left}color:{grp_color};font-size:0.68rem;text-align:center;'>{short}</th>"
            prev_grp = grp

        rows_html_acid = ""
        for acid_name, acid_data in all_acids.items():
            acid_classes = get_storage_class(acid_name, acid_data)
            short_row = acid_name.split("(")[0].strip()
            row_html = f"<td style='background:#1a2236;padding:6px 10px;border:1px solid #2a3650;color:#4ecdc4;font-size:0.75rem;white-space:nowrap;font-weight:600;'>{short_row}</td>"
            prev_grp = None
            for grp, col_name in col_labels_flat:
                grp_color = {"🧪 Asam Lain":"#4ecdc4","🔵 Basa Kuat/Sedang":"#38bdf8","💥 Oksidator":"#ffe66d","🔥 Flammable Pelarut":"#ff6b35"}.get(grp,"#8892a4")
                border_left = "border-left:3px solid " + grp_color + "50;" if grp != prev_grp else ""
                if col_name == acid_name:
                    row_html += f"<td style='background:#111827;padding:6px 4px;border:1px solid #2a3650;{border_left}text-align:center;color:#475569;font-size:0.85rem;'>—</td>"
                else:
                    col_data = CHEMICALS.get(col_name, {})
                    col_classes = get_storage_class(col_name, col_data)
                    s, r = storage_compat(acid_classes, col_classes)
                    row_html += f"<td style='{cell_style(s)}{border_left}padding:6px 4px;border:1px solid #2a3650;text-align:center;font-size:0.9rem;' title='{r}'>{cell_icon(s)}</td>"
                prev_grp = grp
            rows_html_acid += f"<tr>{row_html}</tr>"

        st.markdown(f"""
        <div style='overflow-x:auto;margin:8px 0;'>
        <table style='border-collapse:collapse;width:100%;'>
          <thead><tr>{header_html}</tr></thead>
          <tbody>{rows_html_acid}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

        # Aturan khusus asam
        st.markdown("---")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown("""
            <div class="theory-box">
            <div class="theory-title">⚗️ Sub-Tipe Asam & Penyimpanan</div>
            <table style='width:100%;font-size:0.8rem;color:#c7d2fe;border-collapse:collapse;'>
              <tr><th style='text-align:left;padding:4px;color:#a5b4fc;'>Asam</th><th style='padding:4px;color:#a5b4fc;'>Sifat</th><th style='padding:4px;color:#a5b4fc;'>Lemari</th></tr>
              <tr><td style='padding:4px;'>H₂SO₄, HNO₃</td><td style='padding:4px;text-align:center;'><span style='color:#ffe66d;'>C+O</span></td><td style='padding:4px;'>Acid + pisahkan dari asam biasa</td></tr>
              <tr><td style='padding:4px;'>HCl, H₃PO₄</td><td style='padding:4px;text-align:center;'><span style='color:#4ecdc4;'>C</span></td><td style='padding:4px;'>Acid cabinet standard</td></tr>
              <tr><td style='padding:4px;'>CH₃COOH</td><td style='padding:4px;text-align:center;'><span style='color:#ff6b35;'>F</span>+<span style='color:#4ecdc4;'>C</span></td><td style='padding:4px;'>Flammable acid cabinet</td></tr>
              <tr><td style='padding:4px;'>HF</td><td style='padding:4px;text-align:center;'><span style='color:#4ecdc4;'>C</span>+<span style='color:#a29bfe;'>T</span></td><td style='padding:4px;'>Lemari polietilen terpisah</td></tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
        with col_a2:
            st.markdown("""
            <div class="theory-box">
            <div class="theory-title">⚠️ Aturan Kritis Penyimpanan Asam</div>
            <ul style='color:#c7d2fe;font-size:0.82rem;line-height:2;margin:0;padding-left:16px;'>
              <li><strong>Asam ≠ Basa</strong>: Lemari berbeda, rak berbeda</li>
              <li><strong>HNO₃ ≠ Asam organik</strong>: HNO₃ bersifat oksidatif</li>
              <li><strong>HF</strong>: wadah polietilen, jangan kaca!</li>
              <li><strong>Asam + KCN/NaCN</strong>: FATAL → HCN terbentuk</li>
              <li>Simpan di bawah ketinggian mata, secondary containment</li>
              <li>Label jelas, tanggal terima & buka, suhu ruang</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_basa:
        st.markdown("### 🔵 Matrix Penyimpanan: Fokus Bahan BASA")
        st.markdown("""
        <div class="info-strip">Basa kuat (NaOH, KOH) berbeda secara signifikan risikonya dengan basa lemah (Ca(OH)₂, NaHCO₃). Keduanya tidak boleh disimpan bersama asam kuat maupun oksidator kuat.</div>
        """, unsafe_allow_html=True)

        all_acids_b = {n: d for n, d in CHEMICALS.items() if d.get("group") == "Asam"}
        compare_groups_b = [
            ("🧪 Asam Kuat/Sedang", list(all_acids_b.keys())),
            ("🔵 Basa Lain", list(all_bases.keys())),
            ("💥 Oksidator", list(all_oxid.keys())),
            ("🔥 Flammable Pelarut", list(all_solv.keys())[:4]),
        ]

        col_labels_b = []
        for grp_label, grp_names in compare_groups_b:
            for n in grp_names:
                col_labels_b.append((grp_label, n))

        header_html_b = "<th style='background:#111827;padding:8px 6px;border:1px solid #2a3650;color:#8892a4;font-size:0.72rem;min-width:80px;'>Basa ↓ / Simpan dekat →</th>"
        prev_grp_b = None
        for grp, n in col_labels_b:
            grp_color = {"🧪 Asam Kuat/Sedang":"#4ecdc4","🔵 Basa Lain":"#38bdf8","💥 Oksidator":"#ffe66d","🔥 Flammable Pelarut":"#ff6b35"}.get(grp,"#8892a4")
            short = n.split("(")[0].strip()[:14]
            border_left = "border-left:3px solid " + grp_color + ";" if grp != prev_grp_b else ""
            header_html_b += f"<th style='background:#111827;padding:6px 4px;border:1px solid #2a3650;{border_left}color:{grp_color};font-size:0.68rem;text-align:center;'>{short}</th>"
            prev_grp_b = grp

        rows_html_base = ""
        for base_name, base_data in all_bases.items():
            base_classes = get_storage_class(base_name, base_data)
            short_row = base_name.split("(")[0].strip()
            row_html = f"<td style='background:#1a2236;padding:6px 10px;border:1px solid #2a3650;color:#38bdf8;font-size:0.75rem;white-space:nowrap;font-weight:600;'>{short_row}</td>"
            prev_grp_b2 = None
            for grp, col_name in col_labels_b:
                grp_color = {"🧪 Asam Kuat/Sedang":"#4ecdc4","🔵 Basa Lain":"#38bdf8","💥 Oksidator":"#ffe66d","🔥 Flammable Pelarut":"#ff6b35"}.get(grp,"#8892a4")
                border_left = "border-left:3px solid " + grp_color + "50;" if grp != prev_grp_b2 else ""
                if col_name == base_name:
                    row_html += f"<td style='background:#111827;padding:6px 4px;border:1px solid #2a3650;{border_left}text-align:center;color:#475569;font-size:0.85rem;'>—</td>"
                else:
                    col_data = CHEMICALS.get(col_name, {})
                    col_classes = get_storage_class(col_name, col_data)
                    s, r = storage_compat(base_classes, col_classes)
                    row_html += f"<td style='{cell_style(s)}{border_left}padding:6px 4px;border:1px solid #2a3650;text-align:center;font-size:0.9rem;' title='{r}'>{cell_icon(s)}</td>"
                prev_grp_b2 = grp
            rows_html_base += f"<tr>{row_html}</tr>"

        st.markdown(f"""
        <div style='overflow-x:auto;margin:8px 0;'>
        <table style='border-collapse:collapse;width:100%;'>
          <thead><tr>{header_html_b}</tr></thead>
          <tbody>{rows_html_base}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("""
            <div class="theory-box">
            <div class="theory-title">🔵 Sub-Tipe Basa & Penyimpanan</div>
            <table style='width:100%;font-size:0.8rem;color:#c7d2fe;border-collapse:collapse;'>
              <tr><th style='text-align:left;padding:4px;color:#a5b4fc;'>Basa</th><th style='padding:4px;color:#a5b4fc;'>Kekuatan</th><th style='padding:4px;color:#a5b4fc;'>Lemari</th></tr>
              <tr><td style='padding:4px;'>NaOH, KOH</td><td style='padding:4px;text-align:center;'><span style='color:#ef4444;'>Kuat</span></td><td style='padding:4px;'>Alkali cabinet terpisah</td></tr>
              <tr><td style='padding:4px;'>NH₃ (aq)</td><td style='padding:4px;text-align:center;'><span style='color:#f59e0b;'>Lemah+Toksik</span></td><td style='padding:4px;'>Lemari berventilasi</td></tr>
              <tr><td style='padding:4px;'>Ca(OH)₂</td><td style='padding:4px;text-align:center;'><span style='color:#22c55e;'>Sedang</span></td><td style='padding:4px;'>Rak basa umum (kering)</td></tr>
              <tr><td style='padding:4px;'>NaHCO₃</td><td style='padding:4px;text-align:center;'><span style='color:#22c55e;'>Sangat lemah</span></td><td style='padding:4px;'>Rak umum aman</td></tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
        with col_b2:
            st.markdown("""
            <div class="theory-box">
            <div class="theory-title">⚠️ Aturan Kritis Penyimpanan Basa</div>
            <ul style='color:#c7d2fe;font-size:0.82rem;line-height:2;margin:0;padding-left:16px;'>
              <li><strong>Basa kuat ≠ Asam kuat</strong>: Lemari berbeda WAJIB</li>
              <li><strong>NaOH higroskopis</strong>: wadah kedap, jauhkan dari CO₂</li>
              <li><strong>NH₃</strong>: jauhkan dari klorin dan asam apa pun</li>
              <li><strong>Basa + alumunium</strong>: menghasilkan H₂ (flammable!)</li>
              <li>Secondary containment wajib untuk basa kuat</li>
              <li>APD: wajib kacamata splash-proof + sarung tangan karet</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab_panduan_simpan:
        st.markdown("### 📖 Panduan Lengkap Penyimpanan Bahan Kimia")

        st.markdown("""
        <div class="theory-box">
        <div class="theory-title">🏛️ Prinsip Dasar Penyimpanan (OSHA / NFPA 45 / Permenaker 5/2018)</div>
        <ol style='color:#c7d2fe;font-size:0.85rem;line-height:2;margin:0;padding-left:20px;'>
          <li>Pisahkan bahan berdasarkan <strong>sifat bahaya utama</strong> (FCOT), bukan hanya berdasarkan nama</li>
          <li>Bahan yang berdekatan harus <strong>kompatibel</strong> — tidak boleh bereaksi berbahaya jika terjadi kebocoran</li>
          <li>Gunakan <strong>lemari penyimpanan khusus</strong> sesuai golongan (flammable, acid, alkali, poison cabinet)</li>
          <li>Setiap bahan wajib memiliki <strong>SDS (Safety Data Sheet)</strong> yang mudah diakses</li>
          <li><strong>Secondary containment</strong> (baki/nampan) untuk bahan cair korosif dan flammable</li>
          <li>Ventilasi memadai untuk bahan dengan tekanan uap tinggi atau bahan yang mengeluarkan gas</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        sp_cols = st.columns(2)
        with sp_cols[0]:
            st.markdown("""
            <div class="info-box">
            <h4>🔥 Lemari Flammable (Flammable Cabinet)</h4>
            <p>• Standar: FM/UL Listed, baja 18-gauge<br>
            • Maks 60 galon (~227L) total<br>
            • Ventilasi ke luar atau bersirkulasi dengan karbon aktif<br>
            • Grounding anti-statis wajib<br>
            • <strong>Tidak boleh</strong>: oksidator, asam oksidatif</p>
            </div>
            <div class="info-box" style='margin-top:10px;'>
            <h4>🧪 Lemari Asam (Acid Cabinet)</h4>
            <p>• Material: polietilen atau baja berlapis epoksi tahan asam<br>
            • Pisahkan asam oksidatif (HNO₃) dari asam biasa<br>
            • HF: lemari polietilen terpisah khusus<br>
            • <strong>Tidak boleh</strong>: basa, sianida, bahan flammable</p>
            </div>
            """, unsafe_allow_html=True)
        with sp_cols[1]:
            st.markdown("""
            <div class="info-box">
            <h4>🔵 Lemari Basa (Alkali Cabinet)</h4>
            <p>• Material: tahan korosi alkali (polipropilen, SS 316)<br>
            • NaOH disimpan dalam wadah kedap udara (higroskopis)<br>
            • Amonia: lemari berventilasi khusus, dipisah dari basa padat<br>
            • <strong>Tidak boleh</strong>: asam, oksidator kuat</p>
            </div>
            <div class="info-box" style='margin-top:10px;'>
            <h4>☠️ Lemari Racun (Poison Cabinet)</h4>
            <p>• Harus terkunci (double-lock untuk narkotika/psikotropika)<br>
            • Buku stok dan logbook wajib diisi<br>
            • Pisahkan toksik volatil dari toksik padat<br>
            • <strong>Khusus</strong>: KCN/NaCN harus JAUH dari semua asam</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Checklist Inspeksi Penyimpanan Harian")
        checklist_items = [
            ("Semua wadah tertutup rapat dan tidak bocor","📦"),
            ("Label terbaca jelas — nama, konsentrasi, tanggal buka","🏷️"),
            ("Tidak ada asam berdekatan dengan basa di rak yang sama","🧪"),
            ("Oksidator tersimpan di lemari terpisah dari flammable","💥"),
            ("SDS tersedia dan mudah dijangkau untuk semua bahan","📄"),
            ("APAR (fire extinguisher) dalam jangkauan dan aktif","🧯"),
            ("Ventilasi berfungsi, tidak ada bau menyengat","🌀"),
            ("Secondary containment (baki) bersih dan tidak penuh","🫙"),
            ("Stok sianida/arsenik terkunci dan sesuai logbook","🔐"),
            ("Bahan mudah terbakar jauh dari sumber panas/api terbuka","🔥"),
        ]
        for item, icon in checklist_items:
            st.markdown(f"""
            <div style='background:rgba(30,58,138,0.15);border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;
                 padding:8px 14px;margin:4px 0;font-size:0.85rem;color:#e2e8f0;display:flex;align-items:center;gap:10px;'>
              <span style='font-size:1.1rem;'>{icon}</span> {item}
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  PAGE: DATABASE BAHAN
# ═══════════════════════════════════════════
elif menu == "📚 Database Bahan":
    st.markdown("## 📚 Database Bahan Kimia")
    all_db3 = {**CHEMICALS, **st.session_state.custom_chemicals}

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        search_q = st.text_input("🔍 Cari bahan kimia...", placeholder="Nama atau rumus")
    with col_f2:
        groups = ["Semua"] + sorted(set(v.get("group","—") for v in all_db3.values()))
        filter_group = st.selectbox("Filter Kelompok", groups)

    filter_fcot = st.multiselect("Filter FCOT", ["F – Flammable","C – Corrosive","O – Oxidator","T – Toxic"])
    selected_fcot = [x.split(" – ")[0] for x in filter_fcot]

    filtered3 = {}
    for name, data in all_db3.items():
        if search_q and search_q.lower() not in name.lower() and search_q.lower() not in data.get("formula","").lower():
            continue
        if filter_group != "Semua" and data.get("group") != filter_group:
            continue
        if selected_fcot and not any(c in data.get("fcot",[]) for c in selected_fcot):
            continue
        filtered3[name] = data

    st.markdown(f"**Menampilkan {len(filtered3)} dari {len(all_db3)} bahan kimia**")
    st.markdown("---")

    if not filtered3:
        st.warning("Tidak ada bahan kimia yang sesuai filter.")
    else:
        for name, data in filtered3.items():
            icon = "🔶" if data.get("group")=="Kustom" else "🧪"
            with st.expander(f"{icon} **{name}** | {data.get('formula','—')} | {data.get('class','—')}"):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown(f"**Rumus:** {data.get('formula','—')}")
                    st.markdown(f"**CAS:** `{data.get('cas','—')}`")
                    st.markdown(f"**Kelompok:** {data.get('group','—')} | **pH:** {data.get('ph','—')}")
                    st.markdown(f"**Deskripsi:** {data.get('description','—')}")
                    st.markdown("**Klasifikasi FCOT:**")
                    st.markdown(fcot_html(data.get("fcot",[])), unsafe_allow_html=True)
                with col_d2:
                    if data.get("ghs"):
                        st.markdown("**Simbol GHS:**")
                        st.markdown(ghs_html(data["ghs"]), unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-box"><h4>⚠️ Bahaya Utama</h4><p>{data.get('hazard','—')}</p></div>
                    <div class="info-box"><h4>🗄️ Penyimpanan</h4><p>{data.get('storage','—')}</p></div>
                    <div class="info-box"><h4>🩺 Pertolongan Pertama</h4><p>{data.get('first_aid','—')}</p></div>
                    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  PAGE: MATERI FCOT
# ═══════════════════════════════════════════
elif menu == "📖 Materi FCOT":
    st.markdown("## 📖 Materi & Teori FCOT")
    st.markdown("Pelajari dasar teori pengendalian bahan kimia berbahaya berdasarkan klasifikasi **FCOT**.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 Flammable","🧪 Corrosive","💥 Oxidator","☠️ Toxic","📜 GHS & SDS"])

    with tab1:
        st.markdown("## 🔥 F — Flammable (Mudah Terbakar)")
        st.markdown("""<div class="theory-box"><div class="theory-title">Definisi</div>
        <p style='color:#c7d2fe;font-size:0.88rem'>Bahan yang mudah terbakar adalah zat yang dapat menyala dan mempertahankan pembakaran pada suhu dan tekanan normal. Klasifikasi berdasarkan <b>Flash Point (titik nyala)</b>.</p></div>""", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("""
**Klasifikasi Flash Point:**
| Kategori | Flash Point |
|----------|-------------|
| Extremely Flammable | < 23°C |
| Highly Flammable | 23–60°C |
| Flammable | 60–93°C |

**Contoh Bahan:**
- Etanol (FP: 13°C) | Metanol (FP: 11°C)
- Aseton (FP: -20°C) | Benzena (FP: -11°C)
- Toluena (FP: 4°C) | Dietil eter (FP: -45°C)
            """)
        with col_f2:
            st.markdown("""
**Teori Segitiga Api (Fire Triangle):**

Kebakaran memerlukan 3 elemen simultan:
1. **Bahan Bakar** (Fuel) — zat flammable
2. **Oksigen** — minimal 16% di udara
3. **Sumber Panas/Ignisi** — percikan, panas

**Pengendalian:**
- Simpan dalam lemari tahan api (flammable cabinet)
- Jauhkan dari sumber panas & api terbuka
- Ventilasi memadai | Grounding anti-statis
            """)

    with tab2:
        st.markdown("## 🧪 C — Corrosive (Korosif)")
        st.markdown("""<div class="theory-box"><div class="theory-title">Definisi</div>
        <p style='color:#c7d2fe;font-size:0.88rem'>Bahan korosif menyebabkan kerusakan jaringan hidup atau material melalui reaksi kimia, diklasifikasikan berdasarkan pH dan kemampuan merusak jaringan.</p></div>""", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
**Skala Korosivitas (pH):**
| pH | Klasifikasi |
|----|-------------|
| < 2 | Asam Kuat (sangat korosif) |
| 2–4 | Asam Sedang |
| 7 | Netral |
| 10–12 | Basa Sedang |
| > 12 | Basa Kuat (sangat korosif) |
            """)
        with col_c2:
            st.markdown("""
**Mekanisme Kerusakan:**

**Asam Kuat:** Denaturasi protein → koagulasi jaringan

**Basa Kuat:** Saponifikasi lemak → kolikatif nekrosis (menembus lebih dalam, lebih berbahaya untuk mata!)

**APD Wajib:** Face shield, sarung tangan karet tebal, apron PE, sepatu boots
            """)

    with tab3:
        st.markdown("## 💥 O — Oxidator (Pengoksidasi)")
        st.markdown("""<div class="theory-box"><div class="theory-title">Definisi</div>
        <p style='color:#c7d2fe;font-size:0.88rem'>Oksidator adalah zat yang menyediakan oksigen atau menerima elektron, meningkatkan kemampuan terbakar bahan lain atau memulai/memperkuat reaksi pembakaran.</p></div>""", unsafe_allow_html=True)
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            st.markdown("""
**Contoh Oksidator:**
| Bahan | Kekuatan |
|-------|----------|
| KMnO₄ | Kuat |
| HNO₃ (pekat) | Kuat |
| H₂O₂ (>30%) | Sedang-Kuat |
| NaOCl | Sedang |
| K₂Cr₂O₇ | Kuat |
| O₃ (ozon) | Sangat Kuat |
            """)
        with col_o2:
            st.markdown("""
**Bahaya Kombinasi:**
- Oksidator + Flammable = **KEBAKARAN/LEDAKAN**
- Oksidator + Asam Kuat = gas toksik (Cl₂, O₃)
- Oksidator + Reduktor organik = runaway reaction

**Aturan Emas:**
> Jangan simpan oksidator bersama bahan organik atau mudah terbakar!
            """)

    with tab4:
        st.markdown("## ☠️ T — Toxic (Toksik/Beracun)")
        st.markdown("""<div class="theory-box"><div class="theory-title">Definisi</div>
        <p style='color:#c7d2fe;font-size:0.88rem'>Bahan toksik menyebabkan cedera, penyakit, atau kematian ketika masuk ke tubuh melalui inhalasi, ingesti, atau absorpsi kulit.</p></div>""", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
**Klasifikasi Toksisitas (LD₅₀ oral, tikus):**
| Kategori | LD₅₀ (mg/kg) |
|----------|--------------|
| Sangat Toksik | < 25 |
| Toksik | 25–200 |
| Berbahaya | 200–2000 |
| Iritan | 2000–5000 |

**Rute Paparan:**
1. **Inhalasi** — uap, gas, aerosol, debu
2. **Ingesti** — tertelan
3. **Absorpsi Kulit** — HF, benzena
4. **Injeksi** — luka tusuk tak sengaja
            """)
        with col_t2:
            st.markdown("""
**Toksisitas Akut vs Kronik:**

**Akut:** Efek cepat setelah paparan dosis tinggi

**Kronik:** Efek lambat akibat paparan berulang dosis rendah → kanker, kerusakan organ

**Nilai Batas Paparan:**
- **TLV-TWA:** 8 jam/hari
- **TLV-STEL:** 15 menit paparan singkat
- **IDLH:** Immediately Dangerous to Life/Health

**APD Kritis:** Respirator N95/SCBA, sarung tangan impermeable, kacamata rapat, overall
            """)

    with tab5:
        st.markdown("## 📜 GHS & SDS")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("""
### Sistem Harmonisasi Global (GHS)
Standar internasional klasifikasi & pelabelan bahan kimia berbahaya.

**9 Simbol Bahaya GHS:**
| Kode | Simbol | Arti |
|------|--------|------|
| GHS01 | 💥 | Eksplosif |
| GHS02 | 🔥 | Mudah Terbakar |
| GHS03 | ⬆️🔥 | Oksidator |
| GHS04 | 🔵 | Gas Bertekanan |
| GHS05 | 🧪 | Korosif |
| GHS06 | ☠️ | Toksik Akut |
| GHS07 | ❗ | Bahaya/Iritan |
| GHS08 | ⚠️ | Bahaya Kesehatan |
| GHS09 | 🌿❌ | Bahaya Lingkungan |
            """)
        with col_g2:
            st.markdown("""
### Safety Data Sheet (SDS/MSDS)
Dokumen wajib untuk setiap bahan kimia berbahaya. Berisi 16 Seksi:

| Seksi | Isi |
|-------|-----|
| 1–3 | Identifikasi & Komposisi |
| 4–6 | P3K, Kebakaran, Tumpahan |
| 7–8 | Penanganan & APD |
| 9–10 | Sifat Fisika & Reaktivitas |
| 11–12 | Toksikologi & Ekologi |
| 13–16 | Limbah, Transportasi, Regulasi |

**Sumber SDS Terpercaya:**
- [PubChem (NCBI)](https://pubchem.ncbi.nlm.nih.gov)
- [Sigma-Aldrich SDS](https://www.sigmaaldrich.com)
- [ChemBlink](https://www.chemblink.com)
            """)

# ═══════════════════════════════════════════
#  PAGE: FAVORIT
# ═══════════════════════════════════════════
elif menu == "⭐ Favorit":
    st.markdown("## ⭐ Pasangan Favorit")
    st.markdown("""<div class="info-strip">Simpan kombinasi yang sering Anda cek. Tambahkan dari halaman <strong>Cek Kompatibilitas</strong>.</div>""", unsafe_allow_html=True)

    if not st.session_state.favorites:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;color:#8892a4;'>
          <div style='font-size:3rem;margin-bottom:12px;'>📋</div>
          <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:8px;'>Belum ada favorit</div>
          <p>Cek kompatibilitas dua bahan lalu klik <strong>⭐ Simpan ke Favorit</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_h1, col_h2 = st.columns([3,1])
        with col_h1:
            st.markdown(f"**{len(st.session_state.favorites)} pasangan tersimpan**")
        with col_h2:
            if st.button("🗑️ Hapus Semua", use_container_width=True):
                st.session_state.favorites = []
                st.rerun()

        for i, fav in enumerate(st.session_state.favorites):
            fav_result = lookup_compatibility(fav["chem1"], fav["chem2"])
            fav_status = fav_result["status"] if fav_result else "SAFE"
            em = status_emoji(fav_status)
            lbl = status_label(fav_status)
            sc = status_color(fav_status)
            dot = status_dot(fav_status)

            col_f1, col_f2 = st.columns([5, 1])
            with col_f1:
                st.markdown(f"""
                <div class="fav-card">
                  <div class="fav-dot {dot}"></div>
                  <div style='flex:1;'>
                    <div style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;'>
                      {fav['chem1'].split('(')[0].strip()}
                      <span style='color:#8892a4;font-weight:400;'> + </span>
                      {fav['chem2'].split('(')[0].strip()}
                    </div>
                    <div style='margin-top:4px;font-size:0.78rem;font-weight:700;color:{sc};'>{em} {lbl}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with col_f2:
                if st.button("🗑️", key=f"fav_del_{i}", help="Hapus dari favorit"):
                    st.session_state.favorites.pop(i)
                    st.rerun()

        # Export CSV
        if st.button("📥 Download Favorit sebagai CSV"):
            rows = []
            for fav in st.session_state.favorites:
                fav_result = lookup_compatibility(fav["chem1"], fav["chem2"])
                fav_status = fav_result["status"] if fav_result else "—"
                rows.append({"Bahan 1":fav["chem1"],"Bahan 2":fav["chem2"],"Status":status_label(fav_status)})
            df_fav = pd.DataFrame(rows)
            csv = df_fav.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Unduh CSV", csv, "fcot_favorites.csv", "text/csv")

# ═══════════════════════════════════════════
#  PAGE: RIWAYAT
# ═══════════════════════════════════════════
elif menu == "🕐 Riwayat":
    st.markdown("## 🕐 Riwayat Pengecekan")

    if not st.session_state.history:
        st.info("Belum ada riwayat. Lakukan pengecekan di menu **Cek Kompatibilitas**.")
    else:
        total = len(st.session_state.history)
        danger_c = sum(1 for h in st.session_state.history if h["status"]=="DANGER")
        caution_c = sum(1 for h in st.session_state.history if h["status"]=="CAUTION")
        safe_c = sum(1 for h in st.session_state.history if h["status"]=="SAFE")

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card"><div class="metric-num">{total}</div><div class="metric-label">Total Cek</div></div>
            <div class="metric-card"><div class="metric-num" style="color:#ef4444">{danger_c}</div><div class="metric-label">Berbahaya</div></div>
            <div class="metric-card"><div class="metric-num" style="color:#f59e0b">{caution_c}</div><div class="metric-label">Hati-Hati</div></div>
            <div class="metric-card"><div class="metric-num" style="color:#22c55e">{safe_c}</div><div class="metric-label">Aman</div></div>
        </div>
        """, unsafe_allow_html=True)

        filter_hist = st.selectbox("Filter Status", ["Semua","🔴 BERBAHAYA","🟡 BERHATI-HATI","🟢 AMAN"])
        st.markdown("---")

        for idx, h in enumerate(st.session_state.history):
            if filter_hist == "🔴 BERBAHAYA" and h["status"] != "DANGER": continue
            if filter_hist == "🟡 BERHATI-HATI" and h["status"] != "CAUTION": continue
            if filter_hist == "🟢 AMAN" and h["status"] != "SAFE": continue

            em = status_emoji(h["status"])
            lbl = status_label(h["status"])
            sc = status_color(h["status"])

            st.markdown(f"""
            <div class="history-item">
                <div>
                    <span class="history-chem">{em} {h['chem1'].split('(')[0].strip()}</span>
                    <span style='color:#475569'> + </span>
                    <span class="history-chem">{h['chem2'].split('(')[0].strip()}</span>
                    <span style='display:inline-block;margin-left:0.75rem;padding:0.15rem 0.6rem;
                          background:{sc}22;border:1px solid {sc}55;border-radius:10px;
                          color:{sc};font-size:0.75rem;font-weight:600'>{lbl}</span>
                </div>
                <span class="history-time">🕐 {h['time']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🗑️ Hapus Semua Riwayat"):
            st.session_state.history = []
            st.rerun()

# ═══════════════════════════════════════════
#  PAGE: PANDUAN
# ═══════════════════════════════════════════
elif menu == "📋 Panduan":
    st.markdown("## 📋 Panduan Penggunaan FCOT ChemSafe")

    st.markdown("""<div class="theory-box"><div class="theory-title">🎯 Tujuan Aplikasi</div>
    <p style='color:#c7d2fe;font-size:0.88rem'>FCOT ChemSafe membantu teknisi K3, petugas laboratorium, dan mahasiswa untuk memahami kompatibilitas antar bahan kimia berbahaya berdasarkan teori FCOT dan standar GHS internasional.</p></div>""", unsafe_allow_html=True)

    steps = [
        ("1️⃣","Pilih Menu","Gunakan sidebar kiri untuk navigasi antar fitur."),
        ("2️⃣","Cek Kompatibilitas","Pilih 2 bahan kimia dari dropdown → Klik ⚡ CEK KOMPATIBILITAS."),
        ("3️⃣","Baca Hasil","Lihat status (🔴 BERBAHAYA / 🟡 HATI-HATI / 🟢 AMAN), reaksi, produk, dan analisis FCOT."),
        ("4️⃣","Simpan Favorit","Klik ⭐ Simpan ke Favorit untuk menyimpan pasangan yang sering dicek."),
        ("5️⃣","Lihat Database","Eksplorasi 35+ bahan kimia di Database Bahan dengan filter kelompok dan FCOT."),
        ("6️⃣","Tambah Bahan Kustom","Tambah bahan kimia kustom via form di halaman Cek Kompatibilitas."),
        ("7️⃣","Pelajari Materi","Buka Materi FCOT untuk belajar teori mendalam tentang F, C, O, T, dan GHS."),
        ("8️⃣","Riwayat","Cek riwayat semua pengecekan yang telah dilakukan di menu Riwayat."),
    ]
    for emoji, title, desc in steps:
        st.markdown(f"""<div class="info-box"><h4>{emoji} {title}</h4><p>{desc}</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.warning("""
**⚠️ Penting: Keterbatasan Aplikasi**

FCOT ChemSafe adalah **alat bantu referensi**, bukan pengganti SDS resmi!
- Selalu konsultasikan **SDS (Safety Data Sheet)** resmi dari produsen
- Pasangan yang tidak ada di database dianalisis secara heuristik — hasilnya bersifat estimasi
- Untuk bahan kimia eksotis/jarang, konsultasikan dengan ahli K3 kimia
    """)

    st.markdown("---")
    st.markdown("### 📞 Tindakan Darurat")
    col_em1, col_em2, col_em3 = st.columns(3)
    with col_em1:
        st.error("**🔥 Kebakaran Kimia**\n1. Aktifkan alarm\n2. Evakuasi area\n3. Jangan gunakan air untuk logam aktif\n4. CO₂ atau dry powder\n5. Hubungi: **113**")
    with col_em2:
        st.error("**☠️ Paparan Bahan Toksik**\n1. Pindahkan ke udara segar\n2. Lepas pakaian terkontaminasi\n3. Bilas mata/kulit 15–20 menit\n4. Jangan induksi muntah\n5. Hubungi: **119** (SPGDT)")
    with col_em3:
        st.error("**🧪 Tumpahan Kimia**\n1. Kenakan APD sebelum mendekati\n2. Batasi penyebaran dengan absorben\n3. Ventilasi area segera\n4. Netralkan sesuai SDS\n5. Lapor ke penanggung jawab lab")

    st.markdown("---")
    st.markdown("### 🎓 Referensi")
    st.markdown("""
| Sumber | Deskripsi |
|--------|-----------|
| **PubChem (NIH)** | Database senyawa kimia terlengkap + SDS |
| **NIOSH Pocket Guide** | Panduan bahaya kimia untuk pekerja |
| **GHS Purple Book (UN)** | Standar GHS resmi dari PBB |
| **Permenaker No.5/2018** | Regulasi K3 Kimia Indonesia |
| **PP 74/2001** | Pengelolaan Bahan Berbahaya & Beracun (B3) |
    """)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#475569;font-size:0.78rem;padding:12px 0;'>
  ⚗️ <strong style='color:#e2e8f0;'>FCOT ChemSafe v3</strong> &nbsp;·&nbsp;
  Kompatibilitas Penyimpanan FCOT · Matrix Asam-Basa · GHS Standard &nbsp;·&nbsp;
  <em>Selalu konsultasikan SDS (Safety Data Sheet) bahan kimia Anda</em>
</div>
""", unsafe_allow_html=True)
