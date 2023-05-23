from django.shortcuts import render, redirect, get_object_or_404
from .models import Week, EmployeeHours
from .forms import WeekForm, EmployeeHoursForm
from django.forms import formset_factory
from datetime import timedelta

def week_list(request):
    weeks = Week.objects.all()
    return render(request, 'workload/week_list.html', {'weeks': weeks})

def week_create(request):
    if request.method == 'POST':
        form = WeekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workload:week_list')
    else:
        form = WeekForm()
    return render(request, 'workload/week_form.html', {'form': form})

def week_detail(request, pk):
    week = get_object_or_404(Week, pk=pk)
    employees = week.client.employee_set.all()
    week_dates = [week.start_date + timedelta(days=i) for i in range(7)]

    employee_hours = EmployeeHours.objects.filter(week=week, employee__in=employees).select_related('employee')

    EmployeeHoursFormSet = formset_factory(EmployeeHoursForm, extra=0)

    if request.method == 'POST':
        formset = EmployeeHoursFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.week = week
                instance.save()
            return redirect('workload:week_detail', pk=week.pk)
    else:
        initial_data = [{'date': hours.date, 'hours_worked': hours.hours_worked} for hours in employee_hours]
        formset = EmployeeHoursFormSet(initial=initial_data)

    context = {
        'week': week,
        'employees': employees,
        'week_dates': week_dates,
        'employee_hours': employee_hours,
        'formset': formset,
    }

    return render(request, 'workload/week_detail.html', context)

def week_delete(request, pk):
    week = get_object_or_404(Week, pk=pk)
    week.delete()
    return redirect('workload:week_list')

def week_edit(request, week_pk, employee_pk, date):
    week = get_object_or_404(Week, pk=week_pk)
    employee = get_object_or_404(Employee, pk=employee_pk)
    employee_hours = get_object_or_404(EmployeeHours, week=week, employee=employee, date=date)

    if request.method == 'POST':
        form = EmployeeHoursForm(request.POST, instance=employee_hours)
        if form.is_valid():
            form.save()
            return redirect('workload:week_detail', pk=week.pk)
    else:
        form = EmployeeHoursForm(instance=employee_hours)

    return render(request, 'workload/employee_hours_edit.html', {'form': form})
