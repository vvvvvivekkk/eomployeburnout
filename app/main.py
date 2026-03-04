"""
main.py - FastAPI application entry point.

Defines all routes for:
  - Authentication (signup, login, logout)
  - Dashboard
  - Data generation
  - Model training
  - Prediction
  - CSV upload/export
  - PDF report
  - Health check
"""

import os
import io
import pandas as pd
from fastapi import FastAPI, Request, Depends, UploadFile, File, Form
from fastapi.responses import (
    HTMLResponse, RedirectResponse, StreamingResponse, JSONResponse
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.database import get_db, init_db
from app.models import User, EmployeeData, Prediction
from app.dataset_generator import generate_synthetic_dataset, store_dataset_in_db
from app.preprocessing import load_data_from_db, preprocess_data
from app.ml_model import train_models, load_training_metrics, models_exist
from app.prediction import predict_employee
from app.report_generator import generate_pdf_report
from app.utils import (
    hash_password, verify_password, get_current_user,
    require_login, set_flash, get_flash, export_employees_csv
)

# ── App Setup ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="AI-Based Employee Burnout & Attrition Detection System",
    description="HR tool to detect employee burnout and attrition risk using ML",
    version="1.0.0",
)

# Session middleware for authentication
app.add_middleware(SessionMiddleware, secret_key="burnout-detection-secret-key-2026")

# Static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ── Startup Event ──────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()


# ── Template Context Helper ───────────────────────────────
def get_context(request: Request, db: Session, **kwargs):
    """Build template context with user info and flash messages."""
    user = get_current_user(request, db)
    flash_messages = get_flash(request)
    context = {
        "request": request,
        "user": user,
        "flash_messages": flash_messages,
    }
    context.update(kwargs)
    return context


# ══════════════════════════════════════════════════════════
#  AUTHENTICATION ROUTES
# ══════════════════════════════════════════════════════════

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, db: Session = Depends(get_db)):
    """Render signup page."""
    return templates.TemplateResponse("signup.html", get_context(request, db))


@app.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle user registration."""
    # Validate passwords match
    if password != confirm_password:
        set_flash(request, "Passwords do not match.", "error")
        return templates.TemplateResponse("signup.html", get_context(request, db))

    # Validate password length
    if len(password) < 6:
        set_flash(request, "Password must be at least 6 characters.", "error")
        return templates.TemplateResponse("signup.html", get_context(request, db))

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        set_flash(request, "Username already exists.", "error")
        return templates.TemplateResponse("signup.html", get_context(request, db))

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        set_flash(request, "Email already registered.", "error")
        return templates.TemplateResponse("signup.html", get_context(request, db))

    # Create user
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.add(new_user)
    db.commit()

    set_flash(request, "Account created successfully! Please login.", "success")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """Render login page."""
    return templates.TemplateResponse("login.html", get_context(request, db))


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle user login."""
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()

    if not user or not verify_password(password, user.password_hash):
        set_flash(request, "Invalid username or password.", "error")
        return templates.TemplateResponse("login.html", get_context(request, db))

    # Set session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    set_flash(request, f"Welcome back, {user.username}!", "success")
    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    """Handle user logout."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


# ══════════════════════════════════════════════════════════
#  INDEX / HOME
# ══════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Home page — redirect to dashboard if logged in, else to login."""
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("index.html", get_context(request, db))


# ══════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Render the main dashboard with charts and statistics."""
    redirect = require_login(request)
    if redirect:
        return redirect

    # Gather statistics
    total_employees = db.query(EmployeeData).count()
    total_predictions = db.query(Prediction).count()

    # Burnout distribution
    employees = db.query(EmployeeData).all()
    burnout_counts = {"Low": 0, "Medium": 0, "High": 0}
    attrition_counts = {"Stay": 0, "Leave": 0}
    salary_burnout_data = []

    for emp in employees:
        if emp.burnout_level in burnout_counts:
            burnout_counts[emp.burnout_level] += 1
        if emp.attrition_status in attrition_counts:
            attrition_counts[emp.attrition_status] += 1
        salary_burnout_data.append({
            "salary": emp.salary,
            "burnout": emp.burnout_level,
        })

    # Prediction risk counts
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(20).all()
    all_predictions = db.query(Prediction).all()
    high_risk_count = sum(1 for p in all_predictions if p.risk_level == "High Risk")

    # Training metrics
    metrics = load_training_metrics()
    model_trained = models_exist()

    context = get_context(
        request, db,
        total_employees=total_employees,
        total_predictions=total_predictions,
        burnout_counts=burnout_counts,
        attrition_counts=attrition_counts,
        salary_burnout_data=salary_burnout_data,
        high_risk_count=high_risk_count,
        recent_predictions=predictions,
        metrics=metrics,
        model_trained=model_trained,
    )
    return templates.TemplateResponse("dashboard.html", context)


# ══════════════════════════════════════════════════════════
#  DATA GENERATION
# ══════════════════════════════════════════════════════════

@app.get("/generate-data")
async def generate_data(request: Request, db: Session = Depends(get_db)):
    """Generate synthetic employee dataset and store in database."""
    redirect = require_login(request)
    if redirect:
        return redirect

    # Clear existing employee data
    db.query(EmployeeData).delete()
    db.commit()

    # Generate and store
    df = generate_synthetic_dataset(2000)
    count = store_dataset_in_db(df, db)

    set_flash(request, f"Successfully generated {count} employee records.", "success")
    return RedirectResponse(url="/dashboard", status_code=303)


# ══════════════════════════════════════════════════════════
#  MODEL TRAINING
# ══════════════════════════════════════════════════════════

@app.get("/train")
async def train(request: Request, db: Session = Depends(get_db)):
    """Train ML models on employee data."""
    redirect = require_login(request)
    if redirect:
        return redirect

    # Load data
    df = load_data_from_db(db)
    if df.empty:
        set_flash(request, "No employee data found. Please generate or upload data first.", "error")
        return RedirectResponse(url="/dashboard", status_code=303)

    # Preprocess
    try:
        (X_train, X_test, y_train_burnout, y_test_burnout,
         y_train_attrition, y_test_attrition,
         scaler, burnout_encoder, attrition_encoder) = preprocess_data(df)
    except Exception as e:
        set_flash(request, f"Preprocessing error: {str(e)}", "error")
        return RedirectResponse(url="/dashboard", status_code=303)

    # Train models
    try:
        results = train_models(
            X_train, X_test,
            y_train_burnout, y_test_burnout,
            y_train_attrition, y_test_attrition,
            scaler, burnout_encoder, attrition_encoder,
        )
    except Exception as e:
        set_flash(request, f"Training error: {str(e)}", "error")
        return RedirectResponse(url="/dashboard", status_code=303)

    set_flash(request, "Models trained successfully!", "success")
    return RedirectResponse(url="/dashboard", status_code=303)


# ══════════════════════════════════════════════════════════
#  PREDICTION
# ══════════════════════════════════════════════════════════

@app.get("/prediction", response_class=HTMLResponse)
async def prediction_page(request: Request, db: Session = Depends(get_db)):
    """Render prediction form."""
    redirect = require_login(request)
    if redirect:
        return redirect

    return templates.TemplateResponse("prediction.html", get_context(
        request, db, model_trained=models_exist()
    ))


@app.post("/predict")
async def predict(
    request: Request,
    working_hours: float = Form(...),
    overtime: str = Form(...),
    job_satisfaction: int = Form(...),
    salary: float = Form(...),
    performance_rating: int = Form(...),
    years_at_company: int = Form(...),
    db: Session = Depends(get_db),
):
    """Make prediction for a single employee."""
    redirect = require_login(request)
    if redirect:
        return redirect

    data = {
        "working_hours": working_hours,
        "overtime": overtime,
        "job_satisfaction": job_satisfaction,
        "salary": salary,
        "performance_rating": performance_rating,
        "years_at_company": years_at_company,
    }

    try:
        result = predict_employee(data, db)
    except ValueError as e:
        set_flash(request, str(e), "error")
        return RedirectResponse(url="/prediction", status_code=303)
    except Exception as e:
        set_flash(request, f"Prediction error: {str(e)}", "error")
        return RedirectResponse(url="/prediction", status_code=303)

    set_flash(request, "Prediction completed successfully!", "success")
    return templates.TemplateResponse("prediction.html", get_context(
        request, db, result=result, model_trained=models_exist()
    ))


# ══════════════════════════════════════════════════════════
#  CSV UPLOAD
# ══════════════════════════════════════════════════════════

@app.post("/upload-csv")
async def upload_csv(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a CSV file with employee data."""
    redirect = require_login(request)
    if redirect:
        return redirect

    if not file.filename.endswith(".csv"):
        set_flash(request, "Please upload a CSV file.", "error")
        return RedirectResponse(url="/dashboard", status_code=303)

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Validate required columns
        required_cols = [
            "working_hours", "overtime", "job_satisfaction",
            "salary", "performance_rating", "years_at_company"
        ]
        optional_cols = ["burnout_level", "attrition_status"]

        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            set_flash(request, f"Missing columns: {', '.join(missing_cols)}", "error")
            return RedirectResponse(url="/dashboard", status_code=303)

        # Add optional columns if they don't exist
        for col in optional_cols:
            if col not in df.columns:
                df[col] = None

        all_cols = required_cols + optional_cols

        # Store in database
        count = store_dataset_in_db(df[all_cols], db)
        set_flash(request, f"Successfully uploaded {count} records from CSV.", "success")

    except Exception as e:
        set_flash(request, f"Upload error: {str(e)}", "error")

    return RedirectResponse(url="/dashboard", status_code=303)


# ══════════════════════════════════════════════════════════
#  CSV EXPORT
# ══════════════════════════════════════════════════════════

@app.get("/export-csv")
async def export_csv(request: Request, db: Session = Depends(get_db)):
    """Export employee data as CSV download."""
    redirect = require_login(request)
    if redirect:
        return redirect

    csv_buffer = export_employees_csv(db)
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=employee_data.csv"},
    )


# ══════════════════════════════════════════════════════════
#  PDF REPORT
# ══════════════════════════════════════════════════════════

@app.get("/report")
async def report(request: Request, db: Session = Depends(get_db)):
    """Generate and download PDF report."""
    redirect = require_login(request)
    if redirect:
        return redirect

    try:
        pdf_buffer = generate_pdf_report(db)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=burnout_report.pdf"},
        )
    except Exception as e:
        set_flash(request, f"Report generation error: {str(e)}", "error")
        return RedirectResponse(url="/dashboard", status_code=303)


# ══════════════════════════════════════════════════════════
#  HEALTH CHECK
# ══════════════════════════════════════════════════════════

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    Returns database status, counts, and model status.
    """
    try:
        employee_count = db.query(EmployeeData).count()
        prediction_count = db.query(Prediction).count()
        db_status = "connected"
    except Exception:
        employee_count = 0
        prediction_count = 0
        db_status = "disconnected"

    model_status = {
        "burnout_model": models_exist(),
        "attrition_model": models_exist(),
        "trained": models_exist(),
    }

    return {
        "status": "healthy",
        "database_status": db_status,
        "number_of_employees": employee_count,
        "number_of_predictions": prediction_count,
        "model_status": model_status,
    }


# ══════════════════════════════════════════════════════════
#  API ENDPOINTS (JSON)
# ══════════════════════════════════════════════════════════

@app.get("/api/dashboard-data")
async def dashboard_data(request: Request, db: Session = Depends(get_db)):
    """Return dashboard data as JSON for Chart.js."""
    redirect = require_login(request)
    if redirect:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    employees = db.query(EmployeeData).all()
    burnout_counts = {"Low": 0, "Medium": 0, "High": 0}
    attrition_counts = {"Stay": 0, "Leave": 0}
    salary_burnout = []

    for emp in employees:
        if emp.burnout_level in burnout_counts:
            burnout_counts[emp.burnout_level] += 1
        if emp.attrition_status in attrition_counts:
            attrition_counts[emp.attrition_status] += 1
        salary_burnout.append({
            "salary": emp.salary,
            "burnout": emp.burnout_level,
        })

    metrics = load_training_metrics()

    return {
        "burnout_counts": burnout_counts,
        "attrition_counts": attrition_counts,
        "salary_burnout": salary_burnout,
        "metrics": metrics,
        "total_employees": len(employees),
    }
