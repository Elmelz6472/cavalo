from django import forms
from .models import Week, WorkEntry

class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ['start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ['client', 'employee', 'hours_worked']
