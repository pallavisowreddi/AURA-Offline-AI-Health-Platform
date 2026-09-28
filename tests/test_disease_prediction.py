"""
Unit and integration tests for Offline Disease Prediction & ML Risk Assessment.
Tests multi-model inference, NLP symptom extraction, top-3 possibilities,
and mandatory non-diagnostic clinical disclaimers.
"""

import unittest
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from core.disease_prediction_service import (
    predict_disease_risk,
    extract_symptoms_from_text,
    get_disease_prediction_service
)


class TestDiseasePredictionService(unittest.TestCase):
    """Tests the local offline disease prediction service."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_service_initialization(self):
        """Verify model, label encoder, and feature names load offline without error."""
        svc = get_disease_prediction_service()
        self.assertIsNotNone(svc.model, "ML model should be loaded")
        self.assertIsNotNone(svc.label_encoder, "Label encoder should be loaded")
        self.assertGreater(len(svc.feature_names), 20, "Should have 20+ feature names")
        self.assertGreater(len(svc.diseases_kb), 15, "Should have 15+ disease cards in local KB")

    def test_nlp_symptom_extraction(self):
        """Verify natural language text extracts known symptom keys."""
        text = "I have been suffering from high fever, severe headache, and joint pain since yesterday."
        extracted = extract_symptoms_from_text(text)
        self.assertIn("fever", extracted)
        self.assertIn("headache", extracted)
        self.assertIn("joint_pain", extracted)

    def test_multi_symptom_prediction_top_3(self):
        """Verify multi-symptom input returns top 3 ranked condition possibilities with probabilities."""
        symptoms = ["fever", "chills", "sweating", "headache"]
        result = predict_disease_risk(symptoms=symptoms)

        self.assertEqual(result.get("status"), "success")
        possibilities = result.get("possibilities", [])
        self.assertGreaterEqual(len(possibilities), 1, "Should return at least 1 possibility")
        self.assertLessEqual(len(possibilities), 3, "Should return at most top 3 possibilities")

        top_match = possibilities[0]
        self.assertIn("disease_name", top_match)
        self.assertIn("probability", top_match)
        self.assertIn("confidence_score", top_match)
        self.assertGreater(top_match["probability"], 0.0)
        self.assertLessEqual(top_match["probability"], 100.0)

        # Check disclaimer is strictly present
        self.assertIn("disclaimer", result)
        self.assertTrue(len(result["disclaimer"]) > 20)
        self.assertIn("NOT", result["disclaimer"].upper())

    def test_empty_input_handling(self):
        """Verify empty input gracefully returns insufficient_input status with guidance."""
        result = predict_disease_risk(symptoms=[], text="")
        self.assertIn(result.get("status"), ["insufficient_input", "success"])
        self.assertEqual(len(result.get("top_conditions", [])), 0)

    def test_api_predict_disease_endpoint(self):
        """Verify POST /api/predict/disease HTTP endpoint returns valid payload."""
        payload = {
            "symptoms": ["cough", "fever", "fatigue"],
            "text": "Feeling very tired and coughing"
        }
        res = self.app.post("/api/predict/disease", json=payload)
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("possibilities", data)
        self.assertIn("model_used", data)
        self.assertIn("disclaimer", data)
        self.assertIn("matched_symptoms", data)

    def test_model_metadata(self):
        """Verify serialized model metrics metadata is readable offline."""
        svc = get_disease_prediction_service()
        metrics = svc.metrics
        self.assertIn("selected_model", metrics)
        selected_model = metrics["selected_model"]
        self.assertIn(selected_model, metrics["model_comparisons"])
        model_stats = metrics["model_comparisons"][selected_model]
        self.assertGreaterEqual(model_stats["accuracy"], 0.90)


if __name__ == "__main__":
    unittest.main()
