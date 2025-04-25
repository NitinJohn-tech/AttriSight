from django.db import models

class EmployeeAttrition(models.Model):
    employee_number = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)  # If name is available
    job_role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    overtime = models.CharField(max_length=10)  # Yes or No
    monthly_income = models.IntegerField()
    years_at_company = models.IntegerField()
    job_satisfaction = models.IntegerField()

    attrition_risk = models.CharField(max_length=10)  # High, Medium, Low
    suggested_action = models.TextField()

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee #{self.employee_number} - Risk: {self.attrition_risk}"
