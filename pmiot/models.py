# from django.db import models
# from djongo import models

import atexit

import inspect

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from datetime import datetime
import pytz
KyivTz = pytz.timezone("Europe/Kiev")


def print_finction_class():
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name
    class_name = frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else None

    print()
    if class_name:
        print(f"Class: {class_name}, Function: {function_name}")
    else:
        print(f"Function: {function_name}")

class MongoDB():
    # connections
    ###############################################################
    
    # fileds
    client = None
    _initialized = None

    # def __new__(cls, *args, **kwargs):
    #     print_finction_class()

    #     if not cls._instance:
    #         cls._instance = super().__new__(cls)
    #         try:
    #             cls._instance.client = MongoClient('mongodb://student:pmiot2023@localhost:27017/SerialDB')
    #             cls.client = cls._instance.client
    #         except ConnectionFailure as e:
    #             print(f"Failed to connect to MongoDB: {e}")
    #     else:
    #         print('Already connected!')
        
    #     atexit.register(cls._instance.close_mongo_connection) 
    #     return cls._instance

    # def get_connection(self):
    #     print_finction_class()

    #     return self._instance.client

    # # when instance is created
    # def __new__(cls, *args, **kwargs):
    #     print_finction_class()

    #     if not cls._instance:
    #         print("Creating a new instance")
    #         cls._instance = super().__new__(cls)
    #         cls._instance.client = None
    #         cls._instance._initialized = False

    #         try:
    #             cls._instance.client = MongoClient('mongodb://student:pmiot2023@localhost:27017/SerialDB')
    #             print('Client connected!\n', cls._instance.client)
    #             cls._instance.find_measurements()
    #         except ConnectionFailure as e:
    #             print(f"Failed to connect to MongoDB: {e}")

    #         atexit.register(cls._instance.close_mongo_connection)
    #         cls._instance._initialized = True
    #     else:
    #         print("Returning existing instance")

    #     return cls._instance
# 
    # connect to database
    def __init__(self):
        if self._initialized:
            print('Already connected!')
            return
        
        print_finction_class()
        
        try:
            self.client = MongoClient('mongodb://student:pmiot2023@localhost:27017/SerialDB')
            # debug
            print('Client connected!\n', self.client)
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
        
        atexit.register(self.close_mongo_connection)
        self._initialized = True
    
    # close connection if application is closed
    def close_mongo_connection(self):
        print_finction_class()

        if self.client:
            self.client.close()
    
    # collections
    ###############################################################
    
    # collection of sensors
    def get_collection_measurement(self):
        print_finction_class()

        db = self.client['SerialDB']
        collection = db['Measurement']
        return collection
    
    # collection of previous values
    def get_collection_archive(self):
        print_finction_class()

        db = self.client['SerialDB']
        collection = db['Archive']
        return collection
    
    # find sensors
    ###############################################################

    # get all sensors
    def find_measurements(self):
        print_finction_class()

        result = self.get_collection_measurement().find()
        # debug
        print('Cursor:', result)
        document_list = list(result)
        print(len(document_list))
        # debug
        for doc in document_list:
            print('Sensors found:', doc)
        return result
    
    # get sensor by measurementType
    def find_measurement(self, value, id=True):
        print_finction_class()

        if id:
            result = self.get_collection_measurement().find_one({'_id': value})
        else:
            result = self.get_collection_measurement().find_one({'measurementType': value})
        # debug
        print('Sensor found:', result)
        return result
    
    # operations with sensors
    ###############################################################

    # add document to collection of sensors
    def insert_measurement(self, data):
        print_finction_class()

        data.pop('_id', None)
        result = self.get_collection_measurement().insert_one(data).inserted_id
        # debug
        print('Sensor id:', result)
        print('Sensor added:', self.find_measurement(result))
        return result
    
    # change document to collection of sensors
    def update_measurement(self, data):
        print_finction_class()

        sensor = self.find_measurement(data['pk'])
        element = {'_id': sensor.get('_id')}
        value = {'value': data['value']}
        self.get_collection_measurement().update_one(element, value)
        # debug
        print('Sensor changed:', self.find_measurement(sensor.get('_id')))
    
    def delete_measurement(self, data):
        print_finction_class()

        sensor = self.find_measurement(data['pk'])
        element = {'_id': sensor.get('_id')}
        self.get_collection_measurement().delete_one(element)
        # debug
        print('Sensor deleted:', data['pk'])
    
    # find archive
    ###############################################################

    # get all instances of archive by id
    def find_archive(self, value):
        print_finction_class()

        result = self.get_collection_archive().find({'_id': value})
        # debug
        print('Data found:', result)
        return result
    
    # operations with archive
    ###############################################################        
    
    # add document to collection of previous values
    def insert_archive(self, data):
        print_finction_class()

        data.pop('_id', None)
        result = self.get_collection_archive().insert_one(data).inserted_id
        # debug
        print('Archive id:', result)
        print('Archive added:', self.find_archive(result))
        return result


class Measurement():
    def __init__(self, data):
        print_finction_class()

        self.pk = data._id if '_id' in data else None
        self.measurementName = data['measurementName']
        self.measurementType = data['measurementType']
        self.description = data['description'] if 'description' in data else None
        self.min_value = data['min_value'] if 'min_value' in data else 0
        self.max_value = data['max_value'] if 'max_value' in data else 100
        self.value = data['value'] if 'value' in data else 0
        self.dimension = data['dimension'] if 'dimension' in data else '°C'
        self.isWorking = data['isWorking'] if 'isWorking' in data else False

        self.image = data['image'] if 'image' in data else None

        self.min_comfort = data['min_comfort'] if 'min_comfort' in data else 0
        self.max_comfort = data['max_comfort'] if 'max_comfort' in data else 0
        self.need_notification = data['need_notification'] if 'need_notification' in data else False
        self.is_notified = data['is_notified'] if 'is_notified' in data else False
        self.last_notified = data['last_notified'] if 'last_notified' in data else True
    
    def to_dict(self):
        print_finction_class()

        result = self.__dict__
        # debug
        print('To dict:\n', result)
        return result
    
    def save(self):
        print_finction_class()

        print(f'{self.measurementName} is saved!')
        mongo_db.update_measurement(self.to_dict())

class Archive():
    def __init__(self, data):
        print_finction_class()

        self.sensor_id = data['sensor_id']
        self.value = data['value'] if 'value' in data else 0
        self.timestamp = data['timestamp'] if 'timestamp' in data else datetime.now(KyivTz)
    
    def to_dict(self):
        print_finction_class()

        result = self.__dict__
        # debug
        print('To dict:\n', result)
        return result


mongo_db = MongoDB()

# class Measurement(models.Model):
#     measurementName = models.CharField(default='Name', max_length=250)
#     measurementType = models.CharField(default='Type', max_length=250)
#     description = models.CharField(max_length=250, blank=True, null=True)
#     min_value = models.IntegerField(default=0)
#     max_value = models.IntegerField(default=100)
#     value = models.FloatField(default=0, blank=True, null=True)
#     dimension = models.CharField(default='°C', max_length=10)
#     isWorking = models.BooleanField(default=False)

#     image = models.ImageField(default=None, upload_to='', null=True)

#     min_comfort = models.IntegerField(default=0)
#     max_comfort = models.IntegerField(default=100)
#     need_notification = models.BooleanField(default=False)
#     is_notified = models.BooleanField(default=False)
#     last_notified = models.DateTimeField(default=None, null=True)

#     class Meta:
#         ordering = ['measurementName']

#     def __str__(self):
#         return f'{self.measurementName} - {self.measurementType} - {self.value}'


# class Archive(models.Model):
#     sensor_id = models.ForeignKey(Measurement,on_delete=models.CASCADE)
#     value = models.FloatField(default=0)
#     timestamp = models.DateTimeField(default=None)

#     class Meta:
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.sensor_id} - {self.value} - {self.timestamp}"
