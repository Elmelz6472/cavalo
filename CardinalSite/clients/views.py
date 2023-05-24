from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Client
from .forms import ClientForm
from employees.models import Employee
from week.models import EmployeeWeekWork, Week
from .resources import ClientResource
from itertools import groupby
from operator import itemgetter

def client_export(request):
    client_resources = ClientResource()
    dataset = client_resources.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-disposition'] = 'attachment; filename="client_list.csv"'
    return response


def client_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    weeks = Week.objects.filter(client=client)
    work_data = EmployeeWeekWork.objects.filter(week__in=weeks).annotate(
        total_pay=(
            Sum(F('monday') + F('tuesday') + F('wednesday') + F('thursday') + F('friday') + F('saturday') + F('sunday')) * F('employee__hourly_salary')
        )
    ).values('week__start_date', 'total_pay').order_by('week__start_date')

    # Group work_data by 'week__start_date' and sum up 'total_pay' for each group
    grouped_work_data = []
    for key, group in groupby(work_data, key=itemgetter('week__start_date')):
        total_pay = sum(item['total_pay'] for item in group)
        grouped_work_data.append({'week__start_date': key, 'total_pay': total_pay})

    total_pay_global = sum(item['total_pay'] for item in grouped_work_data)

    return render(request, 'clients/client_view.html', {'client': client, 'work_data': grouped_work_data, 'total_pay_global': total_pay_global})


def client_list(request):
    clients = Client.objects.all()
    client_employee_count = {}

    for client in clients:
        employee_count = Employee.objects.filter(work_location=client).count()
        client_employee_count[client.pk] = employee_count
    return render(request, 'clients/client_list.html', {'clients': clients, 'client_employee_count': client_employee_count})


def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clients:client_list')
    return render(request, 'clients/client_form.html', {'form': form})

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('clients:client_list')
    return render(request, 'clients/client_form.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('clients:client_list')


