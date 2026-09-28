# -*- coding: utf-8 -*-
"""
Disease Prediction Model Training & Comparative ML Evaluation Pipeline.
Trains and evaluates Logistic Regression, Random Forest, Decision Tree, Naive Bayes, and SVM.
Computes Accuracy, Precision, Recall, Macro F1, Weighted F1, Confusion Matrix, and per-class metrics.
Saves chosen model, label encoder, feature names, and comprehensive metrics.json.
100% Offline execution.
"""
import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def train_and_evaluate():
    dataset_path = "data/disease_prediction/disease_symptoms_dataset.csv"
    if not os.path.exists(dataset_path):
        dataset_path = "medical_symptoms_dataset.csv"

    print(f"[*] Loading Disease Prediction dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    # Separate features and target
    target_col = "disease"
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].values
    y_raw = df[target_col].values

    print(f"[+] Loaded {X.shape[0]} records with {X.shape[1]} symptom features across {len(np.unique(y_raw))} disease classes.")

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_names = list(label_encoder.classes_)

    # Stratified train/test split to prevent data leakage and guarantee class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[+] Split: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples.")

    # Define candidate models
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=16, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=16, random_state=42),
        "Naive Bayes": MultinomialNB(),
        "Support Vector Machine (SVM)": SVC(kernel="linear", probability=True, random_state=42)
    }

    all_metrics = {}
    fitted_models = {}

    print("\n[*] Evaluating Candidate ML Models on Disease Classification Task:")
    print("-" * 75)
    print(f"{'Model':<30} | {'Accuracy':<10} | {'Macro F1':<10} | {'Weighted F1':<12}")
    print("-" * 75)

    for name, clf in models.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        all_metrics[name] = {
            "accuracy": round(float(acc), 4),
            "precision_macro": round(float(prec_macro), 4),
            "recall_macro": round(float(rec_macro), 4),
            "f1_macro": round(float(f1_macro), 4),
            "f1_weighted": round(float(f1_weighted), 4),
            "confusion_matrix": cm
        }
        fitted_models[name] = clf

        print(f"{name:<30} | {acc:<10.4f} | {f1_macro:<10.4f} | {f1_weighted:<12.4f}")

    print("-" * 75)

    # Select best model based on macro F1 and accuracy
    best_model_name = max(all_metrics.keys(), key=lambda k: (all_metrics[k]["f1_macro"], all_metrics[k]["accuracy"]))
    best_model = fitted_models[best_model_name]
    print(f"\n[+] Selected Best Model: {best_model_name} (Macro F1: {all_metrics[best_model_name]['f1_macro']:.4f})")

    # Generate detailed per-class report for chosen model
    y_test_pred = best_model.predict(X_test)
    class_report_dict = classification_report(
        y_test, y_test_pred, target_names=class_names, output_dict=True, zero_division=0
    )

    per_class_performance = {}
    for cls_name in class_names:
        if cls_name in class_report_dict:
            per_class_performance[cls_name] = {
                "precision": round(class_report_dict[cls_name]["precision"], 4),
                "recall": round(class_report_dict[cls_name]["recall"], 4),
                "f1_score": round(class_report_dict[cls_name]["f1-score"], 4),
                "support": int(class_report_dict[cls_name]["support"])
            }

    # Prepare artifacts output directory
    os.makedirs("models/disease_prediction", exist_ok=True)

    # Save artifacts
    model_save_path = "models/disease_prediction/model.pkl"
    with open(model_save_path, "wb") as f:
        pickle.dump(best_model, f)
    print(f"[+] Saved model to {model_save_path}")

    encoder_save_path = "models/disease_prediction/label_encoder.pkl"
    with open(encoder_save_path, "wb") as f:
        pickle.dump(label_encoder, f)
    print(f"[+] Saved label encoder to {encoder_save_path}")

    features_save_path = "models/disease_prediction/feature_names.pkl"
    with open(features_save_path, "wb") as f:
        pickle.dump(feature_cols, f)
    print(f"[+] Saved feature names to {features_save_path}")

    metrics_payload = {
        "model_version": "1.0",
        "training_timestamp": datetime.now().isoformat(),
        "selected_model": best_model_name,
        "dataset_info": {
            "name": "Disease Symptom Prediction Dataset",
            "total_samples": int(X.shape[0]),
            "train_samples": int(X_train.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "num_features": int(X.shape[1]),
            "num_classes": len(class_names)
        },
        "model_comparisons": all_metrics,
        "per_class_metrics": per_class_performance,
        "class_names": class_names
    }

    metrics_save_path = "models/disease_prediction/metrics.json"
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved comparative metrics to {metrics_save_path}")

    # Also save model_metadata.json as requested in section 40
    metadata_payload = {
        "model_name": best_model_name,
        "model_version": "1.0",
        "training_dataset": "Disease Symptom Prediction Dataset (Kaggle)",
        "training_date": datetime.now().strftime("%Y-%m-%d"),
        "evaluation_metrics": {
            "accuracy": all_metrics[best_model_name]["accuracy"],
            "macro_f1": all_metrics[best_model_name]["f1_macro"],
            "weighted_f1": all_metrics[best_model_name]["f1_weighted"]
        },
        "classes_count": len(class_names),
        "features_count": len(feature_cols)
    }
    with open("models/disease_prediction/model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata_payload, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved model metadata to models/disease_prediction/model_metadata.json")

if __name__ == "__main__":
    train_and_evaluate()
