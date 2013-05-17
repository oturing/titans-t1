#coding: utf-8
'''
Baixar bandeiras do site da CIA de modo síncrono
'''

from urllib import urlopen
from contextlib import closing

URL_INDICE = ('https://www.cia.gov/library/publications/the-world-factbook/'
              'docs/flagsoftheworld.html')

LINK = 'src="../graphics/flags/large/af-lgflag.gif"'

with closing(urlopen(URL_INDICE)) as cnx:
    html = cnx.read()

with open('flags.html', 'wb') as saida:
    saida.write(html)

print len(html)
print html[:70]

