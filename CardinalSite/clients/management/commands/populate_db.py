import random
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import timedelta
from employees.models import Employee
from clients.models import Client
from week.models import Week, EmployeeWeekWork
from decimal import Decimal



class Command(BaseCommand):
    help = 'Creates random employees, clients, and week data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of each object type to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']

        for _ in range(total):
            Client.objects.create(
                name=fake.company(),
                location=fake.address(),
                email=fake.email(),
                phonenumber=fake.phone_number(),
                hourly_rate=Decimal("%.2f" % random.uniform(20, 40))  # Generates a random float between 20 and 40
            )

        # Ensure Client objects are created first
        clients = list(Client.objects.all())  # Convert queryset to list

        for client in clients:
            for _ in range(total):  # Create 'total' number of employees for each client
                Employee.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phonenumber=fake.phone_number(),
                    hourly_salary=random.randint(15, 20),
                    is_driver=random.choice([True, False]),
                    work_location=client,  # Assign each client to 'total' number of employees
                )

        employees = Employee.objects.all()

        for client in clients:
            employee_list = list(employees.filter(work_location=client))  # All employees for a specific client
            for employee in employee_list:
                for _ in range(total):  # Creating multiple Week instances for each employee
                    start_date = fake.date_between(start_date='-1y', end_date='today')
                    end_date = start_date + timedelta(days=6)  # Assuming a week duration is 7 days
                    week = Week.objects.create(
                        client=client,
                        start_date=start_date,
                        end_date=end_date,  # Provide end_date here
                    )
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
