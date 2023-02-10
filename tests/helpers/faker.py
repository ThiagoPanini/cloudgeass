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
import io


# Instanciando faker
faker = Faker()
Faker.seed(42)


# Função para geração de csv fictício
def fake_csv_data(
    headers: list = ["col1", "col2", "col3"],
    num_rows: int = 10,
    separator: str = ","
) -> io.BytesIO:
    """
    Gera stream de bytes contendo uma simulação de arquivo CSV.

    Com essa função, o usuário poderá parametrização uma criação fictícia
    de uma stream binária contendo uma string que simula o conteúdo de
    um arquivo CSV. A função utiliza a biblioteca Faker e seu método
    uuid4() para geração de strings aleatórias.

    Parâmetros
    ----------
    :param headers:
        Lista de colunas utilizada como header dos dados gerados.
        [type: lista, default=["col1", "col2", "col3"]]

    :param num_rows:
        Número de linhas de dados a serem gerados.
        [type: int, default=10]

    :param separator:
        Caractere separador dos atributos dos dados fictícios gerados.
        [type: str, default=","]

    Retorno
    -------
    :return fake_data: stream binária contendo os dados gerados.
        [type: io.BytesIO]
    """

    # Gerando string simulando arquivo csv
    fake_row = [[faker.uuid4() for _ in range(len(headers))]
                for _ in range(num_rows)]
    fake_str = "\n".join([separator.join(row) for row in fake_row])
    fake_data = separator.join(headers) + "\n" + fake_str

    return io.BytesIO(bytes(fake_data, encoding="utf-8"))
