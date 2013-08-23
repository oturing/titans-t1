import json

from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('munis.cfg')
db = SQLAlchemy(app)

def criar_bd():
    db.create_all()

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
