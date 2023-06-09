from import_export import resources, fields
from .models import Client


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = (
            "name",
            "contact_resource",
            "phonenumber",
            "location",
            "email",
            "date_joined",
            "hourly_rate_morning",
            "hourly_rate_evening",
            "hourly_rate_night",
        )
