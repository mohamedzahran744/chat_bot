"""
components/chat.py — Chat UI, file handling, voice input, quick actions
"""
import io
import random
import streamlit as st
from services.llm_service import chat_with_aya, text_to_speech, transcribe_audio
from constants.chat_data import QUICK_PROMPTS, CODING_CHALLENGES, REMINDERS, get_today_index


# ─────────────────────────────────────────────
# FILE HANDLING
# ─────────────────────────────────────────────
TEXT_EXTENSIONS = (
    ".txt", ".md", ".py", ".cpp", ".c", ".h", ".js", ".ts",
    ".java", ".json", ".csv", ".xml", ".html", ".css", ".sql",
    ".yaml", ".yml", ".rs", ".go", ".kt",
)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def extract_text_from_file(uploaded_file) -> tuple[str, str]:
    name = uploaded_file.name.lower()
    raw  = uploaded_file.read()

    if any(name.endswith(ext) for ext in TEXT_EXTENSIONS):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")
        return text[:8000], "📄 ملف نصي / كود"

    if name.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            pages = []
            for i, page in enumerate(reader.pages):
                if i >= 50:
                    break
                pages.append(page.extract_text() or "")
            return "\n".join(pages)[:8000], "📕 PDF"
        except Exception as e:
            return f"[PDF ERROR] {e}", "📕 PDF"

    if name.endswith(".docx"):
        try:
            from docx import Document
            doc  = Document(io.BytesIO(raw))
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            return text[:8000], "📝 Word Document"
        except Exception as e:
            return f"[DOCX ERROR] {e}", "📝 Word Document"

    if any(name.endswith(ext) for ext in IMAGE_EXTENSIONS):
        return "[IMAGE_UPLOADED]", "🖼️ صورة"

    return f"[UNSUPPORTED]: {name}", "📎 ملف"


def build_file_context(extracted_text: str, file_label: str, filename: str) -> str:
    if extracted_text == "[IMAGE_UPLOADED]":
        return f"المستخدم رفعت صورة باسم '{filename}'. اذكري ذلك وساعديها."
    if not extracted_text.strip():
        return f"المستخدم رفعت ملف '{filename}' لكن لا يوجد محتوى قابل للقراءة."
    return (
        f"المستخدم رفعت {file_label} باسم '{filename}'.\n"
        f"محتوى الملف:\n```\n{extracted_text}\n```\n"
        "حللي المحتوى وردي على سؤالها."
    )


# ─────────────────────────────────────────────
# FILE UPLOAD WIDGET
# ─────────────────────────────────────────────
def render_file_upload() -> None:
    with st.expander("📎 ارفعي ملف أو صورة", expanded=False):
        st.markdown(
            '<p style="color:rgba(255,192,220,0.7);font-size:.85rem;margin-bottom:.5rem;">'
            "PDF، Word، Python، C++، TXT، JSON، CSV، صور 🌸</p>",
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "upload",
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
            st.success(f"✅ تم رفع {label}: **{uploaded.name}** 🌸")

    if st.session_state.file_name:
        st.markdown(
            f'<div style="background:rgba(244,67,138,0.1);border-radius:14px;'
            f'padding:.5rem 1rem;margin-bottom:.5rem;'
            f'border:1px solid rgba(244,67,138,0.25);font-size:.85rem;'
            f'color:rgba(255,192,220,0.85);">'
            f'📎 ملف محمّل: <b style="color:#ff7eb6;">{st.session_state.file_name}</b>'
            f' — اسأليني عنه 💕</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# VOICE INPUT WIDGET
# ─────────────────────────────────────────────
def render_voice_input(api_key: str) -> str | None:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border:1.5px dashed rgba(244,67,138,0.3);
        border-radius:18px;padding:1rem 1.2rem;text-align:center;margin-bottom:.5rem;">
        <div style="font-size:1.8rem;">🎙️</div>
        <p style="color:#ff7eb6;font-weight:600;margin:.3rem 0 .1rem;font-size:.9rem;">
            سجلي رسالتك الصوتية</p>
        <p style="color:rgba(255,192,220,0.5);font-size:.78rem;margin:0;">
            اضغطي للتسجيل ثم ارسلي</p>
    </div>""", unsafe_allow_html=True)

    transcribed = None

    try:
        audio_value = st.audio_input("🎙️ اضغطي لتسجيل رسالة")
        if audio_value is not None:
            with st.spinner("🌸 بتحوّل الكلام لنص..."):
                try:
                    transcribed = transcribe_audio(api_key, audio_value.read(), "recording.wav")
                except Exception as e:
                    st.error(f"😔 مشكلة في الصوت: {e}")
    except Exception:
        uploaded = st.file_uploader(
            "📤 ارفعي ملف صوتي",
            type=["wav", "mp3", "m4a", "ogg", "webm"],
            key="voice_upload_fallback",
        )
        if uploaded:
            with st.spinner("🌸 بتحوّل الكلام لنص..."):
                try:
                    transcribed = transcribe_audio(api_key, uploaded.read(), uploaded.name)
                except Exception as e:
                    st.error(f"😔 مشكلة: {e}")

    if transcribed:
        st.success(f"✅ تم التعرف على: **{transcribed}**")

    return transcribed


# ─────────────────────────────────────────────
# QUICK ACTION BUTTONS
# ─────────────────────────────────────────────
def render_quick_actions() -> None:
    from constants.chat_data import CODING_CHALLENGES as CC

    idx             = get_today_index()
    today_challenge = CC[idx % len(CC)]
    mode            = st.session_state.mode
    q_list          = QUICK_PROMPTS.get(mode, QUICK_PROMPTS["💬 عام"])

    if not q_list:
        return

    st.markdown(
        '<p style="color:rgba(255,192,220,0.6);font-size:.78rem;'
        'font-weight:600;margin:.4rem 0 .3rem;letter-spacing:0.04em;">⚡ اختصارات سريعة</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(len(q_list))
    for col, (label, msg_text) in zip(cols, q_list):
        if msg_text is None:
            msg_text = f"ساعديني أحل: {today_challenge}"
        with col:
            if st.button(label, use_container_width=True, key=f"quick_{label}_{mode}"):
                st.session_state.pending_input = msg_text
                st.rerun()


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────
def render_empty_state() -> None:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;opacity:0.85;">
        <div style="font-size:4rem;line-height:1;margin-bottom:1rem;
            animation:float 3s ease-in-out infinite;display:inline-block;">🌸</div>
        <h2 style="
            font-family:'Playfair Display',serif;
            background:linear-gradient(135deg,#ff7eb6,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;font-size:1.8rem;margin:.5rem 0;
        ">مرحباً يا آية! 💕</h2>
        <p style="color:rgba(255,192,220,0.6);font-size:.95rem;max-width:380px;
            margin:0 auto;line-height:1.7;">
            أنا AYA AI ✨ — مساعدتك الذكية الشخصية<br>
            اكتبي أي حاجة وأنا هنا 🌸
        </p>
        <div style="margin-top:1.5rem;display:flex;justify-content:center;gap:1.5rem;
            flex-wrap:wrap;">
            <div style="background:rgba(244,67,138,0.1);border:1px solid rgba(244,67,138,0.25);
                border-radius:14px;padding:.7rem 1.2rem;font-size:.82rem;
                color:rgba(255,192,220,0.7);">🇨🇳 لغة صينية</div>
            <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);
                border-radius:14px;padding:.7rem 1.2rem;font-size:.82rem;
                color:rgba(255,192,220,0.7);">💻 مساعدة برمجة</div>
            <div style="background:rgba(244,67,138,0.1);border:1px solid rgba(244,67,138,0.25);
                border-radius:14px;padding:.7rem 1.2rem;font-size:.82rem;
                color:rgba(255,192,220,0.7);">📚 خطة مذاكرة</div>
        </div>
    </div>
    <style>
    @keyframes float{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-8px);}}}}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────
def render_chat_history() -> None:
    if not st.session_state.messages:
        render_empty_state()
        return

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# ─────────────────────────────────────────────
# REMINDER
# ─────────────────────────────────────────────
def maybe_show_reminder(msg_count: int) -> None:
    if msg_count > 0 and msg_count % 8 == 0:
        st.info(random.choice(REMINDERS))


# ─────────────────────────────────────────────
# SEND MESSAGE PIPELINE
# ─────────────────────────────────────────────
def handle_chat_input() -> None:
    typed_prompt = st.chat_input("اكتبي رسالتك هنا يا آية... 🌸")

    user_text = None
    if st.session_state.pending_input:
        user_text                    = st.session_state.pending_input
        st.session_state.pending_input = None
    elif typed_prompt:
        user_text = typed_prompt

    if not user_text:
        return

    if not st.session_state.api_key:
        st.error("💕 يا آية، محتاجة تضعي Groq API Key في الـ Sidebar الأول!")
        st.stop()

    with st.chat_message("user"):
        st.markdown(user_text)

    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.total_messages += 1

    with st.chat_message("assistant"):
        with st.spinner("⏳ AYA AI بتفكر... 🌸"):
            try:
                reply = chat_with_aya(
                    api_key      = st.session_state.api_key,
                    messages     = st.session_state.messages,
                    mode         = st.session_state.mode,
                    mood         = st.session_state.mood,
                    extra_context= st.session_state.file_context,
                )
                st.markdown(reply)

                if st.session_state.voice_output:
                    try:
                        audio_bytes = text_to_speech(reply)
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception:
                        pass

                st.session_state.messages.append({"role": "assistant", "content": reply})
                maybe_show_reminder(st.session_state.total_messages)

            except Exception as e:
                err_msg = str(e)
                if "api_key" in err_msg.lower() or "authentication" in err_msg.lower():
                    st.error("🔑 الـ API Key غلط يا آية! تأكدي منه من console.groq.com")
                elif "rate_limit" in err_msg.lower():
                    st.warning("⏳ الـ API وصلت للحد — انتظري ثانية وحاولي تاني!")
                else:
                    st.error(f"😔 في مشكلة صغيرة يا آية: `{err_msg}`")
                # pop the user message we just added so chat stays clean
                if st.session_state.messages:
                    st.session_state.messages.pop()
