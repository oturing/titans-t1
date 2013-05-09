# coding: utf-8

# todos os imports
from contextlib import closing
import pymongo
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuração
DATABASE = 'flaskr'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# criar nossa pequena aplicação :)
app = Flask(__name__)
app.config.from_object(__name__)

################################################# Configuração

def conectar_bd():
    cliente = pymongo.MongoClient()
    return cliente[app.config['DATABASE']]

@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.connection.close()


################################################# Views

@app.route('/')
def exibir_entradas():
    entradas = g.bd.posts.find()

    return render_template('exibir_entradas.html', entradas=entradas)

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

    # insert into entradas (titulo, texto) values (?, ?)
    post = dict(titulo=request.form['titulo'],
                texto=request.form['texto'])
    entradas = g.bd.posts.insert(post)

    flash('Nova entrada registrada com sucesso')
    return redirect(url_for('exibir_entradas'))

if __name__ == '__main__':
    app.run()
