"""
AYA AI ✨ — Beautiful Chat UI
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="AYA AI ✨",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ─────────────────────────────────────────────
from components.sidebar import render_sidebar, render_header, render_mode_banner
from components.chat import (
    render_chat_history,
    handle_chat_input,
)

# ── INJECT FULL CUSTOM HTML/CSS UI ────────────────────
def load_custom_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&family=Playfair+Display:wght@400;700&family=Fira+Code:wght@400;500&display=swap');

    :root {
        --rose:       #f43f8a;
        --rose-light: #ff7eb6;
        --rose-pale:  #ffe4f0;
        --plum:       #7c3aed;
        --plum-light: #a78bfa;
        --cream:      #fff8fc;
        --glass:      rgba(255,255,255,0.75);
        --glass-b:    rgba(244,114,182,0.25);
        --dark:       #2d0a1f;
        --mid:        #8b3a62;
        --soft:       #c084a0;
        --shadow:     0 8px 40px rgba(244,67,138,0.18);
    }

    /* ── GLOBAL RESET ── */
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
    }

    /* ── ANIMATED BACKGROUND ── */
    .stApp {
        background: linear-gradient(135deg, #1a0010 0%, #2d0a1f 30%, #1a0535 60%, #2d0a1f 100%) !important;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(244,67,138,0.15) 0%, transparent 60%),
            radial-gradient(ellipse 60% 60% at 80% 80%, rgba(124,58,237,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 40% 40% at 50% 50%, rgba(255,126,182,0.06) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: bgPulse 8s ease-in-out infinite alternate;
    }

    @keyframes bgPulse {
        0%   { opacity: 0.7; }
        100% { opacity: 1; }
    }

    /* Floating petals */
    .stApp::after {
        content: '🌸 ✨ 💕 🌸 ✨ 💖 🌸';
        position: fixed;
        top: -50px;
        left: 0;
        right: 0;
        font-size: 1.5rem;
        letter-spacing: 8rem;
        white-space: nowrap;
        opacity: 0.07;
        animation: petalFall 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes petalFall {
        0%   { transform: translateY(-60px) rotate(0deg); opacity: 0.05; }
        50%  { opacity: 0.1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0.03; }
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg,
            rgba(45,10,31,0.97) 0%,
            rgba(30,5,50,0.97) 100%) !important;
        border-right: 1px solid rgba(244,67,138,0.2) !important;
        box-shadow: 4px 0 30px rgba(0,0,0,0.4) !important;
    }

    [data-testid="stSidebar"] * {
        color: #f0d0e0 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ff7eb6 !important;
    }

    [data-testid="stSidebar"] .stTextInput input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(244,67,138,0.3) !important;
        color: #f0d0e0 !important;
        border-radius: 12px !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: var(--rose) !important;
        box-shadow: 0 0 0 2px rgba(244,67,138,0.25) !important;
    }

    /* Sidebar radio */
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(244,67,138,0.2) !important;
        border-radius: 14px !important;
        padding: 0.4rem 1rem !important;
        color: #f0d0e0 !important;
        transition: all 0.2s !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(244,67,138,0.15) !important;
        border-color: var(--rose) !important;
    }

    /* Sidebar toggle */
    [data-testid="stSidebar"] .stToggle {
        color: #f0d0e0 !important;
    }

    /* Metric cards in sidebar */
    [data-testid="stSidebar"] [data-testid="metric-container"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(244,67,138,0.2) !important;
        border-radius: 14px !important;
        padding: 0.8rem !important;
    }

    [data-testid="stSidebar"] [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ff7eb6 !important;
        font-size: 1.5rem !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* ── MAIN CONTENT AREA ── */
    .main .block-container {
        padding: 1rem 1.5rem 2rem !important;
        max-width: 900px !important;
        position: relative;
        z-index: 1;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--rose), var(--plum)) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1.4rem !important;
        box-shadow: 0 4px 20px rgba(244,67,138,0.35) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        letter-spacing: 0.01em !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 10px 30px rgba(244,67,138,0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(244,67,138,0.15) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px) !important;
        margin-bottom: 0.8rem !important;
        padding: 0.8rem 1rem !important;
        animation: msgSlide 0.35s cubic-bezier(0.34, 1.2, 0.64, 1) !important;
        color: #f0d0e0 !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #f0d0e0 !important;
    }

    [data-testid="stChatMessage"] code {
        background: rgba(124,58,237,0.25) !important;
        color: #f0d0e0 !important;
        border-radius: 6px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.85em !important;
        padding: 0.15em 0.4em !important;
    }

    [data-testid="stChatMessage"] pre {
        background: rgba(10,0,20,0.6) !important;
        border: 1px solid rgba(124,58,237,0.3) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
    }

    [data-testid="stChatMessage"] pre code {
        background: transparent !important;
        color: #e0c8f0 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.85rem !important;
    }

    @keyframes msgSlide {
        from { opacity: 0; transform: translateY(12px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* User message */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, rgba(244,67,138,0.2), rgba(124,58,237,0.15)) !important;
        border-color: rgba(244,67,138,0.3) !important;
    }

    /* ── CHAT INPUT ── */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(244,67,138,0.3) !important;
        border-radius: 28px !important;
        backdrop-filter: blur(10px) !important;
        transition: border-color 0.2s !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--rose) !important;
        box-shadow: 0 0 0 3px rgba(244,67,138,0.15) !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #f0d0e0 !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(240,208,224,0.5) !important;
    }

    /* ── TEXT INPUTS ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(244,67,138,0.25) !important;
        border-radius: 14px !important;
        color: #f0d0e0 !important;
        font-family: 'Tajawal', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--rose) !important;
        box-shadow: 0 0 0 2px rgba(244,67,138,0.2) !important;
    }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(244,67,138,0.2) !important;
        border-radius: 18px !important;
        backdrop-filter: blur(10px) !important;
        margin-bottom: 0.6rem !important;
    }

    [data-testid="stExpander"] summary {
        color: #ff7eb6 !important;
        font-weight: 600 !important;
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span,
    [data-testid="stExpander"] label {
        color: #f0d0e0 !important;
    }

    /* ── FILE UPLOADER ── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04) !important;
        border: 2px dashed rgba(244,67,138,0.3) !important;
        border-radius: 18px !important;
        padding: 1rem !important;
        transition: border-color 0.2s !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--rose) !important;
    }

    /* ── ALERTS ── */
    .stAlert {
        border-radius: 16px !important;
        border-left: 4px solid var(--rose) !important;
        background: rgba(244,67,138,0.1) !important;
    }

    .stSuccess {
        border-left-color: #22c55e !important;
        background: rgba(34,197,94,0.1) !important;
    }

    .stWarning {
        border-left-color: #f59e0b !important;
        background: rgba(245,158,11,0.1) !important;
    }

    /* ── SPINNER ── */
    .stSpinner > div {
        border-top-color: var(--rose) !important;
    }

    /* ── DIVIDERS ── */
    hr {
        border-color: rgba(244,67,138,0.2) !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--rose), var(--plum));
        border-radius: 10px;
    }

    /* ── MARKDOWN TEXT ── */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #f0d0e0 !important;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ff7eb6 !important;
        font-family: 'Playfair Display', serif !important;
    }

    .stMarkdown strong {
        color: #ffc0dc !important;
    }

    .stMarkdown a {
        color: var(--rose-light) !important;
    }

    /* ── AUDIO PLAYER ── */
    audio {
        border-radius: 24px !important;
        width: 100% !important;
        margin-top: 0.5rem !important;
        filter: hue-rotate(300deg) !important;
    }

    /* ── SELECT SLIDER ── */
    [data-testid="stSelectSlider"], .stSlider {
        color: #f0d0e0 !important;
    }

    /* ── INFO BOXES ── */
    .stInfo {
        background: rgba(124,58,237,0.1) !important;
        border-left: 4px solid var(--plum-light) !important;
        border-radius: 14px !important;
        color: #f0d0e0 !important;
    }

    /* ── TOGGLE ── */
    .stToggle label {
        color: #f0d0e0 !important;
    }

    /* ── GENERAL LABEL COLORS ── */
    label, .stMarkdown p {
        color: #f0d0e0 !important;
    }

    /* Sidebar clear button — danger style */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(244,67,138,0.2), rgba(124,58,237,0.2)) !important;
        border: 1px solid rgba(244,67,138,0.3) !important;
        color: #ff7eb6 !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, rgba(239,68,68,0.3), rgba(220,38,38,0.2)) !important;
        border-color: #ef4444 !important;
        color: #fca5a5 !important;
        box-shadow: 0 4px 16px rgba(239,68,68,0.25) !important;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── BLINK ANIMATION (for dots) ── */
    @keyframes blink {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(0.6); }
    }
    </style>
    """, unsafe_allow_html=True)


load_custom_ui()

# ── STATE ──────────────────────────────────────────────
DEFAULTS = {
    "messages": [],
    "mode": "💬 عام",
    "mood": "😊 سعيدة",
    "api_key": "",
    "voice_output": False,
    "total_messages": 0,
    "total_files": 0,
    "file_context": "",
    "file_name": "",
    "pending_input": None,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIDEBAR ────────────────────────────────────────────
sidebar = render_sidebar({
    "api_key": st.session_state.api_key,
    "mode": st.session_state.mode,
    "mood": st.session_state.mood,
    "voice_output": st.session_state.voice_output,
    "total_messages": st.session_state.total_messages,
    "total_files": st.session_state.total_files,
})

st.session_state.api_key = sidebar["api_key"]
st.session_state.mode = sidebar["mode"]
st.session_state.mood = sidebar["mood"]
st.session_state.voice_output = sidebar["voice_output"]

if sidebar.get("pending_voice"):
    st.session_state.pending_input = sidebar["pending_voice"]

if sidebar["clear"]:
    st.session_state.messages = []
    st.session_state.file_context = ""
    st.session_state.file_name = ""
    st.session_state.pending_input = None
    st.session_state.total_messages = 0
    st.rerun()

# ── HEADER ─────────────────────────────────────────────
render_header()

# ── MODE BANNER ────────────────────────────────────────
render_mode_banner(st.session_state.mode)

# ── CHAT HISTORY ───────────────────────────────────────
render_chat_history()

# ── CHAT INPUT ─────────────────────────────────────────
handle_chat_input()

# ── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;
    color:rgba(255,192,220,0.4);font-size:0.72rem;letter-spacing:0.05em;">
    Made with 💕 for Aya &nbsp;•&nbsp; AYA AI ✨ &nbsp;•&nbsp; Powered by Groq ⚡
</div>
""", unsafe_allow_html=True)