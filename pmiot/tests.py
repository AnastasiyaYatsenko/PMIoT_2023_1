import inspect
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from pmiot.models import Measurement, Archive
from pmiot.scheduler.scheduler import data_from_dataset


class FuncTest(TestCase):

    def setUp(self):
    
        Measurement.objects.create(measurementType='Temperature')
        Measurement.objects.create(measurementType='Humidity')

        # output results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print('Number of sensors:', len(Measurement.objects.all()))


    def test_function_with_valid_data(self):
        # Test the function with valid input data
                # change instances (isWorking = True)
        measurement1 = Measurement.objects.get(measurementType='Temperature')
        measurement1.isWorking = True
        measurement1.save()
        measurement2 = Measurement.objects.get(measurementType='Humidity')
        measurement2.isWorking = True
        measurement2.save()
        
        # run function
        res = data_from_dataset()

        # output results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')
        
        # compare results
        self.assertEqual(len(res), 2)

    def test_function_with_invalid_data(self):
        # Test the function with invalid input data (e.g., empty dataset)
        measurement1 = Measurement.objects.get(measurementType='Temperature')
        measurement1.isWorking = False
        measurement1.save()
        measurement2 = Measurement.objects.get(measurementType='Humidity')
        measurement2.isWorking = False
        measurement2.save()
        
        # run function
        res = data_from_dataset()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')

        self.assertEqual(len(res), 0)

    def tearDown(self):
        Archive.objects.all().delete()
        Measurement.objects.all().delete()
        User.objects.all().delete()    


