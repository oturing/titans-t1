# coding: utf-8

"""
Cria tabelas a partir da descrição em um arquivo .rdb do WinRDB
"""

import io, re, os

import sqlalchemy as sa

# @cliente(cod_contribuinte/char,nome/char,endereco/char):cod_contribuinte
RE_DESCR_TABELA = re.compile(r'^@(\w+)\((.*?)\):(.+)$')

def analisar_descr(linha):
    """Analisa descrição de tabela no arquivo .rdb"""
    res = RE_DESCR_TABELA.match(linha)
    assert res, 'descricao nao bateu com regex'
    tabela, campos_tipos, chaves = res.groups()
    campos_tipos = campos_tipos.split(',')
    campos_tipos = [tuple(ct.split('/')) for ct in campos_tipos]
    chaves = chaves.split(',')
    return tabela, campos_tipos, chaves

def montar_tabela(metadata, nome, campos_tipos, chaves):
    colunas = []
    mapa_tipos = {
        u'char'   : sa.String,
        u'numeric': sa.Integer,
    }
    for nome_col, tipo in campos_tipos:
        pk = nome_col in chaves
        colunas.append(sa.Column(nome_col, mapa_tipos[tipo], primary_key=pk))
    sa.Table(nome, metadata, *colunas)

def main(nome_rdb):
    """
    Esta função:
    1) extrai de um arquivo .rdb as descrições das tabelas
    2) monta os metadadados das tabelas usando sqlalchemy
    3) cria todas as tabelas no BD
    """
    uri = 'sqlite:///%s.sqlite' % (os.path.splitext(nome_rdb)[0])
    engine = sa.create_engine(uri, echo=True)
    metadata = sa.MetaData()

    with io.open(nome_rdb, encoding='utf-8') as arq_rdb:
        for lin in arq_rdb:
            lin = lin.rstrip()
            if lin.startswith('@'):
                tabela, campos_tipos, chaves = analisar_descr(lin)
                montar_tabela(metadata, tabela, campos_tipos, chaves)

    metadata.create_all(engine)

if __name__=='__main__':
    import sys
    main(sys.argv[1])
