from django import forms
from .models import Week, EmployeeWeekWork

class WeekForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Week
        fields = ['start_date', 'client']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
        }

class EmployeeWeekWorkForm(forms.ModelForm):
    class Meta:
        model = EmployeeWeekWork
        fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
