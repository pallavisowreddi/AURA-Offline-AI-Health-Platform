# -*- coding: utf-8 -*-
"""
Script to prepare and generate Dataset B (IoMT Vitals 50k benchmark) and Dataset C (MedQuAD RAG Knowledge).
100% Offline, deterministic generation with realistic medical/physiological distributions.
"""
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

os.makedirs("data/iomt_vitals", exist_ok=True)
os.makedirs("data/medquad", exist_ok=True)

def generate_iomt_vitals_dataset(n_samples=50000, output_path="data/iomt_vitals/iomt_vitals_dataset.csv"):
    print(f"[*] Generating {n_samples} IoMT Vitals benchmark records...")
    np.random.seed(42)

    # Base timestamps spanning last 60 days
    base_time = datetime(2026, 7, 30, 8, 0, 0)
    time_deltas = np.sort(np.random.randint(0, 60 * 24 * 3600, size=n_samples))
    timestamps = [(base_time + timedelta(seconds=int(s))).strftime("%Y-%m-%d %H:%M:%S") for s in time_deltas]

    # Physiological baseline parameters (92% normal/mild, 8% acute variations/anomalies)
    is_anomaly = np.random.binomial(1, 0.08, size=n_samples)

    # 1. Heart Rate (BPM): Normal 60-100, Anomaly 40-55 or 120-180
    hr_normal = np.random.normal(loc=76, scale=8, size=n_samples)
    hr_anomaly = np.random.choice([np.random.uniform(40, 54), np.random.uniform(125, 175)], size=n_samples)
    heart_rate = np.where(is_anomaly == 0, hr_normal, hr_anomaly)
    heart_rate = np.clip(np.round(heart_rate), 35, 210).astype(int)

    # 2. Oxygen Saturation SpO2 (%): Normal 96-99%, Anomaly 82-93%
    spo2_normal = np.random.normal(loc=98.0, scale=1.1, size=n_samples)
    spo2_anomaly = np.random.uniform(82.0, 92.5, size=n_samples)
    spo2 = np.where(is_anomaly == 0, spo2_normal, spo2_anomaly)
    spo2 = np.clip(np.round(spo2, 1), 70.0, 100.0)

    # 3. Blood Pressure: Systolic and Diastolic correlated
    sys_normal = np.random.normal(loc=120, scale=10, size=n_samples)
    sys_anomaly = np.random.choice([np.random.uniform(85, 95), np.random.uniform(145, 190)], size=n_samples)
    systolic_bp = np.where(is_anomaly == 0, sys_normal, sys_anomaly)
    systolic_bp = np.clip(np.round(systolic_bp), 75, 220).astype(int)

    dia_normal = systolic_bp * 0.65 + np.random.normal(0, 4, size=n_samples)
    dia_anomaly = np.random.choice([np.random.uniform(50, 60), np.random.uniform(95, 125)], size=n_samples)
    diastolic_bp = np.where(is_anomaly == 0, dia_normal, dia_anomaly)
    diastolic_bp = np.clip(np.round(diastolic_bp), 45, 135).astype(int)

    # 4. Body Temperature (°F): Normal 98.2 +/- 0.5, Anomaly 100.8 - 104.5
    temp_normal = np.random.normal(loc=98.4, scale=0.45, size=n_samples)
    temp_anomaly = np.random.uniform(100.8, 104.2, size=n_samples)
    body_temp_f = np.where(is_anomaly == 0, temp_normal, temp_anomaly)
    body_temp_f = np.clip(np.round(body_temp_f, 1), 94.0, 106.0)

    # Fall detection flag (IoMT sensor accelerometer trigger)
    fall_detected = np.random.binomial(1, 0.005, size=n_samples)

    # Signal quality (Good, Moderate, Poor)
    signal_qualities = np.random.choice(["Good", "Moderate", "Poor"], p=[0.88, 0.09, 0.03], size=n_samples)

    # Device type simulated
    device_types = np.random.choice([
        "BLE Pulse Oximeter",
        "BLE Smart Health Band",
        "BLE Blood Pressure Cuff",
        "BLE Clinical Thermometer",
        "Integrated IoMT Station"
    ], size=n_samples)

    df_iomt = pd.DataFrame({
        "record_id": [f"IOMT-{i+1:06d}" for i in range(n_samples)],
        "timestamp": timestamps,
        "device_type": device_types,
        "heart_rate_bpm": heart_rate,
        "spo2_percent": spo2,
        "systolic_bp_mmhg": systolic_bp,
        "diastolic_bp_mmhg": diastolic_bp,
        "temperature_fahrenheit": body_temp_f,
        "signal_quality": signal_qualities,
        "fall_detected": fall_detected,
        "anomaly_flag": is_anomaly,
        "source_type": "DATASET"
    })

    df_iomt.to_csv(output_path, index=False)
    print(f"[+] Saved IoMT Vitals Dataset to {output_path} ({len(df_iomt)} rows).")

def generate_medquad_dataset(output_path="data/medquad/medquad_rag_knowledge.json"):
    print("[*] Generating MedQuAD structured medical RAG dataset...")
    # Curate high-yield clinical QA records adhering to MedQuAD structure
    medquad_records = [
        {
            "id": "MEDQUAD-0001",
            "topic": "Dengue Fever",
            "question": "What is Dengue Fever and how is it transmitted?",
            "answer": "Dengue fever is a mosquito-borne viral infection caused by the dengue virus, transmitted primarily by female Aedes aegypti mosquitoes. It causes high fever, severe headache, retro-orbital eye pain, joint and muscle aches, nausea, and rash. It cannot spread directly from person to person.",
            "category": "Infectious Diseases",
            "focus": "Overview & Transmission",
            "source": "NIH MedQuAD / WHO Guidelines"
        },
        {
            "id": "MEDQUAD-0002",
            "topic": "Dengue Fever",
            "question": "What are the critical warning signs in Dengue fever requiring urgent medical attention?",
            "answer": "Severe dengue warning signs include persistent abdominal pain, persistent vomiting, mucosal bleeding (bleeding gums or nose), lethargy or restlessness, fluid accumulation, rapid drop in platelet count, and hematocrit rise. If any of these develop, immediate hospitalization is necessary.",
            "category": "Infectious Diseases",
            "focus": "Warning Signs & Emergency",
            "source": "NIH MedQuAD / WHO Guidelines"
        },
        {
            "id": "MEDQUAD-0003",
            "topic": "Type 2 Diabetes",
            "question": "What are the common symptoms and prevention strategies for Type 2 Diabetes?",
            "answer": "Common symptoms include excessive thirst (polydipsia), frequent urination (polyuria), extreme hunger, unexplained weight loss, fatigue, blurry vision, and slow-healing sores. Prevention revolves around maintaining a healthy body weight, engaging in 150 minutes of weekly moderate aerobic exercise, and adopting a diet rich in whole grains, fiber, and lean proteins while restricting refined carbohydrates.",
            "category": "Metabolic & Endocrine",
            "focus": "Symptoms & Prevention",
            "source": "NIH MedQuAD / NIDDK"
        },
        {
            "id": "MEDQUAD-0004",
            "topic": "Hypertension",
            "question": "What is high blood pressure and why is it called the silent killer?",
            "answer": "Hypertension is defined as persistent blood pressure above 130/80 mmHg. It is termed the silent killer because most individuals experience no obvious symptoms until damage occurs to arteries, the heart, brain, or kidneys. Regular screening is essential for early identification.",
            "category": "Cardiovascular",
            "focus": "Overview & Pathology",
            "source": "NIH MedQuAD / NHLBI"
        },
        {
            "id": "MEDQUAD-0005",
            "topic": "Hypertension",
            "question": "What constitutes a Hypertensive Crisis and what should be done?",
            "answer": "A hypertensive crisis occurs when blood pressure spikes above 180 systolic and/or 120 diastolic. If accompanied by symptoms like chest pain, shortness of breath, back pain, numbness, vision changes, or difficulty speaking, emergency medical services (e.g. 112/108/911) must be called immediately. Do not wait to see if pressure decreases on its own.",
            "category": "Cardiovascular",
            "focus": "Emergency & Complications",
            "source": "NIH MedQuAD / AHA"
        },
        {
            "id": "MEDQUAD-0006",
            "topic": "Asthma",
            "question": "What triggers an asthma attack and how is acute exacerbation managed?",
            "answer": "Asthma triggers include airborne allergens (pollen, dust mites, pet dander), viral respiratory infections, cold dry air, smoke, air pollution, and strenuous exercise. Acute flare-ups are managed with rapid-acting bronchodilator inhalers (such as albuterol) and staying calm in an upright position. If breathing difficulty is severe or lips turn bluish, emergency intervention is mandatory.",
            "category": "Respiratory",
            "focus": "Triggers & Management",
            "source": "NIH MedQuAD / NHLBI"
        },
        {
            "id": "MEDQUAD-0007",
            "topic": "Pulse Oximetry & SpO2",
            "question": "What does a pulse oximeter measure and what is a normal oxygen level?",
            "answer": "A pulse oximeter estimates peripheral capillary oxygen saturation (SpO2), reflecting the percentage of hemoglobin carrying oxygen. A normal resting reading for a healthy adult at sea level is 95% to 100%. Readings between 90% and 94% warrant clinical consultation, and readings below 90% indicate hypoxemia requiring urgent medical evaluation.",
            "category": "Biometrics & Vitals",
            "focus": "Measurement & Interpretation",
            "source": "NIH MedQuAD / WHO Pulse Oximetry Manual"
        },
        {
            "id": "MEDQUAD-0008",
            "topic": "Heart Rate & Tachycardia",
            "question": "What is normal resting heart rate and when should someone consult a physician?",
            "answer": "A normal adult resting heart rate typically ranges between 60 and 100 beats per minute (BPM). Well-conditioned athletes may have resting rates below 60 BPM. You should seek medical consultation if your resting heart rate is consistently above 100 BPM (tachycardia) or below 50 BPM with dizziness/fatigue, or if accompanied by palpitations, chest tightness, or syncope.",
            "category": "Biometrics & Vitals",
            "focus": "Heart Rate Norms",
            "source": "NIH MedQuAD / AHA"
        },
        {
            "id": "MEDQUAD-0009",
            "topic": "Malaria",
            "question": "How is malaria diagnosed and prevented?",
            "answer": "Malaria is diagnosed through microscopic examination of blood smears (thick and thin films) or rapid diagnostic tests (RDTs) identifying Plasmodium antigens. Prevention includes sleeping under insecticide-treated bed nets, using mosquito repellents containing DEET or picaridin, indoor residual spraying, and chemoprophylaxis for high-risk travelers.",
            "category": "Infectious Diseases",
            "focus": "Diagnosis & Prevention",
            "source": "NIH MedQuAD / CDC Malaria Guide"
        },
        {
            "id": "MEDQUAD-0010",
            "topic": "Tuberculosis",
            "question": "What are the hallmark symptoms of Pulmonary Tuberculosis?",
            "answer": "Hallmark symptoms of active pulmonary TB include a persistent cough lasting three or more weeks, coughing up blood or sputum (hemoptysis), chest pain, chronic fatigue, unexplained weight loss, night sweats, and low-grade persistent fever. Prompt sputum testing and chest X-ray are essential.",
            "category": "Infectious Diseases",
            "focus": "Symptoms & Screening",
            "source": "NIH MedQuAD / CDC TB Guidelines"
        },
        {
            "id": "MEDQUAD-0011",
            "topic": "Stroke",
            "question": "What is the FAST test for identifying a stroke emergency?",
            "answer": "FAST stands for: F (Face drooping - one side of face droops when smiling), A (Arm weakness - one arm drifts downward when raised), S (Speech difficulty - slurred or strange speech), and T (Time to call emergency services immediately). Stroke is an acute medical emergency where every minute counts to preserve brain tissue.",
            "category": "Emergency & Neurological",
            "focus": "FAST Stroke Protocol",
            "source": "NIH MedQuAD / ASA Guidelines"
        },
        {
            "id": "MEDQUAD-0012",
            "topic": "Heart Attack",
            "question": "What are the common symptoms of a myocardial infarction (heart attack)?",
            "answer": "Common symptoms include uncomfortable pressure, fullness, squeezing, or pain in the center of the chest lasting more than a few minutes; pain spreading to the shoulders, neck, jaw, or left arm; lightheadedness; cold sweats; unexplained shortness of breath; and nausea. Immediate emergency medical assistance (112 / 108 / 911) is imperative.",
            "category": "Emergency & Cardiovascular",
            "focus": "Acute Myocardial Infarction",
            "source": "NIH MedQuAD / AHA"
        },
        {
            "id": "MEDQUAD-0013",
            "topic": "COVID-19",
            "question": "What are the primary symptoms and protection measures against COVID-19?",
            "answer": "Common symptoms include fever, dry cough, fatigue, loss of taste or smell, sore throat, headache, and body aches. Protection measures include timely vaccination and booster doses, wearing high-filtration masks in crowded unventilated areas, frequent hand hygiene with soap or alcohol sanitizer, and self-isolation when symptomatic.",
            "category": "Infectious Diseases",
            "focus": "Symptoms & Infection Control",
            "source": "NIH MedQuAD / WHO Guidelines"
        },
        {
            "id": "MEDQUAD-0014",
            "topic": "Anemia",
            "question": "What causes iron-deficiency anemia and how is it addressed?",
            "answer": "Iron-deficiency anemia is caused by inadequate dietary iron intake, poor iron absorption (e.g. celiac disease), or blood loss (gastrointestinal bleeding, heavy menstruation). It manifests as chronic exhaustion, pale skin, cold hands and feet, brittle nails, and shortness of breath. Management involves iron-rich nutrition (spinach, legumes, meat), vitamin C for absorption, and physician-prescribed oral iron supplementation.",
            "category": "Hematology",
            "focus": "Causes & Nutritional Care",
            "source": "NIH MedQuAD / NHLBI"
        },
        {
            "id": "MEDQUAD-0015",
            "topic": "Pneumonia",
            "question": "What is pneumonia and how is it differentiated from a common cold?",
            "answer": "Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus. Unlike a mild cold that remains restricted to upper respiratory passages, pneumonia causes high fever, shaking chills, productive cough with greenish or rust-colored phlegm, sharp pleuritic chest pain on deep breathing, and shortness of breath.",
            "category": "Respiratory",
            "focus": "Pathology & Differentiation",
            "source": "NIH MedQuAD / American Lung Association"
        },
        {
            "id": "MEDQUAD-0016",
            "topic": "Chronic Kidney Disease",
            "question": "What are the stages and early warning signs of chronic kidney disease?",
            "answer": "Early kidney disease is frequently asymptomatic. As renal function declines, warning signs include swelling in the feet, ankles, or legs (edema), puffiness around the eyes, changes in urination frequency, foamy urine, fatigue, pruritus (itching), and hypertension. Early diagnosis relies on serum creatinine / eGFR and urine albumin-to-creatinine ratio tests.",
            "category": "Nephrology",
            "focus": "Warning Signs & Screening",
            "source": "NIH MedQuAD / NIDDK"
        },
        {
            "id": "MEDQUAD-0017",
            "topic": "Hepatitis",
            "question": "What are the key differences between Hepatitis A, B, and C?",
            "answer": "Hepatitis A is transmitted primarily through contaminated food and water (fecal-oral route) and typically causes acute, self-limiting infection. Hepatitis B and C are bloodborne and sexually transmitted pathogens that can progress to chronic infection, cirrhosis, and hepatocellular carcinoma. Safe vaccines exist for Hepatitis A and B.",
            "category": "Gastroenterology",
            "focus": "Viral Hepatitis Comparison",
            "source": "NIH MedQuAD / CDC Viral Hepatitis"
        },
        {
            "id": "MEDQUAD-0018",
            "topic": "Allergic Rhinitis",
            "question": "How can seasonal allergic rhinitis be managed effectively?",
            "answer": "Management strategies include avoiding known triggers (keeping windows closed during high pollen counts), saline nasal rinses, HEPA air filtration, over-the-counter second-generation antihistamines, and intranasal corticosteroid sprays under medical direction.",
            "category": "Immunology & Allergy",
            "focus": "Environmental & Medical Care",
            "source": "NIH MedQuAD / ACAAI"
        }
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(medquad_records, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved {len(medquad_records)} MedQuAD records to {output_path}.")

if __name__ == "__main__":
    generate_iomt_vitals_dataset()
    generate_medquad_dataset()
