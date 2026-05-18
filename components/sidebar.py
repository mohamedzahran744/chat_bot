"""
components/sidebar.py — Sidebar controls: mode, mood, voice, file upload, stats
API key is loaded from .env automatically — no user input needed.
"""
import streamlit as st
from constants.chat_data import APP_NAME, APP_VERSION, MODES, MOODS, MODE_META
from components.chat import extract_text_from_file, build_file_context
from services.llm_service import transcribe_audio


def render_header() -> None:
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 0 0.8rem;">
        <div style="font-size:4rem;line-height:1;margin-bottom:.3rem;display:inline-block;">🌸</div>
        <h1 style="
            font-family:'Playfair Display',serif;
            color:#ff7eb6;
            font-size:2.8rem;margin:.3rem 0 .1rem;letter-spacing:0.02em;
            text-shadow:0 0 40px rgba(244,67,138,0.45);
        ">{APP_NAME}</h1>
        <p style="color:rgba(255,192,220,0.65);font-size:0.88rem;margin:0;
            font-family:'Tajawal',sans-serif;">مساعدتك الذكية الشخصية ✨</p>
        <div style="display:flex;justify-content:center;gap:8px;margin-top:.9rem;">
            <span style="width:8px;height:8px;border-radius:50%;background:#f43f8a;
                display:inline-block;box-shadow:0 0 8px rgba(244,63,138,.6);"></span>
            <span style="width:8px;height:8px;border-radius:50%;background:#a78bfa;
                display:inline-block;box-shadow:0 0 8px rgba(167,139,250,.6);"></span>
            <span style="width:8px;height:8px;border-radius:50%;background:#f43f8a;
                display:inline-block;box-shadow:0 0 8px rgba(244,63,138,.6);"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_mode_banner(mode: str) -> None:
    meta = MODE_META.get(mode, MODE_META["💬 عام"])
    st.markdown(f"""
    <div style="
        background:{meta['bg']};
        border-radius:20px;
        padding:.7rem 1.4rem;
        border:1px solid {meta['border']};
        margin-bottom:1rem;
        text-align:center;
        backdrop-filter:blur(10px);
        box-shadow:0 4px 24px {meta['shadow']};
    ">
        <span style="color:{meta['fg']};font-weight:700;font-size:.92rem;
            letter-spacing:0.02em;">{meta['label']}</span>
    </div>""", unsafe_allow_html=True)


def render_sidebar(state: dict) -> dict:
    pending_voice = None

    with st.sidebar:
        # ── Brand ──────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center;padding:.6rem 0 .4rem;">
            <span style="font-size:2.4rem;display:inline-block;">🌸</span>
            <h2 style="margin:.2rem 0 0;font-family:'Playfair Display',serif;
                color:#ff7eb6 !important;font-size:1.7rem;">AYA AI</h2>
            <p style="font-size:.75rem;color:rgba(255,192,220,0.55);margin:0;">
                مساعدتك الذكية الشخصية 💕</p>
        </div>""", unsafe_allow_html=True)

        st.divider()

        # ── Mode ──────────────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;letter-spacing:.02em;">✨ الوضع</p>', unsafe_allow_html=True)
        mode = st.radio(
            "mode_radio",
            MODES,
            index=MODES.index(state.get("mode", "💬 عام")),
            label_visibility="collapsed",
        )

        st.divider()

        # ── Mood ──────────────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;letter-spacing:.02em;">💕 كيف حالك؟</p>', unsafe_allow_html=True)
        mood = st.radio(
            "mood_radio",
            MOODS,
            index=MOODS.index(state.get("mood", "😊 سعيدة")),
            label_visibility="collapsed",
        )

        st.divider()

        # ── Voice output toggle ────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;letter-spacing:.02em;">🔊 الصوت</p>', unsafe_allow_html=True)
        voice_output = st.toggle(
            "ردود صوتية تلقائية 🔊",
            value=state.get("voice_output", False),
        )

        st.divider()

        # ── File Upload ───────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;letter-spacing:.02em;">📎 رفع ملف</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:rgba(255,192,220,0.5);font-size:.73rem;margin-bottom:.4rem;">'
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
                f'<div style="background:rgba(244,67,138,0.1);border-radius:12px;'
                f'padding:.4rem .9rem;font-size:.78rem;'
                f'color:rgba(255,192,220,0.85);border:1px solid rgba(244,67,138,0.25);">'
                f'📎 <b style="color:#ff7eb6;">{st.session_state.file_name}</b></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Voice Input ───────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:4px;letter-spacing:.02em;">🎙️ رسالة صوتية</p>', unsafe_allow_html=True)

        try:
            audio_value = st.audio_input("🎙️ اضغطي لتسجيل رسالة", key="sidebar_audio")
            if audio_value is not None:
                with st.spinner("🌸 بتحوّل الكلام لنص..."):
                    try:
                        transcribed = transcribe_audio(audio_value.read(), "recording.wav")
                        if transcribed:
                            st.success(f"✅ **{transcribed}** ✨")
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
                        transcribed = transcribe_audio(voice_upload.read(), voice_upload.name)
                        if transcribed:
                            st.success(f"✅ **{transcribed}** ✨")
                            pending_voice = transcribed
                    except Exception as e:
                        st.error(f"😔 مشكلة: {e}")

        st.divider()

        # ── Stats ─────────────────────────────────────────
        st.markdown('<p style="color:rgba(255,192,220,0.85);font-size:.82rem;font-weight:700;margin-bottom:6px;letter-spacing:.02em;">📊 إحصائياتك</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💬 رسائل", state.get("total_messages", 0))
        with col2:
            st.metric("📁 ملفات", state.get("total_files", 0))

        st.divider()

        clear = st.button("🗑️ مسح المحادثة", use_container_width=True)

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
