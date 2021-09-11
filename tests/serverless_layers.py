"""
---------------------------------------------------
------------ TESTS: serverless_layers -------------
---------------------------------------------------
Testes relacionados às funcionalidades do módulo
serverless.py da classe cloudgeass, mais especificamente
nas interações de criação de layers a serem utilizados
como recursos das funções lambda na AWS. Entre as
features testadas, encontram-se a criação de toda
a estrutura de um layer a partir das dependências
python fornecidas por um usuário, ou mesmo extraindo
essa informação diretamente do ambiente virtual de
trabalho, permitindo assim toda a construção do 
arquivo zipado de pacotes. Eventualmente, este arquivo
pode ser subido para o s3 através da classe JimmyBuckets

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Gerenciando layers de funções lambda
    2.1 Testando funções individualmente
    2.2 Função única de criação de layer
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 02/09/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Módulos internos cloudgeass
from cloudgeass.aws.serverless import *

# Bibliotecas padrão
import os
import shutil

# Logging
import logging
from cloudgeass.utils.log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Variáveis de configuração s3 da AWS
REGION = 'sa-east-1'
BUCKET_NAME = 'cloudgeass'
LAYER_KEY = 'layers/serverless/python.zip'

# Variáveis de configuração dos layers
PROJECT_PATH = os.getcwd()
LAYER_ROOT_PATH = 'lambda_layers'
LAYER_NAME = 'test_layer'
RUNTIME_FOLDER = 'python'
TARGET_PATH = os.path.join(LAYER_ROOT_PATH, LAYER_NAME, RUNTIME_FOLDER)

# Eliminando diretório tmp
if os.path.isdir(LAYER_ROOT_PATH):
    shutil.rmtree(path=LAYER_ROOT_PATH)


"""
---------------------------------------------------
----- 2. GERENCIANDO LAYERS DE FUNÇÕES LAMBDA -----
      2.1 Testando funções individualmente
---------------------------------------------------
"""

# Banner
banner = """
_____            _____                                          ______                   
__  /______________  /_   ______________________   ________________  /___________________
_  __/  _ \_  ___/  __/   __  ___/  _ \_  ___/_ | / /  _ \_  ___/_  /_  _ \_  ___/_  ___/
/ /_ /  __/(__  )/ /_     _(__  )/  __/  /   __ |/ //  __/  /   _  / /  __/(__  )_(__  ) 
\__/ \___//____/ \__/     /____/ \___//_/    _____/ \___//_/    /_/  \___//____/ /____/                                                                           

Testando funcionalidades do pacote cloudgeass
"""
# Banner gerado pelo site: https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=NBAflow

# Iniciando programa
print(banner)

# Diretório de dependências do layer
create_layer_path(
    layers_root_path=LAYER_ROOT_PATH,
    layer_name=LAYER_NAME,
    runtime_folder=RUNTIME_FOLDER
)

# Realizando o download das dependências
download_packages(
    target_path=TARGET_PATH,
    packages_from='list',
    packages_list=['pandas', 'numpy', 'requests']
)

# Realizando upload de layer no s3
upload_layer_to_bucket(
    target_path=TARGET_PATH, 
    bucket_name=BUCKET_NAME, 
    key=LAYER_KEY
)


"""
---------------------------------------------------
----- 2. GERENCIANDO LAYERS DE FUNÇÕES LAMBDA -----
      2.1 Função única de criação de layer
---------------------------------------------------
"""

# Eliminando diretório criado
shutil.rmtree(LAYER_ROOT_PATH)

# Criando layer
build_lambda_layer(
    target_path=TARGET_PATH,
    bucket_name=BUCKET_NAME,
    key=LAYER_KEY,
    packages_from='list',
    packages_list=['pandas', 'numpy', 'requests']
)
