"""
main.py — FastAPI backend for Multimodal Construction Intelligence Platform.
Serves the frontend static files AND provides all API endpoints.
"""

import os
import io
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from demo_data import (
    DEMO_SAFETY, DEMO_CRACK, WEATHER_ADVISORIES,
    STRUCTURE_COSTS, TIER_MULTIPLIERS
)

load_dotenv()

# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Construction Intelligence Platform API",
    version="1.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory API key store (per session via header) ─────────────────────────
def get_api_key(request: Request) -> Optional[str]:
    """Read Gemini API key from X-API-Key header or env var."""
    return request.headers.get("X-API-Key") or os.getenv("GEMINI_API_KEY", "")


def try_get_model(api_key: str):
    """Return Gemini model or None if key absent/invalid."""
    if not api_key:
        return None
    try:
        from gemini_utils import get_model
        return get_model(api_key)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Construction Intelligence API running"}


# ── Tab 1: Safety & PPE Audit ─────────────────────────────────────────────────
@app.post("/api/safety-audit")
async def safety_audit(request: Request, file: Optional[UploadFile] = File(None)):
    api_key = get_api_key(request)
    model = try_get_model(api_key)

    if model and file:
        try:
            from gemini_utils import analyse_safety
            image_bytes = await file.read()
            result = analyse_safety(model, image_bytes)
            if result:
                return result
        except Exception as e:
            pass  # fall through to demo

    # Demo mode
    return DEMO_SAFETY


# ── Tab 2: Crack Diagnostics ──────────────────────────────────────────────────
@app.post("/api/crack-analysis")
async def crack_analysis(request: Request, file: Optional[UploadFile] = File(None)):
    api_key = get_api_key(request)
    model = try_get_model(api_key)

    if model and file:
        try:
            from gemini_utils import analyse_crack
            image_bytes = await file.read()
            result = analyse_crack(model, image_bytes)
            if result:
                return result
        except Exception as e:
            pass

    return DEMO_CRACK


# ── Tab 3: Planning & Valuation ───────────────────────────────────────────────
class PlanningRequest(BaseModel):
    structure_type: str
    sqft: float
    location: str
    completion: int  # 0-100
    project_name: str = "My Project"


def fmt_inr(val: float) -> str:
    if val >= 1e7:
        return f"₹{val/1e7:.2f} Cr"
    elif val >= 1e5:
        return f"₹{val/1e5:.2f} L"
    return f"₹{val:,.0f}"


def fuzzy_get(lookup: dict, key: str):
    """Exact match first, then case-insensitive, then first partial match."""
    if key in lookup:
        return lookup[key]
    key_l = key.lower()
    for k, v in lookup.items():
        if k.lower() == key_l:
            return v
    for k, v in lookup.items():
        if key_l in k.lower() or k.lower() in key_l:
            return v
    return None


@app.post("/api/planning")
async def planning(req: PlanningRequest):
    # Guard: sqft must be positive
    if req.sqft <= 0:
        raise HTTPException(422, "Built-up area (sqft) must be greater than 0")

    data = fuzzy_get(STRUCTURE_COSTS, req.structure_type)
    if not data:
        valid = list(STRUCTURE_COSTS.keys())
        raise HTTPException(400, f"Unknown structure type '{req.structure_type}'. Valid: {valid}")

    tier = fuzzy_get(TIER_MULTIPLIERS, req.location)
    if not tier:
        valid = list(TIER_MULTIPLIERS.keys())
        raise HTTPException(400, f"Unknown location '{req.location}'. Valid: {valid}")

    cost_per_sqft = data["base_cost"] * tier["cost"]
    total_budget   = cost_per_sqft * req.sqft
    capex_incurred = total_budget * (req.completion / 100)
    market_val     = total_budget * tier["market"]
    steel_kg       = data["steel_kg"] * req.sqft
    cement_bags    = data["cement_bags"] * req.sqft

    milestones = [
        {"name": "Foundation & Excavation",    "threshold": 15},
        {"name": "Structural Framework",        "threshold": 35},
        {"name": "Slab & Roofing",             "threshold": 55},
        {"name": "Brick Masonry & Plastering", "threshold": 72},
        {"name": "MEP Works",                  "threshold": 85},
        {"name": "Finishing & Handover",       "threshold": 100},
    ]
    for m in milestones:
        done_pct = min(req.completion, m["threshold"])
        m["progress"] = round((done_pct / m["threshold"]) * 100)
        m["complete"] = req.completion >= m["threshold"]

    return {
        "project_name":    req.project_name,
        "cost_per_sqft":   round(cost_per_sqft, 0),
        "total_budget":    fmt_inr(total_budget),
        "total_budget_raw": total_budget,
        "capex_incurred":  fmt_inr(capex_incurred),
        "market_value":    fmt_inr(market_val),
        "steel_kg":        round(steel_kg, 0),
        "steel_mt":        round(steel_kg / 1000, 2),
        "cement_bags":     round(cement_bags, 0),
        "completion":      req.completion,
        "milestones":      milestones,
    }


# ── Tab 4: Weather Advisory ───────────────────────────────────────────────────
@app.get("/api/weather/{condition}")
async def weather(condition: str):
    # URL-decode spaces
    key = condition.replace("_", " ")
    for k in WEATHER_ADVISORIES:
        if k.lower().startswith(key.lower()[:8]):
            return WEATHER_ADVISORIES[k]
    return WEATHER_ADVISORIES["Normal Conditions"]


@app.get("/api/weather-conditions")
async def weather_conditions():
    return list(WEATHER_ADVISORIES.keys())


# ── Tab 4: Chatbot ────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


DEMO_CHAT_RESPONSES = {
    "cover": (
        "**IS 456:2000 Clause 26.4 — Minimum Clear Cover:**\n\n"
        "- **Mild exposure**: 20 mm\n"
        "- **Moderate exposure**: 30 mm\n"
        "- **Severe exposure**: 45 mm\n"
        "- **Very severe / Extreme**: 50–75 mm\n"
        "- **Footings** (Cl. 26.4.2): 50 mm minimum\n\n"
        "Cover must be measured to the outermost reinforcement bar, not the stirrups."
    ),
    "beam": (
        "**Beam Reinforcement (IS 456:2000 Cl. 26.5.1):**\n\n"
        "- **Minimum tension steel**: 0.85 bd / fy\n"
        "- **Maximum tension steel**: 0.04 bD\n"
        "- **Stirrup spacing (max)**: 0.75d or 300 mm (whichever less)\n"
        "- **Side face reinforcement** (depth > 750 mm): 0.1% of web area\n\n"
        "For M25 concrete, fck = 25 MPa. Typical design uses Fe415/500 steel."
    ),
    "default": (
        "Great question! I'm running in **Demo Mode** — enter your Gemini API key "
        "in the sidebar for full live AI responses.\n\n"
        "As a construction engineering assistant, I cover:\n"
        "- IS 456, IS 800, IS 13920, IS 875, IS 1893\n"
        "- OSHA 29 CFR 1926 safety standards\n"
        "- Structural calculations, material specs, site management\n\n"
        "Please add your API key for real-time personalised answers."
    )
}


@app.post("/api/chat")
async def chat(req: ChatRequest, request: Request):
    api_key = get_api_key(request)
    model = try_get_model(api_key)

    if model:
        try:
            from gemini_utils import chat_response
            reply = chat_response(model, req.history, req.message)
            return {"reply": reply, "mode": "live"}
        except Exception as e:
            return {"reply": f"AI error: {str(e)}", "mode": "error"}

    # Demo fallback
    msg_lower = req.message.lower()
    if "cover" in msg_lower:
        key = "cover"
    elif any(w in msg_lower for w in ["beam", "reinforcement", "rebar"]):
        key = "beam"
    else:
        key = "default"

    return {"reply": DEMO_CHAT_RESPONSES[key], "mode": "demo"}


# ─────────────────────────────────────────────────────────────────────────────
#  SERVE FRONTEND STATIC FILES
#  FastAPI serves index.html for all non-API routes (SPA routing)
# ─────────────────────────────────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_DIR / "index.html"))
