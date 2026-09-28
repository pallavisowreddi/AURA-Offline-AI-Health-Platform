<div align="center">

# 🥼 AURA HealthAware AI
### **AI-Driven Public Health Awareness Assistant & 100% Offline Clinical Platform**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Framework - Flask](https://img.shields.io/badge/Framework-Flask_3.x-lightgrey.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Local Database - SQLite](https://img.shields.io/badge/Database-SQLite_Local-003B57.svg?logo=sqlite&logoColor=white)](#)
[![Retrieval - Local RAG](https://img.shields.io/badge/AI_Engine-Local_Semantic_RAG-emerald.svg)](#)
[![Edge AI - 100% Offline](https://img.shields.io/badge/Architecture-100%25_Offline_Zero--Cloud-brightgreen.svg)](#)
[![Languages - EN | HI | TE](https://img.shields.io/badge/Multilingual-English_%7C_हिन्दी_%7C_తెలుగు-teal.svg)](#)
[![Smart India Hackathon 2026](https://img.shields.io/badge/Initiative-Smart_India_Hackathon_2026-amber.svg)](#)

<p align="center">
  <strong>Developed by Pallavi Sowreddi</strong> (B.Tech Student)<br>
  <em>Smart India Hackathon (SIH) 2026 Edition • Project Expo</em>
</p>

</div>

---

## 🟢 OFFLINE ARCHITECTURE OVERVIEW

> **IMPORTANT PRINCIPLE:**  
> **No Internet → No Cloud API Calls → No Remote LLMs → No External Database Required.**  
> AURA runs **100% locally** on standard consumer laptop/PC hardware.

```
                      USER
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Interactive Web Interface   │
        │   HTML5 / CSS3 / Vanilla JS   │
        └───────────────┬───────────────┘
                        │ HTTP (localhost)
                        ▼
        ┌───────────────────────────────┐
        │       Flask Backend API       │
        │     Query Pre-processing      │
        └───────────────┬───────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌────────────────────────┐    ┌────────────────────────┐
│  Emergency Safety      │    │  Local RAG Engine      │
│  Shield (Pre-RAG)      │    │  TF-IDF Vector Space   │
│  Deterministic Rules   │    │  Cosine Similarity     │
└───────────────┬────────┘    └────────────┬───────────┘
                │                          │
                ▼                          ▼
┌────────────────────────┐    ┌────────────────────────┐
│  Emergency Triage Card │    │  Local Knowledge Base  │
│  Golden Hour Directives│    │  SQLite (aura_health)  │
│  108 Hospital Dispatch │    │  22+ Diseases / 52+ Sym│
└───────────────┬────────┘    └────────────┬───────────┘
                │                          │
                ▼                          ▼
        ┌───────────────────────────────┐
        │  Grounded Clinical Synthesizer│
        │  Safe Health Awareness Card   │
        │  + Anti-Diagnosis Validator   │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │    Persistent Chat History    │
        │   SQLite Local Conversations  │
        └───────────────────────────────┘
```

---

## 🌟 Key Upgraded Features

### 1. 🧠 Local RAG (Retrieval-Augmented Generation)
* **Zero Cloud Dependency**: Operates entirely offline using Scikit-Learn TF-IDF vectorizers and cosine similarity over a verified clinical knowledge base.
* **Grounded Responses**: Generates structured **Health Awareness Cards** (Overview, Common Symptoms, Causes, Transmission, Prevention, Warning Signs, and When to Seek Medical Care) with source attribution:
  `Information Source: Local Health Knowledge Base → Diseases → Dengue Fever`
  `Confidence: High (Verified Local Knowledge Base)`
* **Local LLM Ready**: Supports automatic pass-through to locally running Ollama or llama.cpp instances (`http://127.0.0.1:11434`) when present, with seamless fallback to built-in grounded synthesis.

### 2. 🛡️ Deterministic Emergency Safety Shield
* Scans inputs **before** any AI generation for acute life-threatening emergencies (crushing chest pain, severe dyspnea/hypoxia, severe arterial bleeding, anaphylactic airway shock, acute poison ingestion, stroke F.A.S.T.).
* Displays prominent **Urgent Medical Attention** directives with Golden Hour life-saving measures, critical contraindications (e.g. avoid nitrates if systolic BP < 90 mmHg), and direct 108 ambulance dispatch.

### 3. ⚖️ Symptom Awareness (Strictly Non-Diagnostic)
* Adheres strictly to WHO and medical AI guidelines: **Never claims to diagnose diseases or output false certainty probabilities** (e.g. *"You have Dengue with 87% probability"*).
* Instead correlates symptoms: *"These symptoms may occur in several conditions, including Dengue, Viral Fever, and Chikungunya. This tool is for educational awareness and does not diagnose disease. Please consult a physician."*

### 4. 🗄️ Local SQLite Database (`data/aura_health.db`)
* **Tables**:
  * `conversations`: ID, Title, Timestamps
  * `messages`: Conversation ID, Role (user/assistant), Content, Timestamp, Metadata
  * `diseases`: ID, Name, Category, Overview, Causes, Transmission, Prevention, Warning Signs, Raw JSON
  * `symptoms`: ID, Name, Category, Description, Warning Level, Raw JSON
  * `disease_symptoms`: Junction table for relational querying
  * `knowledge_documents`: 93+ indexed chunks for vector retrieval
  * `settings`: Offline configurations and theme preferences
* **Chat History Persistence**: Create new consultations, switch between previous sessions, or delete sessions locally.

### 5. 🦠 Disease Awareness Library
* Searchable directory of **22+ verified diseases** filterable by category:
  * 🦟 **Vector-Borne**: Dengue Fever, Malaria
  * 🦠 **Infectious**: Tuberculosis, Chickenpox, Measles, Food Poisoning, Hepatitis B
  * 🫁 **Respiratory**: COVID-19, Influenza, Bronchial Asthma, Pneumonia, Common Cold
  * ❤️ **Chronic / Metabolic**: Type 2 Diabetes, Hypertension, Anemia, Chronic Kidney Disease, Migraine
  * 💧 **Water-Borne**: Typhoid Fever, Cholera, Hepatitis A
  * 🥗 **Lifestyle**: GERD (Acid Reflux), Dehydration & Heat Exhaustion
* Interactive modal displaying complete pathophysiology, prevention, warning signs, and FAQs.

### 6. 🔍 Symptom Explorer
* Directory of **52+ categorized symptoms** with multi-select toggle pills.
* Instant non-diagnostic correlation analysis mapping symptom clusters to potential medical conditions with red-flag warnings.

### 7. 💡 Preventive Health & Wellness Hub
* Evidence-based guidance across **8 vital health domains**: Mosquito Prevention, Water & Food Hygiene, Hydration, Respiratory Hygiene, Cardiovascular Health, Diabetes & Metabolism, Immunization Defenses, and Sleep/Mental Rest.

### 8. 📶 Bluetooth Smart Health Hub & Water Tracker
* Connects to BLE smartwatches/bands via **Web Bluetooth API** (GATT `0x180D` Heart Rate, `0x1809` Thermometer).
* Built-in **PulseBand Pro 4G BLE Simulator** with Web Audio API cardiac pulse beeps.
* Dynamic AI Hydration Advisor adjusting water targets based on real-time body temperature and heart rate.

### 9. 🏥 Emergency Hub & Medicine Recommender
* Generative AI acute triage assistant with 6 scenario quick pills and free-text symptom analysis.
* First-line emergency medicines (Aspirin + Sorbitrate for cardiac, Salbutamol for asthma, Epinephrine for anaphylaxis) with dosages and contraindications.
* Verified offline hospital directories for **Hyderabad**, **Vijayawada**, **Visakhapatnam**, **Bengaluru**, and **Delhi** with GPS auto-detection.

---

## 📁 Repository Structure

```
.
├── app.py                      # Flask backend API & offline route handlers
├── core/
│   ├── database.py             # SQLite database manager & chat history CRUD
│   ├── safety.py               # Deterministic emergency shield & medical validator
│   ├── rag_engine.py           # Local TF-IDF semantic vector space & RAG generator
│   └── symptom_service.py      # Non-diagnostic symptom awareness correlator
├── data/
│   ├── aura_health.db          # Local SQLite persistent database
│   ├── diseases.json           # 22+ comprehensive disease profiles
│   ├── symptoms.json           # 52+ categorized symptoms
│   ├── health_tips.json        # Categorized prevention guidelines
│   ├── emergency_guidelines.json # Emergency triage and golden hour directives
│   └── faq.json                # Verified public health FAQs
├── static/
│   ├── css/style.css           # Modern healthcare UI styles & responsive cards
│   └── js/app.js               # Client controller (RAG, BLE, Explorer, History, Audio)
├── templates/
│   └── index.html              # Single Page Application viewport tabs
├── tests/
│   └── test_offline_system.py  # 17 unit tests + 20 real-world health queries
├── requirements.txt            # Python dependencies (scikit-learn, flask, etc.)
└── README.md                   # System documentation & offline test guide
```

---

## 🚀 Installation & Running Locally

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Local Offline Server
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```

---

## 🔌 100% Offline Verification Procedure

To verify for project expo juries that AURA operates completely without internet:

1. **Disable all network connections**:
   * Turn off Wi-Fi.
   * Unplug Ethernet cables.
   * Turn off Mobile Hotspots.
2. **Launch the platform**:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000`.
4. Observe the green banner: `🟢 OFFLINE MODE: Local AI • Private • No Internet Required`.
5. In the **AI Chat Assistant**, ask:
   * *"What are the symptoms and prevention for dengue?"*
   * Observe immediate local RAG response with source attribution.
6. Open the **Disease Library** and search for *"Malaria"* or filter by *"Respiratory"*.
7. Open the **Symptom Explorer**, select *"Fever"*, *"Headache"*, and *"Joint Pain"*, and click *"Correlate Symptoms"*.
8. Verify that all features execute with **zero network latency** and **zero external API calls**.

---

## 🧪 Automated Test Suite

Run the full automated test battery (17 unit test cases including 20 sample real-world health queries):

```bash
python tests/test_offline_system.py
```

Expected output:
```
Ran 17 tests in 32.968s
OK
--- Running 20-Query Offline Battery ---
  [✓] Query #01 PASSED: What is dengue?...
  [✓] Query #02 PASSED: What are common symptoms of malaria?...
  [✓] Query #03 PASSED: How can I prevent dengue fever?...
  ...
  [✓] Query #20 PASSED: What are emergency warning signs requiring immediate 108 dispatch?...
```

---

## ⚖️ Academic Disclaimer
*AURA HealthAware AI is an educational public health awareness platform developed for the Smart India Hackathon (SIH) 2026. It does not provide medical diagnosis, write medical prescriptions, or replace consultation with a licensed medical professional.*
