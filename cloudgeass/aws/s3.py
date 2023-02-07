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
import pandas as pd


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Instanciando client e recurso do s3 para uso nas funções
client = boto3.client("s3")
resource = boto3.resource("s3")


"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
       2.1 Definindo funcionalidades comuns
---------------------------------------------------
"""


# Listando buckets já existentes em uma conta AWS
def list_buckets(resource=resource):
    return [b.name for b in resource.buckets.all()]


# Obtendo pandas DataFrame com detalhes de conteúdo de um bucket
def bucket_objects_report(
    bucket_name: str, prefix: str = "", client=client
):
    """
    """

    # Realizando chamada de API para listagem de objetos de bucket
    try:
        r = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )

    except Exception as e:
        logger.error("Erro ao realizar chamada client.list_objects_v2() "
                     f"com Bucket={bucket_name} e Prefix={prefix}. "
                     f"Exception: {e}")
        raise e

    # Transformando resultado da chamada em DataFrame do pandas
    df = pd.DataFrame(r["Contents"])

    # Adicionando nome do bucket e extraindo extensão do objeto
    df["BucketName"] = bucket_name
    df["ObjectType"] = df["Key"].apply(lambda x: x.split(".")[-1])

    # Definindo função para categorização de volume do objeto
    def categorize_file_size(size_in_bytes):
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 ** 2:
            size_in_kb = size_in_bytes / 1024
            return f"{size_in_kb:.2f} KB"
        elif size_in_bytes < 1024 ** 3:
            size_in_mb = size_in_bytes / (1024 ** 2)
            return f"{size_in_mb:.2f} MB"
        elif size_in_bytes < 1024 ** 4:
            size_in_gb = size_in_bytes / (1024 ** 3)
            return f"{size_in_gb:.2f} GB"
        else:
            size_in_tb = size_in_bytes / (1024 ** 4)
            return f"{size_in_tb:.2f} TB"

    # Aplicando função ao DataFrame
    df["SizeFormatted"] = df["Size"].apply(lambda x: categorize_file_size(x))

    # Definindo e aplicando ordenação de colunas do DataFrame
    order_cols = ["BucketName", "Key", "ObjectType", "Size", "SizeFormatted", 
                  "LastModified", "ETag", "StorageClass"]
    df_ordered = df.loc[:, order_cols]

    return df_ordered
