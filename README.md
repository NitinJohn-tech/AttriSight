# AttriSight 🔍

AttriSight is a web-based employee attrition prediction system built using Django and machine learning. It helps organizations identify which employees are at risk of leaving.
(Still in development)

## 🚀 Features

- Predicts the likelihood of employee attrition
- User-friendly interface with login and registration
- Visual display of prediction results
- Easy-to-understand ML model with notebook included

## 🛠 Tech Stack

- Python, Django
- Jupyter Notebook (for model)
- HTML, CSS, JavaScript
- PostgreSQL

## 📁 Project Structure

```
attrition/
├── accounts/                      # Handles user login & registration
│   ├── migrations/               # Django migration files
│   ├── __pycache__/             # Bytecode cache (auto-generated)
│   ├── __init__.py
│   ├── admin.py                 # Admin panel configuration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # Custom user forms
│   ├── models.py                # User-related models
│   ├── tests.py                 # Unit tests
│   ├── urls.py                  # App-specific routing
│   └── views.py                 # Login/register logic
├── attrition/                    # Main Django project directory
├── employee_attrition/          # ML model handling
├── static/                      # CSS, JavaScript, images
├── staticfiles/                 # Auto-collected static files (for deployment)
├── templates/                   # Frontend HTML pages
│   ├── about.html
│   ├── index.html
│   ├── login.html
│   ├── predict.html
│   ├── project.html
│   ├── register.html
│   └── service.html
├── db.sqlite3                   # SQLite DB (can be switched to PostgreSQL)
└── manage.py                    # Django project runner
```
