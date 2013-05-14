#coding: utf-8

from flaskr import db

class Post(db.Model):
    __tablename__ = 'postagens'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128), unique=True)
    texto = db.Column(db.String(2048))
    comentarios = db.relationship('Comentario')

    def __init__(self, titulo, texto):
        self.titulo = titulo
        self.texto = texto

    def __repr__(self):
        return '<Post %r>' % self.id

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('postagens.id'))
    nome = db.Column(db.String(32))
    email = db.Column(db.String(32))
    texto = db.Column(db.String(1024))

    def __init__(self, post, nome, email, texto):
        self.post = post
        self.nome = nome
        self.email = email
        self.texto = texto




