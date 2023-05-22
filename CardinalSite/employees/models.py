from django.db import models
from clients.models import Client

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_driver = models.BooleanField(default=False)
    hourly_salary = models.DecimalField(max_digits=5, decimal_places=2)
    work_location = models.ForeignKey(Client, on_delete=models.CASCADE)
    # date_joined = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
