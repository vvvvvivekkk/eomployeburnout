"""
utils.py - Utility functions.

Provides:
  - Password hashing and verification (bcrypt via passlib)
  - Session authentication helpers
  - CSV export utility
  - Flash message helpers
"""

import io
import csv
import bcrypt
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models import User, EmployeeData


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def get_current_user(request: Request, db: Session):
    """
    Get the currently logged-in user from session.

    Args:
        request: Starlette/FastAPI request
        db: SQLAlchemy session

    Returns:
        User object or None if not logged in
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    user = db.query(User).filter(User.id == user_id).first()
    return user


def require_login(request: Request):
    """
    Check if user is logged in. Returns RedirectResponse to login if not.

    Args:
        request: Starlette/FastAPI request

    Returns:
        RedirectResponse if not logged in, None otherwise
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        return RedirectResponse(url="/login", status_code=303)
    return None


def set_flash(request: Request, message: str, category: str = "info"):
    """
    Set a flash message in the session.

    Args:
        request: Starlette/FastAPI request
        message: Flash message text
        category: Message category (success, error, info, warning)
    """
    if "flash_messages" not in request.session:
        request.session["flash_messages"] = []
    request.session["flash_messages"].append({
        "message": message,
        "category": category
    })


def get_flash(request: Request) -> list:
    """
    Get and clear flash messages from session.

    Args:
        request: Starlette/FastAPI request

    Returns:
        List of flash message dicts
    """
    messages = request.session.pop("flash_messages", [])
    return messages


def export_employees_csv(db: Session) -> io.StringIO:
    """
    Export all employee data to CSV format.

    Args:
        db: SQLAlchemy session

    Returns:
        StringIO buffer containing CSV data
    """
    employees = db.query(EmployeeData).all()
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "working_hours", "overtime", "job_satisfaction",
        "salary", "performance_rating", "years_at_company",
        "burnout_level", "attrition_status"
    ])

    # Data rows
    for emp in employees:
        writer.writerow([
            emp.working_hours, emp.overtime, emp.job_satisfaction,
            emp.salary, emp.performance_rating, emp.years_at_company,
            emp.burnout_level, emp.attrition_status
        ])

    output.seek(0)
    return output
