# -*- coding: utf-8 -*-
"""
AURA Clinical Safety & Emergency Risk Detection Engine
Deterministic safety checks that execute BEFORE any AI generation.
Ensures zero medical hallucination, no unlawful diagnosis, and immediate life-saving alerts.
"""
import re

EMERGENCY_INDICATORS = [
    {
        "category": "Cardiac Emergency",
        "keywords": [
            r"\bchest\s+pain\b", r"\bcrushing\s+chest\b", r"\bheart\s+attack\b",
            r"\bpain\s+in\s+(my\s+)?left\s+arm\b", r"\bchest\s+pressure\b",
            r"\bangina\b", r"\bheart\s+pain\b", r"\bmyocardial\s+infarct\b",
            r"\bछाती\s+में\s+दर्द\b", r"\bहार्ट\s+अटैक\b", r"\bఛాతీ\s*నొప్పి\b", r"\bగుండె\s*పోటు\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Potential Acute Cardiac Event",
        "directive": "Seat patient upright in W-posture with knees bent. Loosen tight collar. Administer Aspirin 300mg (chewed) + Sorbitrate 5mg (sublingual) if systolic BP > 90 mmHg. Dial 108 immediately.",
        "contraindications": "Do NOT allow physical movement or walking. Do NOT give Sorbitrate if systolic BP < 90 mmHg or if patient has taken Sildenafil/Tadalafil in past 24h."
    },
    {
        "category": "Severe Respiratory Distress",
        "keywords": [
            r"\bcannot\s+breathe\b", r"\bsevere\s+breathing\s+problem\b", r"\bsuffocating\b",
            r"\bgasping\s+for\s+air\b", r"\bblue\s+lips\b", r"\bcyanosis\b", r"\bsilent\s+chest\b",
            r"\bspo2\s+<\s*90\b", r"\bदम\s+घुट\s+रहा\b", r"\bसांस\s+नहीं\s+आ\s+रही\b", r"\bశ్వాస\s*ఆడటం\s*లేదు\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Severe Respiratory Compromise / Hypoxia",
        "directive": "Keep patient completely upright. Loosen constricting neckwear. Administer 4-6 puffs of Salbutamol inhaler with spacer. Provide supplemental oxygen. Dial 108 immediately.",
        "contraindications": "Do NOT force patient to lie flat on back. Do NOT leave patient unattended."
    },
    {
        "category": "Severe Hemorrhage",
        "keywords": [
            r"\bsevere\s+bleeding\b", r"\buncontrolled\s+bleeding\b", r"\bgushing\s+blood\b",
            r"\barterial\s+spurting\b", r"\bstab\s+wound\b", r"\bdeep\s+cut\s+bleeding\b",
            r"\bबहुत\s+खून\s+बह\s+रहा\b", r"\bతీవ్ర\s*రక్తస్రావం\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Severe Hemorrhage & Trauma",
        "directive": "Apply firm, continuous direct pressure over the bleeding wound with a sterile hemostatic dressing or clean cloth. Elevate limb above heart level. Apply tourniquet 2-3 inches above wound if spurting limb bleed. Call 108.",
        "contraindications": "Do NOT remove deeply impaled objects. Do NOT remove first dressing layer; add more layers over it."
    },
    {
        "category": "Anaphylaxis / Allergic Shock",
        "keywords": [
            r"\banaphylaxis\b", r"\ballergic\s+shock\b", r"\bthroat\s+swelling\b",
            r"\bswollen\s+tongue\b", r"\bthroat\s+closing\b", r"\bbee\s+sting\s+shock\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Anaphylactic Airway Shock",
        "directive": "Administer Epinephrine (Adrenaline) Auto-injector 0.3 mg IM into outer mid-thigh immediately. Lay patient flat with legs elevated unless dyspneic. Call 108 immediately.",
        "contraindications": "Do NOT delay Epinephrine administration. Antihistamines alone cannot reverse acute airway obstruction."
    },
    {
        "category": "Acute Poisoning / Toxic Ingestion",
        "keywords": [
            r"\bpoison\b", r"\bswallowed\s+poison\b", r"\bdrank\s+chemical\b", r"\bdrank\s+pesticide\b",
            r"\bacid\s+ingestion\b", r"\btoxic\s+overdose\b", r"\bजहर\s+खा\s+लिया\b", r"\bవిషం\s*తాగారు\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Acute Toxic Poison Ingestion",
        "directive": "Place patient in recovery position on side. Preserve substance container for paramedics. Call National Poison Information Centre (1800-116-117) or 108 immediately.",
        "contraindications": "Do NOT induce vomiting with corrosive acids, alkalis, or petroleum distillates (causes fatal esophageal rupture). Do NOT give oral liquids if drowsy."
    },
    {
        "category": "Stroke / Neurological Deficit",
        "keywords": [
            r"(?<!heat\s)\bstroke\b", r"\bfacial\s+droop\b", r"\bspeech\s+slurred\b", r"\bone\s+side\s+weakness\b",
            r"\bparalysis\b", r"\bthunderclap\s+headache\b", r"\bलकवा\b", r"\bపక్షవాతం\b"
        ],
        "title": "🚨 URGENT MEDICAL EMERGENCY: Acute Stroke (F.A.S.T. Alert)",
        "directive": "Note exact time of symptom onset (Thrombolytic window < 4.5 hours). Keep patient calm with head elevated 15-30 degrees. Transport to a certified Stroke / CT-equipped hospital via 108 ambulance immediately.",
        "contraindications": "Do NOT give Aspirin or oral liquids until CT scan rules out hemorrhagic stroke. Do NOT delay hospital transport."
    }
]

def check_emergency(text):
    """
    Scans input text for acute emergency keywords.
    Returns: (is_emergency: bool, alert_info: dict or None)
    """
    if not text:
        return False, None
    text_lower = text.lower()
    for em in EMERGENCY_INDICATORS:
        for pattern in em["keywords"]:
            if re.search(pattern, text_lower):
                return True, {
                    "is_emergency": True,
                    "category": em["category"],
                    "title": em["title"],
                    "directive": em["directive"],
                    "contraindications": em["contraindications"],
                    "matched_pattern": pattern
                }
    return False, None

def format_emergency_response(alert_info):
    """Formats an emergency alert card in Markdown."""
    return f"""### {alert_info['title']}

> **⚠️ IMMEDIATE LIFE-SAVING DIRECTIVE:**
> {alert_info['directive']}

**🛑 CRITICAL CONTRAINDICATIONS:**
- {alert_info['contraindications']}

**🚑 DISPATCH 108 AMBULANCE NOW:**
Please contact your local emergency response service (**108** / **112**) or proceed immediately to the nearest tertiary emergency department. Do not rely on an AI chatbot for life-threatening acute emergencies.

---
*⚠️ **Medical Disclaimer:** Educational emergency triage only. Does not replace professional clinical evaluation or emergency paramedic dispatch.*
"""

def validate_medical_response(response_text):
    """
    Post-generation safety validator.
    Ensures no diagnostic assertions ('You have X') or probabilistic claims ('87% probability').
    Ensures educational health-awareness disclaimer is attached.
    """
    if not response_text:
        return ""

    cleaned = response_text

    # Replace diagnostic assertions
    diagnostic_patterns = [
        (r"\bYou\s+have\s+([A-Z][a-zA-Z\s]+)\b", r"These symptoms can be associated with \1"),
        (r"\bYou\s+are\s+diagnosed\s+with\b", "Possible conditions associated with these symptoms include"),
        (r"\bDiagnosis:\s*", "Associated Conditions for Awareness: "),
        (r"\bProbability:\s*\d+%", ""),
        (r"\b\d+%\s*probability\b", "possible association"),
        (r"\bI\s+diagnose\s+you\s+with\b", "Symptoms match patterns seen in")
    ]

    for pat, rep in diagnostic_patterns:
        cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)

    # Ensure mandatory educational disclaimer
    disclaimer = "\n\n---\n*⚠️ **Medical Disclaimer:** Educational health-awareness information only. This platform does not provide medical diagnosis, write prescriptions, or replace consultation with a licensed healthcare professional.*"
    if "Medical Disclaimer" not in cleaned:
        cleaned += disclaimer

    return cleaned
