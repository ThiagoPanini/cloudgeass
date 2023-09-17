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
import pandas as pd

from cloudgeass.utils.log import log_config
from cloudgeass.utils.prep import categorize_file_size


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

        Returns:
            list: A list of bucket names.

        Raises:
            botocore.exceptions.ClientError: If there's an error while making\
                the request.

        Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.s3 import S3Client

        # Setting up an object and getting the list of buckets with an account
        s3 = S3Client()
        buckets = s3.list_buckets()
        ```
        """

        self.logger.debug("Retrieving the list of S3 bucket names")
        buckets = [
            b["Name"] for b in self.client.list_buckets()["Buckets"]
        ]
        self.logger.debug(f"There are {len(buckets)} buckets in the list")

        return buckets

    def bucket_objects_report(
        self,
        bucket_name: str,
        prefix: str = ""
    ) -> pd.DataFrame:
        """
        Retrieve a report of objects within a specified S3 bucket.

        This method receives a bucket name and an optional bucket prefix to
        return a report in a pandas DataFrame format with all information
        about objects within the bucket and the given prefix.

        Args:
            bucket_name (str): The name of the S3 bucket.
            prefix (str, optional): A prefix to filter objects.

        Returns:
            pd.DataFrame: A DataFrame containing information about the objects.

        Raises:
            botocore.exceptions.ClientError: If there's an error while making\
                the request.

        Note:
            This method lists objects in the specified S3 bucket and creates a
            DataFrame with relevant information. The DataFrame includes columns
            for 'BucketName', 'Key', 'ObjectType', 'Size', 'SizeFormatted',
            'LastModified', 'ETag', and 'StorageClass'. The 'ObjectType' column
            is determined by the file extension of the object key.
            The 'SizeFormatted' column provides a human-readable representation
            of the file size.

        Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.s3 import S3Client

        # Setting up an object and getting the list of buckets with an account
        s3 = S3Client()
        df_objects_report = s3.bucket_objects_report(
            bucket_name="some-bucket-name",
            prefix="some-optional-prefix"
        )
        ```
        """

        self.logger.debug(f"Retrieving objects from {bucket_name}/{prefix}")
        try:
            r = self.client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix
            )

        except Exception as e:
            self.logger.error("Error on calling client.list_objects_v2() "
                              f"method with Bucket={bucket_name} and prefix="
                              f"{prefix}. Exception: {e}")
            raise e

        self.logger.debug("Getting bucket content from response['Contents']")
        try:
            bucket_content = r["Contents"]

        except KeyError:
            self.logger.warning(f"There's no 'Contents' key on list_objects_v2"
                                " method response. This means that there are "
                                f"no objects on {bucket_name}/{prefix}")
            return None

        # Transforming the contents response in a pandas DataFrame
        df = pd.DataFrame(bucket_content)

        # Adding the bucket name and getting the object file extension
        df["BucketName"] = bucket_name
        df["ObjectType"] = df["Key"].apply(lambda x: x.split(".")[-1])

        # Applying a categorization function to get the file size
        df["SizeFormatted"] = df["Size"].apply(
            lambda x: categorize_file_size(x)
        )

        # Sorting DataFrame columns
        order_cols = [
            "BucketName", "Key", "ObjectType", "Size", "SizeFormatted",
            "LastModified", "ETag", "StorageClass"
        ]
        df_objects_report = df.loc[:, order_cols]

        return df_objects_report

    def all_buckets_objects_report(
        self,
        prefix: str = "",
        exclude_buckets: list = list()
    ) -> pd.DataFrame:
        """
        Retrieve a report of objects from all buckets in the AWS account.

        Args:
            prefix (str, optional):
                A prefix to filter objects.

            exclude_buckets (list, optional):
                List of bucket names to exclude from the report..

        Returns:
            pd.DataFrame: A DataFrame containing information about the objects
            from all specified buckets.

        Raises:
            botocore.exceptions.ClientError: If there's an error while making\
                the request.

        Note:
            This method lists calls self.list_buckets() to get a list of all
            buckets within an account and loops over this list to call
            self.bucket_objects_report() for each bucket in order to retrieve a
            pandas DataFrame with information about objects. At the end, all
            individual DataFrames are concatenated together to form the return
            for this method.

        Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.s3 import S3Client

        # Setting up an object and getting the list of buckets with an account
        s3 = S3Client()
        df_all_buckets_report = s3.all_buckets_objects_report()
        ```
        """

        # Retrieving all buckets within an account
        all_buckets = self.list_buckets()

        # Removing buckets according to a filter list
        buckets = [b for b in all_buckets if b not in exclude_buckets]

        # Creating an empty DataFrame and looping over all buckets
        df_report = pd.DataFrame()
        for bucket in buckets:
            # Retrieving objects from the bucket
            df_bucket_report = self.bucket_objects_report(
                bucket_name=bucket,
                prefix=prefix
            )

            # Appending to the final DataFrame
            df_report = pd.concat([df_report, df_bucket_report])

        # Reseting index
        df_report.reset_index(drop=True, inplace=True)

        return df_report
