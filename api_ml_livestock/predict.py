from pickle import load


def run_model(model, data):
    with open(model, "rb") as ml:
        lr = load(ml)
    return lr.predict(data)


def predict_milk(data):
    return run_model("models/random_forest_leite.pkcls", data)


def predict_milk_geral(data):
    return run_model("models/random_forest_leite_GERAL.pkcls", data)


def predict_milk_alimento(data):
    return run_model("models/adaboost_alimento.pkcls", data)


def predict_temperature_date(data):
    print(data)
    return run_model("models/adaboost_avg_temperature.pkcls", data)


def predict_humidity_date(data):
    return run_model("models/adaboost_avg_humidity.pkcls", data)


def predict_leite_animais(data):
    return run_model("models/ada_boost_leite_animal_date.pkcls", data)
