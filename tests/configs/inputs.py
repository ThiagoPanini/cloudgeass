"""
SCRIPT: configs/inputs.py

CONTEXTO E OBJETIVO:
--------------------
Arquivo de configuração de parâmetros e variáveis
utilizadas nos testes. O usuário deve atentar-se a todas
as configurações e declarações de variáveis aqui
realizadas para que os testes unitários possam ser
executados de maneira adequada.
---------------------------------------------------"""


# Região usada no mock dos recursos
MOCKED_REGION = "us-east-1"

# Nome de bucket a ser mockado
MOCKED_BUCKET_NAME = "cloudgeass-mock-bucket"

# Dicionário para inserção de dados mockados em bucket
MOCKED_BUCKET_CONTENT = {
    MOCKED_BUCKET_NAME: {
        "CsvFile1": {
            "Key": "mocked_prefix/file1.csv",
            "Body": "mock_col1,mock_col2,mock_col3"
        },
        "CsvFile2": {
            "Key": "mocked_prefix/file2.csv",
            "Body": "mock_col1,mock_col2,mock_col3"
        }
    }
}

# Lista esperada de colunas em DataFrame report de objetos
EXPECTED_DF_OBJECTS_REPORT_COLS = [
    "BucketName", "Key", "ObjectType", "Size", "SizeFormatted",
    "LastModified", "ETag", "StorageClass"
]
