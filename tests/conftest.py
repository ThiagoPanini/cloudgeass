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
from moto import mock_s3
import boto3
import moto


# Definindo client s3 para operações de mock em us-east-1
@pytest.fixture()
def mocked_s3_resource():
    with mock_s3():
        return boto3.resource("s3", region_name="us-east-1")


@pytest.fixture()
def mocked_resource():
    moto_fake = moto.mock_s3()
    try:
        moto_fake.start()
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket="teste")
        yield conn
    finally:
        moto_fake.stop()
