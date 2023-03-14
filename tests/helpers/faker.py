"""Script auxiliar para facilitar a geração de dados fictícios.

O objetivo deste script é auxiliar utilizado para consolidar processos de
geração de dados fictícios a serem aproveitados em outras etapas de validação
e de testes. As funcionalidades aqui desenvolvidas utilizarão dublês de teste
para simulação de dados nos mais variados formatos.

___
"""

# Importando bibliotecas
from faker import Faker
import pandas as pd


# Instanciando faker
faker = Faker()
Faker.seed(42)


# Função para gerar dados fictícios nos formatos CSV, JSON ou PARQUET
def fake_data(
    format: str = "csv",
    headers: list = ["col1", "col2", "col3"],
    n_rows: int = 10
) -> bytes:
    """
    Gera dados fictícios simulando diferentes formatos de arquivos.

    Com essa função, o usuário poderá obter um dados (em bytes) gerados
    aleatoriamente através da biblioteca Faker para realizar as mais variadas
    validações e testes. A função utiliza um DataFrame do pandas para guiar os
    diferentes formatos de saída. Como exemplo, caso o usuário queira um
    objeto que simule um arquivo CSV (format="csv"), a resposta será dada
    através do método bytes(df.to_csv()), onde df é um DataFrame pandas criado
    com dados fictícios.

    Examples:
        ```python
        from tests.helpers.faker import fake_data

        mocked_data = fake_data(format="parquet")
        ```

    Args:
        format (str): Formato dos dados resultantes.
        headers (list): Lista de headers a serem mockados.
        n_rows (int): Número de registros dos dados resultantes.

    Keyword Args:
        sep (str): Separador em caso de `format="csv"`

    Returns:
        Bytes representando dados fictícios gerados a partir das configurações\
        parametrizadas pelo usuário na chamada da função.
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

    # Validando se o formato de saída remete a um arquivo JSON
    elif format_prep == "json":
        bytes_data = bytes(df_fake.to_json(orient="records"),
                           encoding="utf-8")

    # Validando se o formato de saída remete a um arquivo PARQUET
    elif format_prep == "parquet":
        bytes_data = df_fake.to_parquet(compression="snappy")

    else:
        bytes_data = None

    return bytes_data
