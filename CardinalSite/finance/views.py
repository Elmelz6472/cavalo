from django.db.models import Case, F, Sum, When, ExpressionWrapper, DecimalField
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import Coalesce
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
    clients_count = Client.objects.count()
    employees_count = Employee.objects.count()
    total_profits = []
    total_pay_global = 0
    total_invoice_global = 0

    sum_profit_global = 0
    for client in clients:
        weeks = Week.objects.filter(client=client)
        work_data = (
            EmployeeWeekWork.objects.filter(week__in=weeks)
            .annotate(
                total_pay=(
                    Sum(
                        F("monday")
                        + F("tuesday")
                        + F("wednesday")
                        + F("thursday")
                        + F("friday")
                        + F("saturday")
                        + F("sunday")
                    )
                    * F("employee__hourly_salary")
                )
            )
            .values("week__start_date", "total_pay")
            .order_by("week__start_date")
        )

        grouped_work_data = []
        for key, group in groupby(work_data, key=itemgetter("week__start_date")):
            total_pay = sum(item["total_pay"] for item in group)
            grouped_work_data.append({"week__start_date": key, "total_pay": total_pay})

        total_pay_global += sum(item["total_pay"] for item in grouped_work_data)

        invoice_data = (
        EmployeeWeekWork.objects.filter(week__in=weeks)
        .annotate(
            total_hours=Sum(
                F("monday")
                + F("tuesday")
                + F("wednesday")
                + F("thursday")
                + F("friday")
                + F("saturday")
                + F("sunday")
            )
        )
        .annotate(
            hourly_rate_morning=Case(
                When(
                    week__rate_field="hourly_rate_morning",
                    then=F("total_hours") * F("week__client__hourly_rate_morning"),
                ),
                default=0,
                output_field=DecimalField(),
            ),
            hourly_rate_evening=Case(
                When(
                    week__rate_field="hourly_rate_evening",
                    then=F("total_hours") * F("week__client__hourly_rate_evening"),
                ),
                default=0,
                output_field=DecimalField(),
            ),
            hourly_rate_night=Case(
                When(
                    week__rate_field="hourly_rate_night",
                    then=F("total_hours") * F("week__client__hourly_rate_night"),
                ),
                default=0,
                output_field=DecimalField(),
            ),
        )
        .annotate(
            weekly_invoice=Coalesce(
                "hourly_rate_morning", "hourly_rate_evening", "hourly_rate_night"
            )
        )
        .values("week__start_date", "weekly_invoice")
        .order_by("week__start_date")
        )



        grouped_invoice_data = []
        total_invoice = 0
        for key, group in groupby(invoice_data, key=itemgetter("week__start_date")):
            weekly_invoice = sum(item["weekly_invoice"] for item in group)
            total_invoice += weekly_invoice
            total_invoice_global += weekly_invoice
            grouped_invoice_data.append(
                {"week__start_date": key, "weekly_invoice": weekly_invoice}
            )

        diff_data = []
        for work, invoice in zip(grouped_work_data, grouped_invoice_data):
            if work["week__start_date"] == invoice["week__start_date"]:
                difference = invoice["weekly_invoice"] - work["total_pay"]
                diff_data.append(
                    {
                        "week__start_date": work["week__start_date"],
                        "difference": difference,
                    }
                )

        total_profit = sum(item["difference"] for item in diff_data)
        pay_to_employee = sum(item["total_pay"] for item in grouped_work_data)

        total_profits.append(
            {
                "client": client,
                "total_profit": total_profit,
                "pay_to_employee": pay_to_employee,
            }
        )
        sum_profit_global = 0
        for combo in total_profits:
            sum_profit_global += combo["total_profit"]

    try:
        average_profit_per_employee = sum_profit_global / employees_count
    except ZeroDivisionError:
        average_profit_per_employee = 0

    try:
        average_pay_per_employee = total_pay_global / employees_count
    except ZeroDivisionError:
        average_pay_per_employee = 0

    try:
        average_invoice_per_compagnie = total_invoice_global / clients_count
    except ZeroDivisionError:
        average_invoice_per_compagnie = 0

    return render(
        request,
        "finance/finance_view.html",
        {
            "clients": clients,
            "total_profits": total_profits,
            "total_profit": sum_profit_global,
            "employees": employees_count,
            "total_pay_global": total_pay_global,
            "total_invoice_global": total_invoice_global,
            "average_profit_per_employee": average_profit_per_employee,
            "average_pay_per_employee": average_pay_per_employee,
            "average_invoice_per_compagnie": average_invoice_per_compagnie,
        },
    )
