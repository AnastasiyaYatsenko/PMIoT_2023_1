import inspect
import time
from datetime import datetime

from django.urls import reverse

from django.contrib.auth.models import User
from django.test import TestCase

from pmiot.models import Measurement, Archive
from pmiot.scheduler.scheduler import data_from_dataset


class URLTest(TestCase):
    def setUp(self):
        # create 2 instances with different types
        admin = User.objects.create_superuser(username='admin', password='admin')
        measurement = Measurement.objects.create(measurementType='Temperature',
                                                 image='/static/images/BMP085.jpg')
        Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())
    

    def test_view_performance(self):

        self.client.login(username='admin', password='admin')

        # Вимірюємо час, який потрібен для здійснення запиту до views
        start_time = time.time()
        response = self.client.get('/about', follow=True)
        end_time = time.time()

        # Встановлюємо поріг для часу відповіді 
        response_time_threshold = 0.5  # в секундах

        # Перевіраємо чи час відповіді входить в допустимий діапазон
        response_time = end_time - start_time
        self.assertLessEqual(response_time, response_time_threshold)

    def test_home_view_url(self):
        
        self.client.login(username='admin', password='admin')

        # 
        response = self.client.get('/', follow=True)

        # 
        self.assertEqual(response.status_code, 200)
