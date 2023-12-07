from datetime import datetime
import time
import os
import pandas as pd

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
def process_data():
    data = data_from_dataset()
    print('We got:', data)
    dt = datetime.now()  # .strftime("%Y.%m.%d %H:%M:%S")
    print(dt)

    write_to_db(dt, data)


def write_to_db(dt, data):
    print('infunc', data)
    for sensor_id, value in data.items():
        print(sensor_id)
        measurement = Measurement.objects.get(pk=sensor_id)
        measurement.value = value
        measurement.save()
        archive = Archive(sensor_id=measurement, value=value, timestamp=dt)
        archive.save()
        