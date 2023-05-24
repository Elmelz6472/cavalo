from import_export import resources
from .models import Employee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'is_driver', 'hourly_salary', 'work_location__name', 'date_joined')
