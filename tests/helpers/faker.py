"""Script auxiliar para facilitar a geração de dados fictícios.

O objetivo deste script é auxiliar utilizado para consolidar processos de
geração de dados fictícios a serem aproveitados em outras etapas de validação
e de testes. As funcionalidades aqui desenvolvidas utilizarão dublês de teste
para simulação de dados nos mais variados formatos.

___
"""

# Importing libraries
from faker import Faker
import pandas as pd


# Initializing faker
faker = Faker()
Faker.seed(42)


# Generating fake data in CSV, JSON or PARQUET format
def fake_data(
    format: str = "csv",
    headers: list = ["col1", "col2", "col3"],
    n_rows: int = 10
) -> bytes:
    """
    Generate fake strings to be saved as CSV, JSON, or PARQUET files.

    Args:
        format (str, optional):
            The desired output format ("csv", "json", or "parquet").

        headers (list, optional):
            List of column headers for the fake data file.

        n_rows (int, optional):
            Number of rows of fake data to generate.

    Returns:
        bytes: The generated fake data in bytes format.

    Raises:
        ValueError: If the specified format is not supported.

    Note:
        This function uses the Faker library to generate arbitrary fake values.
        For "csv" format, data is returned as CSV formatted bytes.
        For "json" format, data is returned as JSON formatted bytes.
        For "parquet" format, data is returned as Parquet formatted bytes.

    Examples:
        ```python
        fake_csv_data = fake_data(
            format="csv",
            headers=["name", "email", "phone"],
            n_rows=20
        )
        ```
    """

    # Getting arbitrary fake values using Faker
    fake_values = [[faker.uuid4() for _ in range(len(headers))]
                   for _ in range(n_rows)]

    # Bulding a fake pandas DataFrame
    df_fake = pd.DataFrame(data=fake_values, columns=headers)

    # Preparing the output file extension
    format_prep = format.lower().strip().replace(".", "")

    # Checking if it is a CSV file
    if format_prep == "csv":
        bytes_data = bytes(df_fake.to_csv(index=False),
                           encoding="utf-8")

    # Checking if it is a JSON file
    elif format_prep == "json":
        bytes_data = bytes(df_fake.to_json(orient="records"),
                           encoding="utf-8")

    # Checking if it is a PARQUET file
    elif format_prep == "parquet":
        bytes_data = df_fake.to_parquet(compression="snappy")

    else:
        bytes_data = None

    return bytes_data
