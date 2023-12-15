import inspect
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory

from pmiot.models import Measurement, Archive
from pmiot.scheduler.scheduler import data_from_dataset


class NotificationTests(TestCase):

    # prepare data for every test
    def setUp(self):
        # create 2 instances with different types
        admin = User.objects.create_superuser(username='admin', password='admin')
        measurement = Measurement.objects.create(measurementType='Temperature',
                                                 image='/static/images/BMP085.jpg')
        Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print('Number of sensors:', len(Measurement.objects.all()))

        pass

    def test__value_more_then_comfortable(self):
        # change instance (isWorking = True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        measurement.isWorking = True
        measurement.max_comfort = -5
        measurement.min_comfort = -10
        measurement.is_notified = False
        measurement.need_notification = True
        measurement.save()

        self.client.login(username='admin', password='admin')
        user = User.objects.get(username='admin')
        measurement = Measurement.objects.get(measurementType='Temperature')
        response = self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        print(measurement.value)
        res = measurement.is_notified
        self.assertEqual(res, 1)

    def test__value_less_then_comfortable(self):
        # change instance (isWorking = True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        measurement.isWorking = True
        measurement.max_comfort = 90
        measurement.min_comfort = 100
        measurement.is_notified = False
        measurement.need_notification = True
        measurement.save()

        self.client.login(username='admin', password='admin')
        user = User.objects.get(username='admin')
        measurement = Measurement.objects.get(measurementType='Temperature')
        response = self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        print(measurement.value)
        res = measurement.is_notified
        self.assertEqual(res, 1)

    def tearDown(self):
        Archive.objects.all().delete()
        Measurement.objects.all().delete()
        User.objects.all().delete()