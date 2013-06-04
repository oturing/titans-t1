# coding: utf-8

import io, os, csv, cStringIO

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, mapper

def clientes(sessao):
    """
    E1. Listar cod_contribuinte e nome de cada cliente com cod_contribuinte >= 3
    """
    res = (sessao.query(Cliente.cod_contribuinte, Cliente.nome)
                 .filter(Cliente.cod_contribuinte >= 3)
          )
    for cli in res:
        print cli.cod_contribuinte, cli.nome

def acoes_tecnologia(sessao):
    """
    E2. Listar simbolos das acoes do setor "tecnologia"
    """
    res = (sessao.query(Acao.simbolo)
                 .filter_by(setor = "tecnologia")
          )
    for acao in res:
        print acao.simbolo

Cliente = type('Cliente',(),{})
Acao = type('Acao',(),{})

def main(nome_rdb):
    """
    Lê dados de um arquivo .rdb e insere nas tabelas apropriadas
    """
    uri = 'sqlite:///%s.sqlite' % (os.path.splitext(nome_rdb)[0])
    engine = sa.create_engine(uri, echo=True)
    metadata = sa.MetaData(bind=engine)
    cnx = engine.connect()
    Session = sessionmaker(bind=engine)
    sessao = Session(bind=cnx)

    mapper(Cliente, sa.Table('cliente', metadata, autoload=True))
    mapper(Acao, sa.Table('acao', metadata, autoload=True))

    clientes(sessao)
    acoes_tecnologia(sessao)


if __name__=='__main__':
    import sys
    main(sys.argv[1])
