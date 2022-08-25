import pandas as pd
import re
import json
import numpy as np
import datetime as dt
from datetime import date, datetime

#Padroniza as entradas de Brincos do datasets retirando a parte "-X" e convertendo o formato da coluna para string
def padronizar_brinco(df, col_brinco = "Brinco", separador = '-'):
    if df[col_brinco].dtype == 'float64' or df[col_brinco].dtype == 'int64':
        df[col_brinco] = df[col_brinco].astype(str)
    
    for i in range(len(df[col_brinco])):
        if df.at[i, col_brinco].lower() != 'nan' and re.match("\d+"+separador+"\d+", df.at[i, col_brinco]): 
            df.at[i, col_brinco], lixo = str(df.at[i, col_brinco]).split(separador)
    
    return df


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
            else:
                print("Warning: Sem data ou data não corresponde ao padrão de datas. Index:", i, "Valor:", df.at[i, id_col_data])
                dates.append(df.at[i, id_col_data])
        
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
            else:
                print("Warning: Sem data ou data não corresponde ao padrão de datas. Index:", i, "Valor:", df.at[i, id_col_data])
                dates.append(df.at[i, id_col_data])
                
    df.drop(columns = [id_col_data])
    df[id_col_data] = dates
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
def gerar_dict_linha(df, linha, fazenda = "Fazenda", barcode = "BarCode", brinco = "Brinco", lado = "Lado", data = "Data", tipo = "Tipo", obs = "OBS", quarto = "Quarto", grau = "Grau", resultado = "Resultado", gramPositiva = "Gram Pos", gramNegativa = "Gram Neg", ecoli = "E coli", enterococcusSpp = "Enterococcus spp", klebsiellaEnterobacter = "Klebsiella / Enterobacter", lactococcusSpp = "Lactococcus spp", outrosGramNegativa = "Outros Gram-neg", outrosGramPositiva = "Outros Gram-pos", protothecaLevedura = "Prototheca / Levedura", pseudomonasSpp = "Pseudomonas spp", serratiaSpp = "Serratia spp",  staphNaoAureus = "Staph não aureus", staphAureus = "Staph aureus", strepAgalactiaeDysgalactiae = "Strep agalactiae / dysgalactiae", strepUberis = "Strep uberis"):
    d = {"fazenda": None, "barcode": None, "brinco": None, "lado": None, "data": None, "tipo": None, "obs": None, "quarto": None, "grau": None, "resultado": None, "gramPositiva": None, "gramNegativa": None, "ecoli": None, "enterococcusSpp": None, "klebsiellaEnterobacter": None, "lactococcusSpp": None, "outrosGramNegativa": None, "outrosGramPositiva": None, "protothecaLevedura": None, "pseudomonasSpp": None, "serratiaSpp": None, "staphNãoAureus": None, "staphAureus": None, "strepAgalactiaeDysgalactiae": None, "strepUberis": None}
    
    d["fazenda"] = df.loc[linha, fazenda]
    d["barcode"] = df.loc[linha, barcode]
    d["brinco"] = df.loc[linha, brinco]
    d["lado"] = df.loc[linha, lado]
    d["data"] = df.loc[linha, data]
    d["tipo"] = df.loc[linha, tipo]
    d["obs"] = df.loc[linha, obs]
    d["quarto"] = df.loc[linha, quarto]
    d["grau"] = df.loc[linha, grau]
    d["resultado"] = df.loc[linha, resultado]
    d["gramPositiva"] = df.loc[linha, gramPositiva]
    d["gramNegativa"] = df.loc[linha, gramNegativa]
    d["ecoli"] = df.loc[linha, ecoli]
    d["klebsiellaEnterobacter"] = df.loc[linha, klebsiellaEnterobacter]
    d["lactococcusSpp"] = df.loc[linha, lactococcusSpp]
    d["outrosGramNegativa"] = df.loc[linha, outrosGramNegativa]
    d["outrosGramPositiva"] = df.loc[linha, outrosGramPositiva]
    d["protothecaLevedura"] = df.loc[linha, protothecaLevedura]
    d["pseudomonasSpp"] = df.loc[linha, pseudomonasSpp]
    d["serratiaSpp"] = df.loc[linha, serratiaSpp]
    d["staphNãoAureus"] = df.loc[linha, staphNaoAureus]
    d["staphAureus"] = df.loc[linha, staphAureus]
    d["strepAgalactiaeDysgalactiae"] = df.loc[linha, strepAgalactiaeDysgalactiae]
    d["strepUberis"] = df.loc[linha, strepUberis]
    
    return(json.dumps(d, cls=NpEncoder))


#Gera um dicionario com todos os dicionarios gerados a partir de cada linha do dataset
def gerar_grupo_dicts(df, fazenda = "Fazenda", barcode = "BarCode", brinco = "Brinco", lado = "Lado", data = "Data", tipo = "Tipo", obs = "OBS", quarto = "Quarto", grau = "Grau", resultado = "Resultado", gramPositiva = "Gram Pos", gramNegativa = "Gram Neg", ecoli = "E coli", enterococcusSpp = "Enterococcus spp", klebsiellaEnterobacter = "Klebsiella / Enterobacter", lactococcusSpp = "Lactococcus spp", outrosGramNegativa = "Outros Gram-neg", outrosGramPositiva = "Outros Gram-pos", protothecaLevedura = "Prototheca / Levedura", pseudomonasSpp = "Pseudomonas spp", serratiaSpp = "Serratia spp",  staphNaoAureus = "Staph não aureus", staphAureus = "Staph aureus", strepAgalactiaeDysgalactiae = "Strep agalactiae / dysgalactiae", strepUberis = "Strep uberis"):
    l = []
    for i in range(len(df.index)):
        l.append(gerar_dict_linha(df, i, fazenda, barcode, brinco, lado, data, tipo, obs, quarto, grau, resultado, gramPositiva, gramNegativa, ecoli, enterococcusSpp, klebsiellaEnterobacter, lactococcusSpp, outrosGramNegativa, outrosGramPositiva, protothecaLevedura, pseudomonasSpp, serratiaSpp, staphNaoAureus, staphAureus, strepAgalactiaeDysgalactiae, strepUberis))
    
    d = {"onfarms": l}
    return d

