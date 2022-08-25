import pandas as pd
import re
import json
import numpy as np
import datetime as dt
from datetime import date, datetime

#Formata entradas de data do dataset para um formato padronizado e conversível para o datetime do pandas
def formatar_data(df, id_col_data, data_e_hora = False):
    #O dicionario "qtd_dias_mes" tem como proposito identificar facilmente a quantidade de dias de acordo com o numero do mes passado como index
    qtd_dias_mes = {"01": 31, "02": 28.5, "03": 31, "04": 30, "05": 31, "06": 30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31}
    s = "00" #Segundo para utilizar na conversão para datetime depois
    df[id_col_data] = df[id_col_data].astype(str) #Converte tipo da coluna para string caso já não seja
    l  = []
    dates = []
    
    if data_e_hora:
        for i in range(len(df.index)):
            if re.match("\d\d/\d\d/\d\d\d\d \d\d:\d\d", str(df.at[i, id_col_data])): #Verifica o padrao da entrada
                dd, mm, aaaa = (df.at[i, id_col_data]).split('/') #Divide em dia, mes e ano
                aaaa, h = aaaa.split(' ') #Ao fazer a divisão da linha anterior, normalmente hora e min. ficam dentro da string de ano
                h, m = h.split(':') #Divide em hora e minuto
                l = [dd, mm, aaaa, h, m]
                if any(int(n) < 0 for n in l):
                    l = [abs(x) for x in l] #Trata possíveis valores que estejam como negativos
                    dd, mm, aaaa, h, m = l[0], l[1], l[2], l[3], l[4] #Reatribui depois de tratar os negativos
                if int(mm) > 12 and int(mm) <=31 and (int(qtd_dias_mes[dd]) == mm or round(float(qtd_dias_mes[dd])) == mm):
                        mm, dd = dd, mm #Troca dia e mes se o formato estiver invertido
                if int(dd) > 31:
                    print("Dia inconsistente!", dd, "- Index:", i)
                if int(mm) > 12:
                    print("Mês inconsistente!", dd, "- Index:", i)
                if int(h) > 23:
                    print("Hora inconsistente!", dd, "- Index:", i)
                if int(m) > 59:
                    print("Minuto inconsistente!", dd, "- Index:", i)

                d = dt.datetime(int(aaaa), int(mm), int(dd), int(h), int(m), int(s))
                dates.append(d)
            elif re.match("\d\d/\d\d/\d\d \d\d:\d\d", str(df.at[i, id_col_data])) or re.match("\d\d/\d/\d\d \d\d:\d\d", str(df.at[i, id_col_data])) or re.match("\d\d/\d/\d\d \d:\d\d", str(df.at[i, id_col_data])) or re.match("\d\d/\d\d/\d\d \d:\d\d", str(df.at[i, id_col_data])): #Verifica o padrao da entrada                
                mm, dd, aa = (df.at[i, id_col_data]).split('/')
                aa, h = aa.split(' ') #Ao fazer a divisão da linha anterior, normalmente hora e min. ficam dentro da string de ano
                h, m = h.split(':') #Divide em hora e minuto
                l = [dd, mm, aa, h, m]

                if any(int(n) < 0 for n in l):
                    l = [abs(x) for x in l] #Trata possíveis valores que estejam como negativos
                    dd, mm, aa, h, m = l[0], l[1], l[2], l[3], l[4] #Reatribui depois de tratar os negativos
                if int(mm) > 12 and int(mm) <=31 and (int(qtd_dias_mes[dd]) == mm or round(float(qtd_dias_mes[dd])) == mm):
                        mm, dd = dd, mm #Troca dia e mes se o formato estiver invertido
                if int(dd) > 31:
                    print("Dia inconsistente!", dd, "- Index:", i)
                if int(mm) > 12:
                    print("Mês inconsistente!", dd, "- Index:", i)
                if int(h) > 23:
                    print("Hora inconsistente!", dd, "- Index:", i)
                if int(m) > 59:
                    print("Minuto inconsistente!", dd, "- Index:", i)

                d = dt.datetime(int(aa), int(mm), int(dd), int(h), int(m), int(s))
                # print(str(df.at[i, id_col_data]))
                dates.append(d)
            else:
                print("nao pegou")
                print(str(df.at[i, id_col_data]))

        
    else:        
        for i in range(len(df.index)):
            if re.match("\d\d/\d\d/\d\d\d\d", str(df.at[i, id_col_data])): #Verifica o padrao da entrada
                dd, mm, aaaa = (df.at[i, id_col_data]).split('/') #Divide em dia, mes e ano
                l = [dd, mm, aaaa]
                if any(int(n) < 0 for n in l):
                    l = [abs(x) for x in l] #Trata possíveis valores que estejam como negativos
                    dd, mm, aaaa = l[0], l[1], l[2] #Reatribui depois de tratar os negativos
                if int(mm) > 12 and int(mm) <=31 and (int(qtd_dias_mes[dd]) == mm or round(float(qtd_dias_mes[dd])) == mm):
                    mm, dd = dd, mm #Troca dia e mes se o formato estiver invertido
                    df.at[i, id_col_data] = aaaa + "-" + mm + "-" + dd
                if int(dd) > 31:
                    print("Dia inconsistente!", dd, "- Index:", i)
                if int(mm) > 12:
                    print("Mês inconsistente!", dd, "- Index:", i)

                d = dt.date(int(aaaa), int(mm), int(dd))
                dates.append(d)

    df.drop(columns = [id_col_data])
    df[id_col_data] = dates
    return df


#Substituir valores "NaN" (Not a Number) por um valor dado
def substituir_nan(df, valor = 0):
    df = df.fillna(valor)
    return df


def encontrar_ocorr_lista(nome_col, lista):
    l = []
    for e in lista:
        if re.match(nome_col+".", e) or re.match(nome_col, e):
            l.append(e)
            
    return l

def verif_nulidade(df, col, linha):
    if df.loc[linha, col] == "" or df.loc[linha, col] == " " or df.loc[linha, col] == str(0) or df.loc[linha, col] == str(0.0) or str(df.loc[linha, col]).lower() == 'nan' or df.loc[linha, col] == 0 or df.loc[linha, col] == 0.0:
        return True
    else:
        return False

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
def gerar_dict_linha(df, linha, col_lote = "N.R.", col_data = "INÍCIO", col_num_animais = "Nº. Anim.", qtd_total = "Nom", alimento = "NOME COMPONENTE"):
    d = {"lote":None,"date":None,"numAnimais":None,"totalLote":None,"mediaVaca":None,"alimento":None}
    lista_dicts = []
    
    d['lote'] = df.loc[linha, col_lote]
    d['date'] = df.loc[linha, col_data]
    d['numAnimais'] = df.loc[linha, col_num_animais]
    
    cols_df = list(df.columns)
    ocorr_compon = encontrar_ocorr_lista(alimento, cols_df)
    ocorr_qtd = encontrar_ocorr_lista(qtd_total, cols_df)
    
    num_ocorr_compon = len(ocorr_compon)
    num_ocorr_qtd = len(ocorr_qtd)

    if num_ocorr_compon == num_ocorr_qtd:
        for compon, qtd in zip(ocorr_compon, ocorr_qtd):
            if not verif_nulidade(df, compon, linha) and not verif_nulidade(df, qtd, linha):
                d['alimento'] = df.loc[linha, compon]
                d['totalLote'] = df.loc[linha, qtd]
                d['mediaVaca'] = d['totalLote'] /  d['numAnimais']
                lista_dicts.append(json.dumps(d.copy(), cls=NpEncoder))
            else:
                continue
    else:
        if num_ocorr_compon > num_ocorr_qtd:
            for i in range(num_ocorr_qtd):
                if not verif_nulidade(df, ocorr_compon[i], linha) and not verif_nulidade(df, ocorr_qtd[i], linha):
                    d['alimento'] = df.loc[linha, ocorr_compon[i]]
                    d['totalLote'] = df.loc[linha, ocorr_qtd[i]]
                    d['mediaVaca'] = d['totalLote'] /  d['numAnimais']
                    lista_dicts.append(json.dumps(d.copy(), cls=NpEncoder))
                else:
                    continue
        else:
            for i in range(num_ocorr_compon):
                if not verif_nulidade(df, ocorr_compon[i], linha) and not verif_nulidade(df, ocorr_qtd[i], linha):
                    d['alimento'] = df.loc[linha, ocorr_compon[i]]
                    d['totalLote'] = df.loc[linha, ocorr_qtd[i]]
                    d['mediaVaca'] = d['totalLote'] /  d['numAnimais']
                    lista_dicts.append(json.dumps(d.copy(), cls=NpEncoder))
                else:
                    continue
    
    return lista_dicts


#Gera um dicionario com todos os dicionarios gerados a partir de cada linha do dataset
def gerar_grupo_dicts(df, col_lote = "N.R.", col_data = "INÍCIO", col_num_animais = "Nº. Anim.", qtd_total = "Nom", alimento = "NOME COMPONENTE"):
    l = []
    for i in range(len(df.index)):
        l += gerar_dict_linha(df, i, col_lote, col_data, col_num_animais, qtd_total, alimento)
        
    d = {"alimentos": l}
    return d