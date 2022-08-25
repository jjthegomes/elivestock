import pandas as pd
import re
import json
import numpy as np
from datetime import date, datetime

#Padroniza as entradas de Brincos do datasets retirando a parte "-X" e convertendo o formato da coluna para string
def padronizar_brinco(df, col_brinco = "Brinco", separador = '-'):
    if col_brinco.lower() == "brinco" and col_brinco not in list(df.columns):
        col_brinco = "IDENTIFICAÇÃO"
    elif col_brinco.lower() == "identificação" and col_brinco not in list(df.columns):
        col_brinco = "Brinco"

    if df[col_brinco].dtype == 'float64' or df[col_brinco].dtype == 'int64':
        df[col_brinco] = df[col_brinco].astype(str)
    
    for i in range(len(df[col_brinco])):
        if df.at[i, col_brinco].lower() != 'nan' and re.match("\d+"+separador+"\d+", df.at[i, col_brinco]): 
            df.at[i, col_brinco], lixo = str(df.at[i, col_brinco]).split(separador)
    
    return df

#Remove linhas sem a identificação do animal, uma vez que estas não tem utilidade se não especificarem de que animal se trata
def remover_linhas_sem_id_vaca(df, col_brinco = "Brinco"):
    if col_brinco.lower() == "brinco" and col_brinco not in list(df.columns):
        col_brinco = "IDENTIFICAÇÃO"
    elif col_brinco.lower() == "identificação" and col_brinco not in list(df.columns):
        col_brinco = "Brinco"

    df = df.dropna(subset = [col_brinco])

    return df

#Converte o tipo da coluna do lote para string, CASO ESTA COLUNA EXISTA NO DATASET
def converter_tipo_col_lote(df, col_lote = "LOTE"):
    if col_lote in list(df.columns):
        df = df.astype({col_lote: int})
        df = df.astype({col_lote: str})

    return df

#Trata possíveis valores de produção negativos deixando-os consistentes ou nulos
def tratar_valores_negativos_ordenha(df, col_ord1 = 'Prod Ord 1', col_ord2 = 'Prod Ord 2', col_ord3 = 'Prod Ord 3', col_total = 'Prod Total'):
    for i in range(len(df[col_total])):
        if df.loc[i, col_ord1] < 0: #Vefifica se está negativado
            #Verifica inconsistencias na 1 ordenha:
            if abs(df.loc[i, col_ord1]) == (abs(df.loc[i, col_total]) - abs(df.loc[i, col_ord3]) - abs(df.loc[i, col_ord2])):
                df.loc[i, col_ord1] = abs(df.loc[i, col_ord1]) #Atribui valor absoluto se está compatível com as outras entradas
            else:
                df.loc[i, col_ord1] = None #Deixa vazio caso não esteja compatível com as outras entradas
        
        if df.loc[i, col_ord2] < 0: #Vefifica se está negativado
            #Verifica inconsistencias na 2 ordenha:
            if abs(df.loc[i, col_ord2]) == (abs(df.loc[i, col_total]) - abs(df.loc[i, col_ord3]) - abs(df.loc[i, col_ord1])):
                df.loc[i, col_ord2] = abs(df.loc[i, col_ord2]) #Atribui valor absoluto se está compatível com as outras entradas
            else:
                df.loc[i, col_ord2] = None #Deixa vazio caso não esteja compatível com as outras entradas
        
        if df.loc[i, col_ord3] < 0: #Vefifica se está negativado
            #Verifica inconsistencias na 3 ordenha:
            if abs(df.loc[i, col_ord3]) == (abs(df.loc[i, col_total]) - abs(df.loc[i, col_ord2]) - abs(df.loc[i, col_ord1])):
                df.loc[i, col_ord3] = abs(df.loc[i, col_ord3]) #Atribui valor absoluto se está compatível com as outras entradas
            else:
                df.loc[i, col_ord3] = None #Deixa vazio caso não esteja compatível com as outras entradas
                
        if df.loc[i, col_total] < 0: #Vefifica se está negativado
            #Verifica inconsistencias no total das tres ordenhas:
            if abs(df.loc[i, col_total]) == (abs(df.loc[i, col_ord1]) + abs(df.loc[i, col_ord2]) + abs(df.loc[i, col_ord3])):
                df.loc[i, col_total] = abs(df.loc[i, col_total]) #Atribui valor absoluto se está compatível com as outras entradas
            else:
                #Gera um novo valor total caso não esteja compatível com as outradas entradas:
                df.loc[i, col_total] = abs(df.loc[i, col_ord1]) + abs(df.loc[i, col_ord2]) + abs(df.loc[i, col_ord3])
        
    return df

#Separa valores numéricos e não numéricos do datasets para tratamentos diferentes
def tratar_dados_ordenha(df, lista_cols_nao_num = ['Brinco', 'IDENTIFICAÇÃO']):
    for i in range(len(lista_cols_nao_num)):
        df_num = df.drop(df.filter(regex=lista_cols_nao_num[i]).columns, axis=1)

    df_info = df.filter(lista_cols_nao_num, axis=1)

    df_num = tratar_valores_negativos_ordenha(df_num, 'Prod Ord 1', 'Prod Ord 2', 'Prod Ord 3', 'Prod Total')

    df = pd.concat([df_info, df_num], axis=1)

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
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super(NpEncoder, self).default(obj)

#Gera um dicionario dentro de uma lista a partir dos dados de cada linha do dataset
def gerar_dict_linha(df, linha, data, col_Brinco = "Brinco", col_ord1 = 'Prod Ord 1', col_ord2 = 'Prod Ord 2', col_ord3 = 'Prod Ord 3', col_total = 'Prod Total'):
    d = {"brinco":None, "ordenha1":None, "ordenha2":None, "ordenha3":None, "prodTotal":None, "date":None}
    lista_dict = []
    
    d["brinco"] = str(df.at[linha, col_Brinco]).split()[1]
    d["ordenha1"] = df.at[linha, col_ord1]
    d["ordenha2"] = df.at[linha, col_ord2]
    d["ordenha3"] = df.at[linha, col_ord3]
    d["prodTotal"] = df.at[linha, col_total]
    d["date"] = data
   
    lista_dict.append(json.dumps(d, cls=NpEncoder))    
    return lista_dict

#Gera um dicionario com todos os dicionarios gerados a partir de cada linha do dataset
def gerar_grupo_dicts(df, data, col_Brinco = "Brinco", col_ord1 = "Prod Ord 1", col_ord2 = "Prod Ord 2", col_ord3 = "Prod Ord 3", col_total = "Prod Total"):
    l = []

    if col_Brinco not in list(df.columns):
        if "Brinco" in list(df.columns):
            col_Brinco = "Brinco"
        elif "IDENTIFICAÇÃO" in list(df.columns):
            col_Brinco = "IDENTIFICAÇÃO"

    for i in range(len(df.index)):
        l.append(gerar_dict_linha(df, i, data, col_Brinco, col_ord1, col_ord2, col_ord3, col_total))
        
    d = {"ordenhas": l}
    return d