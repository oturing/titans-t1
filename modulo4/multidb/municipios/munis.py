from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('munis.cfg')
db = SQLAlchemy(app)

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
