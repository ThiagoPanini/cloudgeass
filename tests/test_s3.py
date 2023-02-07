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

from tests.configs.inputs import MOCKED_BUCKET_NAME

from pandas import DataFrame


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
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
       na ciência da existência de um bucket de nome específico
    T: então a lista resultante deve conter o bucket esperado
    """
    assert bucket_list[0] == MOCKED_BUCKET_NAME


@pytest.mark.bucket_objects_report
@mock_s3
def test_report_de_objetos_do_bucket_gera_dataframe_pandas(
    df_objects_report
):
    """
    G: dado que o usuário deseja extrair um report de objetos em um bucket
    W: quando o método bucket_objects_report() for executado com qualquer
       configuração de parâmetros
    T: então um objeto do tipo DataFrame do pandas deve ser retornado
    """
    assert type(df_objects_report) is DataFrame
