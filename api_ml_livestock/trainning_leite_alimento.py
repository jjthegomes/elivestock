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

BASE_NAME = "./models/alimento_"

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


def split_train_data(file = 'data/pesoXleite.csv', values = {'start': 1, 'end': 2}, label = 2):
    dataset = pd.read_csv(file)
    dataset['Algodão'] = dataset['Algodão'].fillna(0)
    dataset['CONCENTRADO'] = dataset['CONCENTRADO'].fillna(0)
    dataset['Complemento alimenta'] = dataset['Complemento alimenta'].fillna(0)
    dataset['Farinha de Milho'] = dataset['Farinha de Milho'].fillna(0)
    dataset['Farinha de Soja'] = dataset['Farinha de Soja'].fillna(0)
    dataset['Feno'] = dataset['Feno'].fillna(0)
    dataset['Silagem de milho'] = dataset['Silagem de milho'].fillna(0)
    dataset['qtd_animais_alimentados'] = dataset['qtd_animais_alimentados'].fillna(0)

    dataset.fillna(0)
    print(dataset.head())
    
    X = dataset.iloc[:, values['start']:values['end']].values # X = dataset.iloc[:, 1:2].values
    y = dataset.iloc[:, label].values                         # y = dataset.iloc[:, 2].values

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


def run_best_model(filename =  './models/alimento_AdaBoostRegressor.pkcls', data = [[52, 0, 0, 110, 126, 30, 0, 904]]):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(data)
    print(result)
    return result


def run_all_models():
    print("Trainning....")
    values = { 'start': 1, 'end': 9} # alimentos
    label = 9 # leite
    X_train, X_test, y_train, y_test = split_train_data('./data/alimentoXtipo.csv', values, label)

    print("RandomForestRegressor: ")
    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    run_model(BASE_NAME+"RandomForestRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nNeural Network MLPRegressor: ")
    regressor = MLPRegressor(random_state=1, max_iter=1000).fit(X_train, y_train)
    run_model(BASE_NAME+"MLPRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

    print("\nKNN KNeighborsRegressor: ")
    regressor =  KNeighborsRegressor(n_neighbors=2)
    run_model(BASE_NAME+"KNeighborsRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test) 

                    # Nao funciona
                    # print("\nKNN RadiusNeighborsRegressor: ")
                    # regressor =  RadiusNeighborsRegressor(radius=1.0)
                    # run_model(BASE_NAME+"RadiusNeighborsRegressor.pkcls", regressor,  X_train, y_train, X_test, y_test)

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
# [[Algodão,CONCENTRADO,Complemento alimenta,Farinha de Milho,Farinha de Soja,Feno,Silagem de milho]]
test = [[52, 0, 0, 110, 126, 30, 0, 904]]
run_best_model('./models/alimento_AdaBoostRegressor.pkcls', test)

# run_all_models()
