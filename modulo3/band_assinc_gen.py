#coding: utf-8
'''
Baixar bandeiras do site da CIA de modo síncrono
'''

from urllib import urlopen
from contextlib import closing
import re

from tornado import httpclient, ioloop, gen

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

@gen.engine
def buscar_e_tratar_resposta(cliente, num, nome):
    print num, nome
    response = yield gen.Task(cliente.fetch, URL_FLAGS + nome)
    if not response.error:
        img = response.body
        print '\t', num, nome
        salvar_bandeira(nome, img)
    else:
        print '***', response.error
    pendentes.discard(nome)
    if not pendentes:
        ioloop.IOLoop.instance().stop()

def baixar_bandeiras(lista_nomes, qtd_max=10):
    cliente = httpclient.AsyncHTTPClient()
    for i, nome in enumerate(lista_nomes[:qtd_max], 1):
        pendentes.add(nome)
        #cliente.fetch(URL_FLAGS + nome, tratar_resposta)
        buscar_e_tratar_resposta(cliente, i, nome)

    ioloop.IOLoop.instance().start()


res = obter_nomes()
print len(res), 'bandeiras conhecidas'
baixar_bandeiras(res)
