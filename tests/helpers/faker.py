"""
SCRIPT: helpers/faker.py

CONTEXTO E OBJETIVO:
--------------------
Script auxiliar utilizado para consolidar processos
de geração de dados fictícios a serem aproveitados
em outras etapas de validação e de testes. As
funcionalidades aqui desenvolvidas utilizarão dublês
de teste para simulação de dados nos mais variados
formatos
---------------------------------------------------
"""

# Importando bibliotecas
from faker import Faker


# Instanciando faker
faker = Faker()
Faker.seed(42)


# Função para geração de csv fictício
def fake_csv_data(
    headers: list = ["col1", "col2", "col3"],
    num_rows: int = 10,
    separator: str = ","
):
    """
    """

    # Gerando string simulando arquivo csv
    fake_row = [[faker.uuid4() for _ in range(len(headers))]
                for _ in range(num_rows)]
    fake_str = "\n".join([separator.join(row) for row in fake_row])
    fake_data = separator.join(headers) + "\n" + fake_str

    return fake_data
