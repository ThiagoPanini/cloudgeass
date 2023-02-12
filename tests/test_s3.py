"""
SCRIPT: test_s3.py

OBJETIVO:
---------
Consolidar uma suíte de testes capaz de testar e validar
funcionalidades presentes no módulo s3 do cloudgeass.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
import pytest
from moto import mock_s3

from pandas import DataFrame

from cloudgeass.aws.s3 import bucket_objects_report,\
    all_buckets_objects_report, read_s3_object

from tests.configs.inputs import MOCKED_BUCKET_CONTENT,\
    NON_EMPTY_BUCKETS, EXPECTED_DF_OBJECTS_REPORT_COLS


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
               2.1 Função list_buckets()
---------------------------------------------------"""


@pytest.mark.list_buckets
@mock_s3
def test_funcao_list_buckets_retorna_uma_lista(bucket_list):
    """
    G: dado que o usuário deseja obter uma lista de buckets em sua conta
    W: quando o método list_buckets() de cloudgeass.aws.s3 for executado
    T: então o elemento resultante deve ser um objeto do tipo lista
    """
    assert type(bucket_list) is list


@pytest.mark.list_buckets
@mock_s3
def test_funcao_list_buckets_retorna_o_bucket_esperado(bucket_list):
    """
    G: dado que o usuário deseja obter uma lista de buckets em sua conta
    W: quando o método list_buckets() de cloudgeass.aws.s3 for executado
       na ciência da existência de uma lista de buckets definidos
    T: então a lista resultante deve conter os buckets esperados
    """
    assert bucket_list == list(MOCKED_BUCKET_CONTENT.keys())


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
          2.2 Função bucket_objects_report()
---------------------------------------------------"""


@pytest.mark.bucket_objects_report
@mock_s3
def test_funcao_bucket_objects_report_gera_dataframe_pandas(
    df_objects_report
):
    """
    G: dado que o usuário deseja extrair um report de objetos em um bucket
    W: quando o método bucket_objects_report() for executado com qualquer
       configuração de parâmetros
    T: então um objeto do tipo DataFrame do pandas deve ser retornado
    """
    assert type(df_objects_report) is DataFrame


@pytest.mark.bucket_objects_report
@mock_s3
def test_funcao_bucket_objects_report_possui_atributos_esperados(
    df_objects_report
):
    """
    G: dado que o usuário deseja extrair um report de objetos em um bucket
    W: quando o método bucket_objects_report() for executado com qualquer
       configuração de parâmetros
    T: então a lista de atributos do DataFrame resultante precisa ser igual
       a uma lista esperada de atributos
    """
    assert list(df_objects_report.columns) == EXPECTED_DF_OBJECTS_REPORT_COLS


@pytest.mark.bucket_objects_report
@mock_s3
def test_funcao_bucket_objects_report_possui_apenas_um_nome_de_bucket(
    df_objects_report
):
    """
    G: dado que o usuário deseja extrair um report de objetos em um bucket
    W: quando o método bucket_objects_report() for executado com qualquer
       configuração de parâmetros
    T: então deve haver apenas um único valor distinto para o atributo
       "BucketName" do DataFrame resultante
    """
    assert len(set(list(df_objects_report["BucketName"].values))) == 1


@pytest.mark.bucket_objects_report
@mock_s3
def test_erro_ao_tentar_gerar_report_de_objetos_com_nome_de_bucket_incorreto(
    mocked_client, prepare_mocked_bucket
):
    """
    G: dado que o usuário deseja extrair um report de objetos em um bucket
    W: quando o método bucket_objects_report() for executado com um nome
       de bucket inexistente na conta alvo
    T: então uma exceção genérica deve ser lançada
    """

    # Preparando ambiente mockado
    prepare_mocked_bucket()

    # Modificando nome de bucket para simulação de erro
    incorrect_bucket_name = "cloudgeass-non-existent-bucket"

    # Chamando função simulando bucket inexistente na conta
    with pytest.raises(Exception):
        bucket_objects_report(
            bucket_name=incorrect_bucket_name,
            client=mocked_client
        )


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
        2.3 Função all_buckets_objects_report()
---------------------------------------------------"""


@pytest.mark.all_buckets_objects_report
@mock_s3
def test_funcao_all_buckets_objects_report_retorna_dataframe_do_pandas(
    df_all_buckets_objects
):
    """
    G: dado que o usuário deseja obter um report completo contendo todos
       os objetos de todos os buckets em sua conta
    W: quando o método all_buckets_objects_report() for executado
    T: então um objeto do tipo DataFrame do pandas deve ser retornado
    """
    assert type(df_all_buckets_objects) is DataFrame


@pytest.mark.all_buckets_objects_report
@mock_s3
def test_funcao_all_buckets_objects_report_retorna_atributos_esperados(
    df_all_buckets_objects
):
    """
    G: dado que o usuário deseja obter um report completo contendo todos
       os objetos de todos os buckets em sua conta
    W: quando o método all_buckets_objects_report() for executado
    T: então um conjunto esperado de atributos deve ser retornado
    """

    # Colunas retornadas no DataFrame resultante
    report_cols = list(df_all_buckets_objects.columns)

    assert report_cols == EXPECTED_DF_OBJECTS_REPORT_COLS


@pytest.mark.all_buckets_objects_report
@mock_s3
def test_funcao_all_buckets_objects_report_contem_lista_de_buckets_nao_vazios(
    df_all_buckets_objects
):
    """
    G: dado que o usuário deseja obter um report completo contendo todos
       os objetos de todos os buckets em sua conta
    W: quando o método all_buckets_objects_report() for executado
    T: então deve haver apenas uma lista esperada contendo buckets onde
       sabe-se previamente que os mesmos estão populados
    """

    # Extraindo lista de buckets não vazios retornados no DataFrame
    buckets = list(set(df_all_buckets_objects["BucketName"].values))

    assert len(buckets) == len(NON_EMPTY_BUCKETS)


@pytest.mark.all_buckets_objects_report
@mock_s3
def test_funcao_all_buckets_objects_report_possui_nomes_esperados_de_buckets(
    df_all_buckets_objects
):
    """
    G: dado que o usuário deseja obter um report completo contendo todos
       os objetos de todos os buckets em sua conta
    W: quando o método all_buckets_objects_report() for executado
    T: então os valores distintos do atributo "BucketName" do DataFrame
       resultante deve ser igual a lista de buckets não vazios esperada
    """

    # Extração de nome de bucket do DataFrame resultante
    bucket_names = list(set(df_all_buckets_objects["BucketName"].values))

    assert set(bucket_names) == set(NON_EMPTY_BUCKETS)


@pytest.mark.all_buckets_objects_report
@mock_s3
def test_funcao_all_buckets_objects_report_com_lista_de_buckets_ignorados(
    mocked_client, prepare_mocked_bucket
):
    """
    G: dado que o usuário deseja obter um report completo contendo todos
       os objetos de todos os buckets em sua conta
    W: quando o método all_buckets_objects_report() for executado com uma
       lista de buckets a serem ignorados pelo processo de extração
    T: então os elementos contidos na lista de buckets ignorados NÃO devem
       estar entre os buckets do DataFrame resultante
    """

    # Preparando ambiente
    prepare_mocked_bucket()

    # Estabelecendo um nome de bucket a ser ignorado
    buckets_to_exclude = NON_EMPTY_BUCKETS[0]

    # Extração de nome de bucket do DataFrame resultante
    df_all_buckets_objects = all_buckets_objects_report(
        client=mocked_client,
        exclude_buckets=buckets_to_exclude
    )

    # Coletando lista de buckets distintos resultantes da função
    bucket_names = list(set(df_all_buckets_objects["BucketName"].values))

    assert buckets_to_exclude not in bucket_names


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
              2.4 Função read_s3_object()
---------------------------------------------------"""


@pytest.mark.read_s3_object
@mock_s3
def test_funcao_read_s3_object_retorna_dataframe_ao_ler_objeto_csv(
    df_csv_from_s3
):
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente no formato CSV e transformá-lo em um DataFrame do
       pandas
    W: quando o método read_s3_object() for executado com uma URI do S3
       que indica a leitura de um objeto JSON de um bucket
    T: então o objeto resultante deve ser um DataFrame do pandas
    """
    assert type(df_csv_from_s3) is DataFrame


@pytest.mark.read_s3_object
@mock_s3
def test_funcao_read_s3_object_retorna_dataframe_ao_ler_objeto_json(
    df_json_from_s3
):
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente no formato JSON e transformá-lo em um DataFrame do
       pandas
    W: quando o método read_s3_object() for executado com uma URI do S3
       que indica a leitura de um objeto JSON de um bucket
    T: então o objeto resultante deve ser um DataFrame do pandas
    """
    assert type(df_json_from_s3) is DataFrame


@pytest.mark.read_s3_object
@mock_s3
def test_funcao_read_s3_object_retorna_dataframe_ao_ler_objeto_parquet(
    df_parquet_from_s3
):
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente no formato PARQUET e transformá-lo em um DataFrame do
       pandas
    W: quando o método read_s3_object() for executado com uma URI do S3
       que indica a leitura de um objeto PARQUET de um bucket
    T: então o objeto resultante deve ser um DataFrame do pandas
    """
    assert type(df_parquet_from_s3) is DataFrame


@pytest.mark.read_s3_object
@mock_s3
def test_funcao_read_s3_object_retora_none_ao_ler_arquivo_com_extensao_png():
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente em um foramto qualquer e transformá-lo em um DataFrame
       do pandas
    W: quando o método read_s3_object() for executado com uma URI do S3
       que indica a leitura de um objeto com uma extensão ainda não
       habilitada para transformação em DataFrame (ex: .png)
    T: então a função não deve retornar nada (None)
    """

    # Definindo URI de teste a ser lida
    file_uri = "s3://mocked-bucket/prefix/file.png"
    assert read_s3_object(file_uri) is None


@pytest.mark.read_s3_object
@mock_s3
def test_funcao_read_s3_object_retora_erro_com_uri_de_objeto_inexistente():
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente em um foramto qualquer e transformá-lo em um DataFrame
       do pandas
    W: quando o método read_s3_object() for executado com uma URI do S3
       que aponta para um objeto inexistente no bucket
    T: então uma exceção FileNotFoundError deve ser lançada
    """

    # Definindo URI de teste a ser lida
    error_uri = "s3://mocked-bucket/prefix/file.csv"

    # Validando lançamento da exceção
    with pytest.raises(FileNotFoundError):
        _ = read_s3_object(error_uri)
