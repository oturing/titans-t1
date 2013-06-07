# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'

    cod_contribuinte = Column(String, primary_key=True)
    nome = Column(String)
    endereco = Column(String)

# @acao(simbolo/char,empresa/char,avaliacao/char,setor/char,
# cotacao_max/numeric,cotacao_min/numeric,cotacao/numeric,retorno_1a/numeric,retorno_5a/numeric):simbolo

class Acao(Base):
    __tablename__ = 'acao'

    simbolo = Column(String, primary_key=True)
    empresa = Column(String)
    setor = Column(String)
    cotacao_max = Column(Integer)
    cotacao_min = Column(Integer)
    cotacao = Column(Integer)
    retorno_1a = Column(Integer)
    retorno_5a = Column(Integer)

# @carteira_acoes(cod_contribuinte/char,simbolo/char,cotas/numeric):cod_contribuinte,simbolo

class CarteiraAcoes(Base):
    __tablename__ = 'carteira_acoes'

    cod_contribuinte = Column(String, ForeignKey('cliente.cod_contribuinte'), primary_key=True)
    simbolo = Column(String, ForeignKey('acao.simbolo'), primary_key=True)
    cotas = Column(Integer)

    # relacionamentos
    cliente = relationship('Cliente', backref=backref('carteiras', order_by=simbolo))
    acao = relationship('Acao', backref=backref('carteiras', order_by=cod_contribuinte))



