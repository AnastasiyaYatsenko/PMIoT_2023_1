# Generated by Django 4.2.6 on 2023-11-07 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmiot', '0002_measurement_isworking_measurement_measurementtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='measurementName',
            field=models.CharField(default='name', max_length=250),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='measurementType',
            field=models.CharField(default='type', max_length=250),
        ),
    ]