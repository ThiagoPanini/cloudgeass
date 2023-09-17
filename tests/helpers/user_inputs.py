"""Centralizing all user inputs for helping on fixtures and test cases.

This file aims to put together all variables used on fixture definitions and
test cases that requires user inputs as a way to configure or validate
something.

The idea behind this file is to have everything related to user inputs on
test cases in a single place. This makes easier to handle, give maintenance,
support and improvements for building new test cases.

___
"""

# Importing libraries
from tests.helpers.faker import fake_data


# A region name to mock resources while testing
MOCKED_REGION = "us-east-1"

# A complete definition of buckets to be mocked and its contents
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
