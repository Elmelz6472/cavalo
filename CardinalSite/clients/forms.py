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
            "location",
            "hourly_rate",
        ]
