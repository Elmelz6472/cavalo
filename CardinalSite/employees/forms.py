from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=('%Y-%m-%d',)
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phonenumber', 'is_driver', 'hourly_salary', 'work_location', 'date_joined']
