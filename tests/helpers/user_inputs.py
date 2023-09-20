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


""" -------------------------------------------------
    USER INPUTS: S3Client class
    Defining variables for testing cloudgeass.aws.s3
------------------------------------------------- """

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


# List of non empty buckets
NON_EMPTY_BUCKETS = [
    b for b in MOCKED_BUCKET_CONTENT.keys()
    if len(MOCKED_BUCKET_CONTENT[b]) > 0
]

# List of empty buckets
EMPTY_BUCKETS = [
    b for b in MOCKED_BUCKET_CONTENT.keys()
    if len(MOCKED_BUCKET_CONTENT[b]) == 0
]

# A non empty bucket name
NON_EMPTY_BUCKET_NAME = NON_EMPTY_BUCKETS[0]

# A empty bucket name
EMPTY_BUCKET_NAME = EMPTY_BUCKETS[0]

# A list of expected columns of bucket_objects_report() method return
EXPECTED_OBJECTS_REPORT_COLS = [
    "BucketName", "Key", "ObjectType", "Size", "SizeFormatted", "LastModified",
    "ETag", "StorageClass"
]

# Bucket names to test the get_last_date_partition() method
PARTITIONED_S3_TABLES = {
    "daily": {
        "bucket_name": "cloudgeass-mock-bucket-01",
        "table_name": "csv",
        "partition_mode": "name=value",
        "partition_name": "anomesdia",
        "expected_partition": 20230119
    },
    "monthly": {
        "bucket_name": "cloudgeass-mock-bucket-02",
        "table_name": "csv",
        "partition_mode": "name=value",
        "partition_name": "anomes",
        "expected_partition": 202303
    }
}


""" -------------------------------------------------
    USER INPUTS: EC2Client class
    Defining variables for testing cloudgeass.aws.ec2
------------------------------------------------- """

# A security group name to test the creation of one with a class method
MOCKED_SG_NAME = "ssh-local-connection-sg"

# A fake local IP address to mock the request response from LOCAL_IP_URL
LOCAL_IP_MOCKED_RESPONSE = "172.0.0.1"

# A dictionary with key pair information to test the method
MOCKED_KP_CONFIG = {
    "key_name": "local-connection-kp",
    "key_type": "rsa",
    "key_format": "ppk",
    "path_to_save_file": "."
}

# A dictionary with EC2 information to test the creation method
MOCKED_EC2_CONFIG = {
    "image_id": "ami-04cb4ca688797756f",
    "instance_type": "t2.micro"
}


""" -------------------------------------------------
    USER INPUTS: SecretsManagerClient class
    Defining variables for testing cloudgeass.aws.secrets
------------------------------------------------- """

# A mocked secret name
MOCKED_SECRET_NAME = "my-mocked-secret"

# A mocked secret value
MOCKED_SECRET_VALUE = "my-mocked-secret-value"
