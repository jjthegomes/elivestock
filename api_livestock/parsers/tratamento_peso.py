import pandas as pd
import re
import json
import numpy as np

#Converte um mes escrito por extenso para o seu respectivo numero
def converter_mes_num(mes):
    meses = {"janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04", "maio":"05", "junho":"06", "julho":"07", "agosto":"08", "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"}
    mes = meses[mes.lower()]
    return mes

#Extrai o dia e o mes a partir do nome do arquivo
def extrair_dia_mes_nome_df(nome_arq):
    #Possíveis padroes no nome dos arquivos:
    padrao1 = "\d+- \w+"
    padrao2 = "\d+-\w+"
    padrao3 = "\d+ -\w+"
    
    #Testa os possíveis padrões:
    teste_p1 = re.findall(padrao1, nome_arq)
    teste_p2 = re.findall(padrao2, nome_arq)
    teste_p3 = re.findall(padrao3, nome_arq)
    
    #Quebra a string em duas de acordo com o padrao:
    if teste_p1 != 0:
        dia, mes = teste_p1[0].split("- ")
    elif teste_p2 != 0:
        dia, mes = teste_p2[0].split("-")
    elif teste_p3 != 0:
        dia, mes = teste_p2[0].split(" -")
    
    mes = converter_mes_num(mes)
    print("mes", mes)
    return dia, mes

#A partir do caminho e do nome do arquivo, importa um dataset e identifica o dia e o mes
def importar_df_e_extrair_data(caminho, nome_arq):
    df = pd.read_excel(caminho, header = 2)
    dia, mes = extrair_dia_mes_nome_df(nome_arq)

    return df, dia, mes

#Padroniza as entradas de Brincos do datasets retirando a parte "-X" e convertendo o formato da coluna para string
def padronizar_brinco(df, col_brinco = "IDENTIFICAÇÃO", separador = '-'):
    if df[col_brinco].dtype == 'float64' or df[col_brinco].dtype == 'int64':
        df[col_brinco] = df[col_brinco].astype(str)
    
    for i in range(len(df[col_brinco])):
        if df.at[i, col_brinco].lower() != 'nan' and re.match("\d+"+separador+"\d+", df.at[i, col_brinco]): 
            df.at[i, col_brinco], lixo = str(df.at[i, col_brinco]).split(separador)
    
    return df

#Trata possíveis valores de peso negativo deixando a entrada vazia
def tratar_neg_peso(df, col_peso = "PESO"):
    for i in range(len(df[col_peso])):
        if df.loc[i, col_peso] < 0:
            df.loc[i, col_peso] = None
    
    return df


#Substituir valores "NaN" (Not a Number) por um valor dado
def substituir_nan(df, valor = 0):
    df = df.fillna(valor)
    return df

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

#Gera um dicionario dentro de uma lista a partir dos dados de cada linha do dataset
def gerar_dict_linha(df, linha, data, brinco = "IDENTIFICAÇÃO", peso = "PESO"):
    d = {"brinco":None, "peso":None, "date":None}
    d["brinco"] = df.at[linha, brinco]
    d["peso"] = df.at[linha, peso]
    d["date"] = data   
     
    return(json.dumps(d, cls=NpEncoder))

#Gera um dicionario com todos os dicionarios gerados a partir de cada linha do dataset
def gerar_grupo_dicts(df, data, brinco = "IDENTIFICAÇÃO", peso = "PESO"):
    l = []
    
    for i in range(len(df.index)):
        l.append(gerar_dict_linha(df, i, data, brinco, peso))
        
    d = {"pesos": l}
    return d