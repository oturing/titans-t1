# coding: utf-8

def media(valores):
    """Calcula a média aritmética de uma lista de números.

    >>> print media([20, 30, 70])
    40.0
    """
    return sum(valores, 0.0) / len(valores)

if __name__=='__main__':
    # Executa eutomaticamente os testes deste módulo
    import doctest
    doctest.testmod()
