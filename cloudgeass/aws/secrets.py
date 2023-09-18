"""
Module: cloudgeass.aws.secrets

The module provides a class for handling operations using Secrets Manager
client and resource from boto3.

___
"""

# Importing libraries
import boto3
import logging

from cloudgeass.utils.log import log_config


class SecretsManagerClient():
    """Handles operations using secrets manager client and resource from boto3.

    This class provides attributes and methods that can improve the way on how
    users operate with Secrets Manager in AWS. In essence, it wraps some boto3
    methods to build some useful features that makes it easy to put, get and
    manager secrets in AWS.

    Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.secrets import SecretsManagerClient

        # Setting up an object and getting a secret string
        sm = SecretsManagerClient()
        secret_string = sm.get_secret_string()
        ```

    There is much more to get using the `SecretsManagerClient` class from
    `cloudgeass.aws.secrets` module. For a comprehensive list of available
    methods, please refere to this documentation page.

    Args:
        logger_level (int, optional):
            The logger level to be configured on the class logger object

    Attributes:
        logger (logging.Logger):
            A logger object to log steps according to a predefined logger level

        client (botocore.client.SecretsManager):
            A SecretsManager boto3 client to execute operations

        resource (botocore.client.SecretsManager):
            A SecretsManager boto3 resource to execute operations

    Tip: About the key word argument **client_kwargs:
        As detailed above, the class sets up a client and a resource for the
        target service using `boto3.client()` and `boto3.resource()` methods.
        So, if users want to get those attributes with custom configurations
        (for example, initialize a client in a different region), they can pass
        additional arguments for the class using the `**client_kwargs`
        attribute. In essence, what happens is that both client and resource
        attributes are then initialized as following:

        ```python
        # Setting up a boto3 client and resource
        self.client = boto3.client("secretsmanager", **client_kwargs)
        self.resource = boto3.resource("secretsmanager", **client_kwargs)
        ```

    Methods:
        get_secret_string() -> str:
            Retrieves a secret string from Secrets Manager based on a secret ID
    """

    def __init__(self, logger_level=logging.INFO, **client_kwargs):
        # Setting up a logger object
        self.logger_level = logger_level
        self.logger = log_config(logger_level=self.logger_level)

        # Setting up a boto3 client and resource
        self.client = boto3.client("secretsmanager", **client_kwargs)

    def get_secret_string(self, secret_id: str) -> str:

        self.logger.info(f"Retrieving secret string for secret {secret_id}")
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
            return response["SecretString"]

        except Exception as e:
            self.logger.error("Error on trying to retrieve the secret string "
                              f"of secret {secret_id}. Exception: {e}")
            raise e
