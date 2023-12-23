# Generated by Django 4.1.13 on 2023-12-23 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurementName', models.CharField(default='Name', max_length=250)),
                ('measurementType', models.CharField(default='Type', max_length=250)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('min_value', models.IntegerField(default=0)),
                ('max_value', models.IntegerField(default=100)),
                ('value', models.FloatField(blank=True, default=0, null=True)),
                ('dimension', models.CharField(default='°C', max_length=10)),
                ('isWorking', models.BooleanField(default=False)),
                ('image', models.ImageField(default=None, null=True, upload_to='')),
                ('min_comfort', models.IntegerField(default=0)),
                ('max_comfort', models.IntegerField(default=100)),
                ('need_notification', models.BooleanField(default=False)),
                ('is_notified', models.BooleanField(default=False)),
                ('last_notified', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'ordering': ['measurementName'],
            },
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('timestamp', models.DateTimeField(default=None)),
                ('sensor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pmiot.measurement')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
