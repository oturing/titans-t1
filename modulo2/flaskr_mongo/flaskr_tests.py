# coding: utf-8

from __future__ import unicode_literals

import unittest
from datetime import datetime

import pymongo

import flaskr

CLIENTE = pymongo.MongoClient()
NOME_BD = str(datetime.now()).replace('.','_').replace(' ','_')

def tearDownModule():
    CLIENTE.drop_database(NOME_BD)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.config['DATABASE'] = NOME_BD
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        '''TODO: fechar conexao com o MongoDB'''
        '''apagar BD de teste no MongoDB'''
        flaskr.conectar_bd().drop_collection('posts')

    def teste_conexao_bd(self):
        bd = flaskr.conectar_bd()
        self.assertIsInstance(bd, pymongo.database.Database)

    def teste_bd_vazio(self):
        res = self.app.get('/')
        self.assertIn(b'nenhuma entrada', res.data)

    def entrar(self, usuario, senha):
        return self.app.post('/entrar', data=dict(
                username=usuario,
                password=senha
            ), follow_redirects=True)

    def teste_login(self):
        rv = self.entrar('admin', 'default')
        self.assertIn(b'Login OK', rv.data)

    def teste_login_invalido(self):
        rv = self.entrar('adminXXX', 'default')
        self.assertIn(b'Usuário inválido', rv.data)
        rv = self.entrar('admin', 'defaultYYY')
        self.assertIn(b'Senha inválida', rv.data)

    def teste_sair(self):
        rv = self.app.get('/sair', follow_redirects=True)
        self.assertIn(b'Logout OK', rv.data)

    def postar(self, titulo, texto):
        self.entrar('admin', 'default')
        return self.app.post('/inserir',
                data=dict(titulo=titulo, texto=texto),
                follow_redirects=True)

    def teste_nova_entrada(self):
        rv = self.postar('<Olá>', '<strong>HTML</strong> é permitido aqui')
        self.assertEquals(rv.status_code, 200)
        self.assertNotIn(b'nenhuma entrada', rv.data)
        self.assertIn(b'&lt;Olá&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> é permitido aqui', rv.data)

    def teste_entradas_em_ordem_inversa(self):
        rv = self.postar('Noticia Um', 'bla, bla, bla')
        self.assertEquals(rv.status_code, 200)
        rv = self.postar('Noticia Dois', 'bla, bla, bla')
        self.assertEquals(rv.status_code, 200)
        with flaskr.app.test_client() as c:
            rv = c.get('/')
            entradas = flaskr.obter_entradas()
        self.assertEquals(entradas[0]['titulo'], 'Noticia Dois')
        self.assertEquals(entradas[1]['titulo'], 'Noticia Um')


if __name__ == '__main__':
    unittest.main()
