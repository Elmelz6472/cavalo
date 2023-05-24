from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Client(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = PhoneNumberField(blank=True)
    location = models.CharField(max_length=255)
    email = models.EmailField(max_length = 255)
    date_joined = models.DateTimeField(auto_now_add=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # added field


    def __str__(self):
        return self.name

