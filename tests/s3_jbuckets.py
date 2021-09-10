"""
---------------------------------------------------
--------------- TESTS: s3_jbuckets ----------------
---------------------------------------------------
Testes relacionados às funcionalidades da classe
JimmyBuckets presente no módulo s3.py do cloudgeass.
Entre as features a serem testadas, encontram-se
a criação e eliminação de buckets, upload e 
leitura de objetos em buckets e, por fim, o upload
e download de diretórios inteiros com a manutenção
da estrutura local de diretórios a partir de prefixos
e folders criados no bucket.

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Gerenciando buckets e objetos
    2.1 Criando e configurando bucket
    2.2 Realizando upload de objetos
    2.3 Realizando o download de objetos
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 01/09/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Módulos internos cloudgeass
from cloudgeass.aws.s3 import JimmyBuckets

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

# Variáveis de configuração AWS
REGION = 'sa-east-1'
BUCKET_NAME = 'cloudgeass'

# Variáveis de diretório
PROJECT_PATH = os.getcwd()
MODULES_PATH = os.path.join(PROJECT_PATH, 'cloudgeass\\aws')
MODULES_PREFIX = 'cloudgeass/aws/'
TXT_FILENAME = 'requirements_dev.txt'
TMP_PATH = os.path.join(PROJECT_PATH, 'tmp')

# Eliminando diretório tmp
if os.path.isdir(TMP_PATH):
    shutil.rmtree(path=TMP_PATH)


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
        2.1 Criando e configurando bucket
---------------------------------------------------
"""

# Banner
banner = """
_____               _____                ________
__  /______ __________  /_       __________|__  /
_  __/_  _ \__  ___/_  __/       __  ___/___/_ < 
/ /_  /  __/_(__  ) / /_         _(__  ) ____/ / 
\__/  \___/ /____/  \__/         /____/  /____/                                                                             

Testando funcionalidades do pacote cloudgeass
"""
# Banner gerado pelo site: https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=NBAflow

# Iniciando programa
print(banner)

logger.debug(f'Instanciando classe JimmyBuckets e configurando ambiente s3')
jbuckets = JimmyBuckets(region=REGION)

# Coletando buckets existentes e aplicando drop + create
account_buckets = jbuckets.list_buckets()
if BUCKET_NAME in account_buckets:
    jbuckets.delete_bucket(bucket_name=BUCKET_NAME, empty_bucket=True)
jbuckets.create_bucket(bucket_name=BUCKET_NAME)


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
        2.2 Realizando o upload de objetos
---------------------------------------------------
"""

# Realizando o upload de arquivo de texto
jbuckets.upload_object(
    file=os.path.join(PROJECT_PATH, TXT_FILENAME),
    bucket_name=BUCKET_NAME,
    key=TXT_FILENAME
)

# Validando funcionalidade
objs_f1 = jbuckets.list_bucket_objects(bucket_name=BUCKET_NAME)
assert len(objs_f1) == 1, f'Bucket {BUCKET_NAME} recém criado possui mais de um objeto em apenas uma solicitação de upload'
assert objs_f1[0] == TXT_FILENAME, f'Objeto presente no bucket {BUCKET_NAME} ({objs_f1[0]}) não é equivalente ao arquivo solicitado ({TXT_FILENAME})'

# Realizando upload individual de múltiplos arquivos em um diretório
logger.debug(f'Iniciando upload individual de arquivos presentes no diretório {MODULES_PATH}')
files = [f for f in os.listdir(MODULES_PATH) if f != '__pycache__']
for file in files:
    jbuckets.upload_object(
        file=os.path.join(MODULES_PATH, file),
        bucket_name=BUCKET_NAME,
        key=MODULES_PREFIX + file ,
        verbose=False
    )

# Validando funcionalidade
objs_f2 = jbuckets.list_bucket_objects(bucket_name=BUCKET_NAME)
assert len(files) + len(objs_f1) == len(objs_f2), f'Quantidade de objetos no bucket ({len(files) + len(objs_f1)}) é diferente do esperado ({len(objs_f2)})'

# Realizando o upload de todos os arquivos em um diretório raíz
dir_files = [f for f in os.listdir(PROJECT_PATH) if '.' in f]
jbuckets.upload_directory(
    directory=PROJECT_PATH,
    bucket_name=BUCKET_NAME
)

# Validando funcionalidade
total_objects = len([name for _, _, files in os.walk(PROJECT_PATH) for name in files])
objs_f3 = jbuckets.list_bucket_objects(bucket_name=BUCKET_NAME)
assert total_objects == len(objs_f3), f'Quantidade de objetos presentes no bucket ({len(objs_f3)}) não equivale ao número esperado ({total_objects})'


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
       2.3 Realizando o download de objetos
---------------------------------------------------
"""

# Baixando todos os objetos de um bucket, incluindo sua estrutura
jbuckets.download_all_objects(
    bucket_name=BUCKET_NAME,
    prefix='',
    local_dir=TMP_PATH,
    verbose=True
)

# Validando funcionalidade
downloaded_files = len([name for _, _, files in os.walk(TMP_PATH) for name in files])
assert len(objs_f3) == downloaded_files, f'Quantidade de arquivos baixados do bucket {downloaded_files}, não equivale ao número esperado ({len(objs_f3)})'
