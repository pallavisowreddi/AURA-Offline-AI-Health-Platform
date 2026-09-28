"""
Unit and integration tests for Live Health & Biometric Telemetry Hub.
Tests multi-source ingestion (REAL_DEVICE, SIMULATED, MANUAL_ENTRY),
physiological validation, clinical awareness alerts, session lifecycle,
trends calculation, and chatbot biometric queries.
"""

import unittest
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from core.database import (
    save_measurement,
    get_latest_vitals,
    get_measurements,
    save_monitoring_session,
    stop_monitoring_session
)
from models.health_analytics.analytics_engine import (
    detect_anomalies,
    calculate_trend_slope,
    evaluate_measurement_awareness
)


class TestLiveHealthMonitoring(unittest.TestCase):
    """Tests the local offline biometric monitoring system."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_manual_biometric_ingestion(self):
        """Verify manual entry stores in SQLite with source_type MANUAL_ENTRY."""
        meas_id = save_measurement(
            metric_type="heart_rate",
            value=76.0,
            unit="BPM",
            source_type="MANUAL_ENTRY",
            device_id="Manual Entry",
            notes="Morning baseline"
        )
        self.assertIsNotNone(meas_id)

        save_measurement(
            metric_type="blood_pressure",
            value=122.0,
            secondary_value=82.0,
            unit="mmHg",
            source_type="MANUAL_ENTRY",
            device_id="Manual BP Cuff"
        )

        # Check latest vitals
        latest = get_latest_vitals()
        self.assertIsNotNone(latest.get("heart_rate"))
        self.assertEqual(latest["heart_rate"]["value"], 76.0)
        self.assertEqual(latest["heart_rate"]["source_type"], "MANUAL_ENTRY")
        self.assertIsNotNone(latest.get("blood_pressure"))
        self.assertEqual(latest["blood_pressure"]["value"], 122.0)
        self.assertEqual(latest["blood_pressure"]["secondary_value"], 82.0)

    def test_simulated_biometric_provenance(self):
        """Verify simulated telemetry is explicitly tagged with source_type SIMULATED."""
        meas_id = save_measurement(
            metric_type="spo2",
            value=97.0,
            unit="%",
            source_type="SIMULATED",
            device_id="PulseBand Pro Simulator",
            signal_quality="SIMULATED_BENCHMARK"
        )
        self.assertIsNotNone(meas_id)

        history = get_measurements(source_type="SIMULATED", limit=10)
        self.assertTrue(any(m["id"] == meas_id and m["source_type"] == "SIMULATED" for m in history))

    def test_biometric_endpoint_ingestion(self):
        """Verify POST /api/biometrics/measurement endpoint responds with 201."""
        payload = {
            "heart_rate": 84,
            "spo2": 96,
            "systolic_bp": 118,
            "diastolic_bp": 78,
            "body_temperature": 98.7,
            "source_type": "MANUAL_ENTRY",
            "device_name": "Clinic Sphygmomanometer",
            "quality_assessment": "MANUALLY_VERIFIED"
        }
        res = self.app.post("/api/biometrics/measurement", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("measurement_id", data)

    def test_clinical_alert_generation(self):
        """Verify acute threshold breaches return awareness alerts."""
        payload = {
            "heart_rate": 115,
            "spo2": 88,
            "systolic_bp": 185,
            "diastolic_bp": 125,
            "body_temperature": 103.5,
            "source_type": "MANUAL_ENTRY"
        }
        res = self.app.post("/api/biometrics/measurement", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        alerts = data.get("alerts", [])
        self.assertGreater(len(alerts), 0, "Should generate clinical awareness alerts for critical bounds")
        alert_full_text = " ".join(f"{a.get('title', '')} {a.get('metric', '')} {a.get('message', '')}" for a in alerts)
        self.assertTrue("Hypoxemia" in alert_full_text or "Oxygen" in alert_full_text or "Blood Pressure" in alert_full_text or "Crisis" in alert_full_text)

    def test_monitoring_session_lifecycle(self):
        """Verify starting and stopping a live monitoring session."""
        session_id = save_monitoring_session(session_type="live_biometrics")
        self.assertIsNotNone(session_id)

        stop_res = stop_monitoring_session(session_id=session_id, notes="Test live stop")
        self.assertTrue(stop_res)

    def test_analytics_anomaly_and_trend(self):
        """Verify analytics engine detects anomalies and slopes."""
        normal_series = [72, 74, 71, 73, 75, 72, 74]
        anomalies = detect_anomalies(normal_series)
        self.assertFalse(any(anomalies), "Normal series should have 0 anomalies")

        spiked_series = [72, 74, 71, 150, 72, 74]
        spiked_anomalies = detect_anomalies(spiked_series)
        self.assertTrue(any(spiked_anomalies), "Spike to 150 should be detected as anomaly")

        rising_series = [60, 65, 70, 78, 85, 92]
        trend = calculate_trend_slope(rising_series)
        self.assertEqual(trend, "Elevated")

    def test_chatbot_biometric_awareness(self):
        """Verify the offline chatbot can answer biometric vitals questions locally."""
        save_measurement(
            metric_type="heart_rate",
            value=78.0,
            unit="BPM",
            source_type="MANUAL_ENTRY"
        )
        save_measurement(
            metric_type="blood_pressure",
            value=120.0,
            secondary_value=80.0,
            unit="mmHg",
            source_type="MANUAL_ENTRY"
        )

        res = self.app.post("/api/chat", json={"message": "What is my latest heart rate and blood pressure?"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        reply = data.get("response", "")
        self.assertIn("78", reply, "Chatbot should state the latest heart rate recorded locally")
        self.assertIn("120", reply, "Chatbot should state the systolic blood pressure recorded locally")

    def test_export_report_endpoint(self):
        """Verify POST /api/reports/generate returns offline report."""
        res = self.app.post("/api/reports/generate", json={"format": "json"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("report", data)
        self.assertIn("disclaimer", data["report"])


if __name__ == "__main__":
    unittest.main()
