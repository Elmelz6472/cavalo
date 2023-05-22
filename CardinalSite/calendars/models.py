from django.db import models
from clients.models import Client
from employees.models import Employee
from datetime import timedelta

class Week(models.Model):
    start_date = models.DateField(unique=True)

    def __str__(self):
        end_date = self.start_date + timedelta(days=6)
        return f"{self.start_date.strftime('%B %d')} to {end_date.strftime('%B %d')}"

class WorkEntry(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.employee} at {self.client} on {self.date} for {self.hours_worked} hours"

    class Meta:
        unique_together = ['week', 'client', 'employee', 'date']
