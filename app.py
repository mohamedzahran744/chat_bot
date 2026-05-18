"""
AYA AI ✨ — Beautiful AI Assistant
Run: streamlit run app.py
API key is loaded from .env automatically — no user input needed!
"""

import streamlit as st

st.set_page_config(
    page_title="AYA AI ✨",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import render_sidebar, render_header, render_mode_banner
from components.chat import render_chat_history, handle_chat_input


# ── CUSTOM CSS — extra cute dark glassmorphism ─────────────────
def load_custom_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&family=Playfair+Display:wght@400;700&family=Fira+Code:wght@400;500&display=swap');

    :root {
        --rose:       #f43f8a;
        --rose-light: #ff7eb6;
        --plum:       #7c3aed;
        --plum-light: #a78bfa;
    }

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
    }

    /* ── ANIMATED BACKGROUND ── */
    .stApp {
        background:
            radial-gradient(ellipse 90% 60% at 15% 5%,  rgba(244,67,138,.18) 0%, transparent 55%),
            radial-gradient(ellipse 70% 70% at 85% 85%, rgba(124,58,237,.15) 0%, transparent 55%),
            radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255,126,182,.06) 0%, transparent 65%),
            linear-gradient(160deg, #1a0010 0%, #2d0a1f 40%, #1a0535 70%, #2d0a1f 100%) !important;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }

    /* Sparkle overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(244,67,138,.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 60% at 80% 80%, rgba(124,58,237,.1) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
        animation: bgPulse 9s ease-in-out infinite alternate;
    }
    @keyframes bgPulse { 0% { opacity:.65; } 100% { opacity:1; } }

    /* Floating petals */
    .stApp::after {
        content: '🌸✨💕🌸✨💖🎀';
        position: fixed;
        top: -60px;
        left: 0; right: 0;
        font-size: 1.4rem;
        letter-spacing: 7rem;
        white-space: nowrap;
        opacity: 0.06;
        animation: petalFall 25s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes petalFall {
        0%   { transform: translateY(-60px) rotate(0deg);   opacity: .04; }
        50%  { opacity: .09; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: .03; }
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg,
            rgba(45,10,31,.97) 0%,
            rgba(26,5,50,.97)  100%) !important;
        border-right: 1px solid rgba(244,67,138,.22) !important;
        box-shadow: 4px 0 32px rgba(0,0,0,.45) !important;
    }
    [data-testid="stSidebar"] * { color: #f0d0e0 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ff7eb6 !important; }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,.05) !important;
        border: 1px solid rgba(244,67,138,.2) !important;
        border-radius: 16px !important;
        padding: .45rem 1rem !important;
        color: #f0d0e0 !important;
        transition: all .2s !important;
        font-size: .88rem !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(244,67,138,.15) !important;
        border-color: var(--rose) !important;
        transform: translateX(-2px) !important;
    }

    [data-testid="stSidebar"] [data-testid="metric-container"] {
        background: rgba(255,255,255,.06) !important;
        border: 1px solid rgba(244,67,138,.2) !important;
        border-radius: 16px !important;
        padding: .8rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #ff7eb6 !important;
        font-size: 1.5rem !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* ── MAIN CONTENT ── */
    .main .block-container {
        padding: 1rem 1.5rem 2rem !important;
        max-width: 920px !important;
        position: relative;
        z-index: 1;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--rose), var(--plum)) !important;
        color: white !important;
        border: none !important;
        border-radius: 28px !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 700 !important;
        font-size: .88rem !important;
        padding: .52rem 1.5rem !important;
        box-shadow: 0 4px 22px rgba(244,67,138,.35) !important;
        transition: all .28s cubic-bezier(.34,1.56,.64,1) !important;
        letter-spacing: .01em !important;
    }
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.04) !important;
        box-shadow: 0 12px 34px rgba(244,67,138,.55) !important;
    }
    .stButton > button:active { transform: translateY(-1px) scale(.97) !important; }

    /* Sidebar clear btn */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg,rgba(244,67,138,.18),rgba(124,58,237,.18)) !important;
        border: 1px solid rgba(244,67,138,.3) !important;
        color: #ff7eb6 !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg,rgba(239,68,68,.3),rgba(220,38,38,.2)) !important;
        border-color: #ef4444 !important;
        color: #fca5a5 !important;
        box-shadow: 0 4px 18px rgba(239,68,68,.28) !important;
    }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.055) !important;
        border: 1px solid rgba(244,67,138,.14) !important;
        border-radius: 22px !important;
        backdrop-filter: blur(14px) !important;
        margin-bottom: .85rem !important;
        padding: .85rem 1.1rem !important;
        animation: msgSlide .38s cubic-bezier(.34,1.2,.64,1) !important;
        color: #f0d0e0 !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span { color: #f0d0e0 !important; }

    [data-testid="stChatMessage"] code {
        background: rgba(124,58,237,.25) !important;
        color: #f0d0e0 !important;
        border-radius: 7px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: .84em !important;
        padding: .15em .42em !important;
    }
    [data-testid="stChatMessage"] pre {
        background: rgba(10,0,20,.62) !important;
        border: 1px solid rgba(124,58,237,.3) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }
    [data-testid="stChatMessage"] pre code {
        background: transparent !important;
        color: #e0c8f0 !important;
        font-size: .85rem !important;
    }

    @keyframes msgSlide {
        from { opacity:0; transform:translateY(14px) scale(.96); }
        to   { opacity:1; transform:translateY(0)   scale(1);   }
    }

    /* ── CHAT INPUT ── */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,.07) !important;
        border: 1.5px solid rgba(244,67,138,.3) !important;
        border-radius: 30px !important;
        backdrop-filter: blur(12px) !important;
        transition: border-color .2s, box-shadow .2s !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--rose) !important;
        box-shadow: 0 0 0 3px rgba(244,67,138,.16) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f0d0e0 !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: .95rem !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(240,208,224,.48) !important;
    }

    /* ── TEXT INPUTS ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,.07) !important;
        border: 1px solid rgba(244,67,138,.25) !important;
        border-radius: 15px !important;
        color: #f0d0e0 !important;
        font-family: 'Tajawal', sans-serif !important;
    }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,.045) !important;
        border: 1px solid rgba(244,67,138,.2) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px) !important;
        margin-bottom: .6rem !important;
    }
    [data-testid="stExpander"] summary {
        color: #ff7eb6 !important;
        font-weight: 700 !important;
    }

    /* ── FILE UPLOADER ── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,.04) !important;
        border: 2px dashed rgba(244,67,138,.3) !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        transition: border-color .2s !important;
    }
    [data-testid="stFileUploader"]:hover { border-color: var(--rose) !important; }

    /* ── ALERTS ── */
    .stAlert  { border-radius: 17px !important; border-left: 4px solid var(--rose) !important; background: rgba(244,67,138,.1) !important; }
    .stSuccess{ border-left-color: #22c55e !important; background: rgba(34,197,94,.1)  !important; }
    .stWarning{ border-left-color: #f59e0b !important; background: rgba(245,158,11,.1) !important; }
    .stInfo   { background: rgba(124,58,237,.1) !important; border-left: 4px solid var(--plum-light) !important; border-radius: 15px !important; }

    /* ── SPINNER ── */
    .stSpinner > div { border-top-color: var(--rose) !important; }

    /* ── DIVIDERS ── */
    hr { border-color: rgba(244,67,138,.18) !important; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,.03); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(var(--rose),var(--plum)); border-radius: 10px; }

    /* ── MARKDOWN ── */
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #f0d0e0 !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #ff7eb6 !important; font-family: 'Playfair Display', serif !important; }
    .stMarkdown strong { color: #ffc0dc !important; }
    .stMarkdown a { color: var(--rose-light) !important; }

    /* ── AUDIO ── */
    audio { border-radius: 26px !important; width: 100% !important; margin-top: .5rem !important; filter: hue-rotate(300deg) !important; }

    /* ── TOGGLE ── */
    .stToggle label { color: #f0d0e0 !important; }

    /* ── HIDE CHROME ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── CUTE SPARKLE CURSOR ── (optional fun) ── */
    @keyframes blink {
        0%,100% { opacity:1; transform:scale(1); }
        50%      { opacity:.3; transform:scale(.6); }
    }
    </style>
    """, unsafe_allow_html=True)


load_custom_ui()

# ── SESSION STATE ───────────────────────────────────────────────
DEFAULTS = {
    "messages":       [],
    "mode":           "💬 عام",
    "mood":           "😊 سعيدة",
    "voice_output":   False,
    "total_messages": 0,
    "total_files":    0,
    "file_context":   "",
    "file_name":      "",
    "pending_input":  None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIDEBAR ─────────────────────────────────────────────────────
sidebar = render_sidebar({
    "mode":           st.session_state.mode,
    "mood":           st.session_state.mood,
    "voice_output":   st.session_state.voice_output,
    "total_messages": st.session_state.total_messages,
    "total_files":    st.session_state.total_files,
})

st.session_state.mode         = sidebar["mode"]
st.session_state.mood         = sidebar["mood"]
st.session_state.voice_output = sidebar["voice_output"]

if sidebar.get("pending_voice"):
    st.session_state.pending_input = sidebar["pending_voice"]

if sidebar["clear"]:
    st.session_state.messages       = []
    st.session_state.file_context   = ""
    st.session_state.file_name      = ""
    st.session_state.pending_input  = None
    st.session_state.total_messages = 0
    st.rerun()

# ── HEADER ──────────────────────────────────────────────────────
render_header()

# ── MODE BANNER ─────────────────────────────────────────────────
render_mode_banner(st.session_state.mode)

# ── CHAT HISTORY ────────────────────────────────────────────────
render_chat_history()

# ── CHAT INPUT ──────────────────────────────────────────────────
handle_chat_input()

# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 .5rem;
    color:rgba(255,192,220,0.35);font-size:.72rem;letter-spacing:.06em;">
    Made with 💕 for Aya &nbsp;•&nbsp; AYA AI ✨ &nbsp;•&nbsp; Powered by Groq ⚡
</div>
""", unsafe_allow_html=True)
