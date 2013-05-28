# coding: utf-8

import io, os, csv, cStringIO

import sqlalchemy as sa

from tabelas import analisar_descr

def montar_registro(campos_tipos, linha):
    buf = cStringIO.StringIO(linha.encode('utf-8'))
    partes = list(csv.reader(buf, quotechar="'"))[0]
    registro = {}
    for (campo, tipo), valor in zip(campos_tipos, partes):
        if tipo == 'numeric':
            valor = int(valor)
        else:
            valor = valor.decode('utf-8')
        registro[campo] = valor
    return registro

def main(nome_rdb):
    """
    Lê dados de um arquivo .rdb e insere nas tabelas apropriadas
    """
    uri = 'sqlite:///%s.sqlite' % (os.path.splitext(nome_rdb)[0])
    engine = sa.create_engine(uri, echo=True)
    metadata = sa.MetaData()
    cnx = engine.connect()
    with io.open(nome_rdb, encoding='utf-8') as arq_rdb:
        for lin in arq_rdb:
            lin = lin.rstrip()
            if not lin:
                continue
            if lin.startswith(u'@'):
                nome_tabela, campos_tipos, chaves = analisar_descr(lin)
                print nome_tabela
            else:
                registro = montar_registro(campos_tipos, lin)
                tabela = sa.Table(nome_tabela, metadata,
                                autoload=True, autoload_with=engine)
                cnx.execute(tabela.insert(), **registro)

if __name__=='__main__':
    import sys
    main(sys.argv[1])
