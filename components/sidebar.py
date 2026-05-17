"""
components/sidebar.py — Sidebar controls: API key, mode, mood, voice, file upload, stats
"""
import streamlit as st
from constants.chat_data import APP_NAME, APP_VERSION, MODES, MOODS, MODE_META
from components.chat import extract_text_from_file, build_file_context
from services.llm_service import transcribe_audio


def render_header() -> None:
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 0 0.8rem;">
        <div style="font-size:3.5rem;line-height:1;
            animation:float 3s ease-in-out infinite;
            display:inline-block;">🌸</div>
        <h1 style="
            font-family:'Playfair Display',serif;
            background:linear-gradient(135deg,#ff7eb6,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;
            font-size:2.8rem;margin:.3rem 0 .1rem;letter-spacing:0.02em;
        ">{APP_NAME}</h1>
        <p style="color:rgba(255,192,220,0.7);font-size:0.9rem;margin:0;
            font-family:'Tajawal',sans-serif;">مساعدتك الذكية الشخصية ✨</p>
        <div style="display:flex;justify-content:center;gap:7px;margin-top:.8rem;">
            <span style="width:8px;height:8px;border-radius:50%;background:#f43f8a;
                display:inline-block;animation:blink 1.4s ease-in-out infinite;
                box-shadow:0 0 8px rgba(244,63,138,0.6);"></span>
            <span style="width:8px;height:8px;border-radius:50%;background:#a78bfa;
                display:inline-block;animation:blink 1.4s ease-in-out .2s infinite;
                box-shadow:0 0 8px rgba(167,139,250,0.6);"></span>
            <span style="width:8px;height:8px;border-radius:50%;background:#f43f8a;
                display:inline-block;animation:blink 1.4s ease-in-out .4s infinite;
                box-shadow:0 0 8px rgba(244,63,138,0.6);"></span>
        </div>
    </div>
    <style>
    @keyframes float{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-7px);}}}}
    </style>
    """, unsafe_allow_html=True)


def render_mode_banner(mode: str) -> None:
    meta = MODE_META.get(mode, MODE_META["💬 عام"])
    st.markdown(f"""
    <div style="
        background:{meta['bg']};
        border-radius:18px;
        padding:.65rem 1.4rem;
        border:1px solid {meta['border']};
        margin-bottom:1rem;
        text-align:center;
        backdrop-filter:blur(10px);
        box-shadow:0 4px 20px {meta['shadow']};
    ">
        <span style="color:{meta['fg']};font-weight:700;font-size:.9rem;
            letter-spacing:0.02em;">{meta['label']}</span>
    </div>""", unsafe_allow_html=True)


def render_sidebar(state: dict) -> dict:
    pending_voice = None

    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="text-align:center;padding:.6rem 0 .4rem;">
            <span style="font-size:2.2rem;">🌸</span>
            <h2 style="margin:.2rem 0 0;font-family:'Playfair Display',serif;
                color:#ff7eb6 !important;font-size:1.6rem;">AYA AI</h2>
            <p style="font-size:.75rem;color:rgba(255,192,220,0.6);margin:0;">
                مساعدتك الذكية الشخصية</p>
        </div>""", unsafe_allow_html=True)

        st.divider()

        # API Key
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">🔑 Groq API Key</p>', unsafe_allow_html=True)
        api_key = st.text_input(
            "api_key_input",
            type="password",
            value=state.get("api_key", ""),
            placeholder="gsk_...",
            help="مجاني 100% من: https://console.groq.com",
            label_visibility="collapsed",
        )
        st.markdown(
            '<a href="https://console.groq.com" target="_blank" '
            'style="color:#a78bfa;font-size:.72rem;text-decoration:none;">'
            '← احصلي على مفتاح مجاني</a>',
            unsafe_allow_html=True,
        )

        st.divider()

        # Mode
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">✨ الوضع</p>', unsafe_allow_html=True)
        mode = st.radio(
            "mode_radio",
            MODES,
            index=MODES.index(state.get("mode", "💬 عام")),
            label_visibility="collapsed",
        )

        st.divider()

        # Mood
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">💕 كيف حالك؟</p>', unsafe_allow_html=True)
        mood = st.radio(
            "mood_radio",
            MOODS,
            index=MOODS.index(state.get("mood", "😊 سعيدة")),
            label_visibility="collapsed",
        )

        st.divider()

        # Voice output toggle
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">🔊 الصوت</p>', unsafe_allow_html=True)
        voice_output = st.toggle(
            "ردود صوتية تلقائية 🔊",
            value=state.get("voice_output", False),
        )

        st.divider()

        # ── FILE UPLOAD ──────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">📎 رفع ملف</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:rgba(255,192,220,0.55);font-size:.75rem;margin-bottom:.4rem;">'
            'PDF، Word، كود، صور 🌸</p>',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "upload_sidebar",
            type=["pdf", "docx", "txt", "md", "py", "cpp", "c", "h", "js", "ts",
                  "java", "json", "csv", "xml", "html", "css", "sql", "yaml", "yml",
                  "png", "jpg", "jpeg", "webp", "gif"],
            label_visibility="collapsed",
        )
        if uploaded:
            extracted, label = extract_text_from_file(uploaded)
            st.session_state.file_context = build_file_context(extracted, label, uploaded.name)
            st.session_state.file_name    = uploaded.name
            st.session_state.total_files += 1
            st.success(f"✅ {label}: **{uploaded.name}** 🌸")

        if st.session_state.get("file_name"):
            st.markdown(
                f'<div style="background:rgba(244,67,138,0.1);border-radius:10px;'
                f'padding:.4rem .8rem;font-size:.78rem;'
                f'color:rgba(255,192,220,0.85);border:1px solid rgba(244,67,138,0.25);">'
                f'📎 <b style="color:#ff7eb6;">{st.session_state.file_name}</b></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── VOICE INPUT ──────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:4px;">🎙️ رسالة صوتية</p>', unsafe_allow_html=True)

        if not api_key:
            st.markdown(
                '<p style="color:rgba(255,192,220,0.45);font-size:.75rem;">أضيفي API Key أولاً 💕</p>',
                unsafe_allow_html=True,
            )
        else:
            try:
                audio_value = st.audio_input("🎙️ اضغطي لتسجيل رسالة", key="sidebar_audio")
                if audio_value is not None:
                    with st.spinner("🌸 بتحوّل الكلام لنص..."):
                        try:
                            from services.llm_service import transcribe_audio
                            transcribed = transcribe_audio(api_key, audio_value.read(), "recording.wav")
                            if transcribed:
                                st.success(f"✅ **{transcribed}**")
                                pending_voice = transcribed
                        except Exception as e:
                            st.error(f"😔 مشكلة: {e}")
            except Exception:
                voice_upload = st.file_uploader(
                    "📤 ارفعي ملف صوتي",
                    type=["wav", "mp3", "m4a", "ogg", "webm"],
                    key="voice_upload_sidebar",
                )
                if voice_upload:
                    with st.spinner("🌸 بتحوّل الكلام لنص..."):
                        try:
                            from services.llm_service import transcribe_audio
                            transcribed = transcribe_audio(api_key, voice_upload.read(), voice_upload.name)
                            if transcribed:
                                st.success(f"✅ **{transcribed}**")
                                pending_voice = transcribed
                        except Exception as e:
                            st.error(f"😔 مشكلة: {e}")

        st.divider()

        # Stats
        st.markdown('<p style="color:rgba(255,192,220,0.8);font-size:.8rem;font-weight:600;margin-bottom:6px;">📊 إحصائياتك</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💬 رسائل", state.get("total_messages", 0))
        with col2:
            st.metric("📁 ملفات", state.get("total_files", 0))

        st.divider()

        clear = st.button("🗑️ مسح المحادثة", use_container_width=True)

        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 0;
            color:rgba(255,192,220,0.4);font-size:.7rem;line-height:1.8;">
            Made with 💕 especially for Aya<br>
            Powered by <b style="color:rgba(255,192,220,0.6);">Groq</b> ⚡<br>
            <span style="font-size:.6rem;opacity:.6;">v{APP_VERSION}</span>
        </div>""", unsafe_allow_html=True)

    return {
        "api_key": api_key,
        "mode": mode,
        "mood": mood,
        "voice_output": voice_output,
        "clear": clear,
        "pending_voice": pending_voice,
    }