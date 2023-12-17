import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import BayesianRidge

from sklearn import tree

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from datetime import datetime
import pytz
KyivTz = pytz.timezone("Europe/Kiev")

from pmiot.models import Archive


def prognose(id):
    dt = datetime.now(KyivTz)
    data = prepare_data(id)
    # method names
    names = ['Linear Regression','Multi-layer Perceptron Regression', 'Decision Trees Regression','Bayesian Ridge Regression']
    # prognoses
    res = []
    res.append(custom_linear_regression(data, dt))
    res.append(custom_mlp_regression(data, dt))
    res.append(custom_decision_trees_regression(data, dt))
    res.append(custom_Bayesian_ridge_regression(data, dt))
    # names: prognoses
    dict = {names[i]: res[i] for i in range(len(names))}
    # debug
    for key, value in dict.items():
        print(key, ': ', value)
    return dict

def prepare_data(id):
    # get records by sensor_id
    archive = Archive.objects.filter(sensor_id=id)
    # transform data to dataframe
    data = pd.DataFrame(list(archive.values('timestamp', 'value')))
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # datetime to seconds
    data['timestamp'] = data['timestamp'].astype(np.int64) // 10**9
    #data = data.drop(columns=['timestamp'])
    return data

def custom_linear_regression(data, dt):
    # split timestamp and value
    X_train, y_train = data[['timestamp']], data['value']
    # create model
    model = make_pipeline(StandardScaler(), LinearRegression())
    # train model
    model.fit(X_train, y_train)
    # predict
    predicted_value = model.predict([[int(dt.timestamp())]])[0]
    # debug
    # print(f'Predicted value on {dt}: {predicted_value}')
    return predicted_value

def custom_mlp_regression(data, dt):
    # split timestamp and value
    X_train, y_train = data[['timestamp']], data['value']
    # create model
    model = make_pipeline(StandardScaler(), MLPRegressor(random_state=1, max_iter=500))
    # train model
    model.fit(X_train, y_train)
    # predict
    predicted_value = model.predict([[int(dt.timestamp())]])[0]
    # debug
    # print(f'Predicted value on {dt}: {predicted_value}')
    return predicted_value

def custom_decision_trees_regression(data, dt):
    # split timestamp and value
    X_train, y_train = data[['timestamp']], data['value']
    # create model
    model = make_pipeline(StandardScaler(), tree.DecisionTreeRegressor())
    # train model
    model.fit(X_train, y_train)
    # predict
    predicted_value = model.predict([[int(dt.timestamp())]])[0]
    # debug
    # print(f'Predicted value on {dt}: {predicted_value}')
    return predicted_value

def custom_Bayesian_ridge_regression(data, dt):
    # print("In Bayes")
    # split timestamp and value
    X_train, y_train = data[['timestamp']], data['value']
    # create model
    model = make_pipeline(StandardScaler(), BayesianRidge())
    # train model
    model.fit(X_train, y_train)
    # predict
    predicted_value = model.predict([[int(dt.timestamp())]])[0]
    # print(predicted_value)
    # print("---")
    # debug
    # print(f'Predicted value on {dt}: {predicted_value}')
    return predicted_value
