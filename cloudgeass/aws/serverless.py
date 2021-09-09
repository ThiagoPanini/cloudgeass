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
import pathlib

# Módulos auxiliares
from utils.log import log_config
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
PATH = os.path.join(os.getcwd(), 'lambda\\layer')
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
def create_layer_path(path, runtime_folder='python'):
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
    
    # Extraindo última parcela do diretório da camada
    if os.path.isdir(path):
        ref_folder = pathlib.PurePath(path).name
    else:
        ref_folder = os.path.basename(os.path.dirname(path))
    
    # Verificando diretório de leitura de camada no lambda
    if ref_folder != runtime_folder:
        path = os.path.join(path, runtime_folder)

    # Criando diretório
    try:
        os.makedirs(path)
        logger.info(f'Diretório de camada criado em {path}')
    except FileExistsError as fee:
        logger.warning(fee)

    return path

# Estruturando dependências do pacote
def get_packages(layer_path, type='venv', **kwargs):
    """
    Coleta e estruturação de pacotes python a serem inclusos no
    layer lambda a partir de dependências registradas manualmente
    ou contidas no ambiente virtual de trabalho. Esta função possui
    a grande vantagem de validar diferentes tipos de seleção de
    dependências para a instalação direcionada dos pacotes a partir
    do comando pip install -t apontando para o diretório do layer
    criado a partir da função create_lambda_layer().

    Existem duas abordagens de atuação para a coleta de dependências:
        * venv: onde a coleta de dependências é feita de forma
        automática considerando as bibliotecas instaladas no ambiente
        virtual de trabalho ativo no momento de execução desta função

        * manual: onde o usuário pode inserir manualmente, de forma 
        prévia, as dependências em um arquivo "requirements.txt" que,
        fornecido como argumento adicional dessa função, serve como
        insumo principal para a instalação direcionada dos pacotes

    Para ambos os casos, validações são realizadas nas primeiras
    etapas de execução da função como, por exemplo, a validação
    da existência de um arquivo de "requirements" válido quando
    é selecionada uma abordagem de atuação "manual". Por padrão,
    quando type="manual", a função considera que as dependências
    estarão alocadas em um arquivo chamado "requirements.txt" 
    localizado na pasta root do diretório de trabalho. Quando o
    usuário seleciona type="venv", um arquivo "requirements_tmp.txt"
    é criado de forma temporária para alocar o resultado do
    comando pip freeze. Ao final, o arquivo "requirements_tmp.txt"
    é excluído.

    Parâmetros
    ----------
    :param layer_path:
        Referência do diretório de alocação das dependências do
        layer a ser criado.
        [type: string]

    :param type:
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

    # Coletando argumentos adicionais e validando requirements
    requirements_path = kwargs['requirements_path'] if 'requirements_path' in kwargs else os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.splitext(requirements_path)[-1] != '.txt':
        logger.error(f'Caminho para requirements {requirements_path} inválido. Utilize um arquivo txt ou gere um via pip freeze')
        return
    elif (type=='manual' and not os.path.isfile(requirements_path)):
        logger.error(f'Arquivo {requirements_path} inexistente. Forneça um caminho válido ou gere um arquivo via pip freeze')
        return

    # Validando parâmetro de tipo de coleta
    if type not in ('venv', 'manual'):
        logger.error(f'Tipo de estruturação (type={type}) inválida. Por favor, selecione entre "manual" ou "venv". Programa encerrado')
        return

    # Coleta automática de pacotes extraindo do venv via pip freeze
    if type == 'venv':
        requirements_path = requirements_path if requirements_path in kwargs else os.path.join(os.getcwd(), 'requirements_tmp.txt')
        logger.debug(f'Coletando pacotes presentes no ambiente virtual ativo via pip freeze e sobrescrevendo arquivo {requirements_path}')
        os.system(f'pip freeze > {requirements_path}')

    # Instalando dependências utilizando arquivo requirements.txt já existente ou recém criado
    logger.debug(f'Realizando instalação direcionada via pip de dependências contidas em {requirements_path}\n')
    os.system(f'pip3 install -r {requirements_path} --no-user -t {layer_path}')
    print()
    logger.info(f'Pacotes contidos em {requirements_path} foram disponibilizados com sucesso em {layer_path}. Verifique se o resultado no prompt contém algum erro após a chamada do pip')

    # Eliminando arquivo de requirements em caso temporário
    if requirements_path == os.path.join(os.getcwd(), 'requirements_tmp.txt'):
        os.remove(requirements_path)

# Zipando e realizando upload do layer em bucket específico
def upload_layer_to_bucket(layer_path, bucket_name, prefix):
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
        shutil.make_archive(layer_path, format='zip', root_dir=layer_path)
        logger.info(f'Diretório de dependências {layer_path} zipado com sucesso')
    except Exception as e:
        logger.error(f'Erro ao zipar diretório de dependências {layer_path}. Exception: {e}')
        return

    # Instanciando classe JimmyBuckets para operações no s3
    jbuckets = JimmyBuckets(region=REGION)
    jbuckets.upload_object(
        file=layer_path + '.zip',
        bucket_name=bucket_name,
        key=prefix + 'python.zip'
    )

# Cria um layer e realiza o upload em um bucket s3
def build_lambda_layer(layer_path, bucket_name, prefix, runtime_folder='python',
                       type_get_package='venv', **kwargs):
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

    # Criando diretório do layer
    layer_path = create_layer_path(
        path=layer_path,
        runtime_folder=runtime_folder
    )

    # Coletando dependências
    requirements_path = kwargs['requirements_path'] if 'requirements_path' in kwargs else os.path.join(os.getcwd(), 'requirements.txt')
    get_packages(
        layer_path=layer_path,
        type=type_get_package,
        requirements_path=requirements_path
    )

    # Zipando layer e subindo pra bucket s3
    upload_layer_to_bucket(
        layer_path=layer_path,
        bucket_name=bucket_name,
        prefix=prefix
    )

    