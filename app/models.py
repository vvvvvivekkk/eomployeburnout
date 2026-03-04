"""
models.py - SQLAlchemy ORM models.

Defines three tables:
  - users: Authentication and user management
  - employee_data: Stored employee records (synthetic or uploaded)
  - predictions: Prediction results from ML models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class EmployeeData(Base):
    """Employee data model for storing employee records."""
    __tablename__ = "employee_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    working_hours = Column(Float, nullable=False)
    overtime = Column(String, nullable=False)          # "Yes" or "No"
    job_satisfaction = Column(Integer, nullable=False)  # 1-5
    salary = Column(Float, nullable=False)
    performance_rating = Column(Integer, nullable=False)  # 1-5
    years_at_company = Column(Integer, nullable=False)
    burnout_level = Column(String, nullable=False)     # Low, Medium, High
    attrition_status = Column(String, nullable=False)  # Stay, Leave


class Prediction(Base):
    """Prediction model for storing ML prediction results."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    working_hours = Column(Float, nullable=False)
    overtime = Column(String, nullable=False)
    job_satisfaction = Column(Integer, nullable=False)
    salary = Column(Float, nullable=False)
    performance_rating = Column(Integer, nullable=False)
    years_at_company = Column(Integer, nullable=False)
    predicted_burnout = Column(String, nullable=False)    # Low, Medium, High
    predicted_attrition = Column(String, nullable=False)  # Stay, Leave
    risk_level = Column(String, nullable=False)           # Low, Medium, High
    created_at = Column(DateTime, server_default=func.now())
