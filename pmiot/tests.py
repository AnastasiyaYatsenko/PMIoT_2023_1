import inspect
import time
from datetime import datetime

from django.urls import reverse

from django.contrib.auth.models import User
from django.test import TestCase

from pmiot.models import Measurement, Archive
from pmiot.scheduler.scheduler import data_from_dataset


class URLTest(TestCase):
    

    def test_view_performance(self):

        # Вимірюємо час, який потрібен для здійснення запиту до views
        start_time = time.time()
        response = self.client.get('/about')
        end_time = time.time()

        # Перевіряємо статус відповіді HTTP
        self.assertEqual(response.status_code, 200)

        # Встановлюємо поріг для часу відповіді 
        response_time_threshold = 0.5  # в секундах

        # Перевіраємо чи час відповіді входить в допустимий діапазон
        response_time = end_time - start_time
        self.assertLessEqual(response_time, response_time_threshold)

        # виводимо результат
        print(f"Response Time for about {response_time} seconds")

    def test_home_view_url(self):
        # 
        response = self.client.get('/')

        # 
        self.assertEqual(response.status_code, 200)

        # 
        # self.assertTemplateUsed(response, 'pmiot/home.html')

        # Output results
        print(f"URL Routing Test Passed for {'/'}")    


