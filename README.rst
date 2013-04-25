==================================
Instalação básica de um virtualenv
==================================

1. Instale o ``virtualenv`` no seu SO

Use o sistema de pacotes do seu GNU/Linux.
Você precisa da conta de administrador (dá para instalar
como usuário comum, mas é mais complicado).

::

	$ sudo apt-get install python-virtualenv
	$

2. Use o ``virtualenv`` para criar um ambiente dentro de um
diretório::

	$ cd meu_projeto
	$ virtualenv --no-site-packages --distribute .meu_env
	$

3. Ative o ambiente (note que o prompt muda)::

	$ source .meu_env/bin/activate
	(.meu_env)$

4. Instale os pacotes desejados no ambiente::

	(.meu_env)$ pip install flask
	(.meu_env)$




