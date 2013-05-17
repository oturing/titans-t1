#coding: utf-8
'''
Baixar bandeiras do site da CIA de modo síncrono
'''

from urllib import urlopen
from contextlib import closing
import re

URL_BASE = 'https://www.cia.gov/library/publications/the-world-factbook/'

URL_FLAGS = URL_BASE + 'graphics/flags/large/'

RE_LINK = re.compile(r'large/(\w\w-lgflag\.gif)')

def obter_nomes():
    with open('flags.html') as arq:
        html = arq.read()
    return RE_LINK.findall(html)

def buscar_bandeira(nome):
    with closing(urlopen(URL_FLAGS + nome)) as cnx:
        img = cnx.read()
    return img

def salvar_bandeira(nome, img):
    with open('bandeiras/' + nome, 'wb') as saida:
        saida.write(img)

def baixar_bandeiras(lista_nomes, qtd_max=10):
    for nome in lista_nomes[:qtd_max]:
        img = buscar_bandeira(nome)
        print len(img), 'bytes em', nome
        salvar_bandeira(nome, img)


res = obter_nomes()
print len(res), 'bandeiras conhecidas'
baixar_bandeiras(res)


