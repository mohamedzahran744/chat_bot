# 🌸 AYA AI — مساعدتك الذكية الشخصية

A full-featured, beautiful AI assistant built with **Python + Streamlit**.  
Dark luxury glassmorphism UI with Arabic support, voice, file upload, and multi-mode chat.

---

## 📁 Project Structure

```
aya_ai/
├── app.py                    ← Main entry point
├── requirements.txt
├── .env                      ← Your API key (create this)
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

## 🚀 Quick Start (Local)

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Run!
streamlit run app.py
```

Get a **free** Groq API key at: https://console.groq.com

---

## 🌐 How to Share AYA AI as a Link (Free!)

### Option 1 — Streamlit Community Cloud (EASIEST ✅)

> **Your friend gets a real link like: `https://aya-ai.streamlit.app`**

**Steps:**
1. Upload your project to **GitHub** (make a free account at github.com)
2. Go to **https://share.streamlit.io** and sign in with GitHub
3. Click **"New app"** → select your repo → set `app.py` as the main file
4. Click **Deploy** 🚀
5. Share the link with your friends!

**⚠️ Important:** Add your Groq API key as a **Secret** in Streamlit Cloud:
- Go to your app settings → "Secrets"
- Add: `GROQ_API_KEY = "gsk_your_key_here"`
- In `app.py`, update to read: `import os; key = os.getenv("GROQ_API_KEY", "")`

**Cost:** FREE for public apps ✅

---

### Option 2 — Share via ngrok (Quick Test)

```bash
# 1. Run streamlit locally
streamlit run app.py

# 2. In a new terminal, install ngrok (https://ngrok.com)
ngrok http 8501

# 3. Share the https://xxxx.ngrok.io link with your friend
```

**Cost:** FREE (temporary link, resets when you stop) ✅

---

### Option 3 — Railway.app (Always Online)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**Cost:** Free tier available ✅

---

## ✨ Features

| Feature | Details |
|---|---|
| 💬 Chat | Groq LLaMA 3.3 70B (free & fast) |
| 🎨 UI | Dark luxury glassmorphism — deep rose & plum |
| 🇨🇳 Chinese Mode | Translation, Pinyin, grammar correction |
| 💻 Coding Mode | Python, C++, DSA with Arabic explanations |
| 📚 Study Mode | Plans, motivation, memory techniques |
| 📎 File Upload | PDF, DOCX, TXT, code, images |
| 🎙️ Voice Input | Whisper transcription via Groq |
| 🔊 Voice Output | gTTS (Arabic, Chinese, English) |
| 😊 Mood System | 4 moods adjust AI personality |
| 🌅 Daily Boost | Chinese word + coding challenge + motivation |

---

Made with 💕 especially for Aya • AYA AI ✨ v2.1.0
