import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import RadiusNeighborsRegressor


from sklearn import metrics
import pickle

BASE_NAME = "./models/leite_"

def save_model(filename = './models/random_forest_leite.sav', regressor = False):
    pickle.dump(regressor, open(filename, 'wb'))


def getErro(test, result):
    mean = metrics.mean_absolute_error(test, result)
    mse =  metrics.mean_squared_error(test, result)
    rmse = np.sqrt(metrics.mean_squared_error(test, result))
    print('Mean Absolute Error:', mean)
    print('Mean Squared Error:', mse)
    print('Root Mean Squared Error:', rmse)
    return mean, mse, rmse


def split_train_data(file = 'data/pesoXleite.csv', values =  {'start': 1, 'end': 2}, label = 2):
    dataset = pd.read_csv(file)
    dataset.fillna(0)
    print(dataset.head())
    
    X = dataset.iloc[:, values['start']:values['end']].values   # X = dataset.iloc[:, 1:2].values
    y = dataset.iloc[:, label].values                           # y = dataset.iloc[:, 2].values

    return train_test_split(X, y, test_size=0.2, random_state=0)



def run_model(name, model, X_train, y_train, X_test, y_test):
    try:
        regressor = model.fit(X_train, y_train)
        save_model(name, regressor)
        y_pred = regressor.predict(X_test)
        getErro(y_test, y_pred)
        return y_pred
    except NameError:
        print(NameError)

def run_best_model(filename =  './models/leite_RandomForestRegressor.pkcls', data = [[489]]):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(data)
    print(result)
    return result


# print(X_test)
# y_pred = regressor.predict([[489]])
# print(y_pred)

def run_all_models():
    print("Trainning....")
    values = { 'start': 1, 'end': 2} # peso
    label = 2 # leite
    X_train, X_test, y_train, y_test = split_train_data('data\pesoXleite.csv', values, label)

    print("RandomForestRegressor: ")
    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    run_model(BASE_NAME+"RandomForestRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nNeural Network MLPRegressor: ")
    regressor = MLPRegressor(random_state=1, max_iter=500).fit(X_train, y_train)
    run_model(BASE_NAME+"MLPRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nKNN KNeighborsRegressor: ")
    regressor =  KNeighborsRegressor(n_neighbors=2)
    run_model(BASE_NAME+"KNeighborsRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nKNN RadiusNeighborsRegressor: ")
    regressor =  RadiusNeighborsRegressor(radius=1.0)
    run_model(BASE_NAME+"RadiusNeighborsRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test)

    print("\nAdaBoostRegressor: ")
    regressor = AdaBoostRegressor(random_state=0, n_estimators=100)
    run_model(BASE_NAME+"AdaBoostRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nBaggingRegressor with SVR: ")
    regressor = BaggingRegressor(base_estimator=SVR(), n_estimators=10, random_state=0)
    run_model(BASE_NAME+"BaggingRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nExtraTreesRegressor: ")
    regressor = ExtraTreesRegressor(n_estimators=100, random_state=0)
    run_model(BASE_NAME+"ExtraTreesRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nGradientBoostingRegressor: ")
    regressor = GradientBoostingRegressor(random_state=0)
    run_model(BASE_NAME+"GradientBoostingRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nHistGradientBoostingRegressor: ")
    regressor = HistGradientBoostingRegressor(random_state=0)
    run_model(BASE_NAME+"HistGradientBoostingRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nEpsilon-Support Vector Regression: ")
    regressor = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
    run_model(BASE_NAME+"SvmRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 


# HOW TO USE
# [[PESO]]
# test = [[495]]
# run_best_model('./models/leite_RandomForestRegressor.pkcls', test)

run_all_models()
