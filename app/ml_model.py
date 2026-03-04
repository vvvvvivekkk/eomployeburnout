"""
ml_model.py - Machine Learning training module.

Trains two classification models:
  - Logistic Regression
  - Random Forest Classifier

For two targets:
  - burnout_level
  - attrition_status

Evaluates with: Accuracy, Precision, Recall, F1 Score, Confusion Matrix.
Automatically selects the best model based on highest Accuracy.
Saves models to disk as .pkl files using Joblib.
"""

import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

# Directory to store trained models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "app")

BURNOUT_MODEL_PATH = os.path.join(MODEL_DIR, "burnout_model.pkl")
ATTRITION_MODEL_PATH = os.path.join(MODEL_DIR, "attrition_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
BURNOUT_ENCODER_PATH = os.path.join(MODEL_DIR, "burnout_encoder.pkl")
ATTRITION_ENCODER_PATH = os.path.join(MODEL_DIR, "attrition_encoder.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "training_metrics.pkl")


def evaluate_model(model, X_test, y_test, average="weighted"):
    """
    Evaluate a classification model and return metrics.

    Args:
        model: Trained sklearn model
        X_test: Test features
        y_test: Test labels
        average: Averaging strategy for multi-class metrics

    Returns:
        Dictionary with accuracy, precision, recall, f1, confusion_matrix
    """
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, average=average, zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, average=average, zero_division=0), 4),
        "f1_score": round(f1_score(y_test, y_pred, average=average, zero_division=0), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
    return metrics


def train_models(X_train, X_test, y_train_burnout, y_test_burnout,
                 y_train_attrition, y_test_attrition,
                 scaler, burnout_encoder, attrition_encoder):
    """
    Train Logistic Regression and Random Forest for both targets.
    Select best model per target based on accuracy. Save to disk.

    Args:
        X_train, X_test: Feature arrays
        y_train_burnout, y_test_burnout: Burnout labels
        y_train_attrition, y_test_attrition: Attrition labels
        scaler: Fitted StandardScaler
        burnout_encoder: Fitted LabelEncoder for burnout
        attrition_encoder: Fitted LabelEncoder for attrition

    Returns:
        Dictionary with training results and metrics
    """
    results = {}

    # ── Train Burnout Models ───────────────────────────────
    # Logistic Regression
    lr_burnout = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    lr_burnout.fit(X_train, y_train_burnout)
    lr_burnout_metrics = evaluate_model(lr_burnout, X_test, y_test_burnout)

    # Random Forest
    rf_burnout = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    rf_burnout.fit(X_train, y_train_burnout)
    rf_burnout_metrics = evaluate_model(rf_burnout, X_test, y_test_burnout)

    # Select best burnout model
    if rf_burnout_metrics["accuracy"] >= lr_burnout_metrics["accuracy"]:
        best_burnout_model = rf_burnout
        best_burnout_name = "Random Forest"
    else:
        best_burnout_model = lr_burnout
        best_burnout_name = "Logistic Regression"

    results["burnout_model"] = {
        "logistic_regression": lr_burnout_metrics,
        "random_forest": rf_burnout_metrics,
        "best_model": best_burnout_name,
    }

    # ── Train Attrition Models ─────────────────────────────
    # Logistic Regression
    lr_attrition = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    lr_attrition.fit(X_train, y_train_attrition)
    lr_attrition_metrics = evaluate_model(lr_attrition, X_test, y_test_attrition)

    # Random Forest
    rf_attrition = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    rf_attrition.fit(X_train, y_train_attrition)
    rf_attrition_metrics = evaluate_model(rf_attrition, X_test, y_test_attrition)

    # Select best attrition model
    if rf_attrition_metrics["accuracy"] >= lr_attrition_metrics["accuracy"]:
        best_attrition_model = rf_attrition
        best_attrition_name = "Random Forest"
    else:
        best_attrition_model = lr_attrition
        best_attrition_name = "Logistic Regression"

    results["attrition_model"] = {
        "logistic_regression": lr_attrition_metrics,
        "random_forest": rf_attrition_metrics,
        "best_model": best_attrition_name,
    }

    # ── Save best models and artifacts ─────────────────────
    joblib.dump(best_burnout_model, BURNOUT_MODEL_PATH)
    joblib.dump(best_attrition_model, ATTRITION_MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(burnout_encoder, BURNOUT_ENCODER_PATH)
    joblib.dump(attrition_encoder, ATTRITION_ENCODER_PATH)
    joblib.dump(results, METRICS_PATH)

    results["best_burnout_model"] = best_burnout_name
    results["best_attrition_model"] = best_attrition_name
    results["message"] = "Models trained and saved successfully."

    return results


def load_trained_models():
    """
    Load saved models and preprocessing artifacts from disk.

    Returns:
        Tuple of (burnout_model, attrition_model, scaler,
                   burnout_encoder, attrition_encoder) or None if not found
    """
    if not all(os.path.exists(p) for p in [
        BURNOUT_MODEL_PATH, ATTRITION_MODEL_PATH,
        SCALER_PATH, BURNOUT_ENCODER_PATH, ATTRITION_ENCODER_PATH
    ]):
        return None

    burnout_model = joblib.load(BURNOUT_MODEL_PATH)
    attrition_model = joblib.load(ATTRITION_MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    burnout_encoder = joblib.load(BURNOUT_ENCODER_PATH)
    attrition_encoder = joblib.load(ATTRITION_ENCODER_PATH)

    return burnout_model, attrition_model, scaler, burnout_encoder, attrition_encoder


def load_training_metrics():
    """
    Load saved training metrics from disk.

    Returns:
        Dictionary with training metrics or None
    """
    if os.path.exists(METRICS_PATH):
        return joblib.load(METRICS_PATH)
    return None


def models_exist() -> bool:
    """Check if trained models exist on disk."""
    return all(os.path.exists(p) for p in [
        BURNOUT_MODEL_PATH, ATTRITION_MODEL_PATH,
        SCALER_PATH, BURNOUT_ENCODER_PATH, ATTRITION_ENCODER_PATH
    ])
