# from django.db import models
from djongo import models
from bson import ObjectId

from datetime import datetime
from django.utils import timezone


class Measurement(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    measurementName = models.CharField(default='Name', max_length=250)
    measurementType = models.CharField(default='Type', max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)
    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    value = models.FloatField(default=0, blank=True, null=True)
    dimension = models.CharField(default='°C', max_length=10)
    isWorking = models.BooleanField(default=False)

    image = models.ImageField(default=None, upload_to='', null=True)

    min_comfort = models.IntegerField(default=0)
    max_comfort = models.IntegerField(default=100)
    need_notification = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
    last_notified = models.DateTimeField(default=None, null=True)

    class Meta:
        ordering = ['measurementName']

    @property
    def measurement_id(self):
        return str(self._id)

    def __str__(self):
        return f'{self.measurement_id}: {self.measurementType} - {self.value}'


class Archive(models.Model):
    sensor_id = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sensor_id.measurement_id} - {self.value} - {self.timestamp}'
