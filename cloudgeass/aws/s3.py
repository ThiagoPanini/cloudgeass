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
import os

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


"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
       2.1 Definindo funcionalidades comuns
---------------------------------------------------
"""


# Listando buckets já existentes em uma conta AWS
def list_buckets(client=client):
    return [b["Name"] for b in client.list_buckets()["Buckets"]]


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
        para obtenção dos objetos do bucket.
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

    # Retornando conteúdo do bucket
    try:
        bucket_content = r["Contents"]

    except KeyError:
        logger.warning(f"Erro ao extrair conteúdo do bucket {bucket_name}. "
                       f"Provavelmente o bucket encontra-se sem objetos.")
        return None

    # Transformando resultado da chamada em DataFrame do pandas
    df = pd.DataFrame(bucket_content)

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


# Realizando a leitura de objetos como DataFrame do pandas
def all_buckets_objects_report(
    prefix: str = "", client=client, exclude_buckets=list()
):
    """
    Retorna um report de todos os objetos de todos os buckets da conta.

    O conteúdo desta função envolve a chamada às funções list_buckets() e
    bucket_objects_report() deste mesmo módulo para, respectivamente,
    obter a lista de nomes de buckets da conta, iterar sobre a mesma e
    extrair um report de objetos de cada um dos buckets como um
    DataFrame do pandas. A cada interação, o DataFrame resultante é
    enriquecido com report individual de cada bucket.

    :param prefix:
        Prefixo opcionalmente utilizado como filtro da extração.
        [type: str, default=""]

    :param client:
        Client S3 utilizado para chamada do método list_objects_v2()
        para obtenção dos objetos do bucket.
        [default=boto3.client("s3")]

    :param exclude_buckets:
        Lista de buckets a serem ignorados no processo de listagem
        de objetos. A cada iteração do laço, buckets presentes nesta
        lista não terão seus objetos adicionados ao report.
        [type: list, default=list()]

    Retorno
    -------
    :return df_report_all:
        DataFrame do pandas contendo informações relevantes sobre os
        objetos presentes em todos os buckets da conta.
        [type: pd.DataFrame]
    """

    # Listando buckets da conta
    all_buckets = list_buckets(client=client)

    # Criando lista definitiva após subtração de elementos no exclude_bucket
    buckets = [b for b in all_buckets if b not in exclude_buckets]

    # Criando DataFrame vazio e iterando sobre buckets para listagem de objs
    df_report = pd.DataFrame()
    for bucket in buckets:
        # Listando objetos do bucket
        df_bucket_report = bucket_objects_report(
            bucket_name=bucket,
            prefix=prefix,
            client=client
        )

        # Unindo ao DataFrame consolidado
        df_report = pd.concat([df_report, df_bucket_report])

    # Resetando index
    df_report.reset_index(drop=True, inplace=True)

    return df_report


# Lendo objeto do S3 com base em URI
def read_s3_object(s3_uri: str, **kwargs):
    """
    Realiza a leitura de objeto no S3 com base em URI fornecida.

    Com esta função, o usuário poderá realizar a leitura de objetos
    no S3 com o output consolidado como um DataFrame do pandas. As
    regras estabelecidas na função visam identificar a extensão do
    objeto a partir da URI para que, dessa forma, o método correto
    de leitura e transformação em DataFrame possa ser chamado (ex:
    pd.read_csv(), pd.read_json()).

    Parâmetros
    ----------
    :param s3_uri:
        URI do objeto no S3 a ser lido e transformado em DataFrame.
        Exemplo: "s3://bucket-name/prefix/object-name.csv"
        [type: str]

    **kwargs
    --------
    Os argumentos adicionais por chave servem para mapear todas as
    possibilidades de parametrização existentes nos métodos
    pd.read_csv(), pd.read_json() e pd.read_parquet().

    Retorno
    -------
    :return df:
        DataFrame do pandas contendo os dados do objeto lido do s3.
        [type: pd.DataFrame]
    """

    # Extraindo parâmetros da URI
    object_name = s3_uri.split("/")[-1]
    object_ext = os.path.splitext(object_name)[-1]

    try:
        # Chamando método específico de leitura com base na extensão
        if object_ext == ".csv":
            return pd.read_csv(s3_uri, **kwargs)
        elif object_ext == ".json":
            return pd.read_json(s3_uri, **kwargs)
        elif object_ext == ".parquet":
            return pd.read_parquet(s3_uri, **kwargs)
        else:
            logger.warning(f"Extensão {object_ext} ainda não habilitada "
                           "para leitura e transformação em DataFrame")
            return None

    except FileNotFoundError as fnfe:
        logger.error(f"Arquivo inexistente ({s3_uri})")
        raise fnfe
