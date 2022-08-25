from datetime import datetime, timedelta
from os import listdir, path as Path
from time import sleep
import threading 
import requests
import json 
import csv

api_url = "http://localhost:3001/api"

path = "../../csv/Temperatura-Umidade"
folders = listdir(path)

header = ['Leitura', 'Data', 'Hora', 'Idade', 'Umidade', 'Temperatura']
months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
list_year = [2017, 2018, 2019, 2020, 2021]

session = requests.Session()
session.headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
}
array_temperature = []
array_umidade = []


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parseDateTime(dateTime):
    return f"0{dateTime.strip()}" if len(dateTime) < 2 else dateTime


#Envia uma requisição para a API do INMET
def get_temperaturas_externas(data = "2022-03-22"):    
    url = "https://apitempo.inmet.gov.br/estacao/" + data + "/" + data + "/" + "A557#"
    response  = session.get(url).json()

    totalTemp = 0
    totalHum = 0

    for temp in response:
        try:
            totalTemp += float(temp['TEM_INS']) if temp["TEM_INS"] is not None else 0
            totalHum += float(temp['UMD_INS'] ) if temp["UMD_INS"] is not None else 0
        except Exception as e:
            print(e)

    totalTemp = (totalTemp / len(response)) if len(response) > 0 else 0
    totalHum = (totalHum / len(response)) if len(response) > 0 else 0
    
    #RECEBA!
    print(data)
    return {
        'date':data,
        'humidityExterna': totalHum,
        'temperaturaExterna': totalTemp,
        'source': 'inmet'
    }
    

def gen_days( year ):
    start_date=datetime( year, 1, 1 )
    end_date=datetime( year, 12, 31 )    
    d=start_date
    dates=[ start_date ]
    while d < end_date:
        d += timedelta(days=1)
        dates.append( d )        
    return [x.strftime('%Y-%m-%d') for x in dates]   


def import_inmet_data():
    save_later = []    
    for year in list_year:
        listOfDays = gen_days(year)
        for day in listOfDays:
            try:
                result = get_temperaturas_externas(day)
                save_later.append(result)
                sleep(0.4)
            except Exception as e:   
                sleep(10)
                try:
                    result = get_temperaturas_externas(day)
                    save_later.append(result)
                    print(e)
                except Exception as er:
                    pass

        with open(f"inmet_data_{year}.json", 'w') as outfile:
            json.dump(save_later, outfile)

# call request to inmet, check json local before run the function bellow
# import_inmet_data()


# get all data inside csv files
for folder in folders:
    if Path.isfile(f"{path}/{folder}/E01LF.CSV"):
        with open(f"{path}/{folder}/E01LF.CSV", newline='') as csvfile:
            try:
                spamreader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
                index = spamreader.index(header)     

                current_year = spamreader[index-1][1].split("/")[-1]

                for row in spamreader[index+1:]:
                    if row[0] == 'FIM': continue
                    splited = row[1].split("/")
                    current_day, current_month = splited[0], splited[1]

                    if current_month in months:                        
                        month_number = parseDateTime(months.index(current_month)+1)
                        row[1] = parseDateTime(current_day) + "/" + parseDateTime(str(month_number))
                    else:                                                
                        current_month = parseDateTime(current_month) 
                        current_day = parseDateTime(current_day)
                        row[1] = current_day + "/" + current_month

                    current_hour, current_minute = row[2].split(':')
                    current_hour = parseDateTime(current_hour.strip()) 
                    current_minute = parseDateTime(current_minute.strip())
                    
                    date_formattad = row[1].replace(" ", '') + "/"+ current_year
                    
                    if(len(date_formattad) < 10):
                        day, mes, year = date_formattad.split("/")
                        date_formattad = f"{parseDateTime(day)}/{parseDateTime(mes)}/{year}"

                    objetoTemperatura = {
                        'date': date_formattad,
                        'horario': f"{current_hour}:{current_minute}:00",
                        'tempInterna': float(row[5].replace(",", ".")),
                        'tempExterna': 0,
                        'source': 'sensor'
                    }
                    array_temperature.append(objetoTemperatura)


                    objetoUmidade = {
                        'date':date_formattad,
                        'horario': f"{current_hour}:{current_minute}:00",
                        'humidityInterna': float(row[4].replace(",", ".")),
                        'humidityExterna': 0,
                        'source': 'sensor'
                    }
                    array_umidade.append(objetoUmidade)

                print("-"*50)
            except Exception as e:
                # print('erro down', e)
                pass
    else:
        pass

# get all data inside json files
for year in list_year:
    with open(f"../inmet_data_{year}.json", 'r') as outfile:
        data = json.load(outfile)
        for item in data:
            date = item['date'].split('-')
            objetoUmidade = {
                'date': f"{date[2]}/{date[1]}/{date[0]}",
                'horario': "00:00:00",
                'humidityExterna': item['humidityExterna'],
                'humidityInterna': 0,
                'source': 'inmet'
            }
            objetoTemperatura = {
                'date': f"{date[2]}/{date[1]}/{date[0]}",
                'horario': "00:00:00",
                'tempExterna': item['temperaturaExterna'],
                'tempInterna': 0,
                'source': 'inmet'
            }   

            array_temperature.append(objetoTemperatura)
            array_umidade.append(objetoUmidade)


chunksize = 100

total_temeperatura = len(array_temperature)
total_umidade = len(array_umidade)

array_temperature = chunks(array_temperature, chunksize)
array_umidade = chunks(array_umidade, chunksize)

def flatten(t):
    return [item for sublist in t for item in sublist]

def saveData(endpoint, body):
    result = requests.post(url=f"{api_url}/{endpoint}/", json=body)    
    print(result)

print("Cadastrando Dados...")
threads = [[threading.Thread(target=saveData, args=('temperature', {"temperaturas": chunk})) for chunk in array_temperature],
    [threading.Thread(target=saveData, args=('humidity', {"humidades": chunk})) for chunk in array_umidade]]

threads = flatten(threads)

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print("Done!")

