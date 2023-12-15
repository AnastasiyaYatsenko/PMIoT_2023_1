import inspect
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from pmiot.models import Measurement, Archive
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
        measurement.save()

        # c = Client(enforce_csrf_checks=True)
        self.client.login(username='admin', password='admin')
        user = User.objects.get(username='admin')
        measurement = Measurement.objects.get(measurementType='Temperature')
        # response = c.get('/measurement_details/' + str(measurement.pk))
        # factory = RequestFactory()
        # request = factory.get('/measurement_details/' + str(measurement.pk))
        response = self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        # self.assertRedirects(response, ('/measurement_details/' + str(measurement.pk)),
        #                      status_code=301, target_status_code=200)
        # response = c.get('/', follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        print(measurement.value)
        res = measurement.is_notified
        self.assertEqual(response.status_code, 200)

    def test__value_less_then_comfortable(self):
        # change instance (isWorking = True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        measurement.isWorking = True
        measurement.max_comfort = 90
        measurement.min_comfort = 100
        measurement.is_notified = False
        measurement.save()

        # c = Client(enforce_csrf_checks=True)
        self.client.login(username='admin', password='admin')
        user = User.objects.get(username='admin')
        measurement = Measurement.objects.get(measurementType='Temperature')
        # response = c.get('/measurement_details/' + str(measurement.pk))
        # factory = RequestFactory()
        # request = factory.get('/measurement_details/' + str(measurement.pk))
        response = self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        # self.assertRedirects(response, ('/measurement_details/' + str(measurement.pk)),
        #                      status_code=301, target_status_code=200)
        # response = c.get('/', follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        print(measurement.value)
        res = measurement.is_notified
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        Archive.objects.all().delete()
        Measurement.objects.all().delete()
        User.objects.all().delete()

class DetailsViewsTests(TestCase):
    # prepare data for every test
    def setUp(self):
        # create 2 instances with different types
        admin = User.objects.create_superuser(username='admin', password='admin')
        measurement = Measurement.objects.create(measurementType='Temperature',
                                                 image='/static/images/BMP085.jpg', value=11.0)
        
        Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print('Number of sensors:', len(Measurement.objects.all()))

        pass

    def test__if_value_update(self):
        self.client.login(username='admin', password='admin')
        User.objects.get(username='admin')

        measurement = Measurement.objects.get(measurementType='Temperature')
        self.client.get("/measurement_details/" + str(measurement.pk), follow=True)        
        oldValue = measurement.value
        # print("old value:", oldValue)

        # change instance (isWorking = False)
        measurement = Measurement.objects.get(measurementType='Temperature')
        measurement.isWorking = True
        measurement.save()

        self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        newValue = measurement.value
        # print("new value:", newValue)

        # res = measurement.isWorking
        self.assertNotEqual(oldValue, newValue)


    def test__if_value_not_update(self):
        self.client.login(username='admin', password='admin')
        User.objects.get(username='admin')

        measurement = Measurement.objects.get(measurementType='Temperature')
        self.client.get("/measurement_details/" + str(measurement.pk), follow=True)   
        oldValue = measurement.value

        # change instance (isWorking = False)
        measurement.isWorking = False
        measurement.save()

        self.client.get("/measurement_details/" + str(measurement.pk), follow=True)
        measurement = Measurement.objects.get(measurementType='Temperature')
        newValue = measurement.value
        # print("new value:", newValue)

        # res = measurement.isWorking
        self.assertEqual(oldValue, newValue)
    
    def tearDown(self):
        Archive.objects.all().delete()
        Measurement.objects.all().delete()
        User.objects.all().delete()
