import pandas as pd
import re
import requests
import datetime as dt
import os

#Remove linhas com Data nula, pois não teria utilidade
def remover_datas_nulas(df, col_data = "Data"):
    df = df.dropna(subset = [col_data])
    df = df.reset_index(drop=True)

    return df

#Remove colunas nulas que às vezes surgem por erros no dataset
def remover_colunas_nulas(df):
    for c in df:
        if re.match("Unnamed: \d+", c):
            del df[c]
    return df

#Padroniza formato do horario
def padronizar_hora(df, col_hora = "Hora"):
    times = []

    for i in range(len(df.index)):
        hora, minuto = str(df.loc[i, col_hora]).split(':')
        time = dt.time(int(hora), int(minuto))
        times.append(time)

    df.drop(columns = [col_hora])
    df[col_hora] = times    
    return df

#Converte formato da temperatura devido a possíveis erros, como o vírgulas no lugar de pontos para separar casas decimais, e converte o tipo da coluna para float
def converter_form_temp(df, col_temp = "Temperatura"):
    padrao = '\d+,\d+'
    for i in range(len(df[col_temp])):
        if re.match(padrao, df.loc[i, col_temp]):
            t1, t2 = (df.loc[i, col_temp]).split(',')
            df.loc[i, col_temp] = t1 + '.' + t2
            
    df = df.astype({col_temp: float})
    
    return df

#Define o formato que determinada entrada de Data em uma linha apresenta
def definir_tipo_data(df, linha, col_data = "Data"):
    padrao1 = "\d+/[^\S\n\t]\d+"
    padrao2 = "\d+[^\S\n\t]/[^\S\n\t]\d+"
    padrao3 = "\d+[^\S\n\t]/\d+"
    padrao4 = "\d+/\d+"
    padrao5 = "\d+-\d+"
    padrao6 = "\d+/\w+"
    padrao7 = "\d+ /\w+"
    padrao8 = "\d+/ \w+"
    
    if re.search(padrao1, df.at[linha, col_data]):
        return 1
    elif re.search(padrao2, df.at[linha, col_data]):
        return 2
    elif re.search(padrao3, df.at[linha, col_data]):
        return 3
    elif re.search(padrao4, df.at[linha, col_data]):
        return 4
    elif re.search(padrao5, df.at[linha, col_data]):
        return 5
    elif re.search(padrao6, df.at[linha, col_data]):
        return 6
    elif re.search(padrao7, df.at[linha, col_data]):
        return 7
    elif re.search(padrao8, df.at[linha, col_data]):
        return 8

#Padroniza formatos de data
def tratar_data_temp(df, col_data, ano = '2021'):
    ds = []

    for i in range(len(df[col_data])):
        tipo = definir_tipo_data(df, i, col_data)
        meses = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06", "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}

        if tipo == 1:
            dd, mm = df.at[i, col_data].split('/ ')
        elif tipo == 2:
            dd, mm = df.at[i, col_data].split(' / ')
        elif tipo == 3:
            dd, mm = df.at[i, col_data].split(' /')
        elif tipo == 4:
            dd, mm = df.at[i, col_data].split('/')
        elif tipo == 5:
            dd, mm = df.at[i, col_data].split('-')
        elif tipo == 6:
            dd, mm = df.at[i, col_data].split('/')
            mm = meses[mm.lower()]
        elif tipo == 7:
            dd, mm = df.at[i, col_data].split(' /')
            mm = meses[mm.lower()]
        elif tipo == 8:
            dd, mm = df.at[i, col_data].split('/ ')
            mm = meses[mm.lower()]
        else:
            df = df.drop(df.index[i])
            continue
        
        dd = dd.replace(" ", "")
        mm = mm.replace(" ", "")
        
        data = dt.date(int(ano), int(mm), int(dd))
        ds.append(data)
    
    df.drop(columns = [col_data])
    df[col_data] = ds
    return df


#Substituir valores "NaN" (Not a Number) por um valor dado
def substituir_nan(df, valor = 0):
    df = df.fillna(valor)
    return df

#Envia uma requisição para a API do INMET
def req_temp_inmet(data, hora):
    url_api = "https://apitempo.inmet.gov.br/estacao/" + data + "/" + data + "/" + "A557#"
    r = requests.get(url = url_api)
    data = r.json()
    
    return data[int(hora)]['TEM_INS']

#Gera um dicionario dentro de uma lista a partir dos dados de cada linha do dataset
def gerar_dict_linha(df, linha, col_data = 'Data', col_hora = 'Hora', col_temp = 'Temperatura', temp_ext = None):
    d = {"date":None, "horario":None, "tempInterna":None, "tempExterna":None}
    l = []
    
    d["date"] = df.loc[linha, col_data]
    d["horario"] = df.loc[linha, col_hora]
    d["tempInterna"] = df.loc[linha, col_temp]
    
    if temp_ext == None:
        horario_separado = (str(d["horario"])).split(':', 1)
        hora = horario_separado[0]
        temp_ext_str = req_temp_inmet(str(d["date"]), hora)
        if type(temp_ext_str) != 'string' and type(temp_ext_str) != 'float' and type(temp_ext_str) != 'int':
            temp_externa = None
        else:
            temp_externa = float(temp_ext_str)

    else:
        temp_externa = temp_ext

    d["tempExterna"] = temp_externa
    
    l.append(d)
    return l
    

#Gera um dicionario com todos os dicionarios gerados a partir de cada linha do dataset
def gerar_grupo_dicts(df, col_data = 'Data', col_hora = 'Hora', col_temp = 'Temperatura'):
    l = []
    l_temp = []
    temp_ext = 0
    hora_ant = "25"
    interations  = 0

    for i in range(len(df.index)):
        horario_separado = str(df.loc[i, col_hora]).split(':', 1)
        hora = horario_separado[0]
        if hora == hora_ant:
            l += gerar_dict_linha(df, i, col_data, col_hora, col_temp, temp_ext)
        else:
            l_temp = gerar_dict_linha(df, i, col_data, col_hora, col_temp)
            l += l_temp
            temp_ext = l_temp[0]["tempExterna"]
            hora_ant = hora
        interations = interations + 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Building temperature...",  "{:10.2f}".format(interations*100/len(df.index)), "%")
        
    d = {"temperaturas": l}
    return d