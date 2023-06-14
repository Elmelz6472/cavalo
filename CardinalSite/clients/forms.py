from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), input_formats=("%Y-%m-%d",)
    )

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
