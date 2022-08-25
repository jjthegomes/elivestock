import os
import flask
import pandas as pd

from flask import request, jsonify
from owlready2 import *
from datetime import datetime

import predict
import ontology

fileName = r"new_provcow.owl"
if os.path.isfile(fileName):
    print("Loading OWL file...")
else:
    ontology.generateOntology(True, True, False)


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def run_prediction(request, predict_function):
    data = [request.json]
    df = pd.DataFrame(data)
    result = predict_function(df)

    resultado = {"result": result[0]}

    data.append(resultado)
    return resultado


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Decision e-Livestock ML</h1>
<p>An API for machine learning in livestock.</p>
<p> Ontology and ML Algorithm.</p>'''

@app.route('/api/predict/milk/individual', methods=['POST'])
def api_predict_milk_individual():
    data = run_prediction(request, predict.predict_milk)
    return jsonify(data)

@app.route('/api/predict/milk/animais', methods=['POST'])
def api_predict_milk_animais():
    data = run_prediction(request, predict.predict_leite_animais)
    return jsonify(data)


@app.route('/api/predict/milk/geral', methods=['POST'])
def api_predict_milk_geral():
    body = request.json
    date = datetime.strptime(body['date'], '%Y-%m-%d')

    df = pd.DataFrame([date])
    result = predict.predict_milk_geral(df)
    return jsonify({"result": result[0]})


@app.route('/api/predict/milk/alimento', methods=['POST'])
def api_predict_milk_alimento():
    data = run_prediction(request, predict.predict_milk_alimento)
    return jsonify(data)

@app.route('/api/predict/temperature/date', methods=['POST'])
def api_predict_temperature_date():  
    body = request.json
    date = datetime.strptime(body['date'], '%Y-%m-%d')

    df = pd.DataFrame([date])
    result = predict.predict_temperature_date(df)
    return jsonify({"result": result[0]})

@app.route('/api/predict/humidity/date', methods=['POST'])
def api_predict_humidity_date():
    body = request.json
    date = datetime.strptime(body['date'], '%Y-%m-%d')

    df = pd.DataFrame([date])
    result = predict.predict_humidity_date(df)
    return jsonify({"result": result[0]})

@app.route('/api/predict/animal/lote/mastite', methods=['POST'])
def api_animal_lote_mastiti():
    onto = ontology.generateOntology(True, False, False)
    # onto = get_ontology("./new_provcow.owl").load(reload_if_newer = True)    
    data = ontology.getAnimalsLotes(onto)        
    return jsonify(data)
    
@app.route('/api/predict/ambiente/compost', methods=['POST'])
def api_ambiente_compost():
    onto = get_ontology("./new_provcow_ambiente.owl").load(reload_if_newer = True)        
    data = ontology.getTempAndHumidity(onto)        
    return jsonify(data)

@app.route('/api/predict/animal/lote/leite', methods=['POST'])
def api_animal_lote_leite():
    onto = get_ontology("./new_provcow.owl").load(reload_if_newer = True)    
    data = ontology.getAnimalsPeso(onto)
    body = request.json
    
    listResult = []

    if 'isFullYear' in body:
        listMonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for month in listMonth:
            for peso in data:
                req = [{'Peso': peso, 'date': month}]
                df = pd.DataFrame(req)
                result = predict.predict_milk(df)
                result = {"input": peso, "result": result[0], 'date': month}
                listResult.append(result)
    else:
        if 'month' in body:
            month = body['month']
        else:
            month = datetime.now().month

        for peso in data:
            req = [{'Peso': peso, 'date': month}]
            df = pd.DataFrame(req)
            result = predict.predict_milk(df)
            result = {"input": peso, "result": result[0], 'date': month}
            listResult.append(result)
        
    return jsonify(listResult)


app.run()
