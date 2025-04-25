import os
import joblib
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required

# Load the trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'predictions', 'employee_attrition_model.pkl')
model = joblib.load(MODEL_PATH)

# Store the last predictions in memory for download
predicted_data = []

# Define expected features and mappings
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

business_travel_mapping = {"Non-Travel": 1, "Travel Rarely": 2, "Travel Frequently": 3}
department_mapping = {"HR": 1, "R&D": 2, "Sales": 3}
education_field_mapping = {"Life Sciences": 1, "Medical": 2, "Marketing": 3, "Technical Degree": 4, "Human Resources": 5, "Other": 6}
gender_mapping = {"Male": 1, "Female": 0}
jobrole_mapping={
    "Sales Executive": 1,
    "Research Scientist": 2,
    "Manager": 3,
    "Laboratory Technician": 4,
    "Healthcare Representative": 5,
    "Manufacturing Director": 6,
    "Human Resources": 7,
    "Marketing": 8,
    "Technician": 9,
    "Executive": 10,
    "Business Analyst": 11,
    "Computer Scientist": 12,
    "Recruiter": 13,
    "Other": 14  # You can map any unknown or missing value to "Other"
}
marital_status_mapping = {"Single": 1, "Married": 2, "Divorced": 3}
overtime_mapping = {"Yes": 1, "No": 0}


default_values = {
    "EmployeeCount": 1, "Over18": 1, "StandardHours": 40,
    "BusinessTravel": 2, "Department": 2, "EducationField": 1,
    "Gender": 1, "MaritalStatus": 2, "OverTime": 0,

}


def preprocess_row(row):
    row = row.copy()

    # Map categorical values
    row["BusinessTravel"] = business_travel_mapping.get(row.get("BusinessTravel"), 2)
    row["Department"] = department_mapping.get(row.get("Department"), 2)
    row["EducationField"] = education_field_mapping.get(row.get("EducationField"), 1)
    row["Gender"] = gender_mapping.get(row.get("Gender"), 1)
    row["JobRole"] = jobrole_mapping.get(row.get("JobRole"), 14) 
    row["MaritalStatus"] = marital_status_mapping.get(row.get("MaritalStatus"), 2)
    row["OverTime"] = overtime_mapping.get(row.get("OverTime"), 0)

    # Fill defaults
    for feature in expected_features:
        row.setdefault(feature, default_values.get(feature, 0))

    return row

@login_required
def upload_csv(request):
    global predicted_data
    results = []

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file']
                df = pd.read_csv(file)

                for _, row in df.iterrows():
                    employee_name = row.get('EmployeeName', 'N/A')

                    processed = preprocess_row(row.to_dict())
                    input_df = pd.DataFrame([processed], columns=expected_features)

                    prediction = model.predict(input_df)[0]
                    probability = model.predict_proba(input_df)[0][1]

                    results.append({
                        'Name': employee_name,
                        'Department': row.get('Department', 'N/A'),
                        'AttritionRisk': "High" if prediction == 1 else "Low",
                        'Probability': round(probability, 2),
                        'SuggestedAction': "Schedule retention interview" if prediction == 1 else "Monitor monthly"
                    })

                predicted_data = results
                return render(request, 'project.html', {'form': form, 'results': results})

            except Exception as e:
                return render(request, 'project.html', {'form': form, 'error': f"Error: {e}"})
    else:
        form = UploadFileForm()

    return render(request, 'project.html', {'form': form})

@login_required
def download_excel(request):
    global predicted_data

    df = pd.DataFrame(predicted_data)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=predictions.xlsx'
    df.to_excel(response, index=False)
    return response
