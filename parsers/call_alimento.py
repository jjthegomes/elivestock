import argparse
from os import sep
import pandas as pd
import tratamento_alimento as ta
import exportador_json as ej

'''
c - caminho do arquivo
t - tipo do arquivo ("csv", por default)
l - linha inicial (0, por default) 
s - separador entre colunas (";", por default)
m - mangle_dupe_cols, caso existam colunas duplicadas (1, para True, por default, 0, para False, caso contrário)
u - url da api, por default, "http://localhost:3001/api/alimento"
cols - colunas do dataset, por default são:
[col_lote = "N.R.", col_data = "INÍCIO", col_num_animais = "Nº. Anim.", qtd_total = "Nom", alimento = "NOME COMPONENTE"]
CASO ESTE ARGUMENTO, cols, SEJA USADO, TODOS AS COLUNAS DEVEM ESTAR EXPRESSAS NA ORDEM ACIMA
'''

parser = argparse.ArgumentParser()
parser.add_argument('--c', type=str, required=True)
parser.add_argument('--t', type=str)
parser.add_argument('--l', type=int)
parser.add_argument('--s', type=str)
parser.add_argument('--m', type=int)
parser.add_argument('--u', type=str)
parser.add_argument('--cols', type=str, nargs = 5)

args = parser.parse_args()
carreg_opc_args = [args.t, args.l, args.s, args.m]
todos_nulos = True
for elem in carreg_opc_args:
    if elem is not None:
        todos_nulos = False

tipo = "csv"
linha_inicial = 0
separador = ";"
existe_col_dup = True
url_api = "http://localhost:3001/api/alimento"

if todos_nulos:
    df = pd.read_csv(args.c, sep = separador)

else:
    if args.t:
        tipo = 'excel'
    if args.l:
        linha_inicial = args.l
    if args.s:
        separador = args
    if args.m:
        existe_col_dup = bool(args.m)
    
    if args.t:
        if tipo.lower() == "csv":
            if existe_col_dup:
                df = pd.read_csv(args.c, header = linha_inicial, sep = separador, mangle_dupe_cols = existe_col_dup)
            else:
                df = pd.read_csv(args.c, header = linha_inicial, sep = separador)

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
    df = ta.formatar_data(df, "INÍCIO", True)
    df = ta.formatar_data(df, "FIM", True)
    df = ta.substituir_nan(df)
    d = ta.gerar_grupo_dicts(df)

ej.enviar_post_lista(d, url_api)
