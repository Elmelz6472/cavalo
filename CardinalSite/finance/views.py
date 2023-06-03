from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from clients.models import Client
from clients.forms import ClientForm
from employees.models import Employee
from week.models import EmployeeWeekWork, Week
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from django.contrib.auth.decorators import login_required



@login_required
def finance_view(request):
    clients = Client.objects.all()
    employees = Employee.objects.count()
    total_profits = []
    for client in clients:
        weeks = Week.objects.filter(client=client)
        work_data = EmployeeWeekWork.objects.filter(week__in=weeks).annotate(
            total_pay=(
                Sum(F('monday') + F('tuesday') + F('wednesday') + F('thursday') + F('friday') + F('saturday') + F('sunday')) * F('employee__hourly_salary')
            )
        ).values('week__start_date', 'total_pay').order_by('week__start_date')

        grouped_work_data = []
        for key, group in groupby(work_data, key=itemgetter('week__start_date')):
            total_pay = sum(item['total_pay'] for item in group)
            grouped_work_data.append({'week__start_date': key, 'total_pay': total_pay})

        invoice_data = EmployeeWeekWork.objects.filter(week__in=weeks).annotate(
            total_hours=(
                Sum(F('monday') + F('tuesday') + F('wednesday') + F('thursday') + F('friday') + F('saturday') + F('sunday'))
            ),
            weekly_invoice=F('total_hours') * F('week__client__hourly_rate')
        ).values('week__start_date', 'weekly_invoice').order_by('week__start_date')

        grouped_invoice_data = []
        for key, group in groupby(invoice_data, key=itemgetter('week__start_date')):
            weekly_invoice = sum(item['weekly_invoice'] for item in group)
            grouped_invoice_data.append({'week__start_date': key, 'weekly_invoice': weekly_invoice})

        diff_data = []
        for work, invoice in zip(grouped_work_data, grouped_invoice_data):
            if work['week__start_date'] == invoice['week__start_date']:
                difference = invoice['weekly_invoice'] - work['total_pay']
                diff_data.append({'week__start_date': work['week__start_date'], 'difference': difference})

        total_profit = sum(item['difference'] for item in diff_data)
        total_profits.append({'client': client, 'total_profit': total_profit})
        sum_profit_global = 0
        for combo in total_profits:
            sum_profit_global += combo['total_profit']

    print(total_profits)
    print(sum_profit_global)


    return render(request, 'finance/finance_view.html', {'clients': clients, 'total_profits': total_profits, 'total_profit':sum_profit_global,
    'employees':employees})
