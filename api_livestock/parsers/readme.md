# Execução dos parses para dados e-Livestock

Neste documento são dadas as instruções de execução dos algoritmos de pré-processamento e envio dos dados para a API e-Livestock.

## Execução

Para uma execução básica, usar python3 + nome_parser.py + --c + "./caminho/para/o/arquivo.csv", como no exemplo:

```bash
python3 call_temperatura.py --c "./Temperatura-Umidade/01081341/E01LF.CSV"
```

## Outras flags

A flag "--c", utilizada no exemplo acima, faz referência ao caminho do arquivo. Existem ainda outras flags, que na maioria dos casos não serão necessárias devido ao fato dos parser já carregarem, por padrão, as definições para cada tipo de dataset. Porém, caso se faça necessário, a seguir uma explicação acerca do funcionamento de cada flag:

- "--c" - Caminho para o arquivo, sempre utilizada com seu valor fornecido da maneira "./caminho/para/o/arquivo.csv". Outras extensões, como .xlsx podem ser usadas sem problemas, desde que se deixe expresso por meio da flag "--t", para especificar o tipo de arquivo. Arquivos que normalmente já vem do CompostBarn com extesões diferentes já têm seus parser por padrão funcionando com a dada extensão, não necessitando da adição da flag "--t".

- "--t" - Tipo do arquivo, sempre utilizada com seu valor fornecido da maneira "csv", ou, também, "excel", para arquivos com extesões ".xlsx" ou ".xls".
  Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --t ".xlsx"
```

- "--l" - Linha inicial onde estão os rótulos das colunas do dataset. Alguns datasets não começam seu conteúdo na linha 0, e, por isso, precisam desta especificação. Sempre deve ser utilizada seguida do número da linha inicial sem as aspas. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --l 4
```

- "--s" - Caractere utilizado no arquivo para separar colunas. Utiliza-se da seguinte maneira:

```bash
python3 nome_parser.py --c "caminho/para/o/arquivo.csv" --s ";"
```

- "--m" - Sinaliza que o dataset importado possui colunas com nomes duplicados. Utiliza-se 1, caso sim e 0, caso contrário. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --m 1
```

- "--a" - _Utilizado somente para os parsers dos datasets de temperatura e umidade._ Serve para enviar o ano que deve ser usado dentro das datas do dataset. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --m 1
```

- "--u" - Usa-se para fornecer uma url para envio de POST requests para a API diferente da padrão. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --u "http://url.para/a-api"
```

- "--cols" - Usa-se caso as colunas do dataset importado tenham nomenclaturas diferentes das que estão como padrão no código. Deve-se passar o nome de todas as utilizadas no código mesmo que apenas um subgrupo destas apresente diferenças em relação ao original. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --cols "Coluna A" "Coluna B" "Coluna C"
```

- "--d" - _Utilizado somente para o parser dos datasets de pesagem._ Através da desta flag, envia-se ao parser a data a ser utilizada. Exemplo:

```bash
python3 nomeparser.py --c "caminho/para/o/arquivo.csv" --d "2021-06-24"
```
