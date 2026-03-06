<div align="center">

# AI-Based Employee Attrition Detection System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

An intelligent HR analytics platform that leverages machine learning to identify employees at risk of attrition — enabling proactive intervention and improved workforce well-being.

[Getting Started](#installation) · [Usage Guide](#usage-guide) · [API Reference](#api-reference) · [ML Architecture](#machine-learning-architecture)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Data Input Options](#data-input-options)
- [API Reference](#api-reference)
- [Machine Learning Architecture](#machine-learning-architecture)
- [Future Roadmap](#future-roadmap)
- [License](#license)

---

## Overview

Employee attrition is among the most costly challenges facing modern organizations. This system provides HR teams with a **data-driven, predictive solution** that classifies employees into risk tiers based on behavioral and performance indicators.

**The system predicts three key outcomes:**

| Prediction Target   | Output Classes               |
|----------------------|------------------------------|
| Burnout Level        | Low · Medium · High          |
| Attrition Status     | Stay · Leave                 |
| Overall Risk Level   | Low Risk · Medium Risk · High Risk |

---

## Key Features

- **Dual-Model ML Pipeline** — Logistic Regression + Random Forest with automatic best-model selection
- **Interactive Dashboard** — Real-time visualizations powered by Chart.js (attrition breakdown, salary correlation)
- **Flexible Data Input** — Upload your own CSV datasets or generate synthetic data for testing
- **Individual Prediction** — Enter a single employee's details and receive instant risk assessment
- **PDF Report Generation** — Export comprehensive analysis reports via ReportLab
- **CSV Import/Export** — Full data portability with upload and download support
- **Session-Based Authentication** — Secure login/signup with bcrypt password hashing
- **Auto-Generated API Docs** — Swagger UI and ReDoc available out of the box

---

## Tech Stack

| Layer                | Technology                          |
|----------------------|-------------------------------------|
| **Backend**          | FastAPI, Uvicorn, Starlette         |
| **Database**         | SQLite, SQLAlchemy ORM              |
| **Machine Learning** | Scikit-learn, Joblib                |
| **Data Processing**  | Pandas, NumPy                       |
| **Frontend**         | Jinja2 Templates, Chart.js          |
| **Reporting**        | ReportLab (PDF)                     |
| **Security**         | bcrypt, Session Middleware           |
| **File Handling**    | python-multipart                    |

---

## Project Structure

```
employee-attrition-system/
│
├── app/
│   ├── main.py                 # FastAPI routes & application entry point
│   ├── database.py             # SQLAlchemy engine & session configuration
│   ├── models.py               # ORM models (User, EmployeeData, Prediction)
│   ├── schemas.py              # Pydantic validation schemas
│   ├── dataset_generator.py    # Synthetic dataset generation engine
│   ├── preprocessing.py        # Data cleaning, encoding & feature scaling
│   ├── ml_model.py             # Model training, evaluation & persistence
│   ├── prediction.py           # Inference pipeline with risk classification
│   ├── report_generator.py     # PDF report builder (ReportLab)
│   └── utils.py                # Authentication helpers & CSV export utilities
│
├── templates/
│   ├── index.html              # Landing page
│   ├── login.html              # User login
│   ├── signup.html             # User registration
│   ├── dashboard.html          # Analytics dashboard with charts
│   └── prediction.html         # Prediction form & results display
│
├── static/
│   ├── css/style.css           # Application stylesheet
│   └── js/dashboard.js         # Chart.js visualization logic
│
├── uploads/                    # User-uploaded CSV datasets
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/vvvvvivekkk/employeeattrition.git
cd employeeattrition

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate           # Windows
# source venv/bin/activate      # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
uvicorn app.main:app --reload
```

The application will be available at **http://127.0.0.1:8000**

---

## Usage Guide

| Step | Action | Description |
|------|--------|-------------|
| 1    | **Sign Up** | Create a new user account |
| 2    | **Log In** | Authenticate with your credentials |
| 3    | **Load Data** | Generate synthetic data (up to 2,000 records) **or** upload your own CSV |
| 4    | **Train Models** | Train Logistic Regression & Random Forest classifiers on the loaded data |
| 5    | **Predict** | Enter individual employee details to receive attrition predictions |
| 6    | **Analyze** | View dashboard charts for workforce-wide insights |
| 7    | **Export** | Download results as CSV or generate a PDF report |

---

## Data Input Options

The system supports two methods for loading employee data:

### 1. Synthetic Data Generation

Click **"Generate Dataset"** on the dashboard to create realistic synthetic employee records with domain-driven attrition labels.

### 2. CSV File Upload

Upload your own dataset via the **"Upload CSV"** feature. The CSV must include the following columns:

| Column | Type | Range / Values | Required |
|--------|------|----------------|----------|
| `working_hours` | float | 35 – 70 | Yes |
| `overtime` | string | Yes / No | Yes |
| `job_satisfaction` | int | 1 – 5 | Yes |
| `salary` | float | 20,000 – 150,000 | Yes |
| `performance_rating` | int | 1 – 5 | Yes |
| `years_at_company` | int | 0 – 20 | Yes |
| `burnout_level` | string | Low / Medium / High | Optional |
| `attrition_status` | string | Stay / Leave | Optional |

> **Note:** If `burnout_level` and `attrition_status` are omitted, the system will store the data for prediction-only workflows. Include them for training purposes.

A sample file with 1,000 records is available at `uploads/employee_data_1000.csv`.

---

## API Reference

Interactive API documentation is auto-generated at runtime:

- **Swagger UI** — [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** — [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Landing page |
| `GET` | `/health` | Health check with system status |
| `POST` | `/signup` | Register a new user |
| `POST` | `/login` | Authenticate and start session |
| `GET` | `/logout` | End the current session |
| `GET` | `/dashboard` | Main analytics dashboard |
| `GET` | `/generate-data` | Generate synthetic employee dataset |
| `GET` | `/train` | Train ML models on stored data |
| `GET` | `/prediction` | Prediction form page |
| `POST` | `/predict` | Submit employee data for prediction |
| `POST` | `/upload-csv` | Upload a CSV dataset |
| `GET` | `/export-csv` | Download employee data as CSV |
| `GET` | `/report` | Generate and download PDF report |

---

## Machine Learning Architecture

### Feature Engineering

| Feature | Type | Description |
|---------|------|-------------|
| `working_hours` | Continuous | Weekly working hours (35–70) |
| `overtime` | Binary | Encoded as 1 (Yes) / 0 (No) |
| `job_satisfaction` | Ordinal | Self-reported satisfaction (1–5) |
| `salary` | Continuous | Annual compensation ($20K–$150K) |
| `performance_rating` | Ordinal | Manager-assessed rating (1–5) |
| `years_at_company` | Discrete | Tenure in years (0–20) |

### Preprocessing Pipeline

```
Raw Data → Duplicate Removal → Missing Value Imputation → Categorical Encoding → StandardScaler → Train/Test Split (80/20)
```

### Models

| Model | Role | Strengths |
|-------|------|-----------|
| **Logistic Regression** | Baseline classifier | Interpretable, fast training |
| **Random Forest** | Ensemble classifier | Handles non-linearity, higher accuracy |

The system evaluates both models and automatically selects the **best-performing model** for each prediction target based on test accuracy.

### Evaluation Metrics

- **Accuracy** — Overall correct prediction rate
- **Precision** — True positive rate among predicted positives
- **Recall** — True positive rate among actual positives
- **F1 Score** — Harmonic mean of precision and recall
- **Confusion Matrix** — Detailed classification breakdown

### Risk Classification Logic

| Risk Level | Condition |
|------------|-----------|
| **High Risk** | Burnout = High **OR** Attrition = Leave |
| **Medium Risk** | Burnout = Medium |
| **Low Risk** | All other cases |

---

## Future Roadmap

- [ ] Additional ML models (SVM, XGBoost, Neural Networks)
- [ ] Role-based access control (Admin, HR Manager, Viewer)
- [ ] Email notifications for high-risk employees
- [ ] Time-series analysis for attrition trend tracking
- [ ] JWT-based REST API for external integrations
- [ ] Docker containerization for streamlined deployment
- [ ] Employee profile pages with prediction history
- [ ] Batch prediction from CSV upload
- [ ] Model comparison and A/B testing framework
- [ ] HRIS system integration

---

## License

This project is developed for educational and demonstration purposes.

---

<div align="center">

**Built with FastAPI · Scikit-learn · Chart.js**

</div>
