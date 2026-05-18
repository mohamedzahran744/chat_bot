# 🌸 AYA AI — مساعدتك الذكية الشخصية

A full-featured, beautiful AI assistant built with **Python + Streamlit**.  
Dark luxury glassmorphism UI with Arabic support, voice, file upload, and multi-mode chat.

> **v2.2.0** — API key is now loaded automatically from `.env` — no manual input needed! 🎀

---

## 📁 Project Structure

```
aya_ai/
├── app.py                    ← Main entry point
├── requirements.txt
├── .env                      ← Your API key (create from .env.example)
├── .env.example              ← Template
│
├── .streamlit/
│   └── config.toml           ← Dark luxury theme
│
├── components/
│   ├── chat.py               ← Chat UI, file handler, voice input
│   └── sidebar.py            ← Sidebar, header, mode banner
│
├── constants/
│   ├── chat_data.py          ← Modes, moods, daily content, prompts
│   └── system_prompt.py      ← System prompt builder
│
└── services/
    └── llm_service.py        ← Groq chat + TTS + Whisper
```

---

## 🚀 Quick Start

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Create .env file from template
cp .env.example .env

# 3. Edit .env and add your key
# GROQ_API_KEY=gsk_your_key_here

# 4. Run!
streamlit run app.py
```

Get a **free** Groq API key at: https://console.groq.com

> ✅ The API key is loaded **automatically** from `.env` — users never need to type it in the app!

---

## 🌐 Deploy to Streamlit Community Cloud

1. Push project to **GitHub**
2. Go to **https://share.streamlit.io** → "New app" → select repo → `app.py`
3. Under **Secrets**, add:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. Deploy 🚀

---

## ✨ Features

| Feature | Details |
|---|---|
| 💬 Chat | Groq LLaMA 3.3 70B (free & fast) |
| 🎨 UI | Dark luxury glassmorphism — deep rose & plum |
| 🔑 API Key | Auto-loaded from `.env` — no UI input needed |
| 🇨🇳 Chinese Mode | Translation, Pinyin, grammar correction |
| 💻 Coding Mode | Python, C++, DSA with Arabic explanations |
| 📚 Study Mode | Plans, motivation, memory techniques |
| 📎 File Upload | PDF, DOCX, TXT, code, images |
| 🎙️ Voice Input | Whisper transcription via Groq |
| 🔊 Voice Output | gTTS (Arabic, Chinese, English) |
| 😊 Mood System | 4 moods adjust AI personality |

---

Made with 💕 especially for Aya • AYA AI ✨ v2.2.0
