# Generated by Django 4.2.7 on 2023-12-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmiot', '0005_merge_0004_auto_20231208_1203_0004_measurement_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
