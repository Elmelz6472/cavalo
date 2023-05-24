from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from week.models import EmployeeWeekWork
from django.http import HttpResponse
from .resources import EmployeeResource


def employee_export(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    return response

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = Employee.objects.get(pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return redirect('employees:employee_list')


def employee_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    work_data = EmployeeWeekWork.objects.filter(employee=employee).order_by('week__start_date')
    return render(request, 'employees/employee_view.html', {
        'employee': employee,
        'work_data': work_data
    })