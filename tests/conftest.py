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
from moto import mock_s3

from cloudgeass.aws.s3 import list_buckets, bucket_objects_report,\
    all_buckets_objects_report, pandas_df_from_csv

from tests.configs.inputs import MOCKED_REGION, MOCKED_BUCKET_CONTENT,\
    MOCKED_BUCKET_NAME


# Definindo resource s3 para operações de mock
@pytest.fixture()
def mocked_resource():
    with mock_s3():
        resource = boto3.resource("s3", region_name=MOCKED_REGION)
        return resource


# Definindo client s3 para operações de mock
@pytest.fixture()
def mocked_client():
    with mock_s3():
        client = boto3.client("s3", region_name=MOCKED_REGION)
        return client


# Retornando função como fixture para preparação de bucket mockado
@pytest.fixture()
def prepare_mocked_bucket(mocked_resource, mocked_client):
    def create_elements():
        # Iterando por dicionário de definição de mock no s3
        for bucket_name, content_definition in MOCKED_BUCKET_CONTENT.items():
            # Criando bucket s3 definido no dicionário
            mocked_resource.create_bucket(Bucket=bucket_name)

            # Iterando por definição de conteúdo para upload de objetos
            for _, content in content_definition.items():
                mocked_client.put_object(
                    Bucket=bucket_name,
                    Body=content["Body"],
                    Key=content["Key"]
                )

    return create_elements


"""---------------------------------------------------
-------- 2. DEFINIÇÃO DE FIXTURES DE MÓDULOS ---------
       2.1 Funcionalidades do módulo test_s3.py
---------------------------------------------------"""


# Lista resultante da função list_buckets()
@pytest.fixture()
@mock_s3
def bucket_list(mocked_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando lista de buckets mockados no ambiente
    return list_buckets(client=mocked_client)


# DataFrame resultante da função bucket_objects_report()
@pytest.fixture()
@mock_s3
def df_objects_report(mocked_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando DataFrame com report de objetos
    return bucket_objects_report(
        bucket_name=MOCKED_BUCKET_NAME, client=mocked_client
    )


# DataFrame resultante da função all_buckets_objects_report()
@pytest.fixture()
@mock_s3
def df_all_buckets_objects(mocked_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Gerando DataFrame com report de objetos de todos os buckets
    return all_buckets_objects_report(client=mocked_client)


# DataFrame resultante da função csv_object_to_df()
@pytest.fixture()
@mock_s3
def df_from_csv_object(mocked_client, prepare_mocked_bucket):
    # Preparando ambiente mockado no s3
    prepare_mocked_bucket()

    # Extraindo parâmetros para referência de objeto mockado
    bucket_name = MOCKED_BUCKET_NAME
    object_key = MOCKED_BUCKET_CONTENT[MOCKED_BUCKET_NAME]["file-001"]["Key"]

    # Gerando DataFrame com base em dados mockados no s3
    return pandas_df_from_csv(
        bucket_name=bucket_name,
        object_key=object_key,
        client=mocked_client
    )
