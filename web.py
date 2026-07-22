import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(
    page_title="Analisis Medis AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg:         #f0f4ff;
    --surface:    #ffffff;
    --surface2:   #e8eeff;
    --border:     #d0d9f5;
    --text:       #0f1535;
    --muted:      #5a6490;
    --accent:     #4f46e5;
    --accent2:    #7c3aed;
    --accent-lt:  #eef2ff;
    --diab:       #0ea5e9;
    --diab-dk:    #0369a1;
    --diab-lt:    #e0f5ff;
    --heart:      #f43f5e;
    --heart-dk:   #be123c;
    --heart-lt:   #fff0f3;
    --green:      #10b981;
    --green-dk:   #065f46;
    --green-lt:   #ecfdf5;
    --gold:       #f59e0b;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1e1b4b 0%, #312e81 50%, #1e3a5f 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}

.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 880px !important;
}

/* Hide toolbar */
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], header[data-testid="stHeader"],
#MainMenu { display: none !important; visibility: hidden !important; }

/* ── Sidebar elements ── */
.sb-logo {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.3px;
}
.sb-sub {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: #a5b4fc;
    margin-top: 3px;
    margin-bottom: 1.8rem;
}
.sb-divider {
    border: none;
    border-top: 1px solid rgba(165,180,252,0.2);
    margin: 1.3rem 0;
}
.sb-section-label {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: #a5b4fc;
    margin-bottom: 0.6rem;
    opacity: 0.7;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.07) !important;
    color: #c7d2fe !important;
    border: 1px solid rgba(165,180,252,0.2) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    text-align: left !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border-color: rgba(165,180,252,0.5) !important;
    transform: translateX(3px) !important;
}

/* ── Page heading ── */
.page-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.5rem;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
}
.eyebrow-home  { background: #eef2ff; color: var(--accent); }
.eyebrow-diab  { background: var(--diab-lt); color: var(--diab-dk); }
.eyebrow-heart { background: var(--heart-lt); color: var(--heart-dk); }

.page-title {
    font-family: 'Lora', serif;
    font-size: 2.2rem;
    font-weight: 600;
    line-height: 1.2;
    background: linear-gradient(135deg, #0f1535 0%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
}
.page-title-diab {
    font-family: 'Lora', serif;
    font-size: 2.2rem;
    font-weight: 600;
    line-height: 1.2;
    background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
}
.page-title-heart {
    font-family: 'Lora', serif;
    font-size: 2.2rem;
    font-weight: 600;
    line-height: 1.2;
    background: linear-gradient(135deg, #be123c 0%, #f43f5e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
}
.page-lead {
    font-size: 0.93rem;
    color: var(--muted);
    line-height: 1.75;
    max-width: 580px;
    margin-bottom: 2rem;
}

/* ── Info cards ── */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
}
.info-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.info-card:nth-child(1)::before { background: linear-gradient(90deg, #4f46e5, #7c3aed); }
.info-card:nth-child(2)::before { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
.info-card:nth-child(3)::before { background: linear-gradient(90deg, #10b981, #34d399); }
.info-card .ic-icon  { font-size: 1.5rem; margin-bottom: 0.5rem; }
.info-card .ic-title { font-size: 0.78rem; font-weight: 700; color: var(--text); margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.5px; }
.info-card .ic-body  { font-size: 0.81rem; color: var(--muted); line-height: 1.6; }

/* ── How box ── */
.how-box {
    background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
    border: 1px solid #c7d2fe;
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    margin-bottom: 1.5rem;
}
.how-box .hb-title { font-size: 0.8rem; font-weight: 700; color: var(--accent); margin-bottom: 0.25rem; }
.how-box .hb-body  { font-size: 0.82rem; color: #4338ca; line-height: 1.65; }

/* ── Steps ── */
.steps-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 2rem;
}
.step {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 0.9rem;
    text-align: center;
    transition: all 0.2s;
}
.step .s-num {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 0.55rem;
    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
}
.step .s-text { font-size: 0.78rem; color: var(--muted); line-height: 1.5; }

/* ── CTA buttons on home ── */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    border: none !important;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(79,70,229,0.4) !important;
}

/* ── Form ── */
.form-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(79,70,229,0.06);
}
.form-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px dashed var(--border);
}
.form-top .ft-title { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.model-badge {
    font-size: 0.66rem;
    font-weight: 700;
    padding: 0.28rem 0.75rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-diab  {
    background: linear-gradient(135deg, #bae6fd, #e0f5ff);
    color: var(--diab-dk);
    border: 1px solid #7dd3fc;
}
.badge-heart {
    background: linear-gradient(135deg, #fecdd3, var(--heart-lt));
    color: var(--heart-dk);
    border: 1px solid #fda4af;
}

/* ── Widget overrides ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    background: #fff !important;
}
label, [data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Result cards ── */
.result-danger {
    background: linear-gradient(135deg, #fff0f3 0%, #ffe4e9 100%);
    border: 1.5px solid #fda4af;
    border-left: 5px solid var(--heart);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(244,63,94,0.1);
}
.result-safe {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border: 1.5px solid #6ee7b7;
    border-left: 5px solid var(--green);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(16,185,129,0.1);
}
.result-label {
    font-size: 0.67rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-bottom: 0.35rem;
}
.result-danger .result-label { color: var(--heart-dk); }
.result-safe   .result-label { color: var(--green-dk); }
.result-title {
    font-family: 'Lora', serif;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.result-danger .result-title { color: var(--heart-dk); }
.result-safe   .result-title { color: var(--green-dk); }
.result-prob-row { display: flex; align-items: baseline; gap: 0.45rem; margin-bottom: 0.6rem; }
.result-prob { font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; }
.result-danger .result-prob { color: var(--heart); }
.result-safe   .result-prob { color: var(--green); }
.result-prob-label { font-size: 0.79rem; color: var(--muted); font-weight: 500; }
.result-advice {
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.7;
    border-top: 1px solid rgba(0,0,0,0.07);
    padding-top: 0.65rem;
    margin-top: 0.1rem;
}

/* ── Disclaimer ── */
.disclaimer {
    font-size: 0.73rem;
    color: #94a3b8;
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1.1rem;
    border-top: 1px dashed var(--border);
    line-height: 1.7;
}

/* ── Sidebar disclaimer ── */
.sb-note {
    font-size: 0.71rem;
    color: #a5b4fc;
    line-height: 1.7;
    opacity: 0.75;
}
</style>
""", unsafe_allow_html=True)

# ─── Model Loading ──────────────────────────────────────────────────────────
MODEL_DIR = os.path.dirname(__file__)

@st.cache_resource
def load_models():
    heart  = joblib.load(os.path.join(MODEL_DIR, "jantung"))
    diabet = joblib.load(os.path.join(MODEL_DIR, "diabetes"))
    return heart, diabet

model_heart, model_diabet = load_models()

if "page" not in st.session_state:
    st.session_state.page = "home"

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">Analisis Medis AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Menu Utama</div>', unsafe_allow_html=True)

    if st.button("🏠  Beranda",            key="nav_home",  use_container_width=True):
        st.session_state.page = "home";  st.rerun()
    if st.button("🩸  Prediksi Diabetes",  key="nav_diab",  use_container_width=True):
        st.session_state.page = "diab";  st.rerun()
    if st.button("❤️  Prediksi Jantung",   key="nav_heart", use_container_width=True):
        st.session_state.page = "heart"; st.rerun()

    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sb-note">⚠️ Hasil bersifat indikatif.<br>Bukan pengganti diagnosis dokter.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# BERANDA
# ════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="page-eyebrow eyebrow-home">Selamat Datang</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Analisis Medis AI</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="page-lead">
        Platform skrining kesehatan berbasis <strong>Machine Learning</strong> yang membantu Anda
        memperkirakan risiko Diabetes dan Penyakit Jantung secara cepat dan mudah.
        Masukkan data klinis, dan dapatkan estimasi risiko dalam hitungan detik.
    </p>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-grid">
        <div class="info-card">
            <div class="ic-icon">🎯</div>
            <div class="ic-title">Akurasi Tinggi</div>
            <div class="ic-body">Model dilatih pada dataset medis tervalidasi dengan performa yang optimal.</div>
        </div>
        <div class="info-card">
            <div class="ic-icon">⚡</div>
            <div class="ic-title">Hasil Instan</div>
            <div class="ic-body">Prediksi real-time tanpa menunggu — hasil analisis langsung tersedia.</div>
        </div>
        <div class="info-card">
            <div class="ic-icon">🔒</div>
            <div class="ic-title">Privasi Terjaga</div>
            <div class="ic-body">Data Anda tidak disimpan. Setiap sesi bersih dan sepenuhnya terlindungi.</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="how-box">
        <span style="font-size:1.2rem; margin-top:1px;">📋</span>
        <div>
            <div class="hb-title">Cara Penggunaan</div>
            <div class="hb-body">
                Pilih menu <strong>Prediksi Diabetes</strong> atau <strong>Prediksi Jantung</strong>
                di sidebar kiri → Isi formulir data klinis → Klik <strong>Prediksi Sekarang</strong>
                → Lihat hasil beserta rekomendasi tindakan.
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="steps-row">
        <div class="step"><div class="s-num">1</div><div class="s-text">Pilih jenis pemeriksaan dari menu sidebar</div></div>
        <div class="step"><div class="s-num">2</div><div class="s-text">Isi data klinis sesuai hasil laboratorium</div></div>
        <div class="step"><div class="s-num">3</div><div class="s-text">Tekan tombol Prediksi dan lihat hasilnya</div></div>
        <div class="step"><div class="s-num">4</div><div class="s-text">Konsultasikan ke dokter jika diperlukan</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🩸  Mulai Prediksi Diabetes", use_container_width=True):
            st.session_state.page = "diab"; st.rerun()
    with c2:
        if st.button("❤️  Mulai Prediksi Jantung", use_container_width=True):
            st.session_state.page = "heart"; st.rerun()

    st.markdown("""
    <div class="disclaimer">
        ⚠️ Analisis Medis AI hanya untuk skrining awal dan bersifat indikatif.<br>
        Hasil ini <strong>tidak menggantikan</strong> diagnosis dan pemeriksaan medis profesional.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# PREDIKSI DIABETES
# ════════════════════════════════════════════════════════════════════
elif st.session_state.page == "diab":
    st.markdown('<div class="page-eyebrow eyebrow-diab">🩸 Skrining · Diabetes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title-diab">Prediksi Diabetes</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="page-lead">
        Masukkan 7 parameter klinis berikut untuk memperkirakan risiko diabetes
        menggunakan model <strong>Decision Tree</strong>.
    </p>""", unsafe_allow_html=True)

    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-top">
        <div class="ft-title">📝 Data Klinis Pasien</div>
        <div class="model-badge badge-diab">Decision Tree · 7 Fitur</div>
    </div>""", unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        pregnancies = st.number_input("Jumlah Kehamilan", 0, 20, 0)
        glucose     = st.number_input("Glukosa (mg/dL)", 0, 300, 0)
        blood_pres  = st.number_input("Tekanan Darah Diastolik (mmHg)", 0, 150, 0)
        insulin     = st.number_input("Insulin (µU/mL)", 0, 900, 0)
    with d2:
        bmi   = st.number_input("BMI (kg/m²)", 0.0, 70.0, 0.0, step=0.1)
        dpf   = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.0, step=0.01)
        age_d = st.number_input("Usia (tahun)", 1, 120, 1, key="age_d")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍  Prediksi Sekarang", key="btn_diab", use_container_width=True):
        X    = np.array([[pregnancies, insulin, bmi, age_d, glucose, blood_pres, dpf]])
        pred = model_diabet.predict(X)[0]
        prob = model_diabet.predict_proba(X)[0]
        if pred == 1:
            st.markdown(f"""
            <div class="result-danger">
                <div class="result-label">⚠️ Hasil Deteksi</div>
                <div class="result-title">Terdeteksi Risiko Diabetes</div>
                <div class="result-prob-row">
                    <div class="result-prob">{prob[1]*100:.1f}%</div>
                    <div class="result-prob-label">probabilitas risiko</div>
                </div>
                <div class="result-advice">
                    Berdasarkan parameter yang dimasukkan, terdapat indikasi risiko diabetes yang perlu diperhatikan.
                    Disarankan berkonsultasi dengan <strong>dokter spesialis endokrinologi</strong> untuk pemeriksaan lanjutan.
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-label">✅ Hasil Deteksi</div>
                <div class="result-title">Tidak Terdeteksi Diabetes</div>
                <div class="result-prob-row">
                    <div class="result-prob">{prob[0]*100:.1f}%</div>
                    <div class="result-prob-label">probabilitas aman</div>
                </div>
                <div class="result-advice">
                    Tidak ditemukan indikasi risiko diabetes berdasarkan parameter yang dimasukkan.
                    Pertahankan pola makan sehat, kontrol gula darah rutin, dan aktif berolahraga.
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ Hasil prediksi bersifat indikatif dan tidak menggantikan diagnosis medis profesional.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# PREDIKSI JANTUNG
# ════════════════════════════════════════════════════════════════════
elif st.session_state.page == "heart":
    st.markdown('<div class="page-eyebrow eyebrow-heart">❤️ Skrining · Kardiovaskular</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title-heart">Prediksi Penyakit Jantung</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="page-lead">
        Masukkan 4 parameter klinis berikut untuk memperkirakan risiko penyakit jantung
        menggunakan model <strong>Random Forest</strong>.
    </p>""", unsafe_allow_html=True)

    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-top">
        <div class="ft-title">📝 Data Klinis Pasien</div>
        <div class="model-badge badge-heart">Random Forest · 4 Fitur</div>
    </div>""", unsafe_allow_html=True)

    h1, h2 = st.columns(2)
    with h1:
        age  = st.number_input("Usia (tahun)", 1, 120, value=1, key="age_h")
        sex  = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    with h2:
        bp   = st.number_input("Tekanan Darah / BP (mmHg)", 50, 250, value=50)
        chol = st.number_input("Kolesterol (mg/dL)", 50, 600, value=50)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍  Prediksi Sekarang", key="btn_heart", use_container_width=True):
        sex_val = 1 if sex == "Laki-laki" else 0
        X    = np.array([[age, sex_val, bp, chol]])
        pred = model_heart.predict(X)[0]
        prob = model_heart.predict_proba(X)[0]
        if pred == 1:
            st.markdown(f"""
            <div class="result-danger">
                <div class="result-label">⚠️ Hasil Deteksi</div>
                <div class="result-title">Risiko Tinggi Penyakit Jantung</div>
                <div class="result-prob-row">
                    <div class="result-prob">{prob[1]*100:.1f}%</div>
                    <div class="result-prob-label">probabilitas risiko</div>
                </div>
                <div class="result-advice">
                    Terdapat indikasi risiko penyakit jantung yang signifikan berdasarkan parameter yang dimasukkan.
                    Disarankan segera berkonsultasi dengan <strong>dokter spesialis jantung (kardiolog)</strong>
                    untuk pemeriksaan EKG dan penanganan lebih lanjut.
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-label">✅ Hasil Deteksi</div>
                <div class="result-title">Risiko Rendah Penyakit Jantung</div>
                <div class="result-prob-row">
                    <div class="result-prob">{prob[0]*100:.1f}%</div>
                    <div class="result-prob-label">probabilitas aman</div>
                </div>
                <div class="result-advice">
                    Tidak ditemukan indikasi risiko penyakit jantung yang serius berdasarkan parameter yang dimasukkan.
                    Tetap jaga pola hidup sehat, hindari merokok, dan lakukan pemeriksaan jantung secara rutin.
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ Hasil prediksi bersifat indikatif dan tidak menggantikan diagnosis medis profesional.
    </div>""", unsafe_allow_html=True)