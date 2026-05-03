import streamlit as st
from PIL import Image
import io

from model import predict_spiral

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-PD | Early Parkinson's Detection",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    min-height: 100vh;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 32px;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(100, 116, 139, 0.3);
    margin: -1rem -1rem 2rem -1rem;
    border-radius: 0;
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    text-decoration: none;
}

.navbar-brand span { color: #22d3ee; }

/* Hero section */
.hero {
    text-align: center;
    padding: 2rem 0 2.5rem 0;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.hero-title span { color: #22d3ee; }

.hero-subtitle {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.75rem;
}

.hero-desc {
    font-size: 1rem;
    color: #94a3b8;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Cards */
.card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(100, 116, 139, 0.3);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(10px);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
    margin-bottom: 0.5rem;
}

.card-text {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* Section headings for About */
.about-heading {
    font-size: 1.4rem;
    font-weight: 700;
    color: #22d3ee;
    margin-bottom: 0.75rem;
}

.about-text {
    color: #cbd5e1;
    line-height: 1.75;
    font-size: 0.95rem;
}

/* Result box */
.result-positive {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.5);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}

.result-negative {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.5);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}

.result-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.disclaimer-box {
    background: rgba(234, 179, 8, 0.1);
    border: 1px solid rgba(234, 179, 8, 0.4);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: 0.85rem;
    color: #fde68a;
    line-height: 1.6;
}

/* Spiral SVG wrapper */
.spiral-wrapper {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
}

/* Nav buttons — compact horizontal pills */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(100,116,139,0.35) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.35rem 1.1rem !important;
    font-size: 0.9rem !important;
    width: auto !important;
    white-space: nowrap !important;
    writing-mode: horizontal-tb !important;
    text-orientation: mixed !important;
    min-height: unset !important;
    height: auto !important;
    line-height: 1.4 !important;
    letter-spacing: normal !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
    background: rgba(34,211,238,0.12) !important;
    color: #22d3ee !important;
    border-color: #22d3ee !important;
}

/* Action buttons (Analyze / Clear) */
.action-btn div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.action-btn div[data-testid="stButton"] button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.35) !important;
}

/* File uploader — larger */
[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 2px dashed rgba(100, 116, 139, 0.5) !important;
    border-radius: 14px !important;
    padding: 2rem 1.5rem !important;
}

[data-testid="stFileUploader"] label {
    font-size: 1.05rem !important;
    color: #e2e8f0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 140px !important;
    display: flex !important;
    justify-content: center !important;
}

/* Divider */
hr { border-color: rgba(100, 116, 139, 0.3); }

/* Page title */
.page-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 1.5rem;
}
/* ============================= */
/* TRUE RESPONSIVE PATCH (SAFE) */
/* ============================= */

@media (max-width: 768px) {

    /* Fix navbar overflow */
    .navbar {
        padding: 12px 16px !important;
        margin: -1rem -1rem 1.2rem -1rem !important;
        flex-wrap: wrap !important;
        gap: 8px;
    }

    .navbar-brand {
        font-size: 1.1rem !important;
    }

    /* Reduce hero size slightly */
    .hero-title {
        font-size: 2.1rem !important;
    }

    .hero-subtitle {
        font-size: 1.05rem !important;
    }

    .hero-desc {
        font-size: 0.9rem !important;
        padding: 0 10px;
    }

    /* Allow nav buttons to wrap instead of overflow */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 6px;
    }

    /* Keep nav buttons clean */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
        font-size: 0.8rem !important;
        padding: 0.3rem 0.8rem !important;
    }

    /* Stack columns vertically (Streamlit fix) */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 100% !important;
    }

    /* Fix Analyze/Clear buttons */
    .action-btn div[data-testid="stButton"] button {
        width: 100% !important;
    }

    /* Prevent image overflow */
    img {
        max-width: 100% !important;
        height: auto !important;
    }

    /* Reduce card padding slightly */
    .card {
        padding: 1.3rem !important;
    }

    /* Fix file uploader scaling */
    [data-testid="stFileUploader"] {
        padding: 1.5rem 1rem !important;
    }
}
            
* ===== CARD HOVER EFFECT ===== */
.card {
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

/* ===== PAGE FADE-IN ===== */
.stApp {
    animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
            
/* ===== FILE UPLOADER HOVER ===== */
[data-testid="stFileUploader"] {
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #22d3ee !important;
    background: rgba(30,41,59,0.75) !important;
}
            
/* ===== RESULT REVEAL ANIMATION ===== */
.reveal {
    animation: revealFade 0.5s ease forwards;
}

@keyframes revealFade {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─── Navbar ──────────────────────────────────────────────────────────────────
col_brand, col_spacer, col_nav = st.columns([3, 4, 2])

with col_brand:
    st.markdown('<div class="navbar-brand">🧠 <span>AI-PD</span></div>', unsafe_allow_html=True)

with col_nav:
    nav_c1, nav_c2 = st.columns(2)
    with nav_c1:
        if st.button("Home", key="nav_home"):
            st.session_state.page = "Home"
            st.rerun()
    with nav_c2:
        if st.button("About", key="nav_about"):
            st.session_state.page = "About"
            st.rerun()

st.markdown("<hr style='margin-top:0.3rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":

    # Hero
    st.markdown("""
    <div class="hero" style="text-align:center; width:100%;">
        <div class="hero-title" style="text-align:center;">⚡ <span>AI-PD</span></div>
        <div class="hero-subtitle">Early Parkinson's Detection</div>
        <div class="hero-desc">
            Upload your spiral drawing and let our AI analyze early symptoms within seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sample spiral card — smaller SVG
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div class="card-title">📐 Sample Spiral Drawing</div>
        <div class="card-text">Draw a spiral on paper similar to this example and upload a photo.</div>
        <div class="spiral-wrapper">
            <svg width="160" height="160" viewBox="0 0 200 200">
                <defs>
                    <linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#06b6d4"/>
                        <stop offset="100%" stop-color="#2563eb"/>
                    </linearGradient>
                </defs>
                <path d="M 100,100 C 100,90 110,85 115,90 C 120,95 120,105 115,110
                         C 110,115 95,115 90,105 C 85,95 85,80 95,70
                         C 105,60 125,60 135,70 C 145,80 150,100 140,115
                         C 130,130 110,135 90,125 C 70,115 60,95 65,75
                         C 70,55 90,40 115,45 C 140,50 160,70 160,95
                         C 160,120 145,145 120,150 C 95,155 70,140 60,115
                         C 50,90 55,60 80,45 C 105,30 140,35 160,60"
                      fill="none" stroke="url(#sg)" stroke-width="3"
                      stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload section
    uploaded_file = st.file_uploader(
        "Upload your spiral drawing (JPG or PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible",
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"✅ {uploaded_file.name}", use_container_width=True)

    # Buttons
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        analyze_clicked = st.button(
            "🔍 Analyze Drawing",
            disabled=(uploaded_file is None),
            key="analyze_btn",
        )

    with col2:
        if uploaded_file:
            clear_clicked = st.button("✖ Clear", key="clear_btn")
            if clear_clicked:
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Analysis result ──────────────────────────────────────────────────────
    if analyze_clicked and uploaded_file:
        with st.spinner("Analyzing your spiral drawing…"):

            
            prediction, confidence, explanation = predict_spiral(image)
            # ----------------------------------------------------------------

        if prediction is None:
            st.markdown("""
            <div class="card" style="text-align:center; border-color: rgba(6,182,212,0.4);">
                <div style="font-size:2rem;">🔬</div>
                <div style="color:#22d3ee; font-size:1.2rem; font-weight:700; margin:0.5rem 0;">
                    Analysis Ready
                </div>
                <div style="color:#94a3b8; font-size:0.95rem;">
                    The ML model backend is not yet connected.<br>
                    Replace the <code style="color:#22d3ee;">TODO</code> block in <code style="color:#22d3ee;">app.py</code>
                    with your model inference code to see real predictions.
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif prediction:
            st.markdown(f"""
            <div class="result-positive reveal">
                <div class="result-title" style="color:#f87171;">⚠️ Parkinson's Indicators Detected</div>
                <div style="color:#fca5a5; font-size:1rem;">Confidence: {confidence*100:.1f}%</div>
                <div style="color:#fca5a5; margin-top:0.5rem; font-size:0.9rem;">{explanation}</div>
            </div>
            """, unsafe_allow_html=True)
    
        else:
            st.markdown(f"""
            <div class="result-negative reveal">
                <div class="result-title" style="color:#4ade80;">✅ No Parkinson's Indicators</div>
                <div style="color:#86efac; font-size:1rem;">Confidence: {confidence*100:.1f}%</div>
                <div style="color:#86efac; margin-top:0.5rem; font-size:0.9rem;">{explanation}</div>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("""
        <div class="disclaimer-box" style="margin-top:1rem;">
            ⚠️ <strong>Disclaimer:</strong> This tool is for screening purposes only and is not a substitute
            for professional medical diagnosis. Please consult a qualified neurologist for an accurate assessment.
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  ABOUT PAGE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "About":

    st.markdown('<div class="page-title">About AI-PD</div>', unsafe_allow_html=True)

    sections = [
        (
            "🎯 Our Mission",
            """AI-PD is dedicated to revolutionizing early detection of Parkinson's Disease through
            advanced artificial intelligence. Our mission is to provide accessible, accurate, and
            rapid screening tools that empower healthcare professionals and patients with early
            insights into neurological health.""",
        ),
        (
            "🧠 Understanding Parkinson's Disease",
            """Parkinson's Disease is a progressive neurological disorder that affects movement control.
            Early symptoms include tremors or shaking (usually beginning in a limb), slowed movement
            (bradykinesia), rigid muscles and reduced flexibility, impaired posture and balance,
            and changes in speech and handwriting.""",
        ),
        (
            "⚙️ How AI-PD Works",
            """Our AI model analyzes spiral drawings using deep learning algorithms trained on thousands
            of verified cases. The system identifies subtle tremor patterns and motor irregularities
            that may indicate early-stage Parkinson's Disease — often before traditional symptoms
            become clinically apparent. The analysis considers stroke consistency, tremor frequency,
            and spatial regularity of the drawn spiral.""",
        ),
        (
            "⚠️ Important Disclaimer",
            """AI-PD is a screening tool designed to assist healthcare professionals. It is not a
            substitute for professional medical diagnosis or treatment. All results should be reviewed
            by qualified neurologists or movement disorder specialists. If you or someone you know is
            experiencing symptoms, please consult with a healthcare provider immediately.""",
        ),
    ]

    for title, body in sections:
        st.markdown(f"""
        <div class="card">
            <div class="about-heading">{title}</div>
            <div class="about-text">{body}</div>
        </div>
        """, unsafe_allow_html=True)
