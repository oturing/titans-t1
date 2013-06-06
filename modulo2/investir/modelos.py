# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'

    cod_contribuinte = Column(String, primary_key=True)
    nome = Column(String)
    endereco = Column(String)

