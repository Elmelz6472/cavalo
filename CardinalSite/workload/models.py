from django.db import models
from datetime import timedelta
from clients.models import Client
from employees.models import Employee

class Week(models.Model):
    start_date = models.DateField(unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.create_employee_hours()

    def create_employee_hours(self):
        employees = Employee.objects.filter(work_location=self.client)
        for i in range(7):
            date = self.start_date + timedelta(days=i)
            for employee in employees:
                EmployeeHours.objects.create(week=self, employee=employee, date=date, hours_worked=0)

    def __str__(self):
        end_date = self.start_date + timedelta(days=6)
        return f"Week of {self.start_date.strftime('%B %d')} to {end_date.strftime('%B %d')}"


class EmployeeHours(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ['week', 'employee', 'date']
