"""
SCRIPT: configs/inputs.py

CONTEXTO E OBJETIVO:
--------------------
Arquivo de configuração de parâmetros e variáveis
utilizadas nos testes. O usuário deve atentar-se a todas
as configurações e declarações de variáveis aqui
realizadas para que os testes unitários possam ser
executados de maneira adequada.
---------------------------------------------------
"""

# Importando bibliotecas e módulos
from tests.helpers.faker import fake_csv_data


# Região usada no mock dos recursos
MOCKED_REGION = "us-east-1"

# Dicionário contendo definição de cenário a ser mockado no s3
MOCKED_BUCKET_CONTENT = {
    "cloudgeass-mock-bucket": {
        "CsvFile1": {
            "Key": "anomesdia=20230117/file1.csv",
            "Body": fake_csv_data()
        },
        "CsvFile2": {
            "Key": "anomesdia=20230108/file2.csv",
            "Body": fake_csv_data()
        }
    },
    "cloudgeass-mock-empty-bucket": {}
}

# Lista de buckets não vazios definidos no dicionário
NON_EMPTY_BUCKETS = [b for b in MOCKED_BUCKET_CONTENT.keys()
                     if len(MOCKED_BUCKET_CONTENT[b]) > 0]

# Nome específico de bucket usado na extração individual de report
MOCKED_BUCKET_NAME = NON_EMPTY_BUCKETS[0]

# Lista esperada de colunas em DataFrame report de objetos
EXPECTED_DF_OBJECTS_REPORT_COLS = [
    "BucketName", "Key", "ObjectType", "Size", "SizeFormatted",
    "LastModified", "ETag", "StorageClass"
]
