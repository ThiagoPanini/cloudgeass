"""
Módulo responsável por alocar desenvolvimentos relacionados à utilização do
boto3 para o gerencimento de operações do S3 na AWS. Aqui será possível
encontrar funcionalidades prontas para realizar as mais variadas atividades
no S3.

Ao longo deste módulo, será possível encontrar funções definidas e documentadas
visando proporcionar a melhor experiência ao usuário!

___
"""

# Importando bibliotecas
import boto3
import logging

from cloudgeass.utils.log import log_config


class S3Client():
    """Handles operations using s3 client and resource from boto3.

    This class provides attributes and methods that can improve the way on how
    users operate with S3 in AWS. In essence, it wraps some boto3 methods to
    build some useful features that makes it easy to extract information and
    manage S3 buckets and objects.

    Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.s3 import S3Client

        # Setting up an object and getting the list of buckets with an account
        s3 = S3Client()
        buckets = s3.list_buckets()
        ```

    There're much more to get using the `S3Client` class from
    `cloudgeass.aws.s3` module. For a comprehensive list of available methods,
    please refere to this documentation page.

    Args:
        logger_level (int, optional):
            The logger level to be configured on the class logger object

    Attributes:
        logger (logging.Logger):
            A logger object to log steps according to a predefined logger level

        client (botocore.client.S3):
            A S3 boto3 client to execute operations

        resource (botocore.client.S3):
            A S3 boto3 resource to execute operations

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
        self.client = boto3.client("s3", **client_kwargs)
        self.resource = boto3.resource("s3", **client_kwargs)
        ```
    """

    def __init__(self, logger_level=logging.INFO, **client_kwargs):
        # Setting up a logger object
        self.logger_level = logger_level
        self.logger = log_config(logger_level=self.logger_level)

        # Setting up a boto3 client and resource
        self.client = boto3.client("s3", **client_kwargs)
        self.resource = boto3.resource("s3", **client_kwargs)

    def list_buckets(self) -> list:
        """
        Lists the names of all S3 buckets associated with the client.

        Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.s3 import S3Client

        # Setting up an object and getting the list of buckets with an account
        s3 = S3Client()
        buckets = s3.list_buckets()
        ```

        Returns:
            list: A list of bucket names.

        Raises:
            botocore.exceptions.ClientError: If there's an error while making\
                the request.
        """

        try:
            self.logger.debug("Retrieving the list of S3 bucket names")
            # Retrieving bucket names using list comprehension
            buckets = [
                b["Name"] for b in self.client.list_buckets()["Buckets"]
            ]
            self.logger.debug(f"There are {len(buckets)} buckets in the list")

            return buckets

        except Exception as e:
            self.logger.error("Error on trying to retrieve a list of S3 "
                              f"buckets. Exception: {e}")
            raise e
