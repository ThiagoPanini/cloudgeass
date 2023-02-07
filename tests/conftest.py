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


# Definindo client s3 para operações de mock em us-east-1
@pytest.fixture()
def mocked_s3_resource():
    with mock_s3():
        resource = boto3.resource("s3", region_name="us-east-1")
        return resource
