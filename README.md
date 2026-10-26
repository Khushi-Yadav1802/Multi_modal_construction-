# 🏗️ Multimodal Construction Intelligence Platform

> **Skill Wallet Capstone Project 1** — AI-powered full-stack web application for smart construction site management.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-4285F4?logo=google)](https://ai.google.dev/)

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🦺 **PPE Safety Audit** | Upload site photos → AI detects helmets, vests, harnesses, boots. Outputs safety score, hazard list, OSHA/IS 456 compliance |
| 🔬 **Crack Diagnostics** | Upload crack images → AI classifies defect type, severity, root cause. Outputs IS 456 / ACI 318 repair protocol |
| 💰 **Project Planning** | Enter sqft + location → Budget, CapEx, market valuation in INR, material quantities, milestone tracker + 3D AI renders |
| 🤖 **Site Assistant** | Multi-turn chatbot for structural queries + real-time weather-aware safety advisories |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multimodelconstruction.git
cd multimodelconstruction
```

### 2. Install dependencies
```bash
pip install fastapi "uvicorn[standard]" python-multipart google-generativeai Pillow requests python-dotenv
```

### 3. (Optional) Add Gemini API key
Create `backend/.env`:
```
GEMINI_API_KEY=your_key_here
```
Leave blank to use **Demo Mode** (pre-built responses, no API key needed).

### 4. Run the server
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Open browser
```
http://localhost:8000
```

---

## 🗂️ Project Structure

```
multimodelconstruction/
├── backend/
│   ├── main.py            # FastAPI app — all API endpoints
│   ├── gemini_utils.py    # Gemini 1.5 Flash vision + chat helpers
│   ├── demo_data.py       # Demo responses (no API key needed)
│   └── requirements.txt
├── frontend/
│   ├── index.html         # Single-page app shell
│   ├── style.css          # Dark-theme design system
│   └── app.js             # Tab logic, API calls, drag-drop
├── app.py                 # Original Streamlit version (bonus)
├── start.bat              # Windows one-click launcher
└── .gitignore
```

---

## 🧠 Tech Stack

- **Backend**: Python · FastAPI · Uvicorn
- **AI**: Google Gemini 1.5 Flash (vision + text)
- **3D Renders**: Pollinations AI (free, no key needed)
- **Frontend**: Vanilla HTML · CSS · JavaScript (no framework)
- **Standards**: OSHA 29 CFR 1926 · IS 456:2000 · IS 13920 · ACI 318 · NBC 2016

---

## 🌐 Deploy to Cloud

### Render (free)
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect GitHub repo
4. Set **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `GEMINI_API_KEY=your_key`
6. Deploy ✅

### Railway / Fly.io
Similar — point start command to `backend/main.py` via uvicorn.

---

## 📄 License
MIT — free to use, modify, and deploy.
