# Generated by Django 4.2.1 on 2023-05-24 00:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="date_joined",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
