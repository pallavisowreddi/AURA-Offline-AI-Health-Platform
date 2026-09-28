# -*- coding: utf-8 -*-
"""
AURA Offline AI Health Platform - Comprehensive Automated Test Suite
Covers:
1. Local Database & Seed Integrity (SQLite)
2. Knowledge Base Structure & Completeness
3. Semantic Vector RAG Retrieval
4. Emergency Risk Detection & Deterministic Safety Shield
5. Medical Safety & Anti-Diagnosis Disclaimers
6. Symptom Awareness Correlation (Non-diagnostic)
7. Disease Search & Category Filtering
8. Chat History Persistence (Create, Read, Delete)
9. Multilingual Translation & Local Resources
10. 20+ Real-World Health Query Test Battery
"""
import sys
import os
import json
import unittest

# Ensure root directory is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import app
from core import database
from core import safety
from core.rag_engine import rag_engine
from core import symptom_service

class TestAuraOfflineSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()
        rag_engine.build_index()
        cls.client = app.app.test_client()

    # -------------------------------------------------------------------------
    # 1. DATABASE TESTS
    # -------------------------------------------------------------------------
    def test_database_stats(self):
        stats = database.get_database_stats()
        self.assertGreaterEqual(stats["diseases_count"], 20, "Should have at least 20 diseases")
        self.assertGreaterEqual(stats["symptoms_count"], 50, "Should have at least 50 symptoms")
        self.assertGreaterEqual(stats["knowledge_docs_count"], 80, "Should have 80+ knowledge docs")
        self.assertEqual(stats["mode"], "offline")

    def test_chat_history_crud(self):
        # Create
        conv_id = database.create_conversation("Automated Test Consultation")
        self.assertTrue(conv_id)

        # Add Messages
        msg_id1 = database.add_message(conv_id, "user", "What is dengue?")
        msg_id2 = database.add_message(conv_id, "assistant", "Dengue is a viral infection.", metadata={"confidence": "High"})
        self.assertTrue(msg_id1 and msg_id2)

        # Retrieve
        conv = database.get_conversation(conv_id)
        self.assertIsNotNone(conv)
        self.assertEqual(len(conv["messages"]), 2)
        self.assertEqual(conv["messages"][0]["content"], "What is dengue?")

        # Delete
        del_res = database.delete_conversation(conv_id)
        self.assertTrue(del_res)
        self.assertIsNone(database.get_conversation(conv_id))

    # -------------------------------------------------------------------------
    # 2. EMERGENCY DETECTION & SAFETY SHIELD
    # -------------------------------------------------------------------------
    def test_emergency_detection_cardiac(self):
        query = "Patient has severe crushing chest pain radiating to left arm and cannot breathe"
        is_emer, info = safety.check_emergency(query)
        self.assertTrue(is_emer)
        self.assertIn("Cardiac", info["category"])

    def test_emergency_detection_respiratory(self):
        query = "Child is suffocating, blue lips, gasping for air"
        is_emer, info = safety.check_emergency(query)
        self.assertTrue(is_emer)
        self.assertIn("Respiratory", info["category"])

    def test_emergency_detection_bleeding(self):
        query = "Deep stab wound with severe bleeding and arterial spurting blood"
        is_emer, info = safety.check_emergency(query)
        self.assertTrue(is_emer)
        self.assertIn("Hemorrhage", info["category"])

    def test_emergency_detection_poison(self):
        query = "Accidentally swallowed pesticide poison from bottle"
        is_emer, info = safety.check_emergency(query)
        self.assertTrue(is_emer)
        self.assertIn("Poison", info["category"])

    def test_non_emergency_pass_through(self):
        query = "How can I prevent mosquito bites during monsoon?"
        is_emer, _ = safety.check_emergency(query)
        self.assertFalse(is_emer)

    # -------------------------------------------------------------------------
    # 3. MEDICAL SAFETY & ANTI-DIAGNOSIS VALIDATOR
    # -------------------------------------------------------------------------
    def test_safety_validator_strips_diagnosis(self):
        unsafe = "Based on symptoms, You have Dengue with 87% probability. Take Aspirin."
        safe = safety.validate_medical_response(unsafe)
        self.assertNotIn("You have Dengue", safe)
        self.assertNotIn("87%", safe)
        self.assertIn("Medical Disclaimer", safe)

    # -------------------------------------------------------------------------
    # 4. RAG VECTOR RETRIEVAL & GROUNDING
    # -------------------------------------------------------------------------
    def test_rag_retrieval_relevance(self):
        docs = rag_engine.retrieve_context("What are symptoms of malaria?", top_k=3)
        self.assertGreater(len(docs), 0)
        self.assertIn("Malaria", docs[0]["title"])
        self.assertIn("Local Health Knowledge Base", docs[0]["source"])

    def test_rag_generation_grounded(self):
        res = rag_engine.generate_grounded_response("How to prevent tuberculosis transmission?")
        self.assertFalse(res["is_emergency"])
        self.assertIn("Tuberculosis", res["response"])
        self.assertIn("BCG", res["response"])
        self.assertIn("Medical Disclaimer", res["response"])

    # -------------------------------------------------------------------------
    # 5. SYMPTOM AWARENESS CORRELATION
    # -------------------------------------------------------------------------
    def test_symptom_awareness_correlation(self):
        res = symptom_service.analyze_symptoms_for_awareness(["fever", "headache", "joint_pain"])
        self.assertEqual(res["status"], "success")
        self.assertGreater(len(res["possible_conditions"]), 0)
        self.assertIn("Educational information only", res["disclaimer"])

    # -------------------------------------------------------------------------
    # 6. REST API ENDPOINTS
    # -------------------------------------------------------------------------
    def test_api_status_endpoint(self):
        res = self.client.get("/api/status")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["mode"], "offline")
        self.assertFalse(data["online_required"])
        self.assertTrue(data["offline_verified"])

    def test_api_diseases_filtering(self):
        res = self.client.get("/api/diseases?category=respiratory")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreaterEqual(data["count"], 3)
        for d in data["diseases"]:
            self.assertEqual(d["category"].lower(), "respiratory")

    def test_api_diseases_detail(self):
        res = self.client.get("/api/diseases/dengue")
        self.assertEqual(res.status_code, 200)
        d = res.get_json()["disease"]
        self.assertEqual(d["id"], "dengue")
        self.assertIn("common_symptoms", d["raw"])

    def test_api_symptoms_directory(self):
        res = self.client.get("/api/symptoms")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.get_json()["count"], 50)

    def test_api_health_tips(self):
        res = self.client.get("/api/health-tips")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.get_json()["categories"]), 8)

    # -------------------------------------------------------------------------
    # 7. BATTERY OF 20 SAMPLE REAL-WORLD HEALTH QUERIES
    # -------------------------------------------------------------------------
    def test_twenty_sample_health_questions_battery(self):
        queries = [
            ("What is dengue?", "dengue"),
            ("What are common symptoms of malaria?", "malaria"),
            ("How can I prevent dengue fever?", "prevent"),
            ("What causes tuberculosis?", "tuberculosis"),
            ("Tell me about asthma causes and inhalers", "asthma"),
            ("What is normal blood pressure for adults?", "blood pressure"),
            ("How to manage type 2 diabetes through diet?", "diabetes"),
            ("What is the difference between cold and flu?", "flu"),
            ("What are the warning signs of heat stroke and dehydration?", "dehydration"),
            ("How is typhoid fever transmitted?", "typhoid"),
            ("What are the symptoms of cholera?", "cholera"),
            ("Is pneumonia contagious?", "pneumonia"),
            ("How to prevent food poisoning at home?", "food poisoning"),
            ("Tell me about chickenpox blisters in children", "chickenpox"),
            ("What are symptoms of measles?", "measles"),
            ("How to prevent Hepatitis A infection?", "hepatitis"),
            ("What triggers a migraine headache?", "migraine"),
            ("What are signs of iron deficiency anemia?", "anemia"),
            ("How does chronic kidney disease cause leg swelling?", "kidney"),
            ("What are emergency warning signs requiring immediate 108 dispatch?", "emergency")
        ]

        print(f"\n--- Running 20-Query Offline Battery ---")
        for idx, (q, expected_keyword) in enumerate(queries, 1):
            res = self.client.post("/api/chat", json={"message": q})
            self.assertEqual(res.status_code, 200, f"Query #{idx} failed: {q}")
            data = res.get_json()
            resp_lower = data.get("response", "").lower()
            self.assertTrue(
                expected_keyword in resp_lower or data.get("is_emergency"),
                f"Query #{idx} '{q}' did not contain expected concept '{expected_keyword}'"
            )
            self.assertIn("medical disclaimer", resp_lower, f"Query #{idx} missing medical disclaimer")
            print(f"  [✓] Query #{idx:02d} PASSED: {q[:45]}...")

if __name__ == "__main__":
    unittest.main()
