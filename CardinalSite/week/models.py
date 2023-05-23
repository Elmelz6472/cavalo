from django.db import models
from clients.models import Client
from employees.models import Employee

class Week(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Week from {self.start_date} to {self.end_date}"

class EmployeeWeekWork(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)
    sunday = models.IntegerField(default=0)

    class Meta:
        unique_together = [['week', 'employee']]

    def total_hours(self):
        return self.monday + self.tuesday + self.wednesday + self.thursday + self.friday + self.saturday + self.sunday