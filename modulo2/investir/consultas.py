# coding: utf-8

import io, os, csv, cStringIO

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# operadores de Query
from sqlalchemy import or_, func

from modelos import Cliente, Acao, CarteiraAcoes

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

def acoes_cotacao_desc(sessao):
    """
    E3. Listar simbolos e cotacoes das três ações mais caras, acoes em
        ordem decrescente de cotacao
    """
    res = (sessao.query(Acao.simbolo, Acao.cotacao)
                 .order_by(Acao.cotacao.desc())[:3]
          )
    for acao in res:
        print acao.simbolo, acao.cotacao

def acoes_alimentos_ou_farma(sessao):
    """
    E4. Listar simbolos das acoes do setor "alimentos" ou "farmaceutica"
    """
    res = (sessao.query(Acao.simbolo)
                 .filter(or_(Acao.setor == "alimentos",
                             Acao.setor == "farmaceutica")
                        )
          )
    for acao in res:
        print acao.simbolo

def acao_cotacao_23(sessao):
    """
    E5. Exibir simbolo e cotacao da ação com cotação = 23
    """
    query = (sessao.query(Acao.simbolo, Acao.cotacao)
                          .filter_by(cotacao=23))
    try:
        acao = query.one()
        print acao.simbolo, acao.cotacao
    except sa.orm.exc.MultipleResultsFound:
        print 'Não existe apenas uma ação com cotação = 23.'
        print 'Exibindo a primeira delas:'
        acao = query.first()
        print acao.simbolo, acao.cotacao

def cotacao_minima(sessao):
    """
    E6. Exibir menor valor de cotação de todas as ações
    """
    cotacao = sessao.query(func.min(Acao.cotacao)).one()[0]
    print cotacao

def acoes_mais_caras(sessao):
    """
    E7. Exibir simbolo e cotacao de todas as ações com a menor cotação
    """
    res = (sessao.query(Acao.simbolo, Acao.cotacao)
                 .filter(Acao.cotacao.in_(sessao.query(func.max(Acao.cotacao))))
          )
    for acao in res:
        print acao.simbolo, acao.cotacao

def acoes_do_cliente_6_ineficiente(sessao):
    """
    E8i. Exibir simbolo, cotacao e cotas de todas as ações do cliente com
        cod_contribuinte = 6 (implementação altamente ineficiente)
    """
    cliente6 = (sessao.query(Cliente).filter_by(cod_contribuinte = 6).one())
    for carteira in cliente6.carteiras:
        print carteira.acao.simbolo, carteira.acao.cotacao, carteira.cotas

def acoes_do_cliente_6(sessao):
    """
    E8. Exibir simbolo, cotacao e cotas de todas as ações do cliente com
        cod_contribuinte = 6 (implementação altamente ineficiente)
    """
    carteira_cliente6 = (sessao.query(CarteiraAcoes.simbolo, CarteiraAcoes.cotas, Acao.cotacao)
                               .filter_by(cod_contribuinte = 6)
                               .join(Acao))
    for acao in carteira_cliente6:
        print acao.simbolo, acao.cotas, acao.cotacao

def criar_sessao(url_bd, echo=False):
    engine = sa.create_engine(url_bd, echo=echo)
    cnx = engine.connect()
    Session = sessionmaker(bind=engine)
    return Session(bind=cnx)

def listar_consultas():
    """
    Devolve o nome e a referência de todas as funções definidas ou importadas
    neste módulo que tenham o primeiro argumento chamado `sessao`
    """
    consultas = {}
    for chave, valor in globals().items():
        if hasattr(valor, '__code__') and valor.__code__.co_varnames[0] == 'sessao':
            consultas[chave] = valor
    return consultas

def main(argv):
    """
    Executa qualquer função definida ou importada neste módulo que tenha
    o primeiro argumento chamado `sessao`
    """
    consultas = listar_consultas()
    if len(argv) != 2 or argv[1] not in consultas:
        print 'Informe a consulta a ser executada:'
        for nome in sorted(consultas):
            print '\t', nome
        raise SystemExit

    url = 'sqlite:///investir.sqlite'
    sessao = criar_sessao(url, echo=True)
    # executar a consulta
    consultas[argv[1]](sessao)

if __name__=='__main__':
    import sys
    main(sys.argv)
