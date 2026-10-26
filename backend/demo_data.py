"""
demo_data.py — Pre-built fallback responses for demo / no-API-key mode.
"""

DEMO_SAFETY = {
    "safety_score": 67,
    "overall_status": "NEEDS IMPROVEMENT",
    "standards_referenced": ["OSHA 29 CFR 1926", "IS 456:2000", "NBC 2016"],
    "ppe_detection": {
        "hard_hat":       {"detected": True,  "compliance": "Compliant"},
        "high_vis_vest":  {"detected": False, "compliance": "Non-Compliant — missing on 2 workers"},
        "steel_toe_boots":{"detected": True,  "compliance": "Compliant"},
        "safety_harness": {"detected": False, "compliance": "Non-Compliant — required at height > 1.8 m"},
        "safety_gloves":  {"detected": True,  "compliance": "Compliant"},
        "eye_protection": {"detected": False, "compliance": "Non-Compliant"}
    },
    "site_hazards": [
        {
            "hazard": "Workers at height without safety harness",
            "severity": "Critical",
            "remedy": "Halt elevated work immediately. Enforce full-body harness with double-locking carabiner. Run toolbox talk before resuming."
        },
        {
            "hazard": "No high-visibility vests in active vehicle corridor",
            "severity": "High",
            "remedy": "Issue EN ISO 20471 Class 2+ vests. Establish 2-m exclusion zones around moving plant."
        },
        {
            "hazard": "Unguarded excavation pit edge",
            "severity": "High",
            "remedy": "Install rigid barriers ≥ 1 m from pit edge per IS 3764. Add warning signage."
        },
        {
            "hazard": "Debris and trip hazards on walkways",
            "severity": "Medium",
            "remedy": "Implement 5S housekeeping. Mark dedicated pedestrian routes with paint/barriers."
        },
        {
            "hazard": "Inadequate lighting in lower work area",
            "severity": "Low",
            "remedy": "Install portable LED floods ≥ 200 lux per IS 3646 Part I."
        }
    ],
    "recommendations": "Conduct immediate safety stand-down meeting. Update induction records. Re-audit within 72 hours."
}


DEMO_CRACK = {
    "defect_type": "Structural Shear Crack",
    "crack_width_mm": 2.8,
    "crack_length_estimate": "~450 mm visible",
    "pattern": "Diagonal at 45° from beam-column junction",
    "severity": "High",
    "urgency": "Immediate Engineering Assessment Required",
    "root_causes": [
        "Differential foundation settlement",
        "Inadequate shear reinforcement (stirrup spacing > IS 456 limits)",
        "Possible overloading beyond design capacity",
        "High w/c ratio concrete (> 0.55)"
    ],
    "recommended_repairs": [
        {
            "method": "Low-Viscosity Epoxy Injection",
            "detail": "Drill ports @ 150 mm centres along crack. Inject epoxy resin at 0.3–0.5 MPa per ACI 224.1R. Allow 24 h cure before reloading."
        },
        {
            "method": "CFRP Wrapping",
            "detail": "Apply Carbon Fibre Reinforced Polymer strips perpendicular to crack direction for shear strengthening per IS 15988."
        },
        {
            "method": "Structural Re-grouting",
            "detail": "Where crack width > 2 mm at core: re-grout with non-shrink cementitious grout grade ≥ M40 after surface preparation."
        }
    ],
    "standards": ["IS 456:2000", "IS 13920", "ACI 318", "IS 15988"],
    "monitoring": "Install Demec crack-width gauges at 300 mm intervals. Re-survey every 7 days for 4 weeks."
}


WEATHER_ADVISORIES = {
    "High Wind (>50 km/h)": {
        "icon": "💨",
        "level": "warning",
        "title": "High Wind Advisory — Elevated Risk Operations",
        "alerts": [
            "Suspend ALL crane and hoist operations above 50 km/h sustained winds (OSHA 1926.1416).",
            "Secure loose materials, scaffolding boards, and formwork panels — lash or remove.",
            "Check anchorage of temporary structures; increase guy-wire tension by 30%.",
            "Issue double-layer high-vis vests; reduce worker exposure on elevated platforms.",
            "Activate wind speed logging — re-permit crane ops only after 30 min sustained calm.",
            "Inspect all scaffolding ties post-wind event before resuming work at height."
        ]
    },
    "Heavy Rain / Flooding": {
        "icon": "🌧️",
        "level": "info",
        "title": "Heavy Rain & Waterlogging Advisory",
        "alerts": [
            "De-energise all temporary power boards; use GFCI-protected outlets only (electrical hazard).",
            "Halt all excavation — slope stability compromised; inspect shoring for water ingress.",
            "Pump trenches dry before re-entry; test for oxygen deficiency.",
            "Suspend concrete pours if rain rate > 10 mm/hr — dilutes w/c ratio beyond spec.",
            "Install temporary drainage channels to prevent slope erosion.",
            "Issue waterproof PPE (suits + rubber boots to IS 4770) for essential personnel."
        ]
    },
    "Extreme Heat (>42°C)": {
        "icon": "🌡️",
        "level": "danger",
        "title": "Extreme Heat Stress Advisory",
        "alerts": [
            "Mandatory hydration: 1 litre cool water per worker per hour — no exceptions.",
            "Reschedule heavy manual work to before 10:00 AM and after 4:00 PM IST.",
            "Set up shaded rest stations every 200 m; enforce 15-min breaks every 90 min.",
            "Monitor concrete curing — heat accelerates evaporation; apply curing compound within 20 min of finishing.",
            "Station first-aid responders trained in heat stroke; keep ORS and ice packs on site.",
            "Halt all operations if WBGT exceeds 35°C per ACGIH TLV guidelines."
        ]
    },
    "Normal Conditions": {
        "icon": "☀️",
        "level": "success",
        "title": "Standard Operations — All Clear",
        "alerts": [
            "Normal site operations approved — run standard pre-shift safety toolbox talk.",
            "Verify daily checklist: PPE compliance, equipment pre-use inspection, task hazard analysis.",
            "Enforce baseline PPE: hard hat, high-vis vest, steel-toe boots for all personnel.",
            "Proceed with concrete pours, structural works, and equipment per approved method statements.",
            "Good curing conditions — maintain moist curing ≥ 7 days for OPC (IS 456).",
            "Schedule inspections, quality audits, and subcontractor coordination meetings."
        ]
    }
}

STRUCTURE_COSTS = {
    # Keys must match <select> option values in frontend/index.html
    "Residential Villa (G+1)":          {"base_cost": 1800, "steel_kg": 4.5,  "cement_bags": 0.42},
    "Residential Apartment (G+4)	":    {"base_cost": 2100, "steel_kg": 5.8,  "cement_bags": 0.55},
    "Residential Apartment (G+4)":      {"base_cost": 2100, "steel_kg": 5.8,  "cement_bags": 0.55},
    "Residential House":                {"base_cost": 1800, "steel_kg": 4.5,  "cement_bags": 0.42},
    "Commercial Office (G+10)	":       {"base_cost": 2800, "steel_kg": 7.2,  "cement_bags": 0.68},
    "Commercial Office (G+10)":         {"base_cost": 2800, "steel_kg": 7.2,  "cement_bags": 0.68},
    "Industrial Warehouse":             {"base_cost": 1400, "steel_kg": 6.5,  "cement_bags": 0.38},
    "Infrastructure Bridge":            {"base_cost": 4200, "steel_kg": 12.0, "cement_bags": 0.95},
}

TIER_MULTIPLIERS = {
    # Keys must match <select> option values in frontend/index.html
    "Tier 1 (Mumbai/Delhi/Bangalore)":  {"cost": 1.35, "market": 1.55},
    "Tier 2 (Pune/Hyderabad/Chennai)":  {"cost": 1.15, "market": 1.30},
    "Tier 3 (Other Cities)":            {"cost": 1.00, "market": 1.10},
    # Aliases for alternate labels the frontend may send
    "Tier-1 Metro (Delhi/Mumbai/Bangalore)": {"cost": 1.35, "market": 1.55},
    "Tier-2 City (Pune/Hyderabad/Chennai)":  {"cost": 1.15, "market": 1.30},
    "Tier-3 / Small City":                   {"cost": 1.00, "market": 1.10},
}
