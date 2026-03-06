# Handling Database

This guide provides common database questions and quick answers for this project.

Database used: SQLite (`employee_data.db`)

Tables:
- `users`
- `employee_data`
- `predictions`

## 1. How do I access all data from the database?
Use a Python shell in the project root:

```python
from app.database import SessionLocal
from app.models import User, EmployeeData, Prediction

db = SessionLocal()

users = db.query(User).all()
employees = db.query(EmployeeData).all()
predictions = db.query(Prediction).all()

print("Users:", len(users))
print("Employees:", len(employees))
print("Predictions:", len(predictions))

db.close()
```

## 2. How do I remove a user?
Remove by `id`:

```python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
user_id = 1

db.query(User).filter(User.id == user_id).delete()
db.commit()
db.close()
```

Remove by `username`:

```python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
username = "john"

db.query(User).filter(User.username == username).delete()
db.commit()
db.close()
```

## 3. How do I remove a prediction record?
Remove one prediction by `id`:

```python
from app.database import SessionLocal
from app.models import Prediction

db = SessionLocal()
prediction_id = 10

db.query(Prediction).filter(Prediction.id == prediction_id).delete()
db.commit()
db.close()
```

Remove all predictions:

```python
from app.database import SessionLocal
from app.models import Prediction

db = SessionLocal()

db.query(Prediction).delete()
db.commit()
db.close()
```

## 4. How do I check predictions?
Get latest 20 predictions:

```python
from app.database import SessionLocal
from app.models import Prediction

db = SessionLocal()

recent = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(20).all()
for p in recent:
    print(p.id, p.predicted_burnout, p.predicted_attrition, p.risk_level, p.created_at)

db.close()
```

Get count of high-risk predictions:

```python
from app.database import SessionLocal
from app.models import Prediction

db = SessionLocal()
high_risk_count = db.query(Prediction).filter(Prediction.risk_level == "High Risk").count()
print("High risk predictions:", high_risk_count)
db.close()
```

## 5. How do I clear employee data only?

```python
from app.database import SessionLocal
from app.models import EmployeeData

db = SessionLocal()

db.query(EmployeeData).delete()
db.commit()
db.close()
```

## 6. How can I quickly check DB status from the app?
Start the app and open:
- `GET /health` -> shows DB and model status
- `GET /dashboard` -> shows total employees and total predictions

## 7. Safety tip before delete operations
Always back up `employee_data.db` before bulk deletes.

Example (PowerShell):

```powershell
Copy-Item .\employee_data.db .\employee_data_backup.db
```
