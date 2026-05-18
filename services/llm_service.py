"""
services/llm_service.py — Groq API chat + gTTS voice + Whisper transcription
API key is loaded from environment / .env file only — never from user input.
"""
import io
import os
import re
from groq import Groq
from gtts import gTTS
from constants.chat_data import GROQ_MODEL, MAX_TOKENS, TEMPERATURE
from constants.system_prompt import get_system_prompt

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_API_KEY: str = os.getenv("GROQ_API_KEY", "")


def _get_client() -> Groq:
    key = _API_KEY.strip()
    if not key:
        raise ValueError(
            "🔑 GROQ_API_KEY غير موجود!\n"
            "أضيفي مفتاحك في ملف .env:\n"
            "GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx\n"
            "احصلي على مفتاح مجاني من: https://console.groq.com"
        )
    return Groq(api_key=key)


def _clean_reply(text: str) -> str:
    """Strip ```html / ``` wrappers the model sometimes adds."""
    text = text.strip()
    text = re.sub(r'^```[\w]*\n?', '', text)   # remove opening ```html or ```
    text = re.sub(r'\n?```$', '', text)         # remove closing ```
    return text.strip()


def chat_with_aya(
    messages: list[dict],
    mode: str,
    mood: str,
    extra_context: str = "",
) -> str:
    """Send conversation to Groq, return assistant reply (text only)."""
    client = _get_client()

    system = get_system_prompt(mode, mood)
    if extra_context:
        system += f"\n\n[CONTEXT]\n{extra_context}\n[END CONTEXT]"

    clean_messages = [
        {"role": m.get("role", "user"), "content": str(m.get("content", ""))}
        for m in messages
        if m.get("role") in ("user", "assistant")
    ]

    if len(clean_messages) > 30:
        clean_messages = clean_messages[-30:]

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "system", "content": system}, *clean_messages],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return _clean_reply(response.choices[0].message.content)  # ✅ FIX


def text_to_speech(text: str, lang: str = "ar") -> bytes:
    """Convert text → MP3 bytes via gTTS."""
    sample = text[:100]

    if any("\u4e00" <= c <= "\u9fff" for c in sample):
        lang = "zh-TW"
    elif (
        any(c.isascii() and c.isalpha() for c in sample[:50])
        and not any("\u0600" <= c <= "\u06ff" for c in sample[:50])
    ):
        lang = "en"
    else:
        lang = "ar"

    clean = re.sub(r"```[\s\S]*?```", " كود برمجي ", text)
    clean = re.sub(r"`[^`]+`", "", clean)
    clean = re.sub(r"[#*_~>\[\]()]", "", clean).strip()
    clean = clean[:2000]

    tts = gTTS(text=clean, lang=lang, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """Transcribe audio via Groq Whisper. Returns plain text."""
    client = _get_client()
    audio_file = (filename, audio_bytes, "audio/wav")

    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_file,
        response_format="text",
    )

    if isinstance(transcription, str):
        return transcription.strip()
    return getattr(transcription, "text", "").strip()