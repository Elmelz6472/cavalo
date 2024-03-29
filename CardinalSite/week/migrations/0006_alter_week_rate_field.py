# Generated by Django 4.2.1 on 2023-06-08 02:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("week", "0005_week_rate_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="week",
            name="rate_field",
            field=models.CharField(
                choices=[
                    ("hourly_rate_morning", "Morning Rate"),
                    ("hourly_rate_evening", "Evening Rate"),
                    ("hourly_rate_night", "Night Rate"),
                ],
                max_length=20,
            ),
        ),
    ]
