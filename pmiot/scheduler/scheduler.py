from datetime import datetime
import os
import pandas as pd

import paho.mqtt.client as mqtt
from django.conf import settings

import pytz
KyivTz = pytz.timezone("Europe/Kiev")

from pmiot.models import Measurement, Archive

# variables
num_row = 14570
measurement_types = ['Gas', 'Humidity', 'Light', 'Temperature']
column_names = ['Carbon_Monoxide [Ohms]', 'Relative_Humidity [%]',
                'Light_Level [Ohms]', 'Temperature-BMP [Celsius]']
dict = {measurement_types[i]: column_names[i]
        for i in range(len(measurement_types))}


# get data from dataset
def data_from_dataset(id=-1):
    # path to data
    file_path = os.path.dirname(__file__)
    file_path = os.path.dirname(os.path.dirname(file_path))
    file_path = os.path.join(file_path, 'AirPi Data - AirPi.csv')
    # debug
    # print('Path:', file_path)

    # prepare variables
    result = {}
    global num_row

    # check file exists
    if os.path.exists(file_path):
        # read file
        ds = pd.read_csv(file_path)

        # if regular update on all sensors
        if id == -1:
            # get working sensors
            try:
                sensors = Measurement.objects.all().filter(isWorking=True)
            except Measurement.DoesNotExist:
                sensors = None
            # debug
            # print('Working sensors: ', sensors)
        # if turning on one sensor
        else:
            # get working sensor
            try:
                sensors = Measurement.objects.filter(pk=id, isWorking=True)
            except Measurement.DoesNotExist:
                sensors = None
            # debug
            # print('Sensor is working: ', sensors[0].isWorking)

        if sensors is None:
            # debug
            print('No sensors to update!')
        else:
            # link sensors and values
            for s in sensors:
                col = dict.get(s.measurementType)
                val = ds[col][num_row]
                result.update({s.pk: val})
                # debug
                # print('Value:', val)

        # check if last row
        if num_row < 14571:
            num_row = num_row + 1
        else:
            num_row = 0
        # debug
        # print('Row:', num_row)
    else:
        # error warning
        print('Error! No file was found for getting data!')
    return result


# transfer data to database
def process_data(id=-1):
    data = data_from_dataset(id)
    # debug
    # print('We got:', data)
    dt = datetime.now(KyivTz)
    # debug
    # print(dt)

    # try to connect to server
    try:
        def on_connect(mqtt_client, userdata, flags, rc):
            if rc == 0:
                print('Connected successfully')
                mqtt_client.subscribe('django/mqtt')
            else:
                print('Bad connection. Code:', rc)

        def on_message(mqtt_client, userdata, msg):
            print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

        client.connect(
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT
        )

        # try to publish test data
        try:
            client.loop_start()
            rc, mid = client.publish('test topic', 'test message')
            client.loop_stop()
            print(rc, mid)
        except Exception as e:
            print(f"Error publishing message: {e}")

        # try to publish data
        try:
            for pair in data.items():
                # publish data
                publish_data(client, pair)
                # debug
                # print('Pair:', pair)
        except Exception as e:
            print(f"Error publishing message: {e}")

    except ConnectionError as e:
        print(f"Error connecting to MQTT broker: {e}")

    client.disconnect()

    write_to_db(dt, data)

# get topics for all sensors
def get_all_topics():
    # get all sensors
    sensors = Measurement.objects.all()
    # create topics (measurementType) for all sensors
    topics = {i.pk: i.measurementType for i in sensors}
    # debug
    # print('Topics:', topics)
    return topics

# get topic for sensor by id
def get_topic(id):
    return get_all_topics().get(id)

# send data to server
def publish_data(client, data):
    #prepare data
    # get sensor id and value
    key, value = data
    # get topic
    topic = get_topic(key)
    # debug
    # print('Topic - value:', topic, '-', value)

    # publish data
    rc, mid = client.publish(topic, value)
    # debug
    # print('Publish result:', rc, mid)
 
def write_to_db(dt, data):
    # debug
    # print('infunc', data)
    for sensor_id, value in data.items():
        # debug
        # print(sensor_id)
        measurement = Measurement.objects.get(pk=sensor_id)
        measurement.value = value
        measurement.save()
        archive = Archive(sensor_id=measurement, value=value, timestamp=dt)
        archive.save()
