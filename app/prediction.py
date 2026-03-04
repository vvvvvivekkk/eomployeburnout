"""
prediction.py - Prediction module.

Loads trained models and makes predictions for individual employees.
Computes risk level based on burnout and attrition predictions.
Stores predictions in the database.
"""

import logging
import numpy as np
from sqlalchemy.orm import Session
from app.ml_model import load_trained_models
from app.preprocessing import preprocess_single_input
from app.models import Prediction

logger = logging.getLogger(__name__)


def compute_risk_level(predicted_burnout: str, predicted_attrition: str) -> str:
    """
    Compute overall risk level based on predicted burnout and attrition.

    Risk logic:
      - If burnout = High OR attrition = Leave → High Risk
      - If burnout = Medium → Medium Risk
      - Else → Low Risk

    Args:
        predicted_burnout: Predicted burnout level (Low/Medium/High)
        predicted_attrition: Predicted attrition status (Stay/Leave)

    Returns:
        Risk level string: "High Risk", "Medium Risk", or "Low Risk"
    """
    if predicted_burnout == "High" or predicted_attrition == "Leave":
        return "High Risk"
    elif predicted_burnout == "Medium":
        return "Medium Risk"
    else:
        return "Low Risk"


def predict_employee(data: dict, db: Session) -> dict:
    """
    Make burnout and attrition predictions for a single employee.

    Args:
        data: Dictionary with employee features
        db: SQLAlchemy session

    Returns:
        Dictionary with prediction results

    Raises:
        ValueError: If models are not trained yet
    """
    # Load trained models
    models = load_trained_models()
    if models is None:
        raise ValueError("Models are not trained yet. Please train models first.")

    burnout_model, attrition_model, scaler, burnout_encoder, attrition_encoder = models

    # Preprocess input
    X = preprocess_single_input(data, scaler)

    # Make predictions
    burnout_pred = burnout_model.predict(X)[0]
    attrition_pred = attrition_model.predict(X)[0]

    # Decode predictions
    predicted_burnout = burnout_encoder.inverse_transform([burnout_pred])[0]
    predicted_attrition = attrition_encoder.inverse_transform([attrition_pred])[0]

    # Compute risk level
    risk_level = compute_risk_level(predicted_burnout, predicted_attrition)

    # Log prediction results
    logger.info("=== New Prediction ===")
    logger.info(f"Input: working_hours={data['working_hours']}, overtime={data['overtime']}, "
                f"satisfaction={data['job_satisfaction']}, salary={data['salary']}, "
                f"performance={data['performance_rating']}, years={data['years_at_company']}")
    logger.info(f"Predicted Burnout: {predicted_burnout}")
    logger.info(f"Predicted Attrition: {predicted_attrition}")
    logger.info(f"Risk Level: {risk_level}")

    # Store prediction in database
    prediction_record = Prediction(
        working_hours=data["working_hours"],
        overtime=data["overtime"],
        job_satisfaction=data["job_satisfaction"],
        salary=data["salary"],
        performance_rating=data["performance_rating"],
        years_at_company=data["years_at_company"],
        predicted_burnout=predicted_burnout,
        predicted_attrition=predicted_attrition,
        risk_level=risk_level,
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return {
        "predicted_burnout": predicted_burnout,
        "predicted_attrition": predicted_attrition,
        "risk_level": risk_level,
        "working_hours": data["working_hours"],
        "overtime": data["overtime"],
        "job_satisfaction": data["job_satisfaction"],
        "salary": data["salary"],
        "performance_rating": data["performance_rating"],
        "years_at_company": data["years_at_company"],
    }
