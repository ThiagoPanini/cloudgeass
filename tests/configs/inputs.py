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
from tests.helpers.faker import fake_data_buffer


# Região usada no mock dos recursos
MOCKED_REGION = "us-east-1"

# Dicionário contendo definição de cenário a ser mockado no s3
MOCKED_BUCKET_CONTENT = {
    "cloudgeass-mock-bucket-01": {
        "file-001": {
            "Key": "csv/anomesdia=20230117/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-002": {
            "Key": "csv/anomesdia=20230118/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-003": {
            "Key": "csv/anomesdia=20230119/file.csv",
            "Body": fake_data_buffer(format="csv")
        }
    },
    "cloudgeass-mock-bucket-02": {
        "file-001": {
            "Key": "csv/anomes=202301/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-002": {
            "Key": "csv/anomes=202302/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-003": {
            "Key": "csv/anomes=202303/file.csv",
            "Body": fake_data_buffer(format="csv")
        }
    },
    "cloudgeass-mock-bucket-03": {
        "file-001": {
            "Key": "csv/20230117/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-002": {
            "Key": "csv/20230118/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-003": {
            "Key": "csv/20230119/file.csv",
            "Body": fake_data_buffer(format="csv")
        }
    },
    "cloudgeass-mock-bucket-04": {
        "file-001": {
            "Key": "csv/anomesdia=20230117/file.csv",
            "Body": fake_data_buffer(format="csv")
        },
        "file-002": {
            "Key": "json/anomesdia=20230117/file.json",
            "Body": fake_data_buffer(format="json")
        },
        "file-003": {
            "Key": "parquet/anomesdia=20230117/file.parquet",
            "Body": fake_data_buffer(format="parquet")
        }
    },
    "cloudgeass-mock-empty-bucket": {}
}

# Lista de buckets não vazios definidos no dicionário
NON_EMPTY_BUCKETS = [b for b in MOCKED_BUCKET_CONTENT.keys()
                     if len(MOCKED_BUCKET_CONTENT[b]) > 0]

# Nome específico de bucket usado na extração individual de report
EXAMPLE_BUCKET = NON_EMPTY_BUCKETS[0]

# Lista esperada de colunas em DataFrame report de objetos
EXPECTED_DF_OBJECTS_REPORT_COLS = [
    "BucketName", "Key", "ObjectType", "Size", "SizeFormatted",
    "LastModified", "ETag", "StorageClass"
]
