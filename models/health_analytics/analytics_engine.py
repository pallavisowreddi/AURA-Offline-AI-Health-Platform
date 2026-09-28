# -*- coding: utf-8 -*-
"""
Health Analytics Engine - IoMT Vital Signs Analytics, Anomaly Detection & Trend Analysis
100% Offline, Privacy-Preserving Local Computation.
"""
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

class HealthAnalyticsEngine:
    """
    Offline statistical and machine learning analytics engine for vital signs.
    Provides anomaly detection, trend direction, moving averages, and awareness evaluation.
    """
    def __init__(self, thresholds_path="config/health_thresholds.json"):
        self.thresholds = self._load_thresholds(thresholds_path)

    def _load_thresholds(self, path):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def evaluate_measurement_awareness(self, metric_type, value, secondary_value=None):
        """
        Evaluates a measurement against educational awareness ranges from config.
        Returns: { status, severity ('normal', 'info', 'warning', 'critical'), educational_note }
        """
        ranges = self.thresholds.get("educational_ranges", {})
        metric_key = metric_type.lower().replace(" ", "_")

        if "heart_rate" in metric_key or metric_key == "hr":
            hr = float(value)
            cfg = ranges.get("heart_rate_bpm", {})
            if hr < 60:
                return {
                    "status": "Bradycardia Range (<60 BPM)",
                    "severity": "warning",
                    "educational_note": "Heart rate is below typical adult resting levels. If resting or an athlete, this can be normal; if accompanied by dizziness, clinical evaluation is advised."
                }
            elif hr <= 100:
                return {
                    "status": "Normal Resting Heart Rate",
                    "severity": "normal",
                    "educational_note": "Within typical adult resting range (60–100 BPM)."
                }
            elif hr <= 130:
                return {
                    "status": "Mildly Elevated Heart Rate",
                    "severity": "warning",
                    "educational_note": "Heart rate is elevated. Common causes include physical exertion, stress, caffeine, dehydration, or mild fever."
                }
            else:
                return {
                    "status": "Significant Tachycardia (>130 BPM)",
                    "severity": "alert",
                    "educational_note": "Recorded rate is notably elevated. Consider resting and re-checking. If persistent or with chest tightness, seek medical evaluation."
                }

        elif "spo2" in metric_key or "oxygen" in metric_key:
            spo2 = float(value)
            cfg = ranges.get("oxygen_saturation_spo2", {})
            if spo2 >= 95:
                return {
                    "status": "Normal Blood Oxygenation",
                    "severity": "normal",
                    "educational_note": "Normal oxygen saturation level (95–100%)."
                }
            elif spo2 >= 90:
                return {
                    "status": "Mild Hypoxemia (90–94%)",
                    "severity": "warning",
                    "educational_note": "Oxygen saturation is slightly below optimal. Confirm sensor contact and rest. Consult a physician if symptomatic."
                }
            else:
                return {
                    "status": "Severe Hypoxemia (<90%)",
                    "severity": "critical",
                    "educational_note": "Urgent attention advised. Oxygen saturation is significantly reduced. Seek prompt professional medical evaluation."
                }

        elif "blood_pressure" in metric_key or metric_key == "bp":
            sys = float(value)
            dia = float(secondary_value) if secondary_value is not None else 80.0
            if sys >= 180 or dia >= 120:
                return {
                    "status": "Hypertensive Crisis Range",
                    "severity": "critical",
                    "educational_note": "Systolic >= 180 or Diastolic >= 120. If accompanied by chest pain, shortness of breath, or numbness, emergency care is needed immediately."
                }
            elif sys >= 140 or dia >= 90:
                return {
                    "status": "Stage 2 Hypertension Range",
                    "severity": "warning",
                    "educational_note": "Blood pressure reading is in the Stage 2 elevated bracket. Regular monitoring and clinical consultation recommended."
                }
            elif sys >= 130 or dia >= 80:
                return {
                    "status": "Stage 1 Hypertension Range",
                    "severity": "warning",
                    "educational_note": "Blood pressure reading is in the Stage 1 bracket. Lifestyle optimizations are often advised."
                }
            elif sys >= 120 and dia < 80:
                return {
                    "status": "Elevated Blood Pressure",
                    "severity": "info",
                    "educational_note": "Systolic between 120–129 with diastolic < 80. Preventive lifestyle habits help maintain optimal cardiovascular health."
                }
            else:
                return {
                    "status": "Normal Blood Pressure",
                    "severity": "normal",
                    "educational_note": "Within typical healthy adult guidelines (<120/<80 mmHg)."
                }

        elif "temp" in metric_key:
            temp = float(value)
            # Normalize to Fahrenheit if provided in Celsius
            if temp < 50:
                temp = (temp * 9/5) + 32
            if temp < 95.0:
                return {
                    "status": "Hypothermia Range (<95°F)",
                    "severity": "warning",
                    "educational_note": "Body temperature is below expected baseline. Ensure warmth and re-check sensor."
                }
            elif temp <= 99.0:
                return {
                    "status": "Normal Body Temperature",
                    "severity": "normal",
                    "educational_note": "Within standard baseline oral/temporal range (97.0–99.0°F / 36.1–37.2°C)."
                }
            elif temp <= 100.4:
                return {
                    "status": "Low-Grade Temperature Elevation",
                    "severity": "info",
                    "educational_note": "Mild temperature rise. Stay well-hydrated and rest."
                }
            elif temp <= 103.9:
                return {
                    "status": "Fever (Pyrexia)",
                    "severity": "warning",
                    "educational_note": "Fever detected. Maintain hydration, rest, and monitor for accompanying symptoms."
                }
            else:
                return {
                    "status": "High Fever (Hyperpyrexia >=104°F)",
                    "severity": "critical",
                    "educational_note": "High temperature elevation. Prompt medical assessment is advised."
                }

        return {
            "status": "Recorded",
            "severity": "normal",
            "educational_note": "Measurement logged successfully."
        }

    def detect_anomalies(self, values):
        """
        Statistical anomaly detection using Modified Z-score (robust to outliers).
        values: list or numpy array of numeric readings.
        """
        arr = np.array(values, dtype=float)
        if len(arr) < 4:
            return [False] * len(arr)
        
        median = np.median(arr)
        mad = np.median(np.abs(arr - median))
        if mad == 0:
            mad = np.std(arr) or 1.0
        
        modified_z = 0.6745 * (arr - median) / mad
        return (np.abs(modified_z) > 3.0).tolist()

    def compute_summary_statistics(self, values):
        """Computes descriptive statistics for a series of readings."""
        arr = np.array(values, dtype=float)
        if len(arr) == 0:
            return {}
        return {
            "count": int(len(arr)),
            "mean": round(float(np.mean(arr)), 1),
            "median": round(float(np.median(arr)), 1),
            "std": round(float(np.std(arr)), 1),
            "min": round(float(np.min(arr)), 1),
            "max": round(float(np.max(arr)), 1)
        }

    def compute_trend(self, values):
        """
        Determines overall trend direction (Rising, Falling, Stable) using simple linear regression.
        """
        arr = np.array(values, dtype=float)
        if len(arr) < 2:
            return "Stable"
        x = np.arange(len(arr))
        slope, _ = np.polyfit(x, arr, 1)
        if slope > 0.5:
            return "Rising"
        elif slope < -0.5:
            return "Falling"
        return "Stable"

analytics_engine = HealthAnalyticsEngine()

def detect_anomalies(values):
    """Module-level helper to detect anomalies."""
    return analytics_engine.detect_anomalies(values)

def calculate_trend_slope(values):
    """Module-level helper to calculate trend direction."""
    res = analytics_engine.compute_trend(values)
    if res == "Rising":
        return "Elevated"
    elif res == "Falling":
        return "Declining"
    return "Stable"

def evaluate_measurement_awareness(metric_type, value, secondary_value=None):
    """Module-level helper to evaluate awareness."""
    return analytics_engine.evaluate_measurement_awareness(metric_type, value, secondary_value)

