from import_export import resources, fields
from .models import Client


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ("name", "contact_resource", "phonenumber", "location", "email", "date_joined")
