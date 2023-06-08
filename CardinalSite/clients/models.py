from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Client(models.Model):
    name = models.CharField(max_length=100)
    contact_resource = models.CharField(max_length=100, null=True, blank=True)
    phonenumber = PhoneNumberField(blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    date_joined = models.DateField(default=timezone.now, null=True, blank=True)
    hourly_rate_morning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hourly_rate_evening = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hourly_rate_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
