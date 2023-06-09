import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import timedelta, date
from employees.models import Employee
from clients.models import Client
from week.models import Week, EmployeeWeekWork


class Command(BaseCommand):
    help = "Creates random employees, clients, and week data"

    def add_arguments(self, parser):
        parser.add_argument(
            "total",
            type=int,
            help="Indicates the number of each object type to be created",
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs["total"]

        for _ in range(total):
            Client.objects.create(
                name=fake.company(),
                location=fake.address(),
                email=fake.email(),
                phonenumber=fake.phone_number(),
                hourly_rate_morning=Decimal("%.2f" % random.uniform(20, 40)),
                hourly_rate_evening=Decimal("%.2f" % random.uniform(30, 50)),
                hourly_rate_night=Decimal("%.2f" % random.uniform(40, 60)),
            )

        clients = list(Client.objects.all())

        for client in clients:
            for _ in range(total):
                Employee.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phonenumber=fake.phone_number(),
                    hourly_salary=random.randint(15, 18),
                    is_driver=random.choice([True, False]),
                    work_location=client,
                )

        employees = Employee.objects.all()

        for client in clients:
            for _ in range(total):
                start_date = fake.date_between(
                    start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
                )
                end_date = start_date + timedelta(days=6)
                week = Week.objects.create(
                    client=client,
                    start_date=start_date,
                    end_date=end_date,
                    rate_field=random.choice(
                        [
                            "hourly_rate_morning",
                            "hourly_rate_evening",
                            "hourly_rate_night",
                        ]
                    ),
                )
                client_employees = employees.filter(work_location=client)
                for employee in client_employees:
                    EmployeeWeekWork.objects.create(
                        week=week,
                        employee=employee,
                        monday=random.randint(0, 8),
                        tuesday=random.randint(0, 8),
                        wednesday=random.randint(0, 8),
                        thursday=random.randint(0, 8),
                        friday=random.randint(0, 8),
                        saturday=random.randint(0, 8),
                        sunday=random.randint(0, 8),
                    )
