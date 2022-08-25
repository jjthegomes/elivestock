import argparse
import pandas as pd
import tratamento_umidade as tu
import exportador_json as ej

'''
c - caminho do arquivo
t - tipo do arquivo ("csv", por default)
l - linha inicial (5, por default) 
s - separador entre colunas (";", por default)
m - mangle_dupe_cols, caso existam colunas duplicadas (0, para False, por default, 1, para True, caso contrário)
a - ano a ser utilizado nas datas, por padrão, 2021
u - url da api, por default, "http://localhost:3001/api/humidity" 
cols - colunas do dataset, por default são:
[col_data = 'Data', col_hora = 'Hora', col_umid = 'Umidade']
CASO ESTE ARGUMENTO, cols, SEJA USADO, TODOS AS COLUNAS DEVEM ESTAR EXPRESSAS NA ORDEM ACIMA
'''

parser = argparse.ArgumentParser()
parser.add_argument('--c', type=str, required=True)
parser.add_argument('--t', type=str)
parser.add_argument('--l', type=int)
parser.add_argument('--s', type=str)
parser.add_argument('--m', type=int)
parser.add_argument('--u', type=str)
parser.add_argument('--a', type=str)
parser.add_argument('--cols', type=str, nargs = 3)

args = parser.parse_args()
carreg_opc_args = [args.t, args.l, args.s, args.m]
todos_nulos = True
for elem in carreg_opc_args:
    if elem is not None:
        todos_nulos = False

tipo = "csv"
linha_inicial = 5
separador = ";"
existe_col_dup = False
ano = '2021'
url_api = "http://localhost:3001/api/humidity"

if todos_nulos:
    df = pd.read_csv(args.c, header = linha_inicial, sep = separador)

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

if args.a:
    ano = args.a  

if args.cols:
    pass

else:
    df = tu.remover_datas_nulas(df)
    df = tu.remover_colunas_nulas(df)
    df = tu.padronizar_hora(df)
    df = tu.converter_form_umid(df)
    df = tu.tratar_data_umid(df, "Data", ano)
    df = tu.substituir_nan(df)
    d = tu.gerar_grupo_dicts(df)

ej.enviar_post_lista(d, url_api)