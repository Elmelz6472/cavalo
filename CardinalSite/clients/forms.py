from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "contact_resource",
            "phonenumber",
            "email",
            "date_joined",
            "location",
            "hourly_rate_morning",
            "hourly_rate_evening",
            "hourly_rate_night",
        ]
        widgets = {
            "date_joined": forms.DateInput(attrs={"type": "datetime-local"}),
        }
