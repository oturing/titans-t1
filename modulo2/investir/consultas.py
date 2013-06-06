# coding: utf-8

import io, os, csv, cStringIO

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from modelos import Cliente

def clientes(sessao):
    """
    E1. Listar cod_contribuinte e nome de cada cliente com cod_contribuinte >= 3
    """
    res = (sessao.query(Cliente.cod_contribuinte, Cliente.nome)
                 .filter(Cliente.cod_contribuinte >= 3)
          )
    for cli in res:
        print cli.cod_contribuinte, cli.nome

def criar_sessao(url_bd, echo=False):
    engine = sa.create_engine(url_bd, echo=echo)
    cnx = engine.connect()
    Session = sessionmaker(bind=engine)
    return Session(bind=cnx)

def main():
    url = 'sqlite:///investir.sqlite'
    sessao = criar_sessao(url)

    clientes(sessao)
    #acoes_tecnologia(sessao)


if __name__=='__main__':
    main()
