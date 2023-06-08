from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from clients.models import Client


class Employee(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phonenumber = PhoneNumberField(blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    hourly_salary = models.DecimalField(max_digits=5, decimal_places=2)
    work_location = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=date.today, blank=True, null=True)  # add this line

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
