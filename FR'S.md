Abstract 
In modern organizations, employee stress and turnover are major challenges that affect productivity and growth. Continuous workload, overtime, low job satisfaction, and lack of work-life balance can lead to employee burnout, which may further result in attrition. Early detection of these issues can help organizations take preventive measures.
This project presents a simplified AI-based Employee Burnout and Attrition Detection System developed using machine learning techniques. The system analyzes employee-related attributes such as working hours, overtime, job satisfaction, salary, performance rating, and years at the company. It supports dataset upload in CSV format and performs basic data preprocessing, exploratory analysis, and prediction.
The system is implemented using Python, Flask, and Scikit-learn. It uses classification algorithms such as Logistic Regression and Random Forest to predict employee burnout levels (Low/Medium/High) and attrition status (Stay/Leave). The application provides a simple dashboard to display prediction results and basic analytics. This system helps HR teams identify high-risk employees and take early action to reduce turnover and improve employee well-being.
Functional Requirements (Simplified for One Week Implementation)
1. User Management
FR1: The system shall allow users to log in using a basic authentication system.
FR2: The system shall allow users to log out securely.
2. Employee Data Upload
FR3: The system shall allow users to upload employee datasets in CSV format.
FR4: The system shall store uploaded data for analysis.
3. Data Preprocessing
FR5: The system shall handle missing values in the dataset.
FR6: The system shall remove duplicate records.
FR7: The system shall encode categorical variables and scale numerical features before model training.
4. Exploratory Data Analysis
FR8: The system shall generate basic descriptive statistics.
FR9: The system shall display simple visualizations such as bar charts and pie charts for burnout and attrition distribution.
5. Machine Learning & Prediction
(Using 2 classification algorithms)
FR10: The system shall implement Logistic Regression for prediction.
FR11: The system shall implement Random Forest for prediction.
FR12: The system shall train and test models using employee data.
FR13: The system shall display performance metrics such as Accuracy and Confusion Matrix.
FR14: The system shall predict employee burnout levels (Low / Medium / High).
FR15: The system shall predict employee attrition status (Stay / Leave).
FR16: The system shall allow prediction for new employee input data through a form.
6. Dashboard & Results
FR17: The system shall display prediction results clearly on the screen.
FR18: The system shall highlight high-risk employees.
FR19: The system shall show overall burnout and attrition statistics in graphical form.
7. Reporting
FR20: The system shall allow exporting prediction results in CSV format.