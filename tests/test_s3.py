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
from moto import mock_s3
from cloudgeass.aws.s3 import list_buckets


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mock_s3
def test_funcao_list_buckets_retorna_uma_lista(mocked_s3_resource):
    """
    G: dado que o usuário deseja obter uma lista de buckets em sua conta
    W: quando o método list_buckets() de cloudgeass.aws.s3 for executado
    T: então o elemento resultante deve ser um objeto do tipo lista
    """

    # Criando bucket s3 com recurso mockado
    bucket_name = "cloudgeass-mocked-bucket"
    mocked_s3_resource.create_bucket(Bucket=bucket_name)

    # Executando método de listagem de buckets
    buckets = list_buckets(resource=mocked_s3_resource)

    assert type(buckets) is list


@mock_s3
def test_funcao_list_buckets_retorna_o_bucket_esperado(mocked_s3_resource):
    """
    G: dado que o usuário deseja obter uma lista de buckets em sua conta
    W: quando o método list_buckets() de cloudgeass.aws.s3 for executado
       na ciência da existência de um bucket de nome específico
    T: então a lista resultante deve conter o bucket esperado
    """

    # Criando bucket s3 com recurso mockado
    bucket_name = "cloudgeass-mocked-bucket"
    mocked_s3_resource.create_bucket(Bucket=bucket_name)

    # Executando método de listagem de buckets
    buckets = list_buckets(resource=mocked_s3_resource)

    assert buckets[0] == bucket_name
