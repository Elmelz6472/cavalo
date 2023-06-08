from django.db.models import Case, F, Sum, When, ExpressionWrapper, DecimalField
from django.db import models
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Client
from .forms import ClientForm
from employees.models import Employee
from week.models import EmployeeWeekWork, Week
from .resources import ClientResource
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def client_export(request):
    client_resources = ClientResource()
    dataset = client_resources.export()
    response = HttpResponse(dataset.csv, content_type="text/csv")
    now = datetime.now()
    filename = "client_list_{}_{}.csv".format(now.strftime("%d"), now.strftime("%B"))
    response["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


@login_required
def client_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    employees = Employee.objects.filter(work_location=client)
    employee_count = employees.count()
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

    total_pay_global = sum(item["total_pay"] for item in grouped_work_data)



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
                When(week__rate_field="hourly_rate_morning", then=F("total_hours") * F("week__client__hourly_rate_morning")),
                default=0,
                output_field=DecimalField(),
            ),
            hourly_rate_evening=Case(
                When(week__rate_field="hourly_rate_evening", then=F("total_hours") * F("week__client__hourly_rate_evening")),
                default=0,
                output_field=DecimalField(),
            ),
            hourly_rate_night=Case(
                When(week__rate_field="hourly_rate_night", then=F("total_hours") * F("week__client__hourly_rate_night")),
                default=0,
                output_field=DecimalField(),
            ),
        )
        .annotate(
            weekly_invoice=Coalesce("hourly_rate_morning", "hourly_rate_evening", "hourly_rate_night")
        )
        .values("week__start_date", "weekly_invoice")
        .order_by("week__start_date")
    )










    grouped_invoice_data = []
    total_invoice = 0
    for key, group in groupby(invoice_data, key=itemgetter("week__start_date")):
        weekly_invoice = sum(item["weekly_invoice"] for item in group)
        total_invoice += weekly_invoice
        grouped_invoice_data.append(
            {"week__start_date": key, "weekly_invoice": weekly_invoice}
        )

    diff_data = []
    for work, invoice in zip(grouped_work_data, grouped_invoice_data):
        if work["week__start_date"] == invoice["week__start_date"]:
            difference = invoice["weekly_invoice"] - work["total_pay"]
            diff_data.append(
                {"week__start_date": work["week__start_date"], "difference": difference}
            )

    return render(
        request,
        "clients/client_view.html",
        {
            "client": client,
            "work_data": grouped_work_data,
            "total_pay_global": total_pay_global,
            "invoice_data": grouped_invoice_data,
            "employees": employees,
            "total_invoice": total_invoice,
            "diff_data": diff_data,
            "employee_count": employee_count,
        },
    )


@login_required
def client_list(request):
    clients = Client.objects.all()
    client_employee_count = {}
    total_clients = clients.count()

    for client in clients:
        employee_count = Employee.objects.filter(work_location=client).count()
        client_employee_count[client.pk] = employee_count
    return render(
        request,
        "clients/client_list.html",
        {
            "clients": clients,
            "client_employee_count": client_employee_count,
            "total_clients": total_clients,
        },
    )


@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("clients:client_list")
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect("clients:client_list")
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect("clients:client_list")
