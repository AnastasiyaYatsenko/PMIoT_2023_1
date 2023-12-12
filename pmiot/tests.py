import inspect

from django.test import TestCase

from pmiot.models import Measurement
from pmiot.scheduler.scheduler import data_from_dataset

class FunctionTests(TestCase):

    # prepare data for every test
    def setUp(self):
        
        # create 2 instances with different types
        Measurement.objects.create(measurementType='Temperature')
        Measurement.objects.create(measurementType='Humidity')

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print('Number of sensors:', len(Measurement.objects.all()))

        pass

    # test for function 'data_from_dataset'
    # for one instance
    # which is working
    def test__data_from_dataset__id__working(self):
        
        # change instance (isWorking = True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        measurement.isWorking = True
        measurement.save()

        # run function
        res = data_from_dataset(measurement.pk)

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')

        # check results
        self.assertEqual(len(res), 1)

    # test for function 'data_from_dataset'
    # for one instance
    # which is not working
    def test__data_from_dataset__id__not_working(self):
        
        # change instance (isWorking = False)
        measurement = Measurement.objects.get(measurementType='Humidity')
        measurement.isWorking = False
        measurement.save()

        # run function
        res = data_from_dataset(measurement.pk)

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')

        # check results
        self.assertEqual(len(res), 0)

    # test for function 'data_from_dataset'
    # for all instances
    # all of which are working
    def test__data_from_dataset__all__working(self):

        # change instances (isWorking = True)
        measurement1 = Measurement.objects.get(measurementType='Temperature')
        measurement1.isWorking = True
        measurement1.save()
        measurement2 = Measurement.objects.get(measurementType='Humidity')
        measurement2.isWorking = True
        measurement2.save()
        
        # run function
        res = data_from_dataset()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')
        
        # check results
        self.assertEqual(len(res), 2)
    
    # test for function 'data_from_dataset'
    # for all instances
    # all of which are not working
    def test__data_from_dataset__all__not_working(self):
        
        # change instances (isWorking = False)
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
        
        # check results
        self.assertEqual(len(res), 0)

    # test for function 'data_from_dataset'
    # for all instances
    # some of which are working and some are not
    def test__data_from_dataset__all__working_and_not(self):

        # change instances (isWorking = True and isWorking = False)
        measurement1 = Measurement.objects.get(measurementType='Temperature')
        measurement1.isWorking = False
        measurement1.save()
        measurement2 = Measurement.objects.get(measurementType='Humidity')
        measurement2.isWorking = True
        measurement2.save()
        
        # run function
        res = data_from_dataset()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(res)
        print('------------')
        
        # check results
        self.assertEqual(len(res), 1)