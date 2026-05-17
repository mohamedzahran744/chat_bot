"""
services/llm_service.py — Groq API chat + gTTS voice + Whisper transcription
"""
import io
from groq import Groq
from gtts import gTTS
from constants.chat_data import GROQ_MODEL, MAX_TOKENS, TEMPERATURE
from constants.system_prompt import get_system_prompt


def get_groq_client(api_key: str) -> Groq:
    if not api_key or not api_key.strip():
        raise ValueError("الـ API Key فاضي — حطي مفتاحك من console.groq.com")
    return Groq(api_key=api_key.strip())


def chat_with_aya(
    api_key: str,
    messages: list[dict],
    mode: str,
    mood: str,
    extra_context: str = "",
) -> str:
    """Send conversation to Groq, return assistant reply (text only)."""
    client = get_groq_client(api_key)

    system = get_system_prompt(mode, mood)
    if extra_context:
        system += f"\n\n[CONTEXT]\n{extra_context}\n[END CONTEXT]"

    # Strip any non-standard keys before sending to Groq
    clean_messages = [
        {"role": m.get("role", "user"), "content": str(m.get("content", ""))}
        for m in messages
        if m.get("role") in ("user", "assistant")
    ]

    # Keep last 30 messages to avoid token overflow
    if len(clean_messages) > 30:
        clean_messages = clean_messages[-30:]

    response = client.chat.completions.create(
        model       = GROQ_MODEL,
        messages    = [{"role": "system", "content": system}, *clean_messages],
        max_tokens  = MAX_TOKENS,
        temperature = TEMPERATURE,
    )
    return response.choices[0].message.content


def text_to_speech(text: str, lang: str = "ar") -> bytes:
    """Convert text → MP3 bytes via gTTS. Auto-detects Arabic/Chinese/English."""
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

    # Clean text: remove markdown code blocks for TTS
    import re
    clean = re.sub(r"```[\s\S]*?```", " كود برمجي ", text)
    clean = re.sub(r"`[^`]+`", "", clean)
    clean = re.sub(r"[#*_~>\[\]()]", "", clean).strip()
    clean = clean[:2000]  # gTTS limit

    tts = gTTS(text=clean, lang=lang, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def transcribe_audio(api_key: str, audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """Transcribe audio via Groq Whisper. Returns plain text."""
    client     = get_groq_client(api_key)
    audio_file = (filename, audio_bytes, "audio/wav")

    transcription = client.audio.transcriptions.create(
        model           = "whisper-large-v3",
        file            = audio_file,
        response_format = "text",
    )

    if isinstance(transcription, str):
        return transcription.strip()
    return getattr(transcription, "text", "").strip()
