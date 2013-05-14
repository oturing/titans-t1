# coding: utf-8

from __future__ import unicode_literals

import os
import unittest
import tempfile

import flaskr

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.bd_arq, nome_bd = tempfile.mkstemp()
        flaskr.app.config['DATABASE'] = nome_bd
        flaskr.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + nome_bd
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.criar_bd()

    def tearDown(self):
        os.close(self.bd_arq)
        os.unlink(flaskr.app.config['DATABASE'])

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
        entradas = flaskr.obter_entradas()
        self.assertEquals(entradas[0].titulo, 'Noticia Dois')
        self.assertEquals(entradas[1].titulo, 'Noticia Um')

    def teste_detalhes_entrada(self):
        rv = self.postar('<Oi>', '<p>Corpo do post</p>')
        self.assertIn(b'/entrada/1"', rv.data)
        rv = self.app.get('/entrada/1')
        self.assertEquals(rv.status_code, 200)
        self.assertIn(b'#1', rv.data)
        self.assertIn(b'&lt;Oi&gt;', rv.data)
        self.assertIn(b'<p>Corpo do post</p>', rv.data)

    def teste_form_comentario_entrada(self):
        rv = self.postar('Oi', 'Corpo do post')
        rv = self.app.get('/entrada/1')
        self.assertIn(b'<form', rv.data)

    def teste_postar_comentario_entrada(self):
        rv = self.postar('Oi', 'Corpo do post')
        rv = self.app.get('/entrada/1')
        self.assertIn(b'<form', rv.data)
        comentario = dict(nome='Fulano de Tal',
                          email='fu@tal.com',
                          texto='Aqui não pode HTML')
        rv = self.app.post('/entrada/1', data=comentario,
                                         follow_redirects=True)
        for conteudo in comentario.values():
            self.assertIn(conteudo.encode('utf-8'), rv.data)

if __name__ == '__main__':
    unittest.main()
