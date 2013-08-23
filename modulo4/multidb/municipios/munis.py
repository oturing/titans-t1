import json
import os

from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

from flask_sqlalchemy import SQLAlchemy

from pprint import pprint

app = Flask(__name__)
app.config.from_pyfile('munis.cfg')

db = SQLAlchemy(app)

def criar_binds():
    '''TODO: ler diretorio db/ e criar binds para cada database encontrado'''

def criar_bd():
    siglas_uf = set()
    with open('dados/ibge.json') as entrada:
        registros = json.load(entrada)
    for registro in registros:
        if registro['model'] == 'municipios.mesoregiao':
            siglas_uf.add(registro['fields']['uf'])
    binds = app.config['SQLALCHEMY_BINDS']
    for sigla in siglas_uf:
        binds[sigla] = 'sqlite:///'+ os.path.join(app.config['PATH_DBS'], sigla.lower()+'.sqlite')
        db.create_all(bind=sigla)
        print 'db', sigla, 'criado'

def carregar_bd(uf):
    with open('dados/ibge.json') as entrada:
        registros = json.load(entrada)
        contador = 0
        for registro in registros:
            if registro['model'] == 'municipios.municipio':
                if registro['fields']['uf'] == uf:
                    muni = Municipio(registro['fields']['nome'],
                                     uf,
                                     registro['fields']['capital'])
                    db.session.add(muni)
                    db.session.commit()
                    contador += 1
        print contador, 'registros inseridos'

class Municipio(db.Model):
    __tablename__ = 'municipios'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String)
    uf = db.Column(db.String(2))
    capital = db.Column(db.Boolean)

    def __init__(self, nome, uf, capital):
        self.nome = nome
        self.uf = uf
        self.capital = capital

if __name__ == '__main__':
    app.run()
