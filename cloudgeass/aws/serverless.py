"""
---------------------------------------------------
----------------- MÓDULO: lambda ------------------
---------------------------------------------------
Módulo responsável por alocar funcionalidades
associadas ao serviço lambda na AWS, desde a criação
de camadas de maneira dinâmica com ingestão direta
no s3, até outras funcionalidades envolvendo a 
construção e configuração de funções lambda na AWS

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Layers lambda de pacotes python
    2.1 Funções de preparação
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 31/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Biblitocas built-in
import os
import shutil
from sys import platform

# Módulos auxiliares
from cloudgeass.utils.log import log_config
from cloudgeass.aws.s3 import JimmyBuckets

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Definindo variáveis fixas de uso interno
PATH = os.path.join(os.getcwd(), r'lambda\layer')
REQ_FILE = os.path.join(os.getcwd(), 'requrements.txt')
REGION = 'sa-east-1'


"""
---------------------------------------------------
------- 2. LAYERS LAMBDA DE PACOTES PYTHON --------
       2.1 Funções de preparação da camada
---------------------------------------------------
"""

# Criando diretório de layer para integração com runtime do lambda
# https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html
def create_layer_path(layers_root_path, layer_name, runtime_folder='python'):
    """
    Cria um diretório específico para o recebimento das
    dependências/pacotes python a serem inclusos no layer
    a ser criado. Para que o layer lambda funcione 
    adequadamente na provedora AWS, é necessário que
    alguns critérios sejam atendidos de acordo com a
    linguagem de programação utilizada. No caso do python,
    o diretório do layer com as dependências deve possuir,
    como último diretório, as pastas "python/" ou 
    "python/lib/python3.9/site-packages", sendo esta última
    dependendente da versão da linguagem (substituir 3.9 pela
    versão desejada e configurada na função lambda).

    Parâmetros
    ----------
    :param path:
        Caminho no sistema operacional com o diretório alvo
        para alocação do layer a ser zipado. Para auxiliar o
        usuário, uma lógica de verificação foi adicionada na
        função para validar se o último diretório contém
        os requisitos citados acima na documentação. Caso
        o diretório passado não contenha as pastas exigidas,
        o script nesta função adiciona o elemento faltante. 
        Caso o diretório exigido já esteja contemplado neste
        parâmetro, nenhuma ação é realizada.
        [type: string]

    :param runtime_folder:
        Este parâmetro contempla a informação do diretório
        exigido dentro das propostas da linguagem python de
        criação de layers para funções lambda. Por padrão,
        foi escolhida a opção mais simples e intuitiva 
        ("python"), porém nada impede do usuário passar
        seu próprio parâmetro, desde que este esteja
        adequado aos requisitos aceitos dentro das boas
        práticas de construção de layers lambda.
        [type: string, default='python']
    """
    
    # Criando diretório
    try:
        path = os.path.join(layers_root_path, layer_name, runtime_folder)
        os.makedirs(path)
        logger.info(f'Diretório do layer criado em {path}')
    except FileExistsError as fee:
        logger.warning(fee)

    return path

# Estruturando dependências do pacote
def download_packages(target_path, packages_from='list', **kwargs):
    """
    Download e estruturação de pacotes python a serem inclusos no
    layer lambda. A grande vantagem proposta por essa função é o
    encapsulamento dos comandos de download de pacotes a partir
    de insumos fornecidos pelo usuário em uma instalação 
    direcionada em um diretório alvo do layer lambda estruturado.

    Na prática, existem duas possibilidades de definição da origem 
    das dependências a serem consideradas no processo de instalação.
    O usuário pode utilizar o parâmetro "packages_from" para essa
    configuração, sendo as possibilidades dadas por:

        * 'list': nesta configuração, o usuário fornece manualmente
        uma lista de dependências/pacotes a serem baixados dentro
        do diretório alvo ("target_path") de construção do layer.
        Tal lista é passada como argumento adicional dentro do
        parâmetro "packages_list". Adicionalmente, é possível
        configurar este formato para que o usuário preencha
        manualmente as dependências a partir do próprio prompt
        de comando (argumento "user_input");

        * 'venv': aqui, a definição das dependências/pacotes é 
        feita de forma automática a partir da coleta dos insumos
        já existentes no ambiente virtual ativo. Em outras palavras,
        é criado um arquivo de requirements temporário a partir da
        execução do comando "pip freeze > requirements_tmp.txt",
        fazendo assim com que uma lista de dependências seja
        gerada automaticamente considerando os insumos existentes
        no venv de trabalho;

    Após as definições dos pacotes, é realizada uma instalação
    direcionada em um diretório alvo a partir da execução do
    comando "python3 -m pip install -t <target_path> <package>"

    Parâmetros
    ----------
    :param target_path:
        Diretório alvo de instalação dos pacotes do layer a ser
        estruturado. É importante considerar os requisitos necessários
        para a criação de layers lambda de acordo com as versões
        do python consideradas.
        [type: string]

    :param packages_from:
        Informação da origem dos pacotes a serem baixados e instalados
        no diretório alvo do layer. Como mencionado acima, este
        argumento aceita duas entradas possíveis: 'list' e 'venv'.
        Em cada caso, diferentes regras são aplicadas para que
        a instalação direcionada seja feita de forma adequada.
        [type: string, default='list']

    Argumentos Adicionais
    ---------------------
    :kwarg packages_list:
        Argumento a ser preenchido caso o usuário configure a origem
        das dependências a partir de uma lista (packages_from='list').
        Nesta abordagem, este argumento é opcionalmente preenchido
        com uma lista de dependências/pacotes a ser considerada no
        ato da instalação direcionada. Internamente no código, são
        aplicadas transformações de string (.lowere() e .strip())
        para que o pacote seja, na medida do possível, devidamente 
        instalado. Caso o parâmetro "packages_from" seja configurado
        como 'list' e o usuário NÃO forneça uma lista para o 
        argumento "packages_list", obrigatoriamente o argumento 
        "user_input" precisa ser configurado como True para que,
        dessa forma, o usuário tenha a chance de fornecer informações
        dos pacotes diretamente no prompt de comando no ato de execução
        do script de criação de layer.
        [type: list, default=None]

    :kwarg user_input:
        Argumento a ser opcionalmente preenchido caso a configuração
        da função seja dada com packages_from='list' e nenhuma lista
        passada para o argumento "packages_list". Neste caso, este
        argumento em questão trata do preenchimento manual do usuário
        diretamente pelo prompt de comando, informando assim as 
        dependências a serem baixadas para o layer. Assim como no caso
        de "packages_list", este argumento considera tratativas em
        strings para evitar, ao máximo, erros de instalação por 
        referências de pacotes mal formatadas.
        [type: bool, default=False]
    """

    # Validando origem das dependências
    if packages_from == 'list':
        logger.info(f'Pacotes a serem instalados serão fornecidos pelo usuário')
        # Coletando argumentos adicionais pra instalação dos pacotes
        packages_list = kwargs['packages_list'] if 'packages_list' in kwargs else None
        user_input = bool(kwargs['user_input']) if 'user_input' in kwargs else False
        
        # Validando falhas na configuração do modo de coleta de pacotes
        if packages_list is not None and type(packages_list) != list:
            logger.error(f'Argumento "packages_list" não é uma lista. Por favor, forneça uma lista com as dependências')
            return
        if packages_list is None and not user_input:
            logger.warning(f'O parâmetro "packages_from" foi configurado como "list", mas nenhuma lista foi passada como argumento da função')
            logger.error(f'Forneça uma lista de dependências no argumento "packages_list" ou configure "user_input" como True para coleta manual no prompt')
            return
        elif packages_list is not None and user_input:
            logger.warning(f'Foi passada uma lista de dependências no parâmetro "packages_list", mas o parâmetro "user_input" também foi configurado como True')
            logger.error(f'No caso de packages_from="list", recomenda-se fornecer uma lista para o argumento packages_list OU user_input=True para evitar conflito')
            return
        elif packages_list is None and user_input:
            # Coletando pacotes manualmente do usuário
            user_pkgs = input('Insira o nome dos pacotes a serem baixados separados por vírgula: ')
            packages_list = [pkg.lower().strip() for pkg in user_pkgs.split(',')]
        elif packages_list is not None and not user_input:
            # Tratando possíveis equívocos no fornecimento dos pacotes em formato de lista
            packages_list = [pkg.lower().strip() for pkg in packages_list]

        # Definindo comando básico de instalação de acordo com sistema operacional
        if platform == 'linux':
            base_install_cmd = f'python3 -m pip install -t {target_path} <package>'
        else:
            base_install_cmd = f'python3 -m pip install --no-user -t {target_path} <package>'
        
        # Iterando sobre cada pacote para realização da instalação
        logger.debug(f'Instalando os {len(packages_list)} pacotes listados')
        for pkg in packages_list:
            pkg_install_cmd = base_install_cmd.replace('<package>', pkg)
            os.system(pkg_install_cmd)
        logger.info(f'Comando de instalação das dependências {packages_list} executado. Verifique no prompt se há algum erro crítico')

    elif packages_from == 'venv':
        logger.info(f'Pacotes a serem instalados serão extraídos automaticamente do ambiente virtual ativo')
        
        # Definindo arquivo temporário de requirements
        req_file = os.path.join(os.getcwd(), 'requirements_tmp.txt')
        logger.debug(f'Extraindo dependências do venv e salvando temporiamente em {req_file}')
        os.system(f'pip freeze > {req_file}')

        # Definindo comando básico de instalação de acordo com sistema operacional
        if platform == 'linux':
            req_install_cmd = f'python3 -m pip install -r {req_file} -t {target_path}'
        else:
            req_install_cmd = f'python3 -m pip install --no-user -r {req_file} -t {target_path}'
        logger.debug(f'Instalando dependências salvas em arquivo temporário de requirements')
        os.system(req_install_cmd)

        # Eliminando arquivo temporário de requirements
        os.remove(req_file)
        logger.info(f'Comando para instalação das dependências do venv ativo executado. Verifique no prompt se há algum erro crítico')

    else:
        # Origem dos pacotes indefinida
        logger.error(f'Parâmetro packages_from={packages_from} inválido. Selecione entre "list" ou "venv"')
        return

# Zipando e realizando upload do layer em bucket específico
def upload_layer_to_bucket(target_path, bucket_name, key):
    """
    Zipa o layer gerado a partir da instalação das dependências
    e realiza o upload do arquivo zipado para um bucket s3. 
    Este tipo de operação é importante para manter um gerenciamento
    correto dos layers dentro das boas práticas da AWS.

    Para uma melhor organização do conteúdo, é recomendado
    preencher o parâmetro "prefix" como uma espécie de nome do layer
    pois, dessa forma, o objeto a ser subido pro s3 poderá ser
    resgatado considerando o prefixo de diretório no bucket.

    Parâmetros
    ----------
    :param layer_path:
        Caminho de referência do layer gerado.
        [type: string]

    :param bucket_name:
        Nome do bucket alvo do upload do arquivo zipado.
        [type: string]

    :param prefix:
        Diretório do bucket para organização do layer gerado.
        [type: string]
    """

    # Zipando diretório do layer
    try:
        shutil.make_archive(target_path, format='zip', root_dir=target_path)
        logger.info(f'Diretório de dependências {target_path} zipado com sucesso')
    except Exception as e:
        logger.error(f'Erro ao zipar diretório de dependências {target_path}. Exception: {e}')
        return

    # Instanciando classe JimmyBuckets para operações no s3
    jbuckets = JimmyBuckets(region=REGION)
    jbuckets.upload_object(
        file=target_path + '.zip',
        bucket_name=bucket_name,
        key=key
    )

# Cria um layer e realiza o upload em um bucket s3
def build_lambda_layer(target_path, bucket_name, key, 
                       packages_from='list', **kwargs):
    """
    Realiza a construção completa de um layer lambda a partir
    da execução individual de cada uma das etapas associadas
    e encapsuladas neste mesmo módulo. O procedimento
    consolidado nesta função envolve:

        1. Criação de um diretório para armazenamento do 
        conteúdo do layer.

        2. Estruturação e coleta das dependências a serem
        inclusas no layer.

        3. Transformação do diretório em .zip e realização
        do upload do conteúdo zipado em um bucket s3 para
        posterior leitura diretamente pelo lambda.

    Parâmetros
    ----------
    :param path:
        Caminho no sistema operacional com o diretório alvo
        para alocação do layer a ser zipado. Para auxiliar o
        usuário, uma lógica de verificação foi adicionada na
        função para validar se o último diretório contém
        os requisitos citados acima na documentação. Caso
        o diretório passado não contenha as pastas exigidas,
        o script nesta função adiciona o elemento faltante. 
        Caso o diretório exigido já esteja contemplado neste
        parâmetro, nenhuma ação é realizada.
        [type: string]

    :param bucket_name:
        Nome do bucket alvo do upload do arquivo zipado.
        [type: string]

    :param prefix:
        Diretório do bucket para organização do layer gerado.
        [type: string]

    :param runtime_folder:
        Este parâmetro contempla a informação do diretório
        exigido dentro das propostas da linguagem python de
        criação de layers para funções lambda. Por padrão,
        foi escolhida a opção mais simples e intuitiva 
        ("python"), porém nada impede do usuário passar
        seu próprio parâmetro, desde que este esteja
        adequado aos requisitos aceitos dentro das boas
        práticas de construção de layers lambda.
        [type: string, default='python']

    :param type_get_package:
        Tipo de abordagem para a coleta de dependências do layer.
        Opções possíveis: "venv" ou "manual".
        Detalhes fornecidos na documentação acima.
        [type: string, default='venv']

    Argumentos Adicionais
    ---------------------
    :kwarg requirements_path:
        Referência do arquivo de dependências "requirements" com a 
        lista de pacotes a ser instalada de forma direcionada no
        diretório alvo do layer. Caso type="venv", um arquivo
        "requirements_tmp.txt" é criado temporariamente para servir
        de insumo para instalação das dependências do venv. Caso
        type="manual", é feita uma verificação da existência do
        arquivo no diretório fornecido e, caso este argumento não
        seja preenchido externamente na chamada da função, é 
        considerado um arquivo de nome "requirements.txt" na raíz
        do projeto.
        [type: string, default=os.path.join(os.getcwd(), 'requirements.txt')]
    """

    # Coletando argumentos adicionais
    packages_list = kwargs['packages_list'] if 'packages_list' in kwargs else None
    user_input = bool(kwargs['user_input']) if 'user_input' in kwargs else False 

    # Coletando e baixando dependências no diretório alvo
    download_packages(
        target_path=target_path,
        packages_from=packages_from,
        packages_list=packages_list,
        user_input=user_input
    )

    # Zipando layer e subindo pra bucket s3
    upload_layer_to_bucket(
        target_path=target_path,
        bucket_name=bucket_name,
        key=key
    )

    