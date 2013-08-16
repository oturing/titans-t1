# coding: utf-8

"""
Exemplos com a classe Monstro

    >>> tubarao_voador = Monstro('Tubzilla')
    >>> tubarao_voador
    <Monstro "Tubzilla">
    >>> tubarao_voador.nome
    'Tubzilla'
    >>> tubarao_voador.voar()
    Tubzilla: flap, flap, flap
    >>> atributo = 'nome'
    >>> getattr(tubarao_voador, atributo)
    'Tubzilla'
    >>> tubarao_voador.nadar
    Tubzilla nao sabe "nadar"
    >>> tubarao_voador.peso
    Traceback (most recent call last):
        ...
    AttributeError: 'Monstro' object has no attribute 'peso'
    >>> gojira = Monstro('Gojira', arma='fogo', defesa='couraça')
    >>> gojira.arma
    'fogo'
    >>> gojira.peso = 100
    >>> gojira.peso
    100
    >>> gojira.p = 123
    Traceback (most recent call last):
        ...
    TypeError: atributos devem ter mais de uma letra no identificador
    >>> gojira[34029482]
    <Monstro "filhote #34029482 de Gojira">
    >>> gojira + tubarao_voador
    <Monstro "cruzamento de Gojira com Tubzilla">
    >>> gojira * 3
    [<Monstro "Gojira #1">, <Monstro "Gojira #2">, <Monstro "Gojira #3">]
    >>> 2 * gojira
    [<Monstro "Gojira #1">, <Monstro "Gojira #2">]
    >>> gojira * 'bla'
    Traceback (most recent call last):
        ...
    TypeError: multiplicao nao funciona com objetos do tipo str
"""

class Monstro(object):
    """Bicho que não existe"""

    def __init__(self, nome, **caracteristicas):
        self.nome = nome
        self.caracteristicas = caracteristicas

    def __repr__(self):
        return '<Monstro "%s">' % self.nome

    def voar(self):
        print '%s: flap, flap, flap' % self.nome

    def __getattr__(self, nome_atr):
        if nome_atr in self.caracteristicas:
            return self.caracteristicas[nome_atr]
        elif nome_atr.endswith('r'):
            print '%s nao sabe "%s"' % (self.nome, nome_atr)
        else:
            raise AttributeError("'Monstro' object has no attribute '%s'" % nome_atr)

    def __setattr__(self, nome_atr, valor):
        if len(nome_atr) <= 1:
            raise TypeError('atributos devem ter mais de uma letra no identificador')
        else:
            object.__setattr__(self, nome_atr, valor)

    def __getitem__(self, numero):
        return Monstro('filhote #%s de %s' % (numero, self.nome))

    def __add__(self, outro):
        return Monstro('cruzamento de %s com %s' % (self.nome, outro.nome))

    def __mul__(self, outro):
        res = []
        try:
            itens = range(outro)
        except TypeError:
            raise TypeError('multiplicao nao funciona com objetos do tipo %s' % (type(outro).__name__))
        for i in itens:
            res.append(Monstro('%s #%s' % (self.nome, i+1)))
        return res

    __rmul__ = __mul__ # propriedade comutativa da multiplicacao







