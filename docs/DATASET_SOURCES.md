# Dataset Provenance & Data Architecture

This document outlines the three benchmark datasets utilized across the **AURA Offline AI Health Platform**, their licensing, purpose, limitations, and processing pipelines. In strict compliance with medical ethics and academic transparency, data sources are explicitly segregated and labeled.

---

## Summary Matrix

| Dataset Category | Dataset Name | Primary Purpose | Record Count | Features / Dimensions | Nature of Data | Storage Path |
|---|---|---|---|---|---|---|
| **Dataset A** | Disease Symptom Prediction Dataset | Multi-class Disease Prediction from Symptoms | 6,800 records (34 classes) | 67 binary symptom indicators + 1 disease target | Curated Clinical Association Matrix | `data/disease_prediction/` |
| **Dataset B** | IoMT Dataset for ML-Based Health Monitoring | Biometric Analytics, Anomaly & Trend Detection | 50,000 records | HR, SpO₂, Systolic/Diastolic BP, Temp, Sensor Quality, Fall Risk | Synthetic / Physiological Simulation | `data/iomt_vitals/` |
| **Dataset C** | MedQuAD (Medical Question Answering Dataset) | Offline RAG & Health Education Knowledge Retrieval | 18 curated high-yield clinical Q&A modules | Topic, Question, Answer, Focus, Category, Source Authority | NIH / NLM Curated Medical Q&A | `data/medquad/` |

---

## 1. Dataset A — Disease Symptom Prediction

- **Resource & Citation**: [Kaggle Disease Type Prediction using Symptoms](https://www.kaggle.com/code/naga26/disease-type-prediction-using-symptoms) / Columbia University Disease Symptom Ontology.
- **Purpose**: Trains offline multi-class classifiers to estimate condition possibilities from selected symptoms.
- **Record Count**: 6,800 samples across 34 distinct infectious and chronic disease classes (200 balanced samples per class).
- **Features Used**:
  - 67 binary features (0 = absent, 1 = present) including `fever`, `high_fever`, `fatigue`, `chills`, `cough`, `shortness_of_breath`, `chest_pain`, `joint_pain`, `headache`, `nausea`, `vomiting`, `skin_rash`, etc.
  - Target label: `disease` (34 classes).
- **License**: Open Database License (ODbL) / Public Academic Domain.
- **Nature of Data**: Curated symptom co-occurrence matrix based on public health diagnostic criteria.
- **Preprocessing Performed**:
  - Null check and deduplication validation.
  - Stratified 80/20 train/test split.
  - Multi-model evaluation across Logistic Regression, Random Forest, Decision Tree, Naive Bayes, and SVM.
  - Artifact export: `model.pkl`, `label_encoder.pkl`, `feature_names.pkl`, `metrics.json`.
- **Known Limitations**:
  - Models co-occurrence patterns, not patient genetics or chronological severity.
  - Strictly non-diagnostic; intended solely for triage awareness and educational risk evaluation.

---

## 2. Dataset B — IoMT Vital Signs Benchmark Dataset

- **Resource & Citation**: [Kaggle IoMT Dataset for ML-Based Health Monitoring (dsv/7736523)](https://www.kaggle.com/dsv/7736523).
- **Purpose**: Serves as the statistical baseline for vital-sign analytics, anomaly detection, moving averages, and local testing of the Live Health monitoring pipeline.
- **Record Count**: 50,000 records spanning multi-day continuous intervals.
- **Features**:
  - `heart_rate_bpm`: 35 to 210 BPM.
  - `spo2_percent`: 70.0% to 100.0%.
  - `systolic_bp_mmhg`: 75 to 220 mmHg.
  - `diastolic_bp_mmhg`: 45 to 135 mmHg.
  - `temperature_fahrenheit`: 94.0°F to 106.0°F (canonical Celsius stored internally).
  - `signal_quality`: Categorical (`Good`, `Moderate`, `Poor`).
  - `fall_detected`: Binary accelerometer IoMT sensor trigger (0 or 1).
  - `anomaly_flag`: Binary ground-truth flag (0 = normal, 1 = acute variation).
  - `source_type`: Fixed as `DATASET`.
- **License**: CC BY-NC-SA 4.0.
- **Nature of Data**: Synthetically modeled based on published physiological distributions (AHA, WHO, CDC).
- **Known Limitations**:
  - Not derived from actual human clinical trials; used strictly for algorithmic evaluation and pipeline stress-testing.

---

## 3. Dataset C — MedQuAD (Medical Question Answering Dataset)

- **Resource & Citation**: NIH / National Library of Medicine (NLM) MedQuAD Dataset.
- **Purpose**: Powers the local vector retrieval (RAG) and disease overview cards for offline health education.
- **Storage Format**: `data/medquad/medquad_rag_knowledge.json`.
- **Fields**: `id`, `topic`, `question`, `answer`, `category`, `focus`, `source`.
- **License**: Public Domain (NIH / US Government Work).
- **Nature of Data**: Authoritative clinical Q&A curated from official health institutions (CDC, WHO, NIH, AHA, NHLBI).
- **Known Limitations**:
  - General health information only; cannot evaluate personalized clinical presentations.

---

## 4. Strict Medical Data Provenance & Segregation Policy

To prevent false claims and protect user trust, the platform enforces 4 immutable data provenance categories:

1. `REAL_DEVICE`: Live readings streamed from verified Bluetooth/BLE hardware (e.g., GATT Heart Rate `0x180D`, Blood Pressure `0x1810`, Thermometer `0x1809`, Pulse Oximeter `0x1822`).
2. `SIMULATED`: Real-time generated data from the local BLE Simulator when physical hardware is not connected. Always accompanied by the prominent banner: `⚠️ DEMO DATA — NOT A REAL MEASUREMENT`.
3. `MANUAL_ENTRY`: User-inputted biometric readings entered via the **Log Biometrics & BP** interface.
4. `DATASET`: Offline benchmark data used for ML analytics and statistical evaluation.

> [!CRITICAL]
> **Bluetooth Measurement Rule**: Bluetooth is a wireless communication protocol; it does not compute blood pressure from heart rate or oxygen saturation. Blood pressure measurements must originate from a dedicated BP cuff (via BLE `0x1810`) or manual clinical entry.
