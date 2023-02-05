"""
MÓDULO: s3.py

OBJETIVO:
---------
Módulo responsável por alocar desenvolvimentos relacionados à
utilização do boto3 para o gerencimento de operações do S3 na
AWS. Aqui será possível encontrar funcionalidades prontas para
realizar as mais variadas atividades no S3.
--------------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

import logging
from cloudgeass.utils.log import log_config

import boto3


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Instanciando client s3
try:
    logger.debug("Instanciando client e resorce s3 via cloudgeass")
    client = boto3.client("s3")
    resource = boto3.resource("s3")

except Exception as e:
    logger.error("Erro ao iniciar client e resource s3 utilizando "
                 f"boto3. Exception: {e}")
    raise e


"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
       2.1 Definindo funcionalidades comuns
---------------------------------------------------
"""


# Listando buckets já existentes em uma conta AWS
def list_buckets(resource=resource):
    return [b.name for b in resource.buckets.all()]
