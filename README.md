# 🧠 AI-Based Employee Burnout & Attrition Detection System

A full-stack web application that helps HR teams detect employee burnout and attrition risk early using machine learning analysis.

---

## 📋 Project Overview

This system uses **Logistic Regression** and **Random Forest** classifiers to predict:
- **Burnout Level** (Low / Medium / High)
- **Attrition Status** (Stay / Leave)
- **Overall Risk Level** (Low Risk / Medium Risk / High Risk)

It features an interactive dashboard with real-time charts, PDF reporting, CSV import/export, and session-based authentication.

---

## 🏗️ System Architecture

```
employee-burnout-system/
├── app/
│   ├── main.py                # FastAPI routes & app entry point
│   ├── database.py            # SQLAlchemy + SQLite configuration
│   ├── models.py              # ORM models (User, EmployeeData, Prediction)
│   ├── schemas.py             # Pydantic validation schemas
│   ├── dataset_generator.py   # Synthetic dataset generation (2000 records)
│   ├── preprocessing.py       # Data cleaning, encoding, scaling, splitting
│   ├── ml_model.py            # Model training, evaluation, saving
│   ├── prediction.py          # Single-employee prediction with risk logic
│   ├── report_generator.py    # PDF report generation (ReportLab)
│   └── utils.py               # Auth helpers, password hashing, CSV export
├── templates/
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   ├── index.html             # Landing page
│   ├── dashboard.html         # Main dashboard with charts
│   └── prediction.html        # Prediction form & results
├── static/
│   ├── css/style.css          # Application styles
│   └── js/dashboard.js        # Chart.js visualizations
├── uploads/                   # Uploaded CSV files
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── employee_data.db           # SQLite database (auto-created)
```

---

## 🛠️ Tech Stack

| Component          | Technology                    |
|--------------------|-------------------------------|
| Backend Framework  | FastAPI                       |
| Database           | SQLite + SQLAlchemy ORM       |
| Machine Learning   | Scikit-learn                  |
| Data Processing    | Pandas, NumPy                 |
| Visualization      | Chart.js                      |
| Templating         | Jinja2 (FastAPI templates)    |
| Model Persistence  | Joblib                        |
| PDF Reports        | ReportLab                     |
| Authentication     | Session-based (Starlette)     |
| Password Hashing   | Passlib with bcrypt           |
| File Upload        | python-multipart              |
| API Documentation  | Swagger UI (auto via FastAPI) |

---

## 📦 Installation Steps

### 1. Clone or navigate to the project

```bash
cd employee-burnout-system
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Open in browser

```
http://127.0.0.1:8000
```

---

## 🚀 How to Use

1. **Sign Up** — Create a new account
2. **Login** — Authenticate with your credentials
3. **Generate Dataset** — Click "Generate Dataset" to create 2000 synthetic employee records
4. **Train Model** — Click "Train Model" to train Logistic Regression & Random Forest classifiers
5. **Predict** — Enter employee details to get burnout/attrition predictions
6. **Upload CSV** — Upload your own employee dataset
7. **Download Reports** — Export CSV data or generate a PDF report

---

## 📡 API Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Key API Endpoints

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| GET    | `/health`        | Health check with system status    |
| POST   | `/signup`        | User registration                  |
| POST   | `/login`         | User authentication                |
| GET    | `/logout`        | End user session                   |
| GET    | `/dashboard`     | Main dashboard                     |
| GET    | `/generate-data` | Generate synthetic dataset         |
| GET    | `/train`         | Train ML models                    |
| POST   | `/predict`       | Make burnout/attrition prediction  |
| POST   | `/upload-csv`    | Upload CSV employee data           |
| GET    | `/export-csv`    | Download employee data as CSV      |
| GET    | `/report`        | Download PDF report                |

---

## 🤖 Machine Learning Explanation

### Features Used
- `working_hours` (35–70)
- `overtime` (Yes/No → encoded as 1/0)
- `job_satisfaction` (1–5)
- `salary` ($20,000–$150,000)
- `performance_rating` (1–5)
- `years_at_company` (0–20)

### Preprocessing Pipeline
1. Remove duplicate records
2. Handle missing values
3. Encode categorical variables (overtime)
4. Apply StandardScaler normalization
5. Train/Test split (80/20)

### Models Trained
- **Logistic Regression** — Linear classification baseline
- **Random Forest Classifier** — Ensemble method for better accuracy

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

The system automatically selects the **best model** per target based on highest accuracy.

### Risk Classification Logic
- **High Risk**: Burnout = High OR Attrition = Leave
- **Medium Risk**: Burnout = Medium
- **Low Risk**: Otherwise

---

## 📸 Screenshots

> Screenshots can be added here after running the application.

- Landing Page
- Login / Signup
- Dashboard with Charts
- Prediction Form & Results
- PDF Report

---

## 🔮 Future Improvements

- [ ] Add more ML models (SVM, XGBoost, Neural Networks)
- [ ] Implement role-based access control (Admin, HR Manager, Viewer)
- [ ] Add email notifications for high-risk employees
- [ ] Time-series analysis for burnout trends
- [ ] REST API with JWT authentication for external integrations
- [ ] Docker containerization for easy deployment
- [ ] Employee profile pages with historical predictions
- [ ] Batch prediction from CSV upload
- [ ] A/B testing for model comparison
- [ ] Integration with HRIS systems

---

## 📄 License

This project is for educational and demonstration purposes.

---

Built with ❤️ using FastAPI, Scikit-learn, and Chart.js
