"""Consolidação de testes unitários do módulo secrets.py

Neste arquivo, serão consolidados testes unitários
utilizados para validar as funcionalidades presentes na
classe GlueJobManager, visando garantir que todos os insumos
essenciais para execução de jobs do Glue na AWS estejam
sendo entregues com eficiência ao usuário.

___
"""

# Importando bibliotecas
import pytest
from moto import mock_secretsmanager

from cloudgeass.aws.secrets import get_secret_string

from tests.configs.inputs import MOCKED_SECRET_NAME, MOCKED_SECRET_VALUE


"""---------------------------------------------------
------------ 1. DEFININDO SUÍTE DE TESTES ------------
            1.1 Função get_secret_string()
---------------------------------------------------"""


@pytest.mark.get_secret_string
@mock_secretsmanager
def test_coleta_esperada_de_string_de_segredo(
    sm_client, prepare_mocked_secrets
):
    """
    G: dado que o usuário deseja coletar um segredo do Secrets Manager
    W: quando o método get_secret_string() for executado passando um ID
       esperado de segredo cujo valor é conhecido
    T: então o valor esperado deve ser retornado pela função
    """

    # Preparando ambiente mockado
    prepare_mocked_secrets()

    # Coletando segredo
    secret = get_secret_string(secret_id=MOCKED_SECRET_NAME, client=sm_client)

    assert secret == MOCKED_SECRET_VALUE
