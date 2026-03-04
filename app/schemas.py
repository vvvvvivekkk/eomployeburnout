"""
schemas.py - Pydantic schemas for request/response validation.

Defines data transfer objects for API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ─── User Schemas ────────────────────────────────────────────

class UserSignup(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# ─── Employee Data Schemas ───────────────────────────────────

class EmployeeDataSchema(BaseModel):
    """Schema for employee data input."""
    working_hours: float = Field(..., ge=35, le=70)
    overtime: str = Field(..., pattern="^(Yes|No)$")
    job_satisfaction: int = Field(..., ge=1, le=5)
    salary: float = Field(..., ge=20000, le=150000)
    performance_rating: int = Field(..., ge=1, le=5)
    years_at_company: int = Field(..., ge=0, le=20)


# ─── Prediction Schemas ─────────────────────────────────────

class PredictionInput(BaseModel):
    """Schema for prediction request."""
    working_hours: float = Field(..., ge=35, le=70)
    overtime: str = Field(..., pattern="^(Yes|No)$")
    job_satisfaction: int = Field(..., ge=1, le=5)
    salary: float = Field(..., ge=20000, le=150000)
    performance_rating: int = Field(..., ge=1, le=5)
    years_at_company: int = Field(..., ge=0, le=20)


class PredictionResponse(BaseModel):
    """Schema for prediction response."""
    predicted_burnout: str
    predicted_attrition: str
    risk_level: str
    working_hours: float
    overtime: str
    job_satisfaction: int
    salary: float
    performance_rating: int
    years_at_company: int


# ─── Training Response Schema ───────────────────────────────

class TrainingResponse(BaseModel):
    """Schema for training response."""
    message: str
    burnout_model: dict
    attrition_model: dict
    best_burnout_model: str
    best_attrition_model: str


# ─── Health Check Schema ────────────────────────────────────

class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    database_status: str
    number_of_employees: int
    number_of_predictions: int
    model_status: dict
