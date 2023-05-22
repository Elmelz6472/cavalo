from django.shortcuts import render, redirect, get_object_or_404
from .models import Week, WorkEntry
from .forms import WeekForm, WorkEntryForm
from employees.models import Employee
from clients.models import Client
from datetime import timedelta


def week_list(request):
    weeks = Week.objects.all()
    return render(request, 'calendars/week_list.html', {'weeks': weeks})

def week_create(request):
    form = WeekForm(request.POST or None)
    if form.is_valid():
        week = form.save()

        # Retrieve all clients
        clients = Client.objects.all()

        # Iterate over each client
        for client in clients:
            # Retrieve all employees working at the current client
            employees = Employee.objects.filter(work_location=client)

            # Iterate through the days of the week
            for i in range(7):
                day = week.start_date + timedelta(days=i)

                # Create WorkEntry instances with 0 hours for each employee
                for employee in employees:
                    WorkEntry.objects.create(
                        week=week,
                        client=client,
                        employee=employee,
                        hours_worked=0,
                        date=day
                    )

        return redirect('calendars:week_list')
    return render(request, 'calendars/week_form.html', {'form': form})


def week_delete(request, pk):
    week = get_object_or_404(Week, pk=pk)
    week.delete()
    return redirect('calendars:week_list')

def work_entry_list(request, week_pk):
    week = get_object_or_404(Week, pk=week_pk)
    work_entries = WorkEntry.objects.filter(week=week)
    return render(request, 'calendars/work_entry_list.html', {'work_entries': work_entries, 'week': week})

def work_entry_create(request, week_pk):
    week = get_object_or_404(Week, pk=week_pk)
    form = WorkEntryForm(request.POST or None, initial={'week': week})
    if form.is_valid():
        form.instance.week = week
        form.save()
        return redirect('calendars:work_entry_list', week_pk=week_pk)
    return render(request, 'calendars/work_entry_form.html', {'form': form, 'week': week})

def work_entry_delete(request, week_pk, work_entry_pk):
    work_entry = get_object_or_404(WorkEntry, pk=work_entry_pk, week__pk=week_pk)
    work_entry.delete()
    return redirect('calendars:work_entry_list', week_pk=week_pk)
