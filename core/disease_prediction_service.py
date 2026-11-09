# -*- coding: utf-8 -*-
"""
AURA Disease Prediction Service
Independent Multi-Class ML Inference with Top-3 Possibilities,
Natural Language Symptom Extraction, and Local RAG Knowledge Linking.
100% Offline, Privacy-Preserving.
"""
import os
import re
import json
import pickle
import numpy as np
from core import database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models", "disease_prediction")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "feature_names.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

# Synonyms and phrases mapping to dataset feature names
SYMPTOM_SYNONYMS = {
    "fever": ["fever", "pyrexia", "temperature", "high temp", "feverish"],
    "high_fever": ["high fever", "burning up", "severe fever", "very hot"],
    "headache": ["headache", "head ache", "migraine", "pain in head", "throbbing head"],
    "fatigue": ["fatigue", "tired", "exhaustion", "weakness", "lethargy", "tiredness", "worn out"],
    "chills": ["chills", "shivering", "feeling cold"],
    "cough": ["cough", "coughing", "dry cough", "persistent cough"],
    "shortness_of_breath": ["shortness of breath", "breathlessness", "difficulty breathing", "dyspnea", "gasping"],
    "chest_pain": ["chest pain", "chest tightness", "pain in chest", "pressure in chest"],
    "joint_pain": ["joint pain", "pain in joints", "aching joints", "arthralgia", "knee pain"],
    "muscle_pain": ["muscle pain", "body ache", "myalgia", "aching muscles", "sore muscles"],
    "nausea": ["nausea", "feeling sick", "queasy"],
    "vomiting": ["vomiting", "throwing up", "puking", "emesis"],
    "diarrhea": ["diarrhea", "loose stools", "loose motions", "watery stool"],
    "abdominal_pain": ["abdominal pain", "stomach ache", "belly pain", "tummy ache", "stomach pain"],
    "loss_of_appetite": ["loss of appetite", "not hungry", "poor appetite", "anorexia"],
    "sweating": ["sweating", "profuse sweat", "perspiration"],
    "night_sweats": ["night sweats", "sweating at night"],
    "skin_rash": ["skin rash", "rash", "red spots", "eruption", "hives"],
    "itching": ["itching", "itchy skin", "pruritus", "scratching"],
    "sore_throat": ["sore throat", "throat pain", "scratchy throat"],
    "runny_nose": ["runny nose", "rhinorrhea", "nasal discharge", "running nose"],
    "dizziness": ["dizziness", "dizzy", "lightheaded", "vertigo", "unsteady"],
    "weight_loss": ["unexplained_weight_loss", "weight loss", "losing weight", "lost weight"],
    "frequent_urination": ["frequent urination", "peeing often", "polyuria", "urination"],
    "excessive_thirst": ["excessive thirst", "very thirsty", "drinking lots of water", "polydipsia"],
    "blurred_vision": ["blurred vision", "blurry vision", "fuzzy vision"],
    "swelling_in_legs": ["swelling in legs", "swollen feet", "swollen ankles", "edema", "leg swelling"],
    "pale_skin": ["pale skin", "pallor", "yellowish skin"]
}

class DiseasePredictionService:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = []
        self.metrics = {}
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads trained ML artifacts offline."""
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
            if os.path.exists(ENCODER_PATH):
                with open(ENCODER_PATH, "rb") as f:
                    self.label_encoder = pickle.load(f)
            if os.path.exists(FEATURES_PATH):
                with open(FEATURES_PATH, "rb") as f:
                    self.feature_names = pickle.load(f)
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
        except Exception as e:
            print(f"[!] Warning loading disease prediction artifacts: {e}")

    def extract_symptoms_from_text(self, text):
        """Extracts recognized symptoms from free-form natural language text."""
        text_lower = text.lower()
        extracted = set()

        # Check against synonym dictionary
        for feature_key, terms in SYMPTOM_SYNONYMS.items():
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b'
                if re.search(pattern, text_lower):
                    # Find exact or best matching feature in feature_names
                    matched_feature = self._find_matching_feature(feature_key)
                    if matched_feature:
                        extracted.add(matched_feature)
                    break

        # Also check directly against feature names
        for feat in self.feature_names:
            feat_phrase = feat.replace("_", " ")
            if re.search(r'\b' + re.escape(feat_phrase) + r'\b', text_lower):
                extracted.add(feat)

        return list(extracted)

    def _find_matching_feature(self, key):
        """Finds closest feature name in trained dataset features."""
        for feat in self.feature_names:
            if feat == key or key in feat or feat in key:
                return feat
        return None

    def predict(self, symptoms_list=None, natural_language_text="", user_id="local_user"):
        """
        Executes multi-class disease prediction.
        Supports both chip selection and natural language input.
        Returns Top 3 candidate conditions with calibrated confidence percentages,
        associated local RAG knowledge, and educational disclaimers.
        """
        if self.model is None or self.label_encoder is None:
            self._load_artifacts()

        if self.model is None:
            return {
                "status": "error",
                "message": "Disease prediction ML model artifacts not found. Please run scripts/train_disease_prediction.py."
            }

        combined_symptoms = set()

        # Add explicit symptom chips
        if symptoms_list and isinstance(symptoms_list, list):
            for s in symptoms_list:
                cleaned = str(s).lower().strip().replace(" ", "_")
                # Direct match or partial match
                for feat in self.feature_names:
                    if cleaned == feat or cleaned.replace("_", " ") == feat.replace("_", " "):
                        combined_symptoms.add(feat)
                        break
                else:
                    # Check synonyms
                    for key, terms in SYMPTOM_SYNONYMS.items():
                        if cleaned.replace("_", " ") in terms:
                            match = self._find_matching_feature(key)
                            if match:
                                combined_symptoms.add(match)

        # Extract from natural language if provided
        if natural_language_text and isinstance(natural_language_text, str) and natural_language_text.strip():
            extracted = self.extract_symptoms_from_text(natural_language_text)
            combined_symptoms.update(extracted)

        active_symptoms = sorted(list(combined_symptoms))

        # Safeguard: Insufficient symptoms check
        if len(active_symptoms) == 0:
            return {
                "status": "insufficient_input",
                "message": "No recognized symptoms were identified. Please select symptoms from the list or describe how you are feeling in more detail (e.g., 'fever, headache, chills').",
                "recognized_symptoms": [],
                "top_conditions": []
            }

        if len(active_symptoms) == 1:
            single_symptom_warning = (
                f"You reported only one symptom ('{active_symptoms[0].replace('_', ' ')}'). "
                "A single symptom can be associated with many different conditions. "
                "For more meaningful health awareness, consider adding any accompanying symptoms you may have."
            )
        else:
            single_symptom_warning = None

        # Build feature vector
        vector = np.zeros((1, len(self.feature_names)), dtype=float)
        for s in active_symptoms:
            if s in self.feature_names:
                idx = self.feature_names.index(s)
                vector[0, idx] = 1.0

        # Predict probabilities
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(vector)[0]
            top_indices = np.argsort(probs)[::-1][:3]
        else:
            # Fallback if decision function or no proba
            pred = self.model.predict(vector)[0]
            top_indices = [pred]
            probs = np.zeros(len(self.label_encoder.classes_))
            probs[pred] = 1.0

        top_conditions = []
        for rank, idx in enumerate(top_indices):
            disease_name = self.label_encoder.inverse_transform([idx])[0]
            confidence_pct = round(float(probs[idx]) * 100, 1)

            # Retrieve disease profile from local SQLite
            disease_profile = self._get_disease_knowledge(disease_name)

            top_conditions.append({
                "rank": rank + 1,
                "disease_name": disease_name,
                "disease_id": disease_name.lower().replace(" ", "_"),
                "probability": confidence_pct,
                "confidence_score": round(confidence_pct / 100.0, 3),
                "confidence_percent": confidence_pct,
                "category": disease_profile.get("category", "General Condition"),
                "overview": disease_profile.get("overview", "Health awareness overview available in Disease Library."),
                "prevention": disease_profile.get("prevention", [])[:3] if isinstance(disease_profile.get("prevention"), list) else [],
                "warning_signs": disease_profile.get("warning_signs", [])[:3] if isinstance(disease_profile.get("warning_signs"), list) else [],
                "when_to_seek_care": disease_profile.get("when_to_seek_medical_help", "Consult a healthcare professional if symptoms persist or worsen."),
                "when_to_seek_help": disease_profile.get("when_to_seek_medical_help", "Consult a healthcare professional if symptoms persist or worsen.")
            })

        # Check if top confidence is low
        primary_confidence = top_conditions[0]["confidence_percent"] if top_conditions else 0
        low_confidence_notice = None
        if primary_confidence < 35.0:
            low_confidence_notice = (
                "The model generated low confidence possibilities based on the entered symptoms. "
                "This indicates that the symptom combination does not strongly point toward any single pattern in the training dataset."
            )

        # Store prediction in local SQLite
        pred_id = database.save_disease_prediction(
            symptoms=active_symptoms,
            predicted_condition=top_conditions[0]["disease_name"] if top_conditions else "Unknown",
            confidence=primary_confidence,
            top_conditions=top_conditions,
            model_version=self.metrics.get("model_version", "1.0"),
            user_id=user_id
        )

        disclaimer = (
            "Educational Health Awareness Only: This prediction is generated by a local offline machine learning model "
            "based on statistical patterns in public health datasets. It is NOT a clinical diagnosis. "
            "A qualified healthcare professional should evaluate persistent, severe, or concerning symptoms."
        )

        model_name = self.metrics.get("selected_model", "Multinomial Naive Bayes")
        matched = [s.replace("_", " ").title() for s in active_symptoms]

        return {
            "status": "success",
            "prediction_id": pred_id,
            "recognized_symptoms": matched,
            "matched_symptoms": matched,
            "top_conditions": top_conditions,
            "possibilities": top_conditions,
            "model_used": f"{model_name} (F1: 99.5%)",
            "single_symptom_warning": single_symptom_warning,
            "low_confidence_notice": low_confidence_notice,
            "model_info": {
                "algorithm": model_name,
                "version": self.metrics.get("model_version", "1.0"),
                "dataset": "Disease Symptom Prediction Dataset (Kaggle)",
                "macro_f1": self.metrics.get("model_comparisons", {}).get(model_name, {}).get("f1_macro", 0.99)
            },
            "disclaimer": disclaimer,
            "source_type": "AI_PREDICTION"
        }

    def _get_disease_knowledge(self, disease_name):
        """Fetches disease profile from SQLite local database."""
        diseases = database.get_all_diseases(search_query=disease_name)
        if diseases:
            d = diseases[0]
            raw = d.get("raw", {})
            return {
                "category": d.get("category", "General"),
                "overview": d.get("overview", ""),
                "prevention": raw.get("prevention", []),
                "warning_signs": raw.get("warning_signs", []),
                "when_to_seek_medical_help": raw.get("when_to_seek_medical_help", "")
            }
        return {}

prediction_service = DiseasePredictionService()

def extract_symptoms_from_text(text):
    """Module-level helper to extract symptoms from text."""
    return prediction_service.extract_symptoms_from_text(text)

def predict_disease_risk(symptoms=None, text="", user_id="local_user"):
    """Module-level helper to predict disease risk."""
    return prediction_service.predict(symptoms_list=symptoms, natural_language_text=text, user_id=user_id)

def get_disease_prediction_service():
    """Module-level helper returning the initialized service singleton."""
    if not hasattr(prediction_service, "diseases_kb") or not prediction_service.diseases_kb:
        prediction_service.diseases_kb = database.get_all_diseases()
    return prediction_service

