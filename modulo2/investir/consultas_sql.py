# coding: utf-8

import sqlite3
from pprint import pprint

consultas = [
    (
        '''
        E1. Listar cod_contribuinte e nome de cada cliente com cod_contribuinte
            maior ou igual a 3.
        ''',
        '''
        SELECT cod_contribuinte, nome FROM cliente
        WHERE cod_contribuinte >= 3
        '''
    ),
    (
        '''
        E2. Listar simbolos das acoes do setor "tecnologia"
        ''',
        '''
        SELECT simbolo FROM acao WHERE setor >= 3
        '''
    ),

]

cnx = sqlite3.connect('investir.sqlite')
cursor = cnx.cursor()
for pergunta, sql in consultas:
    print '#'* 70
    print pergunta.strip().replace(' '*8, '')
    cursor.execute(sql)
    pprint(cursor.fetchall())
