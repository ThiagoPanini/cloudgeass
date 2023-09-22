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
        secret_string = sm.get_secret_string(secret_id="some-secret-id")
        ```

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

    Methods:
        get_secret_string() -> str:
            Retrieves a secret string from Secrets Manager based on a secret ID

    Tip: About the key word argument **client_kwargs:
        Users can get customized client and resource attributes for the given
        service passing additional keyword arguments. Under the hood, both
        client and resource class attributes are initialized as following:

        ```python
        # Setting up a boto3 client and resource
        self.client = boto3.client("secretsmanager", **client_kwargs)
        self.resource = boto3.resource("secretsmanager", **client_kwargs)
        ```
    """

    def __init__(self, logger_level=logging.INFO, **client_kwargs):
        # Setting up a logger object
        self.logger_level = logger_level
        self.logger = log_config(logger_level=self.logger_level)

        # Setting up a boto3 client and resource
        self.client = boto3.client("secretsmanager", **client_kwargs)

    def get_secret_string(self, secret_id: str) -> str:
        """
        Retrieves the secret string for a given secret ID.

        This method uses the AWS Secrets Manager client to retrieve the secret
        string associated with the provided secret ID.

        Args:
            secret_id (str):
                The ID of the secret to retrieve.

        Returns:
            str: The secret string associated with the provided secret ID.

        Raises:
            Exception: If there is an error while retrieving the secret string.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.secrets import SecretsManagerClient

            # Creating an instance
            sm = SecretsManagerClient()

            # Getting the secret string for a specific secret
            secret_id = "your_secret_id"
            secret_string = sm.get_secret_string(secret_id)
            ```
        """

        self.logger.debug(f"Retrieving secret string for secret {secret_id}")
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
            return response["SecretString"]

        except Exception as e:
            self.logger.error("Error on trying to retrieve the secret string "
                              f"of secret {secret_id}. Exception: {e}")
            raise e
