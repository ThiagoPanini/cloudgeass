"""Configuração de inputs utilizados na criação e validação dos testes.

O objetivo deste arquivo é consolidar variáveis que representam inputs
do usuário para configuração das fixtures e validação de funcionalidades
nos testes unitários. A ideia é centralizar variáveis importantes para
proporcionar um local único de gerenciamento de validações nas etapas de
testes.

___
"""

# Importando bibliotecas e módulos
from tests.helpers.faker import fake_data


"""---------------------------------------------------
-------- 1. DEFINIÇÃO DE INPUTS DE VALIDAÇÃO ---------
         1.1 Inputs utilizados no módulo s3
---------------------------------------------------"""


# Região usada no mock dos recursos
MOCKED_REGION = "us-east-1"

# Dicionário contendo definição de cenário a ser mockado no s3
MOCKED_BUCKET_CONTENT = {
    "cloudgeass-mock-bucket-01": {
        "file-001": {
            "Key": "csv/anomesdia=20230117/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-002": {
            "Key": "csv/anomesdia=20230118/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-003": {
            "Key": "csv/anomesdia=20230119/file.csv",
            "Body": fake_data(format="csv")
        }
    },
    "cloudgeass-mock-bucket-02": {
        "file-001": {
            "Key": "csv/anomes=202301/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-002": {
            "Key": "csv/anomes=202302/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-003": {
            "Key": "csv/anomes=202303/file.csv",
            "Body": fake_data(format="csv")
        }
    },
    "cloudgeass-mock-bucket-03": {
        "file-001": {
            "Key": "csv/20230117/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-002": {
            "Key": "csv/20230118/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-003": {
            "Key": "csv/20230119/file.csv",
            "Body": fake_data(format="csv")
        }
    },
    "cloudgeass-mock-bucket-04": {
        "file-csv": {
            "Key": "csv/anomesdia=20230117/file.csv",
            "Body": fake_data(format="csv")
        },
        "file-json": {
            "Key": "json/anomesdia=20230117/file.json",
            "Body": fake_data(format="json")
        },
        "file-parquet": {
            "Key": "parquet/anomesdia=20230117/file.parquet",
            "Body": fake_data(format="parquet")
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


"""---------------------------------------------------
-------- 1. DEFINIÇÃO DE INPUTS DE VALIDAÇÃO ---------
       1.2 Inputs utilizados no módulo secrets
---------------------------------------------------"""

# Referência nominal do segredo a ser mockado
MOCKED_SECRET_NAME = "some-secret-name"

# Valor do segredo a ser mockado
MOCKED_SECRET_VALUE = "some-secret-value"
