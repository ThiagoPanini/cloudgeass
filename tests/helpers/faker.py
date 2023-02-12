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
import pandas as pd
import io


# Instanciando faker
faker = Faker()
Faker.seed(42)


# Função para gerar dados fictícios nos formatos CSV, JSON ou PARQUET
def fake_data_buffer(
    format: str = "csv",
    headers: list = ["col1", "col2", "col3"],
    n_rows: int = 10
):
    """
    Gera buffer de dados fictícios simulando diferentes formatos de arquivos.

    Com essa função, o usuário poderá obter um buffer de bytes de dados
    gerados aleatoriamente através da biblioteca Faker para realizar as
    mais variadas validações e testes. A função utiliza um DataFrame do
    pandas para guiar os diferentes formatos de buffer de saída. Como
    exemplo, caso o usuário queira um buffer de arquivo CSV (format="csv"),
    a resposta será dada através do método io.BytesIO(bytes(df.to_csv()),
    onde df é o DataFrame pandas criado com dados fictícios.

    Parâmetros
    ----------
    :param format:
        Formato de arquivo a ser simulado pelo processo.
        [type: str, default="csv", allowed=csv|json|parquet]

    :param headers:
        Lista de colunas utilizada como header dos dados gerados.
        [type: lista, default=["col1", "col2", "col3"]]

    :param num_rows:
        Número de linhas de dados a serem gerados.
        [type: int, default=10]

    **kwargs
    --------
    :param sep:
        Caractere separador dos atributos dos dados fictícios gerados
        em caso de format="csv".
        [type: str, default=","]

    Retorno
    -------
    :return buffer: buffer de dados fictícios gerados.
        [type: io.BytesIO]
    """

    # Gerando lista aninhada de valores fictícios usando Faker
    fake_values = [[faker.uuid4() for _ in range(len(headers))]
                   for _ in range(n_rows)]

    # Gerando DataFrame fictício
    df_fake = pd.DataFrame(data=fake_values, columns=headers)

    # Validando formato de saída antes dos direcionamentos
    format_prep = format.lower().strip().replace(".", "")

    # Validando se o formato de saída remete a um arquivo CSV
    if format_prep == "csv":
        bytes_data = bytes(df_fake.to_csv(index=False), 
                           encoding="utf-8")
        buffer = io.BytesIO(bytes_data)

    # Validando se o formato de saída remete a um arquivo JSON
    elif format_prep == "json":
        bytes_data = bytes(df_fake.to_json(orient="records"),
                           encoding="utf-8")
        buffer = io.BytesIO(bytes_data)

    # Validando se o formato de saída remete a um arquivo PARQUET
    elif format_prep == "parquet":
        bytes_data = df_fake.to_parquet(compression="snappy")
        buffer = io.BytesIO(bytes_data)

    else:
        buffer = None

    return buffer
