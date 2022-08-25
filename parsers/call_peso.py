import argparse
import pandas as pd
import tratamento_peso as tp
import exportador_json as ej
import datetime

'''
c - caminho do arquivo
t - tipo do arquivo ("excel", por default)
l - linha inicial (2, por default) 
s - separador entre colunas (",", por default)
m - mangle_dupe_cols, caso existam colunas duplicadas (0, para False, por default, 1, para True, caso contrário)
u - url da api, por default, "http://localhost:3001/api/balanca"
d - data da instancia, por default, coloca-se 01/mes_atual/ano_atual no formato yyyy-mm-dd
cols - colunas do dataset, por default são:
[brinco = "IDENTIFICAÇÃO", peso = "PESO"]
CASO ESTE ARGUMENTO, cols, SEJA USADO, TODOS AS COLUNAS DEVEM ESTAR EXPRESSAS NA ORDEM ACIMA
date - data do registro
'''

parser = argparse.ArgumentParser()
parser.add_argument('--c', type=str, required=True)
parser.add_argument('--t', type=str)
parser.add_argument('--l', type=int)
parser.add_argument('--s', type=str)
parser.add_argument('--m', type=int)
parser.add_argument('--u', type=str)
parser.add_argument('--d', type=str)
parser.add_argument('--cols', type=str, nargs = 2)
parser.add_argument('--date', type=str)

args = parser.parse_args()
carreg_opc_args = [args.t, args.l, args.s, args.m]
todos_nulos = True
for elem in carreg_opc_args:
    if elem is not None:
        todos_nulos = False

tipo = "excel"
linha_inicial = 2
separador = ","
existe_col_dup = False
url_api = "http://localhost:3001/api/balanca"
data_atual = datetime.datetime.now()
data = args.date

if todos_nulos:
    df = pd.read_excel(args.c, header = linha_inicial)

else:
    if args.t:
        tipo = args.t
    if args.l:
        linha_inicial = args.l
    if args.s:
        separador = args
    if args.m:
        existe_col_dup = bool(args.m)
    
    if args.t:
        if tipo.lower() == "csv":
            if existe_col_dup:
                df = pd.read_csv(args.c, header = linha_inicial, sep = separador)
            else:
                df = pd.read_csv(args.c, header = linha_inicial, sep = separador, mangle_dupe_cols = existe_col_dup)

        elif tipo.lower() == "excel":
            if existe_col_dup:
                df = pd.read_excel(args.c, header = linha_inicial, sep = separador, mangle_dupe_cols = existe_col_dup)
            else:
                df = pd.read_excel(args.c, header = linha_inicial, sep = separador)

    else:
        if existe_col_dup:
            df = pd.read_csv(args.c, header = linha_inicial, sep = separador, mangle_dupe_cols = existe_col_dup)
        else:
            df = pd.read_csv(args.c, header = linha_inicial, sep = separador)

if args.u:
    url_api = args.u  

if args.cols:
    pass

else:
    print(args.c)
    df = tp.padronizar_brinco(df)
    df = tp.tratar_neg_peso(df)
    df = tp.substituir_nan(df)
    d = tp.gerar_grupo_dicts(df, data)

ej.enviar_post_lista(d, url_api)