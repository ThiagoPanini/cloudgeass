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
    all_buckets_objects_report

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
            2.4 Função read_csv_object()
---------------------------------------------------"""


@pytest.mark.read_csv_object
@mock_s3
def test_funcao_read_csv_object_retorna_objeto_do_tipo_dataframe(
    df_from_csv_object
):
    """
    G: dado que o usuário deseja realizar a leitura de um objeto no
       s3 presente no formato csv e transformá-lo em um DataFrame do
       pandas
    W: quando o método read_csv_object() for executado com a
       parametrização padrão
    T: então o objeto resultante deve ser um DataFrame do pandas
    """
    assert type(df_from_csv_object) is DataFrame
