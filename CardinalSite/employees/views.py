from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm

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
