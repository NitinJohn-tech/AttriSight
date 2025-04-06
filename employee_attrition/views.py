import os
import joblib
import json
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Load the trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'attrition', 'employee_attrition_model.pkl')
model = joblib.load(MODEL_PATH)

# Features expected by the model
expected_features = [
    "Age", "BusinessTravel", "DailyRate", "Department", "DistanceFromHome",
    "Education", "EducationField", "EmployeeCount", "EnvironmentSatisfaction",
    "Gender", "HourlyRate", "JobInvolvement", "JobLevel", "JobRole",
    "JobSatisfaction", "MaritalStatus", "MonthlyIncome", "MonthlyRate",
    "NumCompaniesWorked", "Over18", "OverTime", "PercentSalaryHike",
    "PerformanceRating", "RelationshipSatisfaction", "StandardHours",
    "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear",
    "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole",
    "YearsSinceLastPromotion", "YearsWithCurrManager"
]

# Mappings for categorical values
business_travel_mapping = {"Non-Travel": 1, "Travel Rarely": 2, "Travel Frequently": 3}
department_mapping = {"HR": 1, "R&D": 2, "Sales": 3}
education_field_mapping = {"Life Sciences": 1, "Medical": 2, "Marketing": 3, "Technical Degree": 4, "Human Resources": 5, "Other": 6}
gender_mapping = {"Male": 1, "Female": 0}
marital_status_mapping = {"Single": 1, "Married": 2, "Divorced": 3}
overtime_mapping = {"Yes": 1, "No": 0}

# Default values for missing fields
default_values = {
    "EmployeeCount": 1, "Over18": 1, "StandardHours": 40,  # Fixed values
    "BusinessTravel": 2, "Department": 2, "EducationField": 1, "Gender": 1, "MaritalStatus": 2, "OverTime": 0  # Defaults
}

@login_required
@csrf_exempt
def predict_attrition(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Convert categorical values to numerical form
            data["BusinessTravel"] = business_travel_mapping.get(data.get("BusinessTravel"), 2)
            data["Department"] = department_mapping.get(data.get("Department"), 2)
            data["EducationField"] = education_field_mapping.get(data.get("EducationField"), 1)
            data["Gender"] = gender_mapping.get(data.get("Gender"), 1)
            data["MaritalStatus"] = marital_status_mapping.get(data.get("MaritalStatus"), 2)
            data["OverTime"] = overtime_mapping.get(data.get("OverTime"), 0)

            # Fill missing values with defaults
            for feature in expected_features:
                data.setdefault(feature, default_values.get(feature, 0))  # Default to 0 if not specified

            # Convert to DataFrame with correct feature order
            input_data = pd.DataFrame([data], columns=expected_features)

            # Predict attrition and probability
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]  # Probability of attrition

            return JsonResponse({"attrition": int(prediction), "probability": float(probability)})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def home(request):
    return render(request, "index.html")

#def index(request):
 #   return render(request, "index.html")

from django.shortcuts import render

@login_required
def home_page(request):
    return render(request, 'index.html')

@login_required
def about_page(request):
    context = {
        "site_name": "Your Site Name",
        "about_heading": "Welcome to Our Company",
        "about_description": "We are dedicated to providing the best services...",
        "features": [
            {"icon": "fa-star", "title": "Quality Service", "description": "We ensure top quality service.", "delay": 0.1},
            {"icon": "fa-cogs", "title": "Efficient Process", "description": "Our process is streamlined for efficiency.", "delay": 0.2},
        ],
        "skills": [
            {"name": "Web Development", "percentage": 90},
            {"name": "Machine Learning", "percentage": 85},
        ],
        "team": [
            {"name": "John Doe", "role": "CEO", "image": "img/team-1.jpg"},
            {"name": "Jane Smith", "role": "CTO", "image": "img/team-2.jpg"},
        ],
    }
    return render(request, 'about.html', context)

@login_required
def service_page(request):
    return render(request, 'service.html')

@login_required
def project_page(request):
    return render(request, 'project.html')





