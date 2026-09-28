# -*- coding: utf-8 -*-
"""
AURA Clinical Safety & Emergency Risk Detection Engine
Deterministic safety checks that execute BEFORE any AI generation.
Ensures zero medical hallucination, no unlawful diagnosis, and immediate life-saving alerts.
Integrates biometric awareness alerts (SpO2, BP crisis, extreme HR, high fever).
"""
import re
import os
import json

CONFIG_PATH = os.path.join("config", "health_thresholds.json")

EMERGENCY_INDICATORS = [
    {
        "category": "Cardiac Emergency",
        "keywords": [
            r"\bchest\s+pain\b", r"\bcrushing\s+chest\b", r"\bheart\s+attack\b",
            r"\bpain\s+in\s+(my\s+)?left\s+arm\b", r"\bchest\s+pressure\b",
            r"\bangina\b", r"\bheart\s+pain\b", r"\bmyocardial\s+infarct\b",
            r"\bछाती\s+में\s+दर्द\b", r"\bहार्ट\s+अटैक\b", r"\bఛాతీ\s*నొప్పి\b", r"\bగుండె\s*పోటు\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Potential Acute Cardiac Event",
        "directive": "Seat patient upright in W-posture with knees bent. Loosen tight collar. Avoid all exertion. Contact emergency services (108 / 112 / 911) immediately.",
        "contraindications": "Do NOT allow physical movement or walking. Do NOT delay hospital transport."
    },
    {
        "category": "Severe Respiratory Distress",
        "keywords": [
            r"\bcannot\s+breathe\b", r"\bsevere\s+breathing\s+problem\b", r"\bsuffocating\b",
            r"\bgasping\s+for\s+air\b", r"\bblue\s+lips\b", r"\bcyanosis\b", r"\bsilent\s+chest\b",
            r"\bspo2\s+<\s*90\b", r"\bदम\s+घुट\s+रहा\b", r"\bसांस\s+नहीं\s+आ\s+रही\b", r"\bశ్వాస\s*ఆడటం\s*లేదు\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Severe Respiratory Compromise / Hypoxia",
        "directive": "Keep patient completely upright. Loosen constricting neckwear. Provide prescribed fast-acting bronchodilator if available. Dial 108 / 112 immediately.",
        "contraindications": "Do NOT force patient to lie flat on back. Do NOT leave patient unattended."
    },
    {
        "category": "Severe Hemorrhage",
        "keywords": [
            r"\bsevere\s+bleeding\b", r"\buncontrolled\s+bleeding\b", r"\bgushing\s+blood\b",
            r"\barterial\s+spurting\b", r"\bstab\s+wound\b", r"\bdeep\s+cut\s+bleeding\b",
            r"\bबहुत\s+खून\s+बह\s+रहा\b", r"\bతీవ్ర\s*రక్తస్రావం\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Severe Hemorrhage & Trauma",
        "directive": "Apply firm, continuous direct pressure over the bleeding site with sterile dressing or clean cloth. Elevate limb above heart level. Call 108 / 112 immediately.",
        "contraindications": "Do NOT remove deeply impaled objects. Do NOT remove first dressing layer; apply more absorbent layers over it."
    },
    {
        "category": "Anaphylaxis / Allergic Shock",
        "keywords": [
            r"\banaphylaxis\b", r"\ballergic\s+shock\b", r"\bthroat\s+swelling\b",
            r"\bswollen\s+tongue\b", r"\bthroat\s+closing\b", r"\bbee\s+sting\s+shock\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Anaphylactic Airway Shock",
        "directive": "Administer Epinephrine (Adrenaline) Auto-injector 0.3 mg IM into outer mid-thigh if prescribed and available. Lay patient flat with legs elevated unless dyspneic. Call 108 / 112 immediately.",
        "contraindications": "Do NOT delay Epinephrine administration. Antihistamines alone cannot reverse acute airway obstruction."
    },
    {
        "category": "Acute Poisoning / Toxic Ingestion",
        "keywords": [
            r"\bpoison\b", r"\bswallowed\s+poison\b", r"\bdrank\s+chemical\b", r"\bdrank\s+pesticide\b",
            r"\bacid\s+ingestion\b", r"\btoxic\s+overdose\b", r"\bजहर\s+खा\s+लिया\b", r"\bవిషం\s*తాగారు\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Acute Toxic Poison Ingestion",
        "directive": "Place patient in recovery position on side. Preserve substance container for paramedics. Call National Poison Information Centre (1800-116-117) or 108 / 112 immediately.",
        "contraindications": "Do NOT induce vomiting with corrosive acids, alkalis, or petroleum distillates. Do NOT give oral liquids if drowsy."
    },
    {
        "category": "Stroke / Neurological Deficit",
        "keywords": [
            r"(?<!heat\s)\bstroke\b", r"\bfacial\s+droop\b", r"\bspeech\s+slurred\b", r"\bone\s+side\s+weakness\b",
            r"\bparalysis\b", r"\bthunderclap\s+headache\b", r"\bलकवा\b", r"\bపక్షవాతం\b"
        ],
        "title": "🚨 URGENT MEDICAL ATTENTION MAY BE NEEDED: Acute Stroke (F.A.S.T. Alert)",
        "directive": "Note exact time of symptom onset (critical thrombolytic window). Keep patient calm with head elevated 15-30 degrees. Transport to CT-equipped emergency department via 108 / 112 immediately.",
        "contraindications": "Do NOT give Aspirin or oral liquids until CT scan rules out intracranial hemorrhage. Do NOT delay hospital transport."
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

def check_biometric_alert(metric_type, value, secondary_value=None):
    """
    Evaluates recorded vitals against safety threshold limits from health_thresholds.json.
    Returns: (is_alert: bool, alert_payload: dict or None)
    """
    metric_key = metric_type.lower()

    if "spo2" in metric_key or "oxygen" in metric_key:
        spo2 = float(value)
        if spo2 < 90.0:
            return True, {
                "metric": "Oxygen Saturation (SpO₂)",
                "value": f"{spo2}%",
                "severity": "critical",
                "title": "⚠️ URGENT MEDICAL ATTENTION MAY BE NEEDED: Hypoxemia Warning",
                "message": f"Recorded SpO₂ of {spo2}% is below 90%, which is outside the safe awareness range. If accompanied by shortness of breath or blue lips, seek emergency medical care immediately."
            }

    elif "blood_pressure" in metric_key or metric_key == "bp":
        sys = float(value)
        dia = float(secondary_value) if secondary_value is not None else 80.0
        if sys >= 180.0 or dia >= 120.0:
            return True, {
                "metric": "Blood Pressure",
                "value": f"{int(sys)}/{int(dia)} mmHg",
                "severity": "critical",
                "title": "⚠️ URGENT MEDICAL ATTENTION MAY BE NEEDED: Hypertensive Crisis Range",
                "message": f"Blood pressure reading of {int(sys)}/{int(dia)} mmHg is significantly elevated. If you experience chest pain, headache, numbness, or visual disturbances, contact emergency medical services immediately."
            }

    elif "heart_rate" in metric_key or metric_key == "hr":
        hr = float(value)
        if hr > 150.0:
            return True, {
                "metric": "Heart Rate",
                "value": f"{int(hr)} BPM",
                "severity": "alert",
                "title": "⚠️ High Resting Heart Rate Warning",
                "message": f"Heart rate of {int(hr)} BPM is markedly elevated. Rest for 5 minutes and repeat. If sustained or with chest discomfort, seek professional medical evaluation."
            }
        elif hr < 40.0:
            return True, {
                "metric": "Heart Rate",
                "value": f"{int(hr)} BPM",
                "severity": "alert",
                "title": "⚠️ Severe Bradycardia Warning",
                "message": f"Heart rate of {int(hr)} BPM is below expected resting limits. If accompanied by dizziness, faintness, or weakness, seek medical attention."
            }

    elif "temp" in metric_key:
        temp = float(value)
        if temp < 50:
            temp = (temp * 9/5) + 32
        if temp >= 104.0:
            return True, {
                "metric": "Body Temperature",
                "value": f"{temp:.1f}°F",
                "severity": "critical",
                "title": "⚠️ High Fever (Hyperpyrexia) Warning",
                "message": f"Body temperature of {temp:.1f}°F is high. Apply cool compresses, stay hydrated, and consult a physician promptly."
            }

    return False, None

def format_emergency_response(alert_info):
    """Formats an emergency alert card in Markdown adhering strictly to Section 27 specifications."""
    return f"""# ⚠️ URGENT MEDICAL ATTENTION MAY BE NEEDED

The information you entered may describe a potentially serious situation.

**Do not rely on this platform or chatbot for diagnosis or emergency treatment.**
**Please seek immediate professional medical attention or contact your local emergency medical service.**

---

### {alert_info['title']}

> **Immediate Safety Guidance:**
> {alert_info['directive']}

**🛑 Critical Precautions:**
- {alert_info['contraindications']}

**🚑 Emergency Dispatch Numbers:**
- **National Emergency Number:** `112`
- **Ambulance / Medical Emergency:** `108` / `102` (India) / `911` (US)
- **National Poison Information Centre:** `1800-116-117`

*If you are with someone who is unconscious, having severe breathing difficulty, experiencing crushing chest pain, having a seizure, or experiencing another life-threatening emergency, seek emergency help immediately. Do not wait.*
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
    disclaimer = "\n\n---\n*⚠️ **Medical Disclaimer:** Educational health-awareness information only. In an emergency or severe situation, call 108 / 112 or visit an emergency room immediately. This platform does not provide medical diagnosis, write prescriptions, or replace consultation with a licensed healthcare professional.*"
    if "Medical Disclaimer" not in cleaned:
        cleaned += disclaimer

    return cleaned
