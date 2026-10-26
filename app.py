"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
"""

import streamlit as st
import json
import math
import requests
import io
import base64
import datetime
from PIL import Image

# ─────────────────────────────────────────────
#  Page configuration (MUST be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Inject custom CSS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1421 40%, #111827 100%);
        color: #e2e8f0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #f8fafc;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #cbd5e1;
        font-size: 0.88rem;
    }

    /* ── Tab styles ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,23,42,0.8);
        border-radius: 16px;
        padding: 6px;
        gap: 4px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 10px 18px;
        transition: all 0.25s ease;
        border: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(51,65,85,0.6);
        color: #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: #ffffff !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(59,130,246,0.4);
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }

    /* ── Hero banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a2a4a 50%, #0f172a 100%);
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.5rem 0;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0;
        font-weight: 400;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 30px rgba(59,130,246,0.2);
        transform: translateY(-2px);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        border-radius: 16px 16px 0 0;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1;
    }
    .metric-delta {
        font-size: 0.82rem;
        color: #34d399;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* ── Status pills ── */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .pill-safe    { background: rgba(52,211,153,0.15); color:#34d399; border:1px solid rgba(52,211,153,0.3); }
    .pill-warning { background: rgba(251,191,36,0.15);  color:#fbbf24; border:1px solid rgba(251,191,36,0.3); }
    .pill-danger  { background: rgba(239,68,68,0.15);   color:#f87171; border:1px solid rgba(239,68,68,0.3); }
    .pill-critical{ background: rgba(220,38,38,0.25);   color:#fca5a5; border:1px solid rgba(220,38,38,0.5); }
    .pill-info    { background: rgba(59,130,246,0.15);  color:#60a5fa; border:1px solid rgba(59,130,246,0.3); }

    /* ── Section headings ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.8rem 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #1e293b;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0;
    }

    /* ── Hazard / Defect cards ── */
    .hazard-card {
        background: rgba(15,23,42,0.8);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #ef4444;
        border-top: 1px solid #1e293b;
        border-right: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
        transition: all 0.2s;
    }
    .hazard-card:hover { background: rgba(30,41,59,0.9); }
    .hazard-title { font-weight: 600; color: #f1f5f9; margin-bottom: 0.25rem; font-size: 0.95rem; }
    .hazard-desc  { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

    /* ── Chat messages ── */
    .chat-user {
        background: linear-gradient(135deg, #1d4ed8, #4f46e5);
        border-radius: 18px 18px 4px 18px;
        padding: 0.85rem 1.1rem;
        margin: 0.5rem 0 0.5rem 20%;
        color: #fff;
        font-size: 0.9rem;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(59,130,246,0.25);
    }
    .chat-assistant {
        background: rgba(30,41,59,0.9);
        border: 1px solid #334155;
        border-radius: 18px 18px 18px 4px;
        padding: 0.85rem 1.1rem;
        margin: 0.5rem 20% 0.5rem 0;
        color: #e2e8f0;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* ── PPE checklist item ── */
    .ppe-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        background: rgba(15,23,42,0.7);
        border: 1px solid #1e293b;
    }
    .ppe-name { font-weight: 500; color: #cbd5e1; font-size: 0.9rem; }
    .ppe-detected { color: #34d399; font-weight: 600; }
    .ppe-missing  { color: #f87171; font-weight: 600; }

    /* ── Progress bar ── */
    .progress-container {
        background: rgba(30,41,59,0.8);
        border-radius: 50px;
        height: 12px;
        overflow: hidden;
        border: 1px solid #334155;
        margin: 0.5rem 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 50px;
        background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6);
        transition: width 0.8s ease;
    }

    /* ── Weather alert box ── */
    .weather-alert {
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .alert-high-wind  { background: rgba(251,191,36,0.1);  border:1px solid rgba(251,191,36,0.35);  color:#fde68a; }
    .alert-heavy-rain { background: rgba(59,130,246,0.1);  border:1px solid rgba(59,130,246,0.35);  color:#bfdbfe; }
    .alert-extreme-heat { background: rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.35);   color:#fecaca; }
    .alert-normal     { background: rgba(52,211,153,0.1);  border:1px solid rgba(52,211,153,0.35);  color:#a7f3d0; }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: rgba(15,23,42,0.6);
        border: 2px dashed #334155;
        border-radius: 14px;
        transition: border-color 0.3s;
    }
    [data-testid="stFileUploader"]:hover { border-color: #3b82f6; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.6rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(59,130,246,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59,130,246,0.5);
    }
    .stButton > button:active { transform: translateY(0); }

    /* ── Inputs ── */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(30,41,59,0.8) !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ── Dividers ── */
    hr { border-color: #1e293b; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width:6px; height:6px; }
    ::-webkit-scrollbar-track { background:#0f172a; }
    ::-webkit-scrollbar-thumb { background:#334155; border-radius:3px; }
    ::-webkit-scrollbar-thumb:hover { background:#475569; }

    /* ── Info box ── */
    .info-box {
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #93c5fd;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    /* ── Architecture node ── */
    .arch-node {
        background: rgba(30,41,59,0.8);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.78rem;
        color: #94a3b8;
        margin: 3px 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── 3D render card ── */
    .render-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid #334155;
        border-radius: 16px;
        overflow: hidden;
        text-align: center;
    }
    .render-label {
        padding: 0.8rem;
        font-size: 0.8rem;
        color: #64748b;
        background: rgba(15,23,42,0.8);
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Gemini helper
# ─────────────────────────────────────────────
def get_gemini_model(api_key: str):
    """Initialise and return a Gemini model, or None on failure."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        st.error(f"Gemini init error: {e}")
        return None


def call_gemini_text(model, prompt: str) -> str:
    """Call Gemini with a text-only prompt."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini error] {e}"


def call_gemini_vision(model, prompt: str, image: Image.Image) -> str:
    """Call Gemini with a text + image prompt."""
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"[Gemini error] {e}"


def extract_json(text: str) -> dict | None:
    """Extract the first JSON object found in a string."""
    import re
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


# ─────────────────────────────────────────────
#  Demo / Fallback data generators
# ─────────────────────────────────────────────
def demo_safety_result() -> dict:
    return {
        "safety_score": 67,
        "overall_status": "NEEDS IMPROVEMENT",
        "standards_referenced": ["OSHA 29 CFR 1926", "IS 456:2000", "NBC 2016"],
        "ppe_detection": {
            "hard_hat": {"detected": True,  "compliance": "Compliant"},
            "high_vis_vest": {"detected": False, "compliance": "Non-Compliant"},
            "steel_toe_boots": {"detected": True, "compliance": "Compliant"},
            "safety_harness": {"detected": False, "compliance": "Non-Compliant – Required at height > 1.8m"},
            "safety_gloves": {"detected": True,  "compliance": "Compliant"},
            "eye_protection": {"detected": False, "compliance": "Non-Compliant"}
        },
        "site_hazards": [
            {
                "hazard": "Workers operating at height without harness",
                "severity": "Critical",
                "remedy": "Immediately halt elevated work; enforce full-body harness with double-locking carabiner. Conduct toolbox talk before resuming."
            },
            {
                "hazard": "No high-visibility vests on workers near vehicle movement zones",
                "severity": "High",
                "remedy": "Issue EN ISO 20471 Class 2+ vests to all personnel in active vehicle corridors. Establish exclusion zones."
            },
            {
                "hazard": "Unguarded excavation pit edge",
                "severity": "High",
                "remedy": "Install rigid barriers and warning tape at ≥ 1m from pit edge per IS 3764. Add signage."
            },
            {
                "hazard": "Scattered debris and trip hazards on walkways",
                "severity": "Medium",
                "remedy": "Implement 5S housekeeping protocol. Designate clearly marked pedestrian pathways."
            },
            {
                "hazard": "Inadequate lighting in lower level work area",
                "severity": "Low",
                "remedy": "Install portable LED flood lights rated ≥ 200 lux as per IS 3646 Part I."
            }
        ],
        "recommendations": "Conduct immediate safety stand-down meeting. Update safety induction records. Re-audit in 72 hours."
    }


def demo_crack_result() -> dict:
    return {
        "defect_type": "Structural Shear Crack",
        "crack_width_mm": 2.8,
        "crack_length_estimate": "~450 mm visible",
        "pattern": "Diagonal at 45° from beam-column junction",
        "severity": "High",
        "urgency": "Immediate Engineering Assessment Required",
        "root_causes": [
            "Differential settlement of foundation",
            "Inadequate shear reinforcement (stirrup spacing > IS 456 limits)",
            "Possible overloading beyond design load",
            "Poor concrete mix with w/c ratio > 0.55"
        ],
        "recommended_repairs": [
            {
                "method": "Epoxy Injection (Low-Viscosity)",
                "detail": "Drill ports @ 150mm centres along crack, inject epoxy resin under pressure (0.3–0.5 MPa) per ACI 224.1R. Allow 24h cure before loading."
            },
            {
                "method": "Carbon Fibre Reinforced Polymer (CFRP) Wrapping",
                "detail": "Apply CFRP strips perpendicular to crack direction for shear strengthening as per IS 15988."
            },
            {
                "method": "Structural Re-grouting",
                "detail": "If crack width > 2mm at core: re-grout with non-shrink cementitious grout (grade ≥ M40) after surface preparation."
            }
        ],
        "standards": ["IS 456:2000", "IS 13920", "ACI 318", "IS 15988"],
        "monitoring": "Install crack width gauge (Demec points) at 300mm intervals. Re-survey every 7 days for 4 weeks."
    }


WEATHER_ADVISORIES = {
    "High Wind (>50 km/h)": {
        "icon": "💨",
        "class": "alert-high-wind",
        "title": "High Wind Advisory — Elevated Risk Operations",
        "alerts": [
            "🚫 **Suspend all crane and hoist operations** immediately above 50 km/h sustained winds (OSHA 1926.1416).",
            "⚠️ Secure all loose materials, scaffolding boards, and formwork panels with lashing or removal.",
            "🔩 Check anchorage of temporary structures; increase guy-wire tension by 30%.",
            "👷 Issue high-visibility double-layer vests; reduce worker exposure on elevated platforms.",
            "📋 Activate wind speed logging protocol — re-permit crane ops only after 30-min sustained calm.",
            "🏗️ Inspect scaffolding ties post-wind event before resuming work at height.",
        ]
    },
    "Heavy Rain / Flooding": {
        "icon": "🌧️",
        "class": "alert-heavy-rain",
        "title": "Heavy Rain & Waterlogging Advisory",
        "alerts": [
            "⚡ **Electrical hazard mitigation**: De-energise all temporary power distribution boards; use GFCI protected outlets only.",
            "🛑 Halt all excavation activities — slope stability compromised; inspect shoring for water ingress.",
            "🏊 Pump out collected water from trenches before worker re-entry; test for oxygen deficiency.",
            "🧱 Suspend concrete pour operations if rain rate > 10mm/hr — dilution of w/c ratio invalidates mix design.",
            "🚧 Redirect site traffic; install temporary drainage channels to prevent erosion of formed slopes.",
            "☂️ Provide waterproof PPE (suits, rubber boots rated to IS 4770) for essential personnel.",
        ]
    },
    "Extreme Heat (>42 °C)": {
        "icon": "🌡️",
        "class": "alert-extreme-heat",
        "title": "Extreme Heat Stress Advisory",
        "alerts": [
            "💧 **Mandatory hydration protocol**: Provide 1 litre cool water per worker per hour; no exceptions.",
            "🌅 Reschedule heavy manual labour to before 10:00 AM and after 4:00 PM IST.",
            "🧊 Set up shaded rest stations every 200m; enforce 15-min cool-down breaks every 90 min.",
            "🏗️ Monitor concrete curing closely — extreme heat accelerates water evaporation; apply curing compound within 20 min of finishing.",
            "🩺 Designate first-aid responders trained in heat stroke management; keep ORS and ice packs on site.",
            "🌡️ Halt operations if wet-bulb globe temperature (WBGT) exceeds 35°C per ACGIH TLV guidelines.",
        ]
    },
    "Normal Conditions": {
        "icon": "☀️",
        "class": "alert-normal",
        "title": "Standard Operations — All Clear",
        "alerts": [
            "✅ Normal site operations approved — conduct standard pre-shift safety toolbox talk.",
            "📋 Verify daily safety checklist: PPE compliance, equipment pre-use inspection, task hazard analysis.",
            "🦺 Enforce baseline PPE: hard hat, high-vis vest, steel-toe boots for all site personnel.",
            "🏗️ Proceed with planned concrete pours, structural works, and equipment operations per approved method statements.",
            "🌱 Good conditions for concrete curing — maintain moist curing for ≥ 7 days for OPC (IS 456).",
            "📅 Schedule non-urgent inspections, quality audits, and subcontractor coordination meetings.",
        ]
    }
}


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
            <div style='font-size:3rem;'>🏗️</div>
            <h2 style='color:#60a5fa; font-size:1.05rem; font-weight:700; margin:0.3rem 0 0 0;'>
                Construction Intelligence
            </h2>
            <p style='color:#475569; font-size:0.75rem; margin:0;'>Skill Wallet Capstone Project 1</p>
        </div>
        <hr style='border-color:#1e293b; margin: 1rem 0;'>
        """, unsafe_allow_html=True)

        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Obtain from https://aistudio.google.com/app/apikey — Leave blank for demo mode.",
            key="gemini_api_key"
        )

        if api_key:
            st.markdown('<span class="status-pill pill-safe">✓ Live AI Mode</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill pill-warning">⚡ Demo Mode</span>', unsafe_allow_html=True)
            st.markdown("""
            <div class="info-box" style="margin-top:0.5rem;">
            Running with pre-computed demonstration data. Enter a valid Gemini API key to enable live multimodal analysis.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e293b; margin: 1rem 0;'>", unsafe_allow_html=True)

        st.markdown("### 🏛️ Architecture")
        st.markdown("""
        <div class="arch-node">🧠 Gemini 1.5 Flash (Multimodal LLM)</div>
        <div class="arch-node">🖼️ Vision API — PPE & Crack Detection</div>
        <div class="arch-node">📊 Plotly — Interactive Visualisations</div>
        <div class="arch-node">🎨 Pollinations AI — 3D Render Generator</div>
        <div class="arch-node">🌐 Streamlit — Zero-infra Deployment</div>
        <div class="arch-node">📦 Zero External Database</div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e293b; margin: 1rem 0;'>", unsafe_allow_html=True)

        st.markdown("### 📂 Feature Modules")
        st.markdown("""
        <div style='font-size:0.83rem; color:#94a3b8; line-height:2;'>
        🦺 <b>Tab 1</b> — Site Safety & PPE Audit<br>
        🔬 <b>Tab 2</b> — Crack Diagnostics<br>
        💰 <b>Tab 3</b> — Planning & Valuation<br>
        🤖 <b>Tab 4</b> — Daily Site Assistant<br>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e293b; margin: 1rem 0;'>", unsafe_allow_html=True)

        st.markdown("""
        <div style='font-size:0.72rem; color:#374151; text-align:center;'>
        Standards: OSHA 29 CFR 1926 · IS 456:2000<br>NBC 2016 · IS 13920 · ACI 318<br><br>
        © 2025 Skill Wallet Capstone
        </div>
        """, unsafe_allow_html=True)

    return api_key


# ─────────────────────────────────────────────
#  TAB 1 — Site Safety & PPE Audit
# ─────────────────────────────────────────────
def render_safety_tab(model):
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">🦺 Site Safety & PPE Audit</h1>
        <p class="hero-subtitle">AI-powered multimodal analysis against OSHA 29 CFR 1926 & IS 456:2000 standards</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Construction Site Photo",
        type=["jpg", "jpeg", "png"],
        key="safety_upload",
        help="Upload a clear site photo for comprehensive PPE compliance and hazard analysis"
    )

    col_img, col_ctrl = st.columns([3, 1])
    image_obj = None

    with col_img:
        if uploaded:
            image_obj = Image.open(uploaded)
            st.image(image_obj, caption="Uploaded Site Photo", use_container_width=True)
        else:
            st.markdown("""
            <div style='background:rgba(15,23,42,0.6); border:1px dashed #334155; border-radius:14px;
                        padding:3rem; text-align:center; color:#475569;'>
                <div style='font-size:3rem;'>📸</div>
                <p style='margin:0.5rem 0 0 0; font-size:0.9rem;'>Upload a site image to begin analysis</p>
            </div>
            """, unsafe_allow_html=True)

    with col_ctrl:
        st.markdown("<br>", unsafe_allow_html=True)
        run_analysis = st.button("🔍 Run PPE Audit", key="run_safety", use_container_width=True)
        st.markdown("**Analysis Covers:**")
        for item in ["Hard Hat", "High-Vis Vest", "Steel-Toe Boots", "Safety Harness", "Safety Gloves", "Eye Protection"]:
            st.markdown(f"- {item}")

    if run_analysis:
        with st.spinner("🤖 Analysing site photo with Gemini Vision..."):
            if model and image_obj:
                prompt = """You are a certified construction safety inspector trained in OSHA 29 CFR 1926 and IS 456:2000.
Analyse this construction site image and return ONLY valid JSON (no markdown fences) with:
{
  "safety_score": <integer 0-100>,
  "overall_status": "<SAFE|NEEDS IMPROVEMENT|UNSAFE|CRITICAL>",
  "standards_referenced": ["<list of applicable standards>"],
  "ppe_detection": {
    "hard_hat": {"detected": <bool>, "compliance": "<text>"},
    "high_vis_vest": {"detected": <bool>, "compliance": "<text>"},
    "steel_toe_boots": {"detected": <bool>, "compliance": "<text>"},
    "safety_harness": {"detected": <bool>, "compliance": "<text>"},
    "safety_gloves": {"detected": <bool>, "compliance": "<text>"},
    "eye_protection": {"detected": <bool>, "compliance": "<text>"}
  },
  "site_hazards": [
    {"hazard": "<description>", "severity": "<Low|Medium|High|Critical>", "remedy": "<actionable remedy>"}
  ],
  "recommendations": "<overall recommendation text>"
}"""
                raw = call_gemini_vision(model, prompt, image_obj)
                result = extract_json(raw)
                if not result:
                    result = demo_safety_result()
                    st.info("⚠️ Could not parse live response — showing structured demo data.")
            else:
                result = demo_safety_result()
                if not model:
                    st.info("ℹ️ Demo mode — enter Gemini API key for live analysis.")
                elif not image_obj:
                    st.warning("Please upload an image first.")
                    return

        _render_safety_results(result)


def _render_safety_results(result: dict):
    score = result.get("safety_score", 0)
    status = result.get("overall_status", "UNKNOWN")

    # Score colour
    if score >= 80:
        score_color = "#34d399"
        pill_class = "pill-safe"
    elif score >= 60:
        score_color = "#fbbf24"
        pill_class = "pill-warning"
    elif score >= 40:
        score_color = "#f87171"
        pill_class = "pill-danger"
    else:
        score_color = "#dc2626"
        pill_class = "pill-critical"

    # ── Top metrics row ──
    st.markdown("<div class='section-header'><h3 class='section-title'>📊 Audit Summary</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Safety Score</div>
            <div class="metric-value" style="color:{score_color};">{score}</div>
            <div class="metric-delta">out of 100</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        ppe = result.get("ppe_detection", {})
        detected_count = sum(1 for v in ppe.values() if isinstance(v, dict) and v.get("detected"))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PPE Detected</div>
            <div class="metric-value">{detected_count}/{len(ppe)}</div>
            <div class="metric-delta">items compliant</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        hazards = result.get("site_hazards", [])
        critical = sum(1 for h in hazards if h.get("severity") in ["Critical", "High"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High+ Hazards</div>
            <div class="metric-value" style="color:#f87171;">{critical}</div>
            <div class="metric-delta">requiring action</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Status</div>
            <div style="margin-top:0.6rem;">
                <span class="status-pill {pill_class}">{status}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_ppe, col_haz = st.columns(2)

    # ── PPE checklist ──
    with col_ppe:
        st.markdown("<div class='section-header'><h3 class='section-title'>🦺 PPE Compliance Checklist</h3></div>", unsafe_allow_html=True)
        ppe_labels = {
            "hard_hat": "🪖 Hard Hat",
            "high_vis_vest": "🦺 High-Vis Vest",
            "steel_toe_boots": "👢 Steel-Toe Boots",
            "safety_harness": "🔗 Safety Harness",
            "safety_gloves": "🧤 Safety Gloves",
            "eye_protection": "🥽 Eye Protection"
        }
        for key, label in ppe_labels.items():
            item = ppe.get(key, {"detected": False, "compliance": "Unknown"})
            detected = item.get("detected", False)
            compliance = item.get("compliance", "")
            status_txt = '<span class="ppe-detected">✓ Detected</span>' if detected else '<span class="ppe-missing">✗ Missing</span>'
            st.markdown(f"""
            <div class="ppe-item">
                <span class="ppe-name">{label}</span>
                <div style="text-align:right;">
                    {status_txt}
                    <div style="font-size:0.75rem; color:#64748b; max-width:180px;">{compliance}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Hazards ──
    with col_haz:
        st.markdown("<div class='section-header'><h3 class='section-title'>⚠️ Identified Site Hazards</h3></div>", unsafe_allow_html=True)
        severity_colors = {"Critical": "#dc2626", "High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}
        for h in hazards:
            sev = h.get("severity", "Low")
            color = severity_colors.get(sev, "#3b82f6")
            st.markdown(f"""
            <div class="hazard-card" style="border-left-color:{color};">
                <div class="hazard-title">
                    {h.get('hazard','Hazard')}
                    <span class="status-pill" style="font-size:0.7rem; padding:3px 10px;
                        background:rgba(255,255,255,0.05); color:{color};
                        border:1px solid {color}40; margin-left:8px;">{sev}</span>
                </div>
                <div class="hazard-desc">🔧 {h.get('remedy','No remedy specified.')}</div>
            </div>""", unsafe_allow_html=True)

    # ── Standards & Recommendations ──
    st.markdown("<div class='section-header'><h3 class='section-title'>📋 Standards & Recommendations</h3></div>", unsafe_allow_html=True)
    stds = result.get("standards_referenced", [])
    cols = st.columns(len(stds) if stds else 1)
    for i, std in enumerate(stds):
        with cols[i]:
            st.markdown(f'<span class="status-pill pill-info">📘 {std}</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box" style="margin-top:1rem;">
    💡 <b>Recommendation:</b> {result.get('recommendations', 'No additional recommendations.')}
    </div>""", unsafe_allow_html=True)

    # ── Downloadable JSON ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "⬇️ Download Full JSON Report",
        data=json.dumps(result, indent=2),
        file_name=f"ppe_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        key="dl_safety"
    )


# ─────────────────────────────────────────────
#  TAB 2 — Crack Diagnostics
# ─────────────────────────────────────────────
def render_crack_tab(model):
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">🔬 Crack Diagnostics & Structural Integrity</h1>
        <p class="hero-subtitle">Multimodal defect classification per IS 456:2000, IS 13920 & ACI 318 repair protocols</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Concrete / Wall Surface Photo",
        type=["jpg", "jpeg", "png"],
        key="crack_upload",
        help="Close-up photos of cracks with a reference scale object give best results"
    )

    col_img, col_ctrl = st.columns([3, 1])
    image_obj = None

    with col_img:
        if uploaded:
            image_obj = Image.open(uploaded)
            st.image(image_obj, caption="Surface Under Analysis", use_container_width=True)
        else:
            st.markdown("""
            <div style='background:rgba(15,23,42,0.6); border:1px dashed #334155; border-radius:14px;
                        padding:3rem; text-align:center; color:#475569;'>
                <div style='font-size:3rem;'>🔬</div>
                <p style='margin:0.5rem 0 0 0; font-size:0.9rem;'>Upload a surface image for crack diagnosis</p>
            </div>
            """, unsafe_allow_html=True)

    with col_ctrl:
        st.markdown("<br>", unsafe_allow_html=True)
        run_crack = st.button("🔍 Analyse Crack", key="run_crack", use_container_width=True)
        st.markdown("**Detectable Defects:**")
        for item in ["Hairline Crack", "Settlement Crack", "Structural Shear", "Thermal Expansion", "Spalling", "Corrosion Staining"]:
            st.markdown(f"- {item}")

    if run_crack:
        with st.spinner("🤖 Running structural defect analysis..."):
            if model and image_obj:
                prompt = """You are a structural forensic engineer specialised in concrete pathology.
Analyse this concrete/wall surface image and return ONLY valid JSON (no markdown fences):
{
  "defect_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Corrosion Staining|Other>",
  "crack_width_mm": <float>,
  "crack_length_estimate": "<text>",
  "pattern": "<describe crack pattern and orientation>",
  "severity": "<Low|Medium|High|Critical>",
  "urgency": "<text>",
  "root_causes": ["<cause1>", "<cause2>"],
  "recommended_repairs": [
    {"method": "<repair method name>", "detail": "<detailed procedure>"}
  ],
  "standards": ["<IS 456:2000>", "<ACI 318>"],
  "monitoring": "<monitoring protocol>"
}"""
                raw = call_gemini_vision(model, prompt, image_obj)
                result = extract_json(raw)
                if not result:
                    result = demo_crack_result()
                    st.info("⚠️ Could not parse live response — showing structured demo data.")
            else:
                result = demo_crack_result()
                if not model:
                    st.info("ℹ️ Demo mode — enter Gemini API key for live analysis.")
                elif not image_obj:
                    st.warning("Please upload an image first.")
                    return

        _render_crack_results(result)


def _render_crack_results(result: dict):
    sev = result.get("severity", "Medium")
    sev_colors = {"Low": "#3b82f6", "Medium": "#f59e0b", "High": "#ef4444", "Critical": "#dc2626"}
    sev_pills  = {"Low": "pill-info", "Medium": "pill-warning", "High": "pill-danger", "Critical": "pill-critical"}
    color = sev_colors.get(sev, "#f59e0b")
    pill  = sev_pills.get(sev, "pill-warning")

    # ── Metrics ──
    st.markdown("<div class='section-header'><h3 class='section-title'>📊 Diagnostic Summary</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Defect Type</div>
            <div style="font-size:1rem; font-weight:700; color:#f1f5f9; margin-top:0.4rem;">
                {result.get('defect_type','Unknown')}
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        w = result.get("crack_width_mm", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Crack Width</div>
            <div class="metric-value" style="color:{color};">{w}</div>
            <div class="metric-delta">millimetres</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Severity</div>
            <div style="margin-top:0.6rem;">
                <span class="status-pill {pill}">{sev}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with c4:
        urgency = result.get("urgency", "Assessment Needed")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Urgency</div>
            <div style="font-size:0.85rem; font-weight:600; color:#fbbf24; margin-top:0.4rem; line-height:1.4;">
                {urgency}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        # ── Pattern & Root Causes ──
        st.markdown("<div class='section-header'><h3 class='section-title'>🔍 Crack Pattern & Root Causes</h3></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
        <b>Pattern:</b> {result.get('pattern','Not determined')}<br>
        <b>Estimated Length:</b> {result.get('crack_length_estimate','N/A')}
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>**Root Causes Identified:**", unsafe_allow_html=True)
        for cause in result.get("root_causes", []):
            st.markdown(f"""
            <div class="hazard-card" style="border-left-color:#f59e0b;">
                <div class="hazard-desc">🔎 {cause}</div>
            </div>""", unsafe_allow_html=True)

        # ── Standards ──
        stds = result.get("standards", [])
        if stds:
            st.markdown("**Referenced Standards:**")
            html_stds = " ".join([f'<span class="status-pill pill-info" style="margin:2px;">📘 {s}</span>' for s in stds])
            st.markdown(html_stds, unsafe_allow_html=True)

    with col_r:
        # ── Repair Methods ──
        st.markdown("<div class='section-header'><h3 class='section-title'>🔧 Recommended Engineering Repairs</h3></div>", unsafe_allow_html=True)
        for i, rep in enumerate(result.get("recommended_repairs", []), 1):
            st.markdown(f"""
            <div class="hazard-card" style="border-left-color:#3b82f6;">
                <div class="hazard-title">#{i} {rep.get('method','Repair Method')}</div>
                <div class="hazard-desc">{rep.get('detail','No details provided.')}</div>
            </div>""", unsafe_allow_html=True)

        # ── Monitoring ──
        monitor = result.get("monitoring", "")
        if monitor:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="weather-alert alert-heavy-rain">
            📏 <b>Monitoring Protocol:</b><br>{monitor}
            </div>""", unsafe_allow_html=True)

    # ── Download ──
    st.download_button(
        "⬇️ Download Crack Diagnostics Report",
        data=json.dumps(result, indent=2),
        file_name=f"crack_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        key="dl_crack"
    )


# ─────────────────────────────────────────────
#  TAB 3 — Planning & Valuation
# ─────────────────────────────────────────────
STRUCTURE_COSTS = {
    "Residential Villa (G+1)": {"base_cost_per_sqft": 1800, "steel_kg_per_sqft": 4.5, "cement_bags_per_sqft": 0.42},
    "Residential Apartment (G+4)": {"base_cost_per_sqft": 2100, "steel_kg_per_sqft": 5.8, "cement_bags_per_sqft": 0.55},
    "Commercial Office (G+10)": {"base_cost_per_sqft": 2800, "steel_kg_per_sqft": 7.2, "cement_bags_per_sqft": 0.68},
    "Industrial Warehouse": {"base_cost_per_sqft": 1400, "steel_kg_per_sqft": 6.5, "cement_bags_per_sqft": 0.38},
    "Infrastructure Bridge": {"base_cost_per_sqft": 4200, "steel_kg_per_sqft": 12.0, "cement_bags_per_sqft": 0.95},
}

TIER_MULTIPLIERS = {"Tier 1 (Mumbai/Delhi/Bangalore)": 1.35, "Tier 2 (Pune/Hyderabad/Chennai)": 1.15, "Tier 3 (Other Cities)": 1.0}

MARKET_PREMIUM = {"Tier 1 (Mumbai/Delhi/Bangalore)": 1.55, "Tier 2 (Pune/Hyderabad/Chennai)": 1.30, "Tier 3 (Other Cities)": 1.10}

def render_planning_tab(model):
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">💰 Planning & Real Estate Valuation</h1>
        <p class="hero-subtitle">Budget estimation, asset valuation in INR & conceptual 3D architectural rendering</p>
    </div>
    """, unsafe_allow_html=True)

    col_inputs, col_results = st.columns([2, 3])

    with col_inputs:
        st.markdown("### 📋 Project Parameters")
        structure_type = st.selectbox("Structure Type", list(STRUCTURE_COSTS.keys()), key="struct_type")
        sqft = st.number_input("Built-Up Area (sq ft)", min_value=500, max_value=500000, value=2500, step=100, key="sqft")
        location = st.selectbox("Location Tier", list(TIER_MULTIPLIERS.keys()), key="location")
        completion = st.slider("Completion Percentage", 0, 100, 45, key="completion")
        project_name = st.text_input("Project Name", value="Sunrise Heights Phase 1", key="proj_name")

        st.markdown("<br>", unsafe_allow_html=True)
        calc_btn = st.button("📊 Calculate & Render", key="calc_valuation", use_container_width=True)

    with col_results:
        if calc_btn:
            data = STRUCTURE_COSTS[structure_type]
            tier_mult = TIER_MULTIPLIERS[location]
            market_premium = MARKET_PREMIUM[location]

            cost_per_sqft = data["base_cost_per_sqft"] * tier_mult
            total_budget_inr = cost_per_sqft * sqft
            capex_incurred = total_budget_inr * (completion / 100)
            market_valuation = total_budget_inr * market_premium
            steel_req = data["steel_kg_per_sqft"] * sqft
            cement_req = data["cement_bags_per_sqft"] * sqft

            def fmt_inr(val):
                if val >= 1e7:
                    return f"₹{val/1e7:.2f} Cr"
                elif val >= 1e5:
                    return f"₹{val/1e5:.2f} L"
                else:
                    return f"₹{val:,.0f}"

            st.markdown("### 📊 Financial Metrics")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Project Budget</div>
                    <div class="metric-value" style="font-size:1.4rem;">{fmt_inr(total_budget_inr)}</div>
                    <div class="metric-delta">@ ₹{cost_per_sqft:,.0f}/sqft</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">CapEx Incurred</div>
                    <div class="metric-value" style="font-size:1.4rem; color:#fbbf24;">{fmt_inr(capex_incurred)}</div>
                    <div class="metric-delta">{completion}% complete</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Market Asset Value</div>
                    <div class="metric-value" style="font-size:1.4rem; color:#34d399;">{fmt_inr(market_valuation)}</div>
                    <div class="metric-delta">At current {location.split('(')[0].strip()} rates</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            m4, m5 = st.columns(2)
            with m4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Steel Requirement</div>
                    <div class="metric-value" style="font-size:1.5rem;">{steel_req:,.0f}</div>
                    <div class="metric-delta">kilograms (MT: {steel_req/1000:.1f})</div>
                </div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Cement Requirement</div>
                    <div class="metric-value" style="font-size:1.5rem;">{cement_req:,.0f}</div>
                    <div class="metric-delta">bags of 50kg each</div>
                </div>""", unsafe_allow_html=True)

            # ── Milestone Progress ──
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🏗️ Milestone Progress")
            milestones = [
                ("Foundation & Excavation", 15),
                ("Structural Framework", 35),
                ("Slab & Roofing", 55),
                ("Brick Masonry & Plastering", 72),
                ("MEP Works", 85),
                ("Finishing & Handover", 100),
            ]
            for ms_name, ms_thresh in milestones:
                ms_done = min(completion, ms_thresh)
                ms_pct = (ms_done / ms_thresh) * 100
                is_complete = completion >= ms_thresh
                icon = "✅" if is_complete else ("🔄" if completion > (ms_thresh - 20) else "⏳")
                st.markdown(f"""
                <div style="margin-bottom:0.8rem;">
                    <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#94a3b8; margin-bottom:3px;">
                        <span>{icon} {ms_name}</span>
                        <span style="color:{'#34d399' if is_complete else '#60a5fa'}">
                            {min(100, round(ms_pct))}%
                        </span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-fill" style="width:{min(100, ms_pct)}%;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style='background:rgba(15,23,42,0.6); border:1px dashed #334155; border-radius:14px;
                        padding:3rem; text-align:center; color:#475569;'>
                <div style='font-size:3rem;'>💰</div>
                <p style='margin:0.5rem 0 0 0; font-size:0.9rem;'>Configure project parameters and click Calculate</p>
            </div>
            """, unsafe_allow_html=True)

    # ── Pollinations 3D Render ──
    st.markdown("<hr style='border-color:#1e293b; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### 🎨 Conceptual 3D Architectural Rendering")
    st.markdown("""
    <div class="info-box">
    Powered by <b>Pollinations AI</b> — generates a photorealistic 3D architectural concept render based on your project inputs.
    </div>""", unsafe_allow_html=True)

    render_col1, render_col2 = st.columns([2, 1])
    with render_col2:
        render_style = st.selectbox("Rendering Style", [
            "Photorealistic Exterior",
            "Architectural Blueprint",
            "Night Illumination",
            "Aerial Bird's Eye View",
            "Interior Lobby Concept"
        ], key="render_style")
        render_btn = st.button("🎨 Generate 3D Render", key="gen_render", use_container_width=True)

    with render_col1:
        if render_btn:
            struct_display = st.session_state.get("struct_type", list(STRUCTURE_COSTS.keys())[0])
            loc_display = st.session_state.get("location", list(TIER_MULTIPLIERS.keys())[0]).split("(")[0].strip()
            proj_nm = st.session_state.get("proj_name", "Modern Building")

            prompt_text = (
                f"Photorealistic {render_style} architectural concept render of a {struct_display}, "
                f"located in {loc_display} India. Modern contemporary design with glass facade, "
                f"landscaping, steel structure visible, golden hour lighting, ultra-detailed 3D CGI, "
                f"8K resolution, professional architectural visualization, Unreal Engine 5 quality, "
                f"clean sharp lines, premium real estate, dramatic sky"
            )
            encoded = requests.utils.quote(prompt_text)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&seed=42&nologo=true"

            with st.spinner("🎨 Generating architectural render..."):
                try:
                    resp = requests.get(img_url, timeout=30)
                    if resp.status_code == 200:
                        render_img = Image.open(io.BytesIO(resp.content))
                        st.markdown('<div class="render-card">', unsafe_allow_html=True)
                        st.image(render_img, use_container_width=True)
                        st.markdown(f'<div class="render-label">🏗️ {proj_nm} — {render_style} | Generated by Pollinations AI</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        img_bytes = io.BytesIO()
                        render_img.save(img_bytes, format="PNG")
                        st.download_button(
                            "⬇️ Download Render",
                            data=img_bytes.getvalue(),
                            file_name=f"render_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png",
                            key="dl_render"
                        )
                    else:
                        st.error(f"Render API returned {resp.status_code}")
                except Exception as e:
                    st.error(f"Render generation failed: {e}")
        else:
            st.markdown("""
            <div style='background:rgba(15,23,42,0.6); border:1px dashed #334155; border-radius:14px;
                        padding:2rem; text-align:center; color:#475569;'>
                <div style='font-size:2.5rem;'>🏛️</div>
                <p style='margin:0.5rem 0 0 0; font-size:0.9rem;'>Select a rendering style and click Generate</p>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TAB 4 — Site Assistant & Weather Advisory
# ─────────────────────────────────────────────
def render_assistant_tab(model):
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">🤖 Daily Site Assistant & Weather Advisory</h1>
        <p class="hero-subtitle">Real-time weather-aware safety alerts and multi-turn construction engineering chatbot</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Weather Advisory ──
    st.markdown("### 🌤️ Weather-Aware Safety Alerts")
    weather = st.selectbox(
        "Current Site Weather Condition",
        list(WEATHER_ADVISORIES.keys()),
        key="weather_select"
    )

    adv = WEATHER_ADVISORIES[weather]
    st.markdown(f"""
    <div class="weather-alert {adv['class']}">
        <div style="font-size:1.1rem; font-weight:700; margin-bottom:0.8rem;">
            {adv['icon']} {adv['title']}
        </div>
        {''.join(f'<div style="margin-bottom:0.4rem;">{a}</div>' for a in adv['alerts'])}
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e293b; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # ── Chatbot ──
    st.markdown("### 💬 Construction Engineering Assistant")
    st.markdown("""
    <div class="info-box" style="margin-bottom:1rem;">
    Ask anything about <b>construction engineering</b>, site management, structural calculations, material specifications, 
    IS/OSHA standards, project planning, or safety protocols.
    </div>""", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "👋 Hello! I'm your **Construction Engineering Assistant**. I can help you with structural calculations, IS code references, material specifications, site management queries, safety protocols, and more. What would you like to know?"
        })

    # Render chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<br>**Quick Queries:**", unsafe_allow_html=True)
    quick_cols = st.columns(3)
    quick_prompts = [
        "What is the minimum cover for concrete as per IS 456?",
        "How to calculate beam reinforcement for M25 concrete?",
        "OSHA requirements for scaffold erection",
        "Concrete curing duration for different grades",
        "How to calculate pile load capacity?",
        "Safety checklist for formwork removal",
    ]
    for i, qp in enumerate(quick_prompts):
        with quick_cols[i % 3]:
            if st.button(qp[:40] + "..." if len(qp) > 40 else qp, key=f"qp_{i}", use_container_width=True):
                st.session_state["prefill_chat"] = qp

    # Chat input
    prefill = st.session_state.pop("prefill_chat", "")
    user_input = st.chat_input("Ask your construction engineering question...", key="chat_input")

    # Handle quick prompt prefill via text area
    if prefill and not user_input:
        user_input = prefill

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("🤖 Thinking..."):
            if model:
                # Build conversation context
                history_text = "\n".join([
                    f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}"
                    for m in st.session_state.chat_history[-8:]  # Last 4 turns
                ])
                prompt = f"""You are an expert construction engineering assistant with deep knowledge of:
- IS codes (IS 456, IS 800, IS 13920, IS 875, IS 1893, IS 3764, NBC 2016)
- OSHA standards (29 CFR 1926)
- Structural engineering, geotechnical engineering, project management
- Material science (concrete, steel, masonry)
- Construction safety and PPE protocols
- Real estate valuation in India

Conversation so far:
{history_text}

Provide a clear, technically accurate, and practical response. Use bullet points where helpful. 
Reference relevant IS codes or OSHA standards when applicable."""
                response_text = call_gemini_text(model, prompt)
            else:
                # Demo responses
                demo_responses = {
                    "cover": "As per **IS 456:2000 Clause 26.4**, minimum clear cover requirements are:\n- **Mild exposure**: 20 mm\n- **Moderate exposure**: 30 mm\n- **Severe exposure**: 45 mm\n- **Very severe/Extreme**: 50–75 mm\n\nFor footings, minimum cover is **50 mm** as per Clause 26.4.2.",
                    "default": f"Great question about construction engineering! In **Demo Mode**, I'm providing curated responses. For live AI-powered answers drawing on your specific query context, please enter your **Gemini API Key** in the sidebar.\n\n**Your question:** _{user_input}_\n\nAs a construction engineering expert, I'd recommend consulting the relevant IS code or OSHA standard for your specific application. Common references include IS 456:2000 for RCC, IS 800:2007 for steel structures, and OSHA 29 CFR 1926 for construction safety."
                }
                resp_key = "cover" if "cover" in user_input.lower() else "default"
                response_text = demo_responses[resp_key]

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.rerun()

    # Clear chat
    if len(st.session_state.chat_history) > 1:
        if st.button("🗑️ Clear Conversation", key="clear_chat"):
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": "👋 Conversation cleared. How can I help you today?"
            }]
            st.rerun()


# ─────────────────────────────────────────────
#  Main App
# ─────────────────────────────────────────────
def main():
    inject_css()
    api_key = render_sidebar()

    # Initialise Gemini model (cached in session)
    model = None
    if api_key:
        if "gemini_model" not in st.session_state or st.session_state.get("last_api_key") != api_key:
            model = get_gemini_model(api_key)
            st.session_state["gemini_model"] = model
            st.session_state["last_api_key"] = api_key
        else:
            model = st.session_state["gemini_model"]

    # ── App Header ──
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
        <h1 style='font-size:2.2rem; font-weight:800;
            background:linear-gradient(135deg,#60a5fa,#a78bfa,#34d399);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text; margin:0;'>
            🏗️ Multimodal Construction Intelligence Platform
        </h1>
        <p style='color:#475569; font-size:0.95rem; margin:0.4rem 0 0 0;'>
            AI-Powered Site Safety • Structural Diagnostics • Financial Planning • Smart Advisory
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺 Site Safety & PPE Audit",
        "🔬 Crack Diagnostics",
        "💰 Planning & Valuation",
        "🤖 Site Assistant"
    ])

    with tab1:
        render_safety_tab(model)
    with tab2:
        render_crack_tab(model)
    with tab3:
        render_planning_tab(model)
    with tab4:
        render_assistant_tab(model)


if __name__ == "__main__":
    main()
