===================
Projeto Pizzaria
===================

--------------
Comandos úteis
--------------

Ativar o ambiente, a partir do diretório onde ele foi criado::

  $ source .django/bin/activate

Criar novas tabelas no BD::

  $ ./manage.py syncdb


Executar o servidor de desenvolvimento::

  $ ./manage.py runserver

Exportar dados::

  $ ./manage.py dumpdata entrega --indent=2 > entrega/fixtures/tres_clientes.json

Carregar dados::

  $ ./manage.py loaddata entrega/fixtures/tres_clientes.json

Remover uma tabela::

  $ ./manage.py dbshell
  sqlite> DROP TABLE entrega_cliente;
  sqilte> .quit

----------------------------------
Interagindo com o shell do Django
----------------------------------

Acessar o console do Django::

  $ ./manage.py shell
  >>>
  

Acessar os registros de uma tabela::

    >>> from entrega.models import *
    >>> Pedido.objects.all()  
    [<Pedido: #1 - 2013-04-18 22:08:50+00:00>, 
     <Pedido: #2 - 2013-04-18 23:14:58+00:00>, 
     <Pedido: #3 - 2013-04-22 21:42:28+00:00>]

Ver o SQL gerado pela consulta mais recente::

    >>> from django.db import connection
    >>> connection.queries[-1]

