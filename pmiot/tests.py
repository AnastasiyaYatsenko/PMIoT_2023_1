import inspect
import time

from datetime import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from pmiot.models import Measurement, Archive
from pmiot.scheduler.scheduler import data_from_dataset

from django.db import IntegrityError

class MongoTests(TestCase):

  # prepare data for every test
  def setUp(self):
        
    # create instance of sensor
    sensor = Measurement.objects.create(measurementType='Humidity')
    # create instance of archive
    archive = Archive.objects.create(sensor_id=sensor, value=sensor.value)

    # print results
    print()
    print(inspect.getframeinfo(inspect.currentframe()).function)
    print('Number of sensors:', len(Measurement.objects.all()))
    print('Number of archives:', len(Archive.objects.all()))

    pass

  # test for getting measurement
  def test__get_sensor(self):
        
    try:
      # get measurement
      sensor = Measurement.objects.get(measurementType='Humidity')
            
      # print results
      print()
      print(inspect.getframeinfo(inspect.currentframe()).function)
      print(f'Sensor: {sensor}')
      print('------------')
      true = True
    except Measurement.DoesNotExist:
      print('Measurement not found!')
      true = False

    # check results
    self.assertTrue(true)
    
  # test for getting archive
  def test__get_archive(self):
        
    try:
      # get measurement
      sensor = Measurement.objects.get(measurementType='Humidity')
      # get archive
      archive = Archive.objects.get(sensor_id=sensor)

      # print results
      print()
      print(inspect.getframeinfo(inspect.currentframe()).function)
      print(f'Archive: {archive}')
      print('------------')
      true = True
    except Archive.DoesNotExist:
      print('Archive not found!')
      true = False

    # check results
    self.assertTrue(true)
    
  # test for creating measurement
  def test__insert_sensor(self):
        
    try:
      # create measurement
      sensor = Measurement.objects.create(measurementType='Temperature')

      # print results
      print()
      print(inspect.getframeinfo(inspect.currentframe()).function)
      print(f'Sensor: {sensor}')
      print('------------')
      true = True
    except IntegrityError:
      print('Measurement not created!')
      true = False

    # check results
    self.assertTrue(true)

  # test for creating archive
  def test__insert_archive(self):
        
    try:
      # create measurement
      sensor = Measurement.objects.create(measurementType='Temperature')
      # create archive
      archive = Archive.objects.create(sensor_id=sensor, value=sensor.value)

      # print results
      print()
      print(inspect.getframeinfo(inspect.currentframe()).function)
      print(f'Archive: {archive}')
      print('------------')
      true = True
    except IntegrityError:
      print('Archive not created!')
      true = False

    # check results
    self.assertTrue(true)
    
    # test for changing measurement
    def test__update_sensor(self):
        
        # get measurement
        sensor = Measurement.objects.get(measurementType='Humidity')
        old_value = sensor.value

        # change value
        sensor.value = sensor.value + 10
        sensor.save()
        new_value = sensor.value

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(f'Value: {old_value} -> {new_value}')
        print('------------')

        # check results
        self.assertNotEqual(old_value, new_value)
    
    # test for deleting measurement
    def test__delete_sensor(self):
        
        # get measurement
        sensor = Measurement.objects.get(measurementType='Humidity')
        start_count = Measurement.objects.count()

        # delete sensor
        sensor.delete()
        end_count = Measurement.objects.count()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(f'Count: {start_count} -> {end_count}')
        print('------------')

        # check results
        self.assertEqual(end_count, start_count - 1)

    # test for deleting archive
    def test__delete_archive(self):
        
        # get measurement
        sensor = Measurement.objects.get(measurementType='Humidity')
        # create archive
        archive = Archive.objects.get(sensor_id=sensor)
        start_count = Archive.objects.count()

        # delete archive
        archive.delete()
        end_count = Archive.objects.count()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(f'Count: {start_count} -> {end_count}')
        print('------------')

        # check results
        self.assertEqual(end_count, start_count - 1)
    
    # test for deleting archive
    def test__delete_sensor_with_archive(self):
        
        # get measurement
        sensor = Measurement.objects.get(measurementType='Humidity')
        # create archive
        archive = Archive.objects.get(sensor_id=sensor)
        start_count = Archive.objects.count()

        # delete sensor
        sensor.delete()
        end_count = Archive.objects.count()

        # print results
        print()
        print(inspect.getframeinfo(inspect.currentframe()).function)
        print(f'Count: {start_count} -> {end_count}')
        print('------------')

        # check results
        self.assertEqual(end_count, start_count - 1)
# class FunctionTests(TestCase):

#     # prepare data for every test
#     def setUp(self):
        
#         # create 2 instances with different types
#         Measurement.objects.create(measurementType='Temperature')
#         Measurement.objects.create(measurementType='Humidity')

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print('Number of sensors:', len(Measurement.objects.all()))

#         pass

#     # test for function 'data_from_dataset'
#     # for one instance
#     # which is working
#     def test__data_from_dataset__id__working(self):
        
#         # change instance (isWorking = True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         measurement.isWorking = True
#         measurement.save()

#         # run function
#         res = data_from_dataset(measurement._id)

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print(res)
#         print('------------')

#         # check results
#         self.assertEqual(len(res), 1)

#     # test for function 'data_from_dataset'
#     # for one instance
#     # which is not working
#     def test__data_from_dataset__id__not_working(self):
        
#         # change instance (isWorking = False)
#         measurement = Measurement.objects.get(measurementType='Humidity')
#         measurement.isWorking = False
#         measurement.save()

#         # run function
#         res = data_from_dataset(measurement._id)

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print(res)
#         print('------------')

#         # check results
#         self.assertEqual(len(res), 0)

#     # test for function 'data_from_dataset'
#     # for all instances
#     # all of which are working
#     def test__data_from_dataset__all__working(self):

#         # change instances (isWorking = True)
#         measurement1 = Measurement.objects.get(measurementType='Temperature')
#         measurement1.isWorking = True
#         measurement1.save()
#         measurement2 = Measurement.objects.get(measurementType='Humidity')
#         measurement2.isWorking = True
#         measurement2.save()
        
#         # run function
#         res = data_from_dataset()

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print(res)
#         print('------------')
        
#         # check results
#         self.assertEqual(len(res), 2)
    
#     # test for function 'data_from_dataset'
#     # for all instances
#     # all of which are not working
#     def test__data_from_dataset__all__not_working(self):
        
#         # change instances (isWorking = False)
#         measurement1 = Measurement.objects.get(measurementType='Temperature')
#         measurement1.isWorking = False
#         measurement1.save()
#         measurement2 = Measurement.objects.get(measurementType='Humidity')
#         measurement2.isWorking = False
#         measurement2.save()
        
#         # run function
#         res = data_from_dataset()

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print(res)
#         print('------------')
        
#         # check results
#         self.assertEqual(len(res), 0)

#     # test for function 'data_from_dataset'
#     # for all instances
#     # some of which are working and some are not
#     def test__data_from_dataset__all__working_and_not(self):

#         # change instances (isWorking = True and isWorking = False)
#         measurement1 = Measurement.objects.get(measurementType='Temperature')
#         measurement1.isWorking = False
#         measurement1.save()
#         measurement2 = Measurement.objects.get(measurementType='Humidity')
#         measurement2.isWorking = True
#         measurement2.save()
        
#         # run function
#         res = data_from_dataset()

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print(res)
#         print('------------')
        
#         # check results
#         self.assertEqual(len(res), 1)

# class NotificationTests(TestCase):

#     # prepare data for every test
#     def setUp(self):
#         # create 2 instances with different types
#         admin = User.objects.create_superuser(username='admin', password='admin')
#         measurement = Measurement.objects.create(measurementType='Temperature',
#                                                  image='/static/images/BMP085.jpg')
#         Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print('Number of sensors:', len(Measurement.objects.all()))

#         pass

#     def test__value_more_then_comfortable(self):
#         # change instance (isWorking = True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         measurement.isWorking = True
#         measurement.max_comfort = -5
#         measurement.min_comfort = -10
#         measurement.is_notified = False
#         measurement.need_notification = True
#         measurement.save()

#         self.client.login(username='admin', password='admin')
#         user = User.objects.get(username='admin')
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         response = self.client.get("/measurement_details/" + str(measurement._id), follow=True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         print(measurement.value)
#         res = measurement.is_notified
#         self.assertEqual(res, 1)

#     def test__value_less_then_comfortable(self):
#         # change instance (isWorking = True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         measurement.isWorking = True
#         measurement.max_comfort = 90
#         measurement.min_comfort = 100
#         measurement.is_notified = False
#         measurement.need_notification = True
#         measurement.save()

#         self.client.login(username='admin', password='admin')
#         user = User.objects.get(username='admin')
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         response = self.client.get("/measurement_details/" + str(measurement._id), follow=True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         print(measurement.value)
#         res = measurement.is_notified
#         self.assertEqual(res, 1)

#     def tearDown(self):
#         Archive.objects.all().delete()
#         Measurement.objects.all().delete()
#         User.objects.all().delete()

# class DetailsViewsTests(TestCase):
#     # prepare data for every test
#     def setUp(self):
#         # create 2 instances with different types
#         admin = User.objects.create_superuser(username='admin', password='admin')
#         measurement = Measurement.objects.create(measurementType='Temperature',
#                                                  image='/static/images/BMP085.jpg', value=11.0)
        
#         Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())

#         # print results
#         print()
#         print(inspect.getframeinfo(inspect.currentframe()).function)
#         print('Number of sensors:', len(Measurement.objects.all()))

#         pass

#     def test__if_value_update(self):
#         self.client.login(username='admin', password='admin')
#         User.objects.get(username='admin')

#         measurement = Measurement.objects.get(measurementType='Temperature')
#         self.client.get("/measurement_details/" + str(measurement._id), follow=True)        
#         oldValue = measurement.value
#         # print("old value:", oldValue)

#         # change instance (isWorking = False)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         measurement.isWorking = True
#         measurement.save()

#         self.client.get("/measurement_details/" + str(measurement._id), follow=True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         newValue = measurement.value
#         # print("new value:", newValue)

#         # res = measurement.isWorking
#         self.assertNotEqual(oldValue, newValue)


#     def test__if_value_not_update(self):
#         self.client.login(username='admin', password='admin')
#         User.objects.get(username='admin')

#         measurement = Measurement.objects.get(measurementType='Temperature')
#         self.client.get("/measurement_details/" + str(measurement._id), follow=True)   
#         oldValue = measurement.value

#         # change instance (isWorking = False)
#         measurement.isWorking = False
#         measurement.save()

#         self.client.get("/measurement_details/" + str(measurement._id), follow=True)
#         measurement = Measurement.objects.get(measurementType='Temperature')
#         newValue = measurement.value
#         # print("new value:", newValue)

#         # res = measurement.isWorking
#         self.assertEqual(oldValue, newValue)
    
#     def tearDown(self):
#         Archive.objects.all().delete()
#         Measurement.objects.all().delete()
#         User.objects.all().delete()

# class URLTest(TestCase):
#     def setUp(self):
#         # create 2 instances with different types
#         admin = User.objects.create_superuser(username='admin', password='admin')
#         measurement = Measurement.objects.create(measurementType='Temperature',
#                                                  image='/static/images/BMP085.jpg')
#         Archive.objects.create(sensor_id = measurement, value = 22.0, timestamp = datetime.now())
    

#     def test_view_performance(self):

#         self.client.login(username='admin', password='admin')

#         # Вимірюємо час, який потрібен для здійснення запиту до views
#         start_time = time.time()
#         response = self.client.get('/about', follow=True)
#         end_time = time.time()

#         # Встановлюємо поріг для часу відповіді 
#         response_time_threshold = 0.5  # в секундах

#         # Перевіраємо чи час відповіді входить в допустимий діапазон
#         response_time = end_time - start_time
#         self.assertLessEqual(response_time, response_time_threshold)

#     def test_home_view_url(self):
        
#         self.client.login(username='admin', password='admin')

#         # 
#         response = self.client.get('/', follow=True)

#         # 
#         self.assertEqual(response.status_code, 200)
    