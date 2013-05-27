# coding: utf-8

import io

"""
Criar tabelas a partir da descrição em um arquivo .rdb do WinRDB
"""

def main(nome_rdb):
    """
    Esta função:
    1) extrai de um arquivo .rdb as descrições das tabelas
    ...
    """
    with io.open(nome_rdb, encoding='utf-8') as arq_rdb:
        for lin in arq_rdb:
            lin = lin.rstrip()
            if lin.startswith('@'):
                print lin

if __name__=='__main__':
    import sys
    main(sys.argv[1])
