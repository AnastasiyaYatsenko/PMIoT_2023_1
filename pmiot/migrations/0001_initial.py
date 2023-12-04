# Generated by Django 4.2.7 on 2023-12-03 17:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isWorking", models.BooleanField(default=False)),
                ("min_value", models.IntegerField(default=0)),
                ("max_value", models.IntegerField(default=100)),
                ("value", models.IntegerField(default=0)),
                ("measurementName", models.CharField(default="name", max_length=250)),
                ("measurementType", models.CharField(default="type", max_length=250)),
                (
                    "description",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
            ],
            options={
                "ordering": ["measurementName"],
            },
        ),
    ]
