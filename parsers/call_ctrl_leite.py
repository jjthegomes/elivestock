import argparse
from numpy import equal
import pandas as pd
import re
import datetime
import tratamento_ctrl_leite_indiv as tl
import exportador_json as ej

'''
c - caminho do arquivo
t - tipo do arquivo ("excel", por default)
l - linha inicial (0, por default) 
s - separador entre colunas (",", por default)
m - mangle_dupe_cols, caso existam colunas duplicadas (0, para False, por default, 1, para True, caso contrário)
u - url da api, por default, "http://localhost:3001/api/prodleite"
cols - colunas do dataset, por default são:
[col_Brinco = "Brinco", col_ord1 = "ordenha1", col_ord2 = "ordenha2", col_ord3 = "ordenha3", col_total = "Prod Total"]
CASO ESTE ARGUMENTO, cols, SEJA USADO, TODOS AS COLUNAS DEVEM ESTAR EXPRESSAS NA ORDEM ACIMA
line - linha inicial (obrigatório)
date - data do registro (obrigatório)
'''

parser = argparse.ArgumentParser()
parser.add_argument('--c', type=str, required=True)
parser.add_argument('--t', type=str)
parser.add_argument('--l', type=int)
parser.add_argument('--s', type=str)
parser.add_argument('--m', type=int)
parser.add_argument('--u', type=str)
parser.add_argument('--cols', type=str, nargs = 5)
parser.add_argument('--line', type=int, required=True)
parser.add_argument('--date', type=str, required=True)

args = parser.parse_args()
carreg_opc_args = [args.t, args.l, args.s, args.m]
todos_nulos = True
for elem in carreg_opc_args:
    if elem is not None:
        todos_nulos = False

tipo = "excel"
linha_inicial = args.line
separador = ","
existe_col_dup = False
url_api = "http://localhost:3001/api/prodleite"

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
    df = tl.padronizar_brinco(df)
    df = tl.remover_linhas_sem_id_vaca(df)
    df = tl.converter_tipo_col_lote(df)
    df = tl.tratar_valores_negativos_ordenha(df)
    df = tl.tratar_dados_ordenha(df)
    df = tl.substituir_nan(df)
    d = tl.gerar_grupo_dicts(df, args.date)

ej.enviar_post_lista(d, url_api)