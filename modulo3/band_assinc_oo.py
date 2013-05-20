#coding: utf-8
'''
Baixar bandeiras do site da CIA de modo síncrono
'''

from urllib import urlopen
from contextlib import closing
import re

from tornado import httpclient, ioloop

URL_BASE = 'https://www.cia.gov/library/publications/the-world-factbook/'

URL_FLAGS = URL_BASE + 'graphics/flags/large/'

RE_LINK = re.compile(r'large/(\w\w-lgflag\.gif)')

pendentes = set()

def obter_nomes():
    with open('flags.html') as arq:
        html = arq.read()
    return RE_LINK.findall(html)

def salvar_bandeira(nome, img):
    with open('bandeiras/' + nome, 'wb') as saida:
        saida.write(img)

def tratar_resposta(response, num, nome):
    if not response.error:
        img = response.body
        print '\t', num, nome
        salvar_bandeira(nome, img)
    else:
        print '***', response.error
    pendentes.discard(nome)
    if not pendentes:
        ioloop.IOLoop.instance().stop()

"""
def faz_tratar_resposta(num, nome):
    def _tratar_resposta(response):
        tratar_resposta(response, num, nome)
    return _tratar_resposta
"""

class Tratador(object):
    def __init__(self, num, nome):
        self.num = num
        self.nome = nome
    def tratar_resposta(self, response):
        tratar_resposta(response, self.num, self.nome)

def baixar_bandeiras(lista_nomes, qtd_max=10):
    cliente = httpclient.AsyncHTTPClient()
    for i, nome in enumerate(lista_nomes[:qtd_max], 1):
        print i, nome
        pendentes.add(nome)
        cliente.fetch(URL_FLAGS + nome, Tratador(i, nome).tratar_resposta)

    ioloop.IOLoop.instance().start()


res = obter_nomes()
print len(res), 'bandeiras conhecidas'
baixar_bandeiras(res)


