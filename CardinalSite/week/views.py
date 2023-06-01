from django.shortcuts import render, redirect, get_object_or_404
from .models import Week, EmployeeWeekWork
from .forms import WeekForm, EmployeeWeekWorkForm
from datetime import timedelta
from employees.models import Employee
from django.http import JsonResponse
from django.template.loader import get_template
from django.http import HttpResponse
from .resources import EmployeeWeekWorkResource
from django.contrib.auth.decorators import login_required

@login_required
def week_export(request, pk):
    week = get_object_or_404(Week, pk=pk)
    employee_week_works = EmployeeWeekWork.objects.filter(week=week)
    employee_week_work_resource = EmployeeWeekWorkResource()
    dataset = employee_week_work_resource.export(employee_week_works)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{week.start_date}_to_{week.end_date}_work_schedule.csv"'
    return response

@login_required
def week_list(request):
    weeks = Week.objects.all()
    total_weeks = weeks.count()
    return render(request, 'week/week_list.html', {'weeks': weeks, 'total_weeks': total_weeks})


@login_required
def week_create(request):
    form = WeekForm(request.POST or None)
    if form.is_valid():
        week = form.save(commit=False)
        week.end_date = week.start_date + timedelta(days=6)
        week.save()
        return redirect('week:week_list')
    return render(request, 'week/week_form.html', {'form': form})

@login_required
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

@login_required
def week_view(request, pk):
    week = get_object_or_404(Week, pk=pk)
    client = week.client
    employees = Employee.objects.filter(work_location=client)
    employee_works = {work.employee_id: work for work in EmployeeWeekWork.objects.filter(week=week, employee__in=employees)}
    return render(request, 'week/week_detail.html', {'week': week, 'employees': employees, 'employee_works': employee_works})

@login_required
def week_delete(request, pk):
    week = get_object_or_404(Week, pk=pk)
    week.delete()
    return redirect('week:week_list')

@login_required
def week_work_edit(request, week_pk, employee_pk):
    week = get_object_or_404(Week, pk=week_pk)
    employee = get_object_or_404(Employee, pk=employee_pk)
    work, created = EmployeeWeekWork.objects.get_or_create(week=week, employee=employee)

    form = EmployeeWeekWorkForm(request.POST or None, instance=work)
    if form.is_valid():
        form.save()
        return redirect('week:week_view', pk=week.pk)


    return render(request, 'week/week_work_form.html', {'form': form, 'employee':employee, 'week':week})

