"""
SCRIPT: conftest.py

CONTEXTO:
---------
Arquivo de conferência/configuração do pytest para
alocação de fixtures e outros elementos e insumos
utilizados durante a execução dos testes.
---------------------------------------------------
"""

# Importando bibliotecas
import pytest
import boto3
from moto import mock_s3, mock_secretsmanager

from cloudgeass.aws.s3 import list_buckets, bucket_objects_report,\
    all_buckets_objects_report, read_s3_object

from tests.configs.inputs import MOCKED_REGION, MOCKED_BUCKET_CONTENT,\
    EXAMPLE_BUCKET, MOCKED_SECRET_NAME, MOCKED_SECRET_VALUE


"""---------------------------------------------------
-------- 1. DEFINIÇÃO DE FIXTURES DE MÓDULOS ---------
         1.1 Fixtures gerais e de preparação
---------------------------------------------------"""


# Definindo resource s3 para operações de mock
@pytest.fixture()
def s3_resource():
    with mock_s3():
        resource = boto3.resource("s3", region_name=MOCKED_REGION)
        return resource


# Definindo client s3 para operações de mock
@pytest.fixture()
def s3_client():
    with mock_s3():
        client = boto3.client("s3", region_name=MOCKED_REGION)
        return client


# Definindo client do secrets manager para operações de mock
@pytest.fixture()
def sm_client():
    with mock_secretsmanager():
        client = boto3.client("secretsmanager", region_name=MOCKED_REGION)
        return client


# Retornando função como fixture para preparação de bucket mockado
@pytest.fixture()
def prepare_mocked_bucket(s3_resource, s3_client):
    def create_elements():
        # Iterando por dicionário de definição de mock no s3
        for bucket_name, content_definition in MOCKED_BUCKET_CONTENT.items():
            # Criando bucket s3 definido no dicionário
            s3_resource.create_bucket(Bucket=bucket_name)

            # Iterando por definição de conteúdo para upload de objetos
            for _, content in content_definition.items():
                s3_client.put_object(
                    Bucket=bucket_name,
                    Body=content["Body"],
                    Key=content["Key"]
                )

    return create_elements


# Retornando função como fixture para preparação de segredos mockados
@pytest.fixture()
def prepare_mocked_secrets(sm_client):
    def create_secret():
        # Criando novo segredo
        sm_client.create_secret(
            Name=MOCKED_SECRET_NAME,
            SecretString=MOCKED_SECRET_VALUE
        )

    return create_secret


"""---------------------------------------------------
-------- 1. DEFINIÇÃO DE FIXTURES DE MÓDULOS ---------
       1.2 Funcionalidades do módulo test_s3.py
---------------------------------------------------"""


# Lista resultante da função list_buckets()
@pytest.fixture()
@mock_s3
def bucket_list(s3_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando lista de buckets mockados no ambiente
    return list_buckets(client=s3_client)


# DataFrame resultante da função bucket_objects_report()
@pytest.fixture()
@mock_s3
def df_objects_report(s3_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando DataFrame com report de objetos
    return bucket_objects_report(
        bucket_name=EXAMPLE_BUCKET, client=s3_client
    )


# DataFrame resultante da função all_buckets_objects_report()
@pytest.fixture()
@mock_s3
def df_all_buckets_objects(s3_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando DataFrame com report de objetos de todos os buckets
    return all_buckets_objects_report(client=s3_client)


# DataFrame resultante de leitura de objeto CSV via read_s3_object()
@pytest.fixture()
@mock_s3
def df_csv_from_s3(prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Formato de objeto
    file_ext = "csv"

    # Extraindo URI para leitura de objeto CSV
    bucket_name = "cloudgeass-mock-bucket-04"
    object_key = f"{file_ext}/anomesdia=20230117/file.{file_ext}"
    s3_uri = f"s3://{bucket_name}/{object_key}"

    # Gerando DataFrame com base em dados mockados no s3
    return read_s3_object(s3_uri=s3_uri)


# DataFrame resultante de leitura de objeto JSON via read_s3_object()
@pytest.fixture()
@mock_s3
def df_json_from_s3(prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Formato de objeto
    file_ext = "json"

    # Extraindo URI para leitura de objeto JSON
    bucket_name = "cloudgeass-mock-bucket-04"
    object_key = f"{file_ext}/anomesdia=20230117/file.{file_ext}"
    s3_uri = f"s3://{bucket_name}/{object_key}"

    # Gerando DataFrame com base em dados mockados no s3
    return read_s3_object(s3_uri=s3_uri)


# DataFrame resultante de leitura de objeto PARQUET via read_s3_object()
@pytest.fixture()
@mock_s3
def df_parquet_from_s3(prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Formato de objeto
    file_ext = "parquet"

    # Extraindo URI para leitura de objeto JSON
    bucket_name = "cloudgeass-mock-bucket-04"
    object_key = f"{file_ext}/anomesdia=20230117/file.{file_ext}"
    s3_uri = f"s3://{bucket_name}/{object_key}"

    # Gerando DataFrame com base em dados mockados no s3
    return read_s3_object(s3_uri=s3_uri)
