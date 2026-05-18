import streamlit as st
from constants.chat_data import APP_NAME, APP_VERSION, MODES, MOODS, MODE_META
from components.chat import extract_text_from_file, build_file_context
from services.llm_service import transcribe_audio

# ... render_header and render_mode_banner stay the same ...

def render_sidebar(state: dict) -> dict:
    pending_voice = None

    with st.sidebar:
        # ── Brand ──────────────────────────────────────────
        st.markdown(f"""
        <div style="text-align:center;padding:.6rem 0 .4rem;">
            <span style="font-size:2.4rem;display:inline-block;">🌸</span>
            <h2 style="margin:.2rem 0 0;font-family:'Playfair Display',serif;
                color:#ff7eb6 !important;font-size:1.7rem;">{APP_NAME}</h2>
            <p style="font-size:.75rem;color:rgba(255,192,220,0.55);margin:0;">
                مساعدتك الذكية الشخصية 💕</p>
        </div>""", unsafe_allow_html=True)

        st.divider()

        # ── Mode & Mood ────────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;">✨ الوضع</p>', unsafe_allow_html=True)
        mode = st.radio(
            "mode_radio", MODES,
            index=MODES.index(state.get("mode", "💬 عام")),
            label_visibility="collapsed",
        )

        st.divider()

        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;">💕 كيف حالك؟</p>', unsafe_allow_html=True)
        mood = st.radio(
            "mood_radio", MOODS,
            index=MOODS.index(state.get("mood", "😊 سعيدة")),
            label_visibility="collapsed",
        )

        st.divider()

        # ── Voice output toggle ────────────────────────────
        voice_output = st.toggle(
            "🔊 ردود صوتية تلقائية",
            value=state.get("voice_output", False),
        )

        st.divider()

        # ── File Upload ───────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;">📎 رفع ملف</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "upload_sidebar",
            type=["pdf", "docx", "txt", "md", "py", "cpp", "c", "h", "js", "ts",
                  "java", "json", "csv", "xml", "html", "css", "sql", "yaml", "yml",
                  "png", "jpg", "jpeg", "webp", "gif"],
            label_visibility="collapsed",
        )
        
        # FIX: Only process file if it's new to avoid infinite incrementing on reruns
        if uploaded and st.session_state.get("last_uploaded_file") != uploaded.name:
            with st.spinner("🌸 جاري معالجة الملف..."):
                extracted, label = extract_text_from_file(uploaded)
                st.session_state.file_context = build_file_context(extracted, label, uploaded.name)
                st.session_state.file_name = uploaded.name
                st.session_state.last_uploaded_file = uploaded.name # Track unique upload
                st.session_state.total_files = st.session_state.get("total_files", 0) + 1
                st.success(f"✅ {label} جاهز!")

        if st.session_state.get("file_name"):
            st.markdown(
                f'<div style="background:rgba(244,67,138,0.1);border-radius:12px;'
                f'padding:.4rem .9rem;font-size:.78rem;'
                f'color:rgba(255,192,220,0.85);border:1px solid rgba(244,67,138,0.25);">'
                f'📎 <b style="color:#ff7eb6;">{st.session_state.file_name}</b></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Voice Input ───────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;">🎙️ رسالة صوتية</p>', unsafe_allow_html=True)

        # Using st.audio_input (Available in Streamlit 1.39+)
        try:
            audio_data = st.audio_input("تسجيل", label_visibility="collapsed", key="sidebar_voice")
            if audio_data and st.session_state.get("last_audio_processed") != audio_data:
                with st.spinner("🌸 جاري التحويل..."):
                    transcribed = transcribe_audio(audio_data.read(), "recording.wav")
                    if transcribed:
                        pending_voice = transcribed
                        st.session_state.last_audio_processed = audio_data # Prevent re-transcribing same audio
        except Exception:
            # Fallback for older versions
            voice_upload = st.file_uploader("رفع ملف صوتي", type=["wav", "mp3"], key="v_up")
            if voice_upload:
                transcribed = transcribe_audio(voice_upload.read(), voice_upload.name)
                pending_voice = transcribed

        st.divider()

        # ── Stats ─────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💬 رسائل", state.get("total_messages", 0))
        with col2:
            st.metric("📁 ملفات", state.get("total_files", 0))

        st.divider()

        clear = st.button("🗑️ مسح المحادثة", use_container_width=True, type="secondary")

        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 0;
            color:rgba(255,192,220,0.35);font-size:.7rem;line-height:2;">
            Made with 💕 especially for Aya<br>
            Powered by <b style="color:rgba(255,192,220,0.55);">Groq</b> ⚡<br>
            <span style="font-size:.65rem;opacity:.7;">v{APP_VERSION}</span>
        </div>""", unsafe_allow_html=True)

    return {
        "mode": mode,
        "mood": mood,
        "voice_output": voice_output,
        "clear": clear,
        "pending_voice": pending_voice,
    }
