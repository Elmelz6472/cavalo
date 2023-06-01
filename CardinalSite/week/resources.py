from import_export import resources, fields
from .models import EmployeeWeekWork

class EmployeeWeekWorkResource(resources.ModelResource):
    total_hours = fields.Field()
    total_pay = fields.Field()

    class Meta:
        model = EmployeeWeekWork
        fields = ('week__client__name', 'employee__first_name', 'employee__last_name',
                  'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'bonus')
        export_order = ('employee__first_name', 'employee__last_name', 'week__client__name', 'total_hours', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    def dehydrate_total_hours(self, employee_week_work):
        return employee_week_work.total_hours()

    def dehydrate_total_pay(self, employee_week_work):
        return employee_week_work.total_pay()