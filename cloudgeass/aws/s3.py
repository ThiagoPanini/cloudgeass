"""
Módulo responsável por alocar desenvolvimentos relacionados à utilização do
boto3 para o gerencimento de operações do S3 na AWS. Aqui será possível
encontrar funcionalidades prontas para realizar as mais variadas atividades
no S3.

Ao longo deste módulo, será possível encontrar funções definidas e documentadas
visando proporcionar a melhor experiência ao usuário!

___
"""

# Importando bibliotecas
import boto3
import pandas as pd
import os

from cloudgeass.utils.log import log_config
from cloudgeass.utils.prep import categorize_file_size


# Configurando objeto de logger
logger = log_config(logger_name=__file__)

# Instanciando client e recurso do s3 para uso nas funções
client = boto3.client("s3")


# Lista buckets já existentes em uma conta AWS
def list_buckets(client=client) -> list:
    """
    Retorna uma lista de nomes de buckets em uma conta AWS.

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import list_buckets

        # Listando buckets s3
        buckets = list_buckets()
        ```

    Args:
        client (botocore.client.S3): Client s3 instanciado via boto3

    Returns:
        Lista contendo nomes de buckets s3 existentes em uma conta
    """
    return [b["Name"] for b in client.list_buckets()["Buckets"]]


# Obtém pandas DataFrame com detalhes de conteúdo de um bucket
def bucket_objects_report(
    bucket_name: str, prefix: str = "", client=client
) -> pd.DataFrame:
    """
    Extração de report de objetos presentes em um bucket S3.

    Função criada para retornar ao usuário um DataFrame do pandas com uma
    série de detalhes sobre os objetos armazenados em um bucket específico
    na AWS.

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import bucket_objects_report

        # Obtendo report de objetos em um bucket
        df_bucket_objects = bucket_objects_report(
            bucket_name="some-bucket-name"
        )

        # Obtendo report de objetos apenas de uma "tabela"
        df_table_objects = bucket_objects_report (
            bucket_name="another-bucket-name",
            prefix="database/table"
        )
        ```

    Args:
        bucket_name (str): Nome do bucket alvo da análise de objetos
        prefix (str): Prefixo opcional para filtragem do report
        client (botocore.client.S3): Client s3 instanciado via boto3

    Returns:
        DataFrame pandas com informações sobre objetos extraídos
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
    prefix: str = "", exclude_buckets: list = list(), client=client
) -> pd.DataFrame:
    """
    Extração de report de objetos presentes em todos os buckets de uma conta.

    O conteúdo desta função envolve a chamada às funções list_buckets() e
    bucket_objects_report() deste mesmo módulo para, respectivamente,
    obter a lista de nomes de buckets da conta, iterar sobre a mesma e
    extrair um report de objetos de cada um dos buckets como um
    DataFrame do pandas. A cada interação, o DataFrame resultante é
    enriquecido com report individual de cada bucket.

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import all_buckets_objects_report

        # Obtendo report de objetos de todos os buckets da conta
        df_all_buckets_objects = all_buckets_objects_report()

        # Eliminando alguns buckets do report de objetos
        df_all_buckets_objects = bucket_objects_report (
            exclude_buckets=["some-bucket-name", "another-bucket-name"]
        )
        ```

    Args:
        prefix (str): Prefixo opcional para filtragem do report
        exclude_buckets (list): Lista de buckets ignorados no report
        client (botocore.client.S3): Client s3 instanciado via boto3

    Returns:
        DataFrame pandas com informações sobre objetos extraídos
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
def read_s3_object(s3_uri: str, **kwargs) -> pd.DataFrame:
    """
    Realiza a leitura de objeto no S3 com base em URI fornecida.

    Com esta função, o usuário poderá realizar a leitura de objetos
    no S3 com o output consolidado como um DataFrame do pandas. As
    regras estabelecidas na função visam identificar a extensão do
    objeto a partir da URI para que, dessa forma, o método correto
    de leitura e transformação em DataFrame possa ser chamado (ex:
    pd.read_csv(), pd.read_json()).

    Note: Sobre os argumentos de chave e valor:
        Argumentos adicionais de chave e valor (**kwargs) podem ser
        utilizados na chamada da função para parametrizar e
        configurar especifidades dos arquivos a serem lidos e
        transformados em DataFrames do pandas.

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import read_s3_object

        # Realizando a leitura de um objeto do tipo PARQUET
        parquet_uti = "s3://some-bucket-name/some-prefix/file.parquet"
        df_parquet = read_s3_object(s3_uri=parquet_uri)

        # Realizando a leitura de um objeto do tipo CSV
        csv_uri = "s3://some-bucket-name/some-prefix/file.csv"
        df_csv = read_s3_object(s3_uri=csv_uri, sep=";")

        # Realizando a leitura de um objeto do tipo JSON
        json_uri = "s3://some-bucket-name/some-prefix/file.json"
        df_json = read_s3_object(s3_uri=json_uri, orient="records")
        ```

    Args:
        s3_uri (str): URI do objeto no S3 a ser lido como im DataFrame pandas
        **kwargs (dict): parametrização das funções de leitura de DataFrame

    Returns:
        DataFrame do pandas contendo os dados do objeto lido do s3

    Raises:
        FileNotFoundError: Erro quando a URI aponta para um objeto inexistente
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
) -> int:
    """
    Coleta o valor da partição de data com base em um prefixo de objeto.

    Esta função foi criada para facilitar e modularizar a operação
    existente na função `get_last_partition()`, também deste módulo.
    Seu objetivo é considerar diferentes cenários para extração do
    valor de uma partição com base no seu formato de prefixo.

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import get_partition_value_from_prefix

        # Extraindo valor da partição com prefixo contendo nome e valor
        example_prefix = "table-name/anomesdia=20230101/file.parquet"
        partition_value = get_partition_value_from_prefix(
            prefix_uri=example_prefix,
            partition_mode="name=value",
            date_partition_name="anomesdia"
        )
        # Resultado: 20230101

        # Extraindo valor da partição com prefixo contendo apenas valor
        another_prefix = "table-name/20230102/file.parquet"
        partition_value = get_partition_value_from_prefix(
            prefix_uri=example_prefix,
            partition_mode="value",
            date_partition_idx=-2
        )
        # Resultado: 20230102
        ```

    Args:
        prefix_uri (str):
            Prefixo de objeto no s3 extraído de tabela particionada

        partition_mode (str):
            Checar documentação da função
            [get_last_partition()][cloudgeass.aws.s3.get_last_partition]

        date_partition_name (str):
            Checar documentação da função
            [get_last_partition()][cloudgeass.aws.s3.get_last_partition]

        date_partition_idx (int):
            Checar documentação da função
            [get_last_partition()][cloudgeass.aws.s3.get_last_partition]

    Returns:
        Valor da partição extraída do prefixo de objeto como um inteiro

    Raises:
        ValueError: Ao tentar converter um valor de partição não\
        "parseável" em inteiro ou ao não encontrar o nome da partição\
        no prefix quando partition_mode="name=value"
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
        partition_value_raw = partition_prefix.split("=")[-1]

    elif partition_mode_prep == "value":
        # Extraindo informação de data de partição com base em index
        partition_value_raw = prefix_uri.split("/")[date_partition_idx]

    # Validando conversão para inteiro
    try:
        partition_value = int(partition_value_raw)

    except ValueError as ve:
        logger.error(f"Erro ao tentar converter partição {partition_value_raw}"
                     " para inteiro. Verifique se os parâmetros da fução "
                     "foram fornecidos de maneira adequada. Este tipo de "
                     "erro pode estar associado ao tentar extrair um valor "
                     "de partição com parâmetro partition_mode='value' "
                     "quando o modo de armazenamento da função é "
                     "'name=value'. Isto implica em tentar converter uma "
                     "string do tipo 'nomeparticao=valorparticao' em "
                     "inteiro, gerando assim a exceção.")
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
) -> int:
    """
    Coleta da última partição de uma tabela no S3.

    Esta função pode ser parametrizada pelo usuário para extrair a última
    partição de data de uma tabela com base em um processo de obtenção
    dos valores de partição de múltiplos prefixos e uma consequente ordenação
    dos resultados.

    Note: Observação sobre a funcionalidade consolidada:
        Como regra de construção, esta função consolida chamadas para outras
        funções do módulo na seguinte sequência:

        - `bucket_objects_report()` para obter report de objetos do bucket
        - `get_partition_value_from_prefix()` p/ obter valores de partição

        Cada prefixo objeto extraído em `bucket_objects_report()`, passa pelo
        processo de extração de valor de partição em consolidado em
        `get_partition_value_from_prefix()`. Os resultados são armazenados em
        uma lista e ordenados. O valor resultante desta função é o último
        elemento da lista, considerando que este seja o inteiro mais recente
        considerando os formatos de data iguais a %Y%m%d (anomesdia) ou
        %Y%m (anomes).

    Examples:
        ```python
        # Importando função
        from cloudgeass.aws.s3 import get_last_partition

        # Coletando última partição de tabela particionada
        last_partition = get_last_partition(
            bucket_name="some-bucket-name",
            table_prefix"some-table-prefix",
            partition_mode="name=value",
            date_partition_name="anomesdia"
        )
        ```

    Args:
        bucket_name (str):
            Nome do bucket onde a tabela particionada se encontra

        table_prefix (str):
            Prefixo de localização da tabela no bucket. Normalmente, este
            prefixo pode ser indicado simplesmente como o nome da tabela.
            Entretanto, existem cenários onde a tabela particionada encontra-se
            em uma série de outros prefixos dentro do mesmo bucket
            (ex: database/table) e, nesses casos, table_prefix deve indicar
            todo o caminho exatamente anterior ao início dos prefixos de
            partição

        partition_mode (str):
            Indica a forma como a partição de data está configurada no
            prefixo e é utilizado para guiar o modo de extraçãodo valor da
            partição com base no padrão fornecido. As opções são:

            - "name=value": indica que a partição de data está armazenada
            em um formato contendo o nome e o valor (ex: anomesdia=20230101)

            - "value": indica que a partição de data está armazenada em
            um formato contendo apenas seu valor (ex: 20230101)

        date_partition_name (str):
            Nome da partição a ser procurada no prefixo. Este parâmetro é
            utilizado apenas quando partition_mode="name=value"

        date_partition_idx (int):
            Indica o índice de localização do valor da partição com
            referência posterior ao processo de split por barra do
            prefixo alvo (prefix_uri.split("/")). Este parâmetro é
            utilizado apenas quando partition_mode="value"

        client (botocore.client.S3):
            Client s3 instanciado via boto3

    Returns:
        Último valor de partição extraído no processo.
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
