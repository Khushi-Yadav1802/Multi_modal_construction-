"""
gemini_utils.py — Gemini AI helper functions.
"""
import json
import re
import io
from PIL import Image


def get_model(api_key: str):
    """Return a configured Gemini GenerativeModel or raise on failure."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def extract_json(text: str) -> dict | None:
    """Pull the first JSON object out of a raw string."""
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


def analyse_safety(model, image_bytes: bytes) -> dict | None:
    img = Image.open(io.BytesIO(image_bytes))
    prompt = """You are a certified construction safety inspector (OSHA 29 CFR 1926, IS 456:2000).
Analyse this site photo. Return ONLY valid JSON — no markdown, no explanation:
{
  "safety_score": <0-100 integer>,
  "overall_status": "<SAFE|NEEDS IMPROVEMENT|UNSAFE|CRITICAL>",
  "standards_referenced": ["<std1>"],
  "ppe_detection": {
    "hard_hat":        {"detected": <bool>, "compliance": "<text>"},
    "high_vis_vest":   {"detected": <bool>, "compliance": "<text>"},
    "steel_toe_boots": {"detected": <bool>, "compliance": "<text>"},
    "safety_harness":  {"detected": <bool>, "compliance": "<text>"},
    "safety_gloves":   {"detected": <bool>, "compliance": "<text>"},
    "eye_protection":  {"detected": <bool>, "compliance": "<text>"}
  },
  "site_hazards": [
    {"hazard": "<desc>", "severity": "<Low|Medium|High|Critical>", "remedy": "<text>"}
  ],
  "recommendations": "<text>"
}"""
    response = model.generate_content([prompt, img])
    return extract_json(response.text)


def analyse_crack(model, image_bytes: bytes) -> dict | None:
    img = Image.open(io.BytesIO(image_bytes))
    prompt = """You are a structural forensic engineer specialised in concrete pathology (IS 456:2000, ACI 318).
Analyse this surface image. Return ONLY valid JSON — no markdown, no explanation:
{
  "defect_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Corrosion Staining|Other>",
  "crack_width_mm": <float>,
  "crack_length_estimate": "<text>",
  "pattern": "<text>",
  "severity": "<Low|Medium|High|Critical>",
  "urgency": "<text>",
  "root_causes": ["<cause>"],
  "recommended_repairs": [{"method": "<name>", "detail": "<text>"}],
  "standards": ["<std>"],
  "monitoring": "<text>"
}"""
    response = model.generate_content([prompt, img])
    return extract_json(response.text)


def chat_response(model, history: list[dict], user_msg: str) -> str:
    history_text = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history[-8:]
    )
    prompt = f"""You are an expert construction engineering assistant with deep knowledge of:
IS codes (IS 456, IS 800, IS 13920, IS 875, IS 1893, IS 3764, NBC 2016), OSHA 29 CFR 1926,
structural/geotechnical engineering, material science, site safety, real estate valuation in India.

Conversation history:
{history_text}
User: {user_msg}

Give a concise, technically accurate response. Use bullet points where helpful.
Reference IS codes or OSHA clauses when applicable. Keep response under 300 words."""
    response = model.generate_content(prompt)
    return response.text
