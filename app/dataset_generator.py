"""
dataset_generator.py - Synthetic employee dataset generation.

Generates 2000 synthetic employee records with realistic burnout
and attrition labels based on domain-driven rules.
"""

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from app.models import EmployeeData


def generate_synthetic_dataset(n_records: int = 2000) -> pd.DataFrame:
    """
    Generate a synthetic employee dataset.

    Burnout logic:
      - Higher working hours increase burnout
      - Overtime increases burnout
      - Low job satisfaction increases burnout
      - Low salary increases burnout

    Attrition logic:
      - High burnout increases attrition
      - Low salary increases attrition
      - Low performance rating increases attrition

    Args:
        n_records: Number of records to generate (default 2000)

    Returns:
        DataFrame with generated employee data
    """
    np.random.seed(42)

    # ── Generate features ──────────────────────────────────
    working_hours = np.random.uniform(35, 70, n_records).round(1)
    overtime = np.random.choice(["Yes", "No"], n_records, p=[0.35, 0.65])
    job_satisfaction = np.random.randint(1, 6, n_records)      # 1-5
    salary = np.random.uniform(20000, 150000, n_records).round(2)
    performance_rating = np.random.randint(1, 6, n_records)    # 1-5
    years_at_company = np.random.randint(0, 21, n_records)     # 0-20

    # ── Compute burnout score (0-100 scale) ────────────────
    burnout_score = np.zeros(n_records)

    # Working hours contribution (35-70 mapped to 0-30)
    burnout_score += ((working_hours - 35) / 35) * 30

    # Overtime contribution (+15 if Yes)
    burnout_score += np.where(overtime == "Yes", 15, 0)

    # Job satisfaction contribution (inverse: 5→0, 1→25)
    burnout_score += ((5 - job_satisfaction) / 4) * 25

    # Salary contribution (inverse: high salary→0, low→20)
    burnout_score += ((150000 - salary) / 130000) * 20

    # Add noise
    burnout_score += np.random.normal(0, 5, n_records)
    burnout_score = np.clip(burnout_score, 0, 100)

    # ── Classify burnout level ─────────────────────────────
    burnout_level = np.where(
        burnout_score >= 60, "High",
        np.where(burnout_score >= 35, "Medium", "Low")
    )

    # ── Compute attrition probability ──────────────────────
    attrition_prob = np.zeros(n_records)

    # Burnout contribution
    attrition_prob += np.where(burnout_level == "High", 0.4, 
                      np.where(burnout_level == "Medium", 0.15, 0.05))

    # Salary contribution (lower salary → higher attrition)
    attrition_prob += ((150000 - salary) / 130000) * 0.25

    # Performance rating contribution (low rating → higher attrition)
    attrition_prob += ((5 - performance_rating) / 4) * 0.2

    # Add noise
    attrition_prob += np.random.normal(0, 0.05, n_records)
    attrition_prob = np.clip(attrition_prob, 0, 1)

    # ── Classify attrition status ──────────────────────────
    attrition_status = np.where(attrition_prob >= 0.45, "Leave", "Stay")

    # ── Build DataFrame ────────────────────────────────────
    df = pd.DataFrame({
        "working_hours": working_hours,
        "overtime": overtime,
        "job_satisfaction": job_satisfaction,
        "salary": salary,
        "performance_rating": performance_rating,
        "years_at_company": years_at_company,
        "burnout_level": burnout_level,
        "attrition_status": attrition_status,
    })

    return df


def store_dataset_in_db(df: pd.DataFrame, db: Session) -> int:
    """
    Store a DataFrame of employee records into the database.

    Args:
        df: DataFrame with employee data
        db: SQLAlchemy session

    Returns:
        Number of records inserted
    """
    records = []
    for _, row in df.iterrows():
        record = EmployeeData(
            working_hours=float(row["working_hours"]),
            overtime=str(row["overtime"]),
            job_satisfaction=int(row["job_satisfaction"]),
            salary=float(row["salary"]),
            performance_rating=int(row["performance_rating"]),
            years_at_company=int(row["years_at_company"]),
            burnout_level=str(row["burnout_level"]),
            attrition_status=str(row["attrition_status"]),
        )
        records.append(record)

    db.bulk_save_objects(records)
    db.commit()
    return len(records)
