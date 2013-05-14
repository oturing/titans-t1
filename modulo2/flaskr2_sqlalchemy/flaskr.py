# coding: utf-8

# todos os imports
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from flask.ext.sqlalchemy import SQLAlchemy

import forms

# configuração
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE

# criar nossa pequena aplicação :)
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

'''
create table entradas (
  id integer primary key autoincrement,
  titulo string not null,
  texto string not null
);
'''

class Post(db.Model):
    __tablename__ = 'postagens'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128), unique=True)
    texto = db.Column(db.String(2048))

    def __init__(self, titulo, texto):
        self.titulo = titulo
        self.texto = texto

    def __repr__(self):
        return '<Post %r>' % self.id


################################################# Configuração

def criar_bd():
    db.create_all()

################################################# Views

def obter_entradas():
    '''select titulo, texto from entradas order by id desc'''
    return Post.query.order_by(Post.id.desc())

@app.route('/')
def exibir_entradas():
    return render_template('entrada_lista.html', entradas=obter_entradas())

@app.route('/entrar', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            erro = u'Usuário inválido'
        elif request.form['password'] != app.config['PASSWORD']:
            erro = u'Senha inválida'
        else:
            session['logado'] = True
            flash('Login OK')
            return redirect(url_for('exibir_entradas'))
    return render_template('login.html', erro=erro)

@app.route('/sair')
def logout():
    session.pop('logado', None)
    flash('Logout OK')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)

    '''insert into entradas (titulo, texto) values (?, ?)'''

    post = Post(request.form['titulo'], request.form['texto'])
    db.session.add(post)
    db.session.commit()

    flash('Nova entrada registrada com sucesso')
    return redirect(url_for('exibir_entradas'))

@app.route('/entrada/<int:post_id>', methods=['GET', 'POST'])
def exibir_detalhe_entrada(post_id):
    post = Post.query.get_or_404(post_id)

    form = forms.ComentarioForm(request.form)
    if request.method == 'POST' and form.validate():
        #comentario = Comentario(form.username.data, form.email.data,
        #            form.password.data)
        #db_session.add(user)
        flash(u'Grato por seu comentário')

    return render_template('entrada_detalhe.html', entrada=post, form=form)



if __name__ == '__main__':
    app.run()
