from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Week, Client, EmployeeHours

class WeekForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = Week
        fields = ['start_date', 'client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all()

class EmployeeHoursForm(forms.ModelForm):
    class Meta:
        model = EmployeeHours
        fields = ['hours_worked']
