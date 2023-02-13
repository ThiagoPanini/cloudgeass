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


# Lista buckets já existentes em uma conta AWS
def list_buckets(client=client):
    return [b["Name"] for b in client.list_buckets()["Buckets"]]


# Obtém pandas DataFrame com detalhes de conteúdo de um bucket
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


# Realiza a leitura de objetos como DataFrame do pandas
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


# Coleta valor de partição com base em um prefixo
def get_partition_value_from_prefix(
    prefix_uri: str,
    partition_mode: str = "name=value",
    date_partition_name: str = "anomesdia",
    date_partition_idx: int = -2
):
    """
    Coleta o valor da partição de data com base em um prefixo de objeto.

    Parâmetros
    ----------
    :param prefix_uri:
        Prefixo de URI de objeto no s3 alvo da extração.
        [type: str]

    :param partition_mode:
        Indica a forma como a partição de data está configurada no
        prefixo e é utilizado para guiar o modo de extraçãodo valor da
        partição com base no padrão fornecido. As opções são:

        - "name=value": indica que a partição de data está armazenada
          em um formato contendo o nome e o valor (ex: anomesdia=20230101)

        - "value": indica que a partição de data está armazenada em
          um formato contendo apenas seu valor (ex: 20230101)

        [type: str, default="name=value", allowed="name=value"|"value"]

    :param date_partition_name:
        Indica o nome da partição a ser procurada no prefixo.Este parâmetro
        é utilizado apenas quando partition_mode="name=value".
        [type: str, default="anomesdia"]

    :param date_partition_idx:
        Índice a partição a ser extraída do prefixo com referência posterior
        ao processo de split por barra (.split("/")). Este parâmetro é
        utilizado apenas quando partition_mode="value" e serve para
        endereçar possíveis casos onde existem múltiplas partições em
        uma tabela. Como exemplo, date_partition_idx=-2 indica que a
        informação de data será coletada a partir do último prefixo
        antes dos nomes dos arquivos (prefix.split("/")[-2]).

        Se a informação de partição de data a ser coletada não segue
        este padrão (se está em um nível anterior, por exemplo), o
        usuário deve fornecer diferentes valores para este parâmetro
        (ex: -3, -4).
        [type: int, default=-2]

    Retorno
    -------
    :return partition_value:
        Valor da partição extraída do prefixo de objeto como um inteiro.
        [type: int]
    """

    # Validando preenchimento de parâmetro partition_mode
    partition_mode_prep = partition_mode.lower().strip()
    if partition_mode_prep not in ["name=value", "value"]:
        raise ValueError("Parâmetro partition_mode inválido. Valores "
                         "permitidos: 'name=value', 'value'")

    if partition_mode_prep == "name=value":
        # Procurando índice de nome de partição de data
        partition_start_idx = prefix_uri.find(date_partition_name + "=")
        if partition_start_idx == -1:
            raise ValueError("Nome de partição informada "
                             f"({date_partition_name}) "
                             f"inexistente no prefixo de URI {prefix_uri}")

        # Extraindo prefixo contendo informação de partição de data
        partition_prefix = prefix_uri[partition_start_idx:].split("/")[0]

        # Extraindo informação de data de partição
        partition_value = int(partition_prefix.split("=")[-1])

    elif partition_mode_prep == "value":
        # Extraindo informação de data de partição com base em index
        partition_value = prefix_uri.split("/")[date_partition_idx]

        # Validando conversão para inteiro
        try:
            partition_value = int(partition_value)

        except ValueError as ve:
            logger.error(f"Erro ao tentar converter partição {partition_value}"
                         " para inteiro. Verifique se os parâmetros da fução "
                         "foram fornecidos de maneira adequada. Este tipo de "
                         "erro pode estar associado ao tentar extrair um valor"
                         " de partição com parâmetro partition_mode='value' "
                         "quando o modo de armazenamento da função é "
                         "'name=value'. Isto implica em tentar converter uma "
                         "string do tipo 'nomeparticao=valorparticao' em "
                         " inteiro, gerando assim a exceção.")
            raise ve

    return partition_value


# Coleta último valor de partição com base em múltiplos prefixos de tabela
def get_last_partition(
    bucket_name: str,
    table_prefix: str,
    partition_mode: str = "name=value",
    date_partition_name: str = "anomesdia",
    date_partition_idx: int = -2,
    client=client
):
    """
    Coleta da última partição de uma tabela no S3.

    Esta função pode ser parametrizada pelo usuário para extrair a última
    partição de data de uma tabela com base em um processo de obtenção
    dos valores de partição de múltiplos prefixos e uma consequente ordenação
    dos resultados.

    Como regra de construção, esta função consolida chamadas para outras
    funções do módulo na seguinte sequência:
        - bucket_objects_report() para obter report de objetos do bucket
        - get_partition_value_from_prefix() para obter valores de partição

    Os valores obtidos em get_partition_value_from_prefix(), para cada prefixo
    de objeto extraído em bucket_objects_report() são então armazenados em uma
    lista e ordenados. O valor resultante desta função é o último elemento
    da lista, considerando que este seja o inteiro mais recente considerando
    os formatos de data iguais a %Y%m%d (anomesdia) ou %Y%m (anomes).

    Parâmetros
    ----------
    :param bucket_name:
        Nome do bucket alvo do processo de extração de prefixos de objeto.
        [type: str]

    :param prefix:
        Parâmetro que indica a extração de objetos de um bucket com base
        apenas em um prefixo. Normalmente, este parâmetro pode ser fornecido
        como o nome da tabela armazenada dentro do bucket, permitindo que
        o valor de partição obtido seja referente apenas à tabela (prefixo)
        fornecido.
        [type: str]

    :param partition_mode:
        Indica a forma como a partição de data está configurada no
        prefixo e é utilizado para guiar o modo de extraçãodo valor da
        partição com base no padrão fornecido. As opções são:

        - "name=value": indica que a partição de data está armazenada
          em um formato contendo o nome e o valor (ex: anomesdia=20230101)

        - "value": indica que a partição de data está armazenada em
          um formato contendo apenas seu valor (ex: 20230101)

        [type: str, default="name=value", allowed="name=value"|"value"]

    :param date_partition_name:
        Indica o nome da partição a ser procurada no prefixo.Este parâmetro
        é utilizado apenas quando partition_mode="name=value".
        [type: str, default="anomesdia"]

    :param date_partition_idx:
        Índice a partição a ser extraída do prefixo com referência posterior
        ao processo de split por barra (.split("/")). Este parâmetro é
        utilizado apenas quando partition_mode="value" e serve para
        endereçar possíveis casos onde existem múltiplas partições em
        uma tabela. Como exemplo, date_partition_idx=-2 indica que a
        informação de data será coletada a partir do último prefixo
        antes dos nomes dos arquivos (prefix.split("/")[-2]).

        Se a informação de partição de data a ser coletada não segue
        este padrão (se está em um nível anterior, por exemplo), o
        usuário deve fornecer diferentes valores para este parâmetro
        (ex: -3, -4).
        [type: int, default=-2]

    Retorno
    -------
    :return last_partition:
        Último valor de partição extraído no processo.
        [type: int]
    """

    # Coletando DataFrame de objetos do buckes
    df_objects = bucket_objects_report(
        bucket_name=bucket_name,
        prefix=table_prefix,
        client=client
    )

    # Extraindo lista de prefixos de objetos
    objs_list = list(df_objects["Key"].values)

    # Iterando sobre cada um dos prefixos de objetos
    partition_values = []
    for obj_prefix in objs_list:
        # Extraindo valor de partição
        partition_value = get_partition_value_from_prefix(
            prefix_uri=obj_prefix,
            partition_mode=partition_mode,
            date_partition_name=date_partition_name,
            date_partition_idx=date_partition_idx
        )

        # Incrementando lista
        partition_values.append(partition_value)

    # Ordenando lista e retornando partição mais recente
    return sorted(partition_values)[-1]
