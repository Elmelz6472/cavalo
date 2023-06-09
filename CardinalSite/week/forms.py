from django import forms
from .models import Week, EmployeeWeekWork


class WeekForm(forms.ModelForm):
    rate_field = forms.ChoiceField(choices=Week.RATE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Week
        fields = ["start_date", "client", "rate_field"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "client": forms.Select(attrs={"class": "form-control"}),
        }


class EmployeeWeekWorkForm(forms.ModelForm):
    class Meta:
        model = EmployeeWeekWork
        fields = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "bonus",
        ]
        widgets = {
            "monday": forms.NumberInput(attrs={"class": "form-control"}),
            "tuesday": forms.NumberInput(attrs={"class": "form-control"}),
            "wednesday": forms.NumberInput(attrs={"class": "form-control"}),
            "thursday": forms.NumberInput(attrs={"class": "form-control"}),
            "friday": forms.NumberInput(attrs={"class": "form-control"}),
            "saturday": forms.NumberInput(attrs={"class": "form-control"}),
            "sunday": forms.NumberInput(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
        }
