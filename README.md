# Flask--taks-tracker
This is my final project on the flask framework.

A simple task management web application built with Flask. 

Features

- ✅ User authentication (Login/Register)
- ❌ Delete tasks
- Mark tasks as complete 
- 👁️ View task details

Technologies

| Category       | Technologies                |
|----------------|-----------------------------|
| Backend        | Flask, Flask-SQLAlchemy     |
| Frontend       | Jinja2, Bootstrap 5         |
| Database       | SQLite                      |
| Authentication | Flask-Login                 |
| Form Handling  | WTForms                     |

Installation

  **Clone the repository**:
   ```bash
   git clone https://github.com/MarkOsovets/Flask--taks-tracker
   cd Flask--taks-tracker
   
   python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate Windows 
    
    pip install -r requirements.txt
    
    python app.py
