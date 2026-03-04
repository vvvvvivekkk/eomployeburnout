"""
preprocessing.py - Data preprocessing pipeline.

Handles:
  - Duplicate removal
  - Missing value imputation
  - Categorical encoding (overtime Yes/No)
  - StandardScaler normalization
  - Train/Test split (80/20)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sqlalchemy.orm import Session
from app.models import EmployeeData


def load_data_from_db(db: Session) -> pd.DataFrame:
    """
    Load all employee records from the database into a DataFrame.

    Args:
        db: SQLAlchemy session

    Returns:
        DataFrame with employee data
    """
    records = db.query(EmployeeData).all()
    if not records:
        return pd.DataFrame()

    data = [{
        "working_hours": r.working_hours,
        "overtime": r.overtime,
        "job_satisfaction": r.job_satisfaction,
        "salary": r.salary,
        "performance_rating": r.performance_rating,
        "years_at_company": r.years_at_company,
        "burnout_level": r.burnout_level,
        "attrition_status": r.attrition_status,
    } for r in records]

    return pd.DataFrame(data)


def preprocess_data(df: pd.DataFrame):
    """
    Full preprocessing pipeline.

    Steps:
      1. Remove duplicate records
      2. Handle missing values (drop rows with NaN)
      3. Encode overtime column (Yes=1, No=0)
      4. Encode target labels
      5. Apply StandardScaler normalization
      6. Train/Test split (80/20)

    Args:
        df: Raw employee DataFrame

    Returns:
        Tuple of (X_train, X_test, y_train_burnout, y_test_burnout,
                   y_train_attrition, y_test_attrition, scaler,
                   burnout_encoder, attrition_encoder)
    """
    # Step 1: Remove duplicates
    df = df.drop_duplicates()

    # Step 2: Handle missing values
    df = df.dropna()

    # Step 3: Encode overtime (Yes=1, No=0)
    df = df.copy()
    df["overtime_encoded"] = df["overtime"].map({"Yes": 1, "No": 0})

    # Step 4: Encode target labels
    burnout_encoder = LabelEncoder()
    attrition_encoder = LabelEncoder()

    df["burnout_encoded"] = burnout_encoder.fit_transform(df["burnout_level"])
    df["attrition_encoded"] = attrition_encoder.fit_transform(df["attrition_status"])

    # Step 5: Select features and targets
    feature_columns = [
        "working_hours", "overtime_encoded", "job_satisfaction",
        "salary", "performance_rating", "years_at_company"
    ]
    X = df[feature_columns].values
    y_burnout = df["burnout_encoded"].values
    y_attrition = df["attrition_encoded"].values

    # Step 6: Apply StandardScaler normalization
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 7: Train/Test split (80/20)
    X_train, X_test, y_train_burnout, y_test_burnout = train_test_split(
        X_scaled, y_burnout, test_size=0.2, random_state=42, stratify=y_burnout
    )
    _, _, y_train_attrition, y_test_attrition = train_test_split(
        X_scaled, y_attrition, test_size=0.2, random_state=42, stratify=y_attrition
    )

    return (
        X_train, X_test,
        y_train_burnout, y_test_burnout,
        y_train_attrition, y_test_attrition,
        scaler, burnout_encoder, attrition_encoder
    )


def preprocess_single_input(data: dict, scaler: StandardScaler) -> np.ndarray:
    """
    Preprocess a single employee input for prediction.

    Args:
        data: Dictionary with employee features
        scaler: Fitted StandardScaler

    Returns:
        Scaled feature array ready for prediction
    """
    overtime_encoded = 1 if data["overtime"] == "Yes" else 0

    features = np.array([[
        data["working_hours"],
        overtime_encoded,
        data["job_satisfaction"],
        data["salary"],
        data["performance_rating"],
        data["years_at_company"],
    ]])

    return scaler.transform(features)
