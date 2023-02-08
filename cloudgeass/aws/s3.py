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

import boto3
import pandas as pd

from cloudgeass.utils.log import log_config
from cloudgeass.utils.prep import categorize_file_size


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = log_config(logger_name=__file__)

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
    Extraindo report de objetos presentes em um bucket S3.

    Função criada para retornar ao usuário um DataFrame do pandas com uma
    série de detalhes sobre os objetos armazenados em um bucket específico
    na AWS.

    Parâmetros
    ----------
    :param bucket_name:
        Nome do bucket alvo da extração.
        [type: str]

    :param prefix:
        Prefixo opcionalmente utilizado como filtro da extração.
        [type: str, default=""]

    :param client:
        Client S3 utilizado para chamada do método list_objects_v2()
        utilizado para obtenção dos objetos do bucket.
        [default=boto3.client("s3")]

    Retorno
    -------
    :return df_objects_report:
        DataFrame do pandas contendo informações relevantes sobre os
        objetos presentes no bucket alvo.
        [type: pd.DataFrame]
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

    # Aplicando função de categorização de tamanho de objeto ao DataFrame
    df["SizeFormatted"] = df["Size"].apply(lambda x: categorize_file_size(x))

    # Definindo e aplicando ordenação de colunas do DataFrame
    order_cols = ["BucketName", "Key", "ObjectType", "Size", "SizeFormatted",
                  "LastModified", "ETag", "StorageClass"]
    df_objects_report = df.loc[:, order_cols]

    return df_objects_report
