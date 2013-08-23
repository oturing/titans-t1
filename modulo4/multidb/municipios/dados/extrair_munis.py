#!/usr/bin/env python

import json
import pprint

tabelas = {}
with open('ibge.json') as entrada:
    db = json.load(entrada)
    print len(db), 'registros'
    for registro in db:
        tabelas[registro['model']] = tabelas.get(registro['model'], 0) + 1
    for registro in db:
        if registro['model'] != 'municipios.municipio':
            continue
        pprint.pprint(registro)
        break

pprint.pprint(tabelas)

