from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
from employees.models import Employee
from week.models import EmployeeWeekWork, Week


def client_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    weeks = Week.objects.filter(client=client)
    work_data = EmployeeWeekWork.objects.filter(week__in=weeks).annotate(
        total_pay=(
            Sum(F('monday') + F('tuesday') + F('wednesday') + F('thursday') + F('friday') + F('saturday') + F('sunday')) * F('employee__hourly_salary')
        )
    ).values('week__start_date', 'total_pay').order_by('week__start_date')

    total_pay_global = work_data.aggregate(total=Sum('total_pay'))['total']

    return render(request, 'clients/client_view.html', {'client': client, 'work_data': work_data, 'total_pay_global': total_pay_global})



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


