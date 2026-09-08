<div align="center">

# 🥼 AURA AI Platform
### **AI-Driven Public Health Chatbot for Disease Awareness & Predictive Screening**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Framework - Flask](https://img.shields.io/badge/Framework-Flask_2.x-lightgrey.svg?logo=flask)](https://flask.palletsprojects.com/)
[![ML - Scikit--Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![Edge AI - 100% Offline](https://img.shields.io/badge/Architecture-100%25_Offline_Zero--Cloud-emerald.svg)](#)
[![Languages - EN | HI | TE](https://img.shields.io/badge/Multilingual-English_%7C_हिन्दी_%7C_తెలుగు-teal.svg)](#)
[![Smart India Hackathon 2026](https://img.shields.io/badge/Initiative-Smart_India_Hackathon_2026-amber.svg)](#)

<p align="center">
  <strong>Developed by Pallavi Sowreddi</strong> (B.Tech Student)<br>
  <em>Smart India Hackathon (SIH) 2026 Edition • Project Expo</em>
</p>

</div>

---

## 📖 Executive Summary

**AURA (Automated Universal Relief & Assessment)** is a clinical-grade, offline-first public health platform engineered to deliver rapid disease screening, preventative awareness, digital lab report biomarker analysis, and emergency triage to populations in remote, rural, disaster-struck, or air-gapped environments without any cloud dependency, WiFi, or external APIs.

By coupling calibrated **Random Forest decision models** with **clinical hallmark heuristics**, **edge computer vision**, and **OCR biomarker parsing**, AURA empowers patients and primary healthcare workers (PHCs / ASHA workers) with instant clinical guidance in their regional languages (**English**, **हिन्दी**, and **తెలుగు**).

---

## 🏛️ Project Expo: 4-Part Architectural Framework

For jury evaluation and project demonstrations, AURA's innovations are structured into **four distinct engineering pillars**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AURA AI PLATFORM                              │
├────────────────────├────────────────────├───────────────────────├──────────┐
│      PART 1        │      PART 2        │      PART 3       │  PART 4   │
│   Multilingual     │   Edge Vision &    │ Preventive Health │ Zero-Cloud│
│   Hybrid Clinical  │   Lab Biomarker    │  Telemetry & NIS  │ Privacy & │
│      AI & XAI      │     Analyzer       │ Vaccine Schedules │  SOS Fast │
└────────────────────┴────────────────────┴───────────────────────┴──────────┘
```

### 🔹 PART 1: Multilingual Hybrid Clinical AI & Explainable Telemetry
* **Core Problem**: Cloud LLMs require high-bandwidth connectivity, suffer from clinical hallucination, and fail in rural network dark-zones.
* **Our Solution**:
  * Dual-layer diagnostic engine: Scikit-learn **Random Forest Classifier** blended with clinical hallmark heuristics, symptom specificity weighting, and dynamic threshold safeguards.
  * Native tri-lingual NLP tokenization for **English**, **Hindi (हिन्दी)**, and **Telugu (తెలుగు)**.
  * **Explainable AI (XAI)** telemetry sidebar featuring live circular progress gauges, differential diagnostics HTML5 canvas charts, decoded symptom tag clouds, and feature importance weight distributions.
  * Built-in red-flag emergency detection (e.g. stroke F.A.S.T protocol, heart attack pain, cholera crisis).

### 🔹 PART 2: Edge Vision Pathology Scanner & Digital Lab Report Analyzer
* **Core Problem**: Patients in rural areas cannot interpret complex pathological laboratory sheets or access certified dermatologists.
* **Our Solution**:
  * **Visual Skin Pathology Scanner**: Fast edge texture and color gradient classifier (RGB/HSV channel variances, redness density profile, surface irregularity) for immediate screening of eczema, psoriasis, acne, and rash.
  * **Digital Lab Report Biomarker Analyzer**: RapidOCR document entity extractor parsing Complete Blood Counts (CBC), fasting glucose, HbA1c, liver function tests (LFT: Bilirubin, SGPT/ALT, SGOT/AST), and lipid profiles with reference-range color coding.

### 🔹 PART 3: Preventative Health Telemetry, Vitals Simulator & Vaccine Schedules
* **Core Problem**: Healthcare systems are reactive rather than preventative; citizens lack accessible immunization tracking.
* **Our Solution**:
  * **Clinical Telemetry & Vitals Simulator**: Animated real-time SVG ECG waveform monitor, systolic/diastolic blood pressure percentile classification, oxygen saturation (SpO2), and overall Composite Health Score.
  * **Universal Immunization Life-Course Matrix**: National Immunization Schedule (NIS) & WHO life-course vaccine registry with age-band filtering (Birth, 6-14 Weeks, 9-12 Months, Childhood, Adults) and one-click printable vaccine cards.
  * **Medication Reminders**: Offline browser scheduling with dosage chimes and persistent local queueing.

### 🔹 PART 4: Zero-Cloud Privacy Sandbox & Acute Emergency SOS Protocols
* **Core Problem**: Centralized health clouds leak sensitive patient telemetry and fail during network infrastructure outages.
* **Our Solution**:
  * **Client-Side Cryptographic Security**: SHA-256 password hashing and on-device private biometric storage. Zero personal data leaves the local sandbox.
  * **Acute Emergency & Toxicology Triage**: Life-saving protocols for snake bites, animal/rabies bites, burns, and scorpion stings with clear *"DOs and STRICT DO NOTs"*.
  * **1-Click SOS Dispatch**: Instant direct call triggers for national helplines (**108** Ambulance, **112** Emergency, **102** Maternity, **104** Health Advice, **1098** Childline).
  * **Mindful 4-7-8 Breathing Overlay**: Interactive parasympathetic nervous system regulator to calm patient anxiety and reduce heart rate during acute distress.

---

## 🛠️ Technology Stack & Edge Specifications

| Layer | Technologies Used |
| :--- | :--- |
| **Backend Core** | Python 3.10+, Flask 2.x Microframework |
| **Machine Learning** | `scikit-learn` (Random Forest Classifiers), `numpy`, `pandas`, `scipy` |
| **Computer Vision** | `OpenCV` (cv2), `Pillow` (PIL) for epidermal RGB/HSV and texture gradient matrix |
| **OCR Document Parsing**| `RapidOCR` with ONNX Runtime for edge text recognition |
| **Frontend Architecture** | Modern Vanilla JavaScript (ES6+), HTML5 Canvas 2D, Responsive CSS3 Glassmorphism |
| **Voice Interaction** | Web Speech API (Native on-device Speech-to-Text & Speech Synthesis) |
| **Data & Storage** | LocalStorage sandbox, Cryptographic SHA-256 WebCrypto hashing |
| **Operating System** | Platform-agnostic (Windows, Linux, macOS, Raspberry Pi edge devices) |

---

## 📂 Repository Directory Structure

```text
AURA-Platform/
├── models/                         # Serialized edge ML decision models
│   ├── symptom_model.pkl           # Random Forest clinical symptom classifier
│   ├── symptoms_list.pkl           # Vectorized symptom dictionary headers
│   └── image_model.pkl             # Skin pathology classifier model
├── static/
│   ├── css/
│   │   └── style.css               # Clinical glassmorphic design system
│   ├── js/
│   │   └── app.js                  # Speech engine, telemetry, canvas charts & state
│   └── assets/                     # Sample clinical test images & presets
├── templates/
│   ├── index.html                  # Main unified single-page application
│   ├── login.html                  # Dedicated clinician & patient sign-in portal
│   └── signup.html                 # Offline digital health card registration
├── app.py                          # Flask routing, multi-tier NLP & diagnostic endpoints
├── model_helper.py                 # ML inference, RapidOCR parsing, hallmark clinical rules
├── train_models.py                 # Synthetic dataset generator & model trainer
├── requirements.txt                # Python dependencies
├── run.bat                         # 1-Click Windows launch script
└── README.md                       # Comprehensive platform documentation
```

---

## 🚀 Quickstart & Installation

### Option 1: One-Click Launch (Windows)
Double-click `run.bat`. The script will automatically:
1. Initialize a Python virtual environment (`.venv`).
2. Install all required dependencies.
3. Verify or train edge ML models.
4. Launch the local Flask server on `http://127.0.0.1:5000/`.
5. Open your default web browser automatically.

### Option 2: Manual Terminal Setup
```bash
# 1. Clone the repository
git clone https://github.com/pallavisowreddi/AURA-Offline-AI-Health-Platform.git
cd AURA-Offline-AI-Health-Platform

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train or verify edge models (takes < 10 seconds)
python train_models.py

# 5. Start the AURA application
python app.py
```
Open **`http://127.0.0.1:5000`** in any web browser.

---

## 🧪 Demonstration & Jury Evaluation Guide

To test AURA's offline capabilities during an evaluation or expo:

1. **Disconnect Internet**: Turn off Wi-Fi or unplug your ethernet cable. Notice that AURA continues operating seamlessly.
2. **Clinical Symptom Query**:
   * Navigate to **Disease Prediction**.
   * Type or speak: *"I have high fever, joint pain, and red skin rashes."*
   * Observe **Dengue Fever** identified with calibrated confidence, clinical care directives, and animated Differential Diagnostics canvas.
3. **Regional Language Switching**:
   * Switch the top navbar language pill to **हिन्दी** or **తెలుగు**.
   * Notice immediate UI translation and clinical response generation in regional scripts.
4. **Digital Lab Report Analysis**:
   * Navigate to **Medical Reports** → **Digital Lab Report Biomarker Analyzer**.
   * Click **Load Dengue Suspect Preset** or upload a clinical CBC sheet.
   * Observe instant extraction of Platelets (62,000 /µL CRITICAL LOW), Hematocrit (52% HIGH), and WBC (2,800 /µL LOW) with clinical interpretation.
5. **Visual Skin Lesion Scanner**:
   * In **Medical Reports**, drag and drop a skin image or select a preset.
   * Observe the visual laser scanning effect and edge classification breakdown.

---

## ⚖️ Clinical Safety & Disclaimer

AURA is an educational public health screening tool designed for initial triage and awareness. It is engineered to adhere to public health safety guidelines by highlighting conservative recommendations, red-flag urgent warnings, and advising consultation with certified medical professionals. It does not replace definitive clinical pathology or physician diagnoses.

---

<div align="center">
  <strong>© 2026 AURA Platform • Smart India Hackathon Edition</strong><br>
  <em>Developed by Pallavi Sowreddi (B.Tech Student)</em>
</div>
