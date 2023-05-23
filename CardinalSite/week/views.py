from django.shortcuts import render, redirect, get_object_or_404
from .models import Week, EmployeeWeekWork
from .forms import WeekForm, EmployeeWeekWorkForm
from datetime import timedelta
from employees.models import Employee



def week_list(request):
    weeks = Week.objects.all()
    return render(request, 'week/week_list.html', {'weeks': weeks})

def week_create(request):
    form = WeekForm(request.POST or None)
    if form.is_valid():
        week = form.save(commit=False)
        week.end_date = week.start_date + timedelta(days=6)
        week.save()
        return redirect('week:week_list')
    return render(request, 'week/week_form.html', {'form': form})

def week_edit(request, pk):
    week = get_object_or_404(Week, pk=pk)
    if request.method == "POST":
        form = WeekForm(request.POST, instance=week)
        if form.is_valid():
            week = form.save(commit=False)
            week.end_date = week.start_date + timedelta(days=6)
            week.save()
            return redirect('week:week_list')
    else:
        form = WeekForm(instance=week)
    return render(request, 'week/week_form.html', {'form': form})


def week_view(request, pk):
    week = get_object_or_404(Week, pk=pk)
    client = week.client
    employees = Employee.objects.filter(work_location=client)
    employee_works = {work.employee_id: work for work in EmployeeWeekWork.objects.filter(week=week, employee__in=employees)}
    return render(request, 'week/week_detail.html', {'week': week, 'employees': employees, 'employee_works': employee_works})


def week_delete(request, pk):
    week = get_object_or_404(Week, pk=pk)
    week.delete()
    return redirect('week:week_list')

def week_work_edit(request, week_pk, employee_pk):
    week = get_object_or_404(Week, pk=week_pk)
    employee = get_object_or_404(Employee, pk=employee_pk)
    work, created = EmployeeWeekWork.objects.get_or_create(week=week, employee=employee)

    form = EmployeeWeekWorkForm(request.POST or None, instance=work)
    if form.is_valid():
        form.save()
        return redirect('week:week_view', pk=week.pk)


    return render(request, 'week/week_work_form.html', {'form': form})