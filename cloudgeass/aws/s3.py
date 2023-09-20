"""
Module: cloudgeass.aws.s3

The module provides a class for handling operations using S3 client and
resource from boto3.

___
"""

# Importing libraries
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

    Methods:
        list_buckets() -> list:
            Lists the names of all S3 buckets associated with the client.

        bucket_objects_report() -> pd.DataFrame:
            Retrieves a report of objects within a specified S3 bucket.

        all_buckets_objects_report() -> pd.DataFrame:
            Retrieves a report of objects from all buckets in the account.

        get_date_partition_value_from_prefix() -> int:
            Extracts the date partition value from a given URI prefix.

        get_last_date_partition() -> int:
            Retrieves the last date partition from a table in a S3 bucket.

    Tip: About the key word argument **client_kwargs:
        Users can get customized client and resource attributes for the given
        service passing additional keyword arguments. Under the hood, both
        client and resource class attributes are initialized as following:

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

            # Setting up a class instance and getting the list of buckets
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

            # Setting up a class instance and getting a complete bucket report
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

            # Getting a report of objects in all buckets
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

    def get_date_partition_value_from_prefix(
        self,
        prefix_uri: str,
        partition_mode: str = "name=value",
        date_partition_name: str = "anomesdia",
        date_partition_idx: int = -2
    ) -> int:
        """
        Extracts the date partition value from a given URI prefix.

        Args:
            prefix_uri (str):
                The URI prefix containing the date partition information.

            partition_mode (str, optional):
                The mode for extracting the partition value.
                Options are "name=value" (default) or "value".

            date_partition_name (str, optional):
                The name of the date partition in the URI.

            date_partition_idx (int, optional):
                The index of the date partition in the URI when using "value"
                mode.

        Returns:
            int: The extracted date partition value.

        Raises:
            ValueError: If there's an issue with the URI or partition\
                extraction.

        Note:
            This method extracts the date partition value from a given URI
            prefix based on the specified partition mode.
            - In "name=value" mode, it looks for the partition name in the URI
            and extracts the corresponding value.
            - In "value" mode, it directly extracts the partition value using
            the specified index.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.s3 import S3Client

            # Setting up a class instance
            s3 = S3Client()

            # Getting the partition value given a partition URI
            uri = "s3://my-bucket/anomesdia=20230101/data/"
            partition_value = s3.get_date_partition_value_from_prefix(
                partition_uri=uri,
                partition_mode="name=value"
            )
            # 20230101
            ```
        """

        # Checking if partition_mode argument is filled properly
        partition_mode_prep = partition_mode.strip().lower()
        if partition_mode_prep not in ["name=value", "value"]:
            raise ValueError("Invalid value for partition_mode argument "
                             f"({partition_mode}). Acceptable values are "
                             "'name=value' and 'value'")

        # Partition mode follows the 'name=value' format
        if partition_mode_prep == "name=value":
            self.logger.debug("The partition mode chosen was 'name=value', so "
                              "let's take the given prefix URI and extract "
                              "name and value of the partition")

            # Starting by finding where the partition name are in the URI
            partition_start_idx = prefix_uri.find(date_partition_name + "=")
            if partition_start_idx == -1:
                raise ValueError(f"Partition name ({date_partition_name}) "
                                 "doesn't exist in the prefix URI "
                                 f"({prefix_uri})")

            # Taking the partition prefix and its value
            partition_prefix = prefix_uri[partition_start_idx:].split("/")[0]
            partition_value_raw = partition_prefix.split("=")[-1]

        # Partition mode follows the 'value' format
        elif partition_mode_prep == "value":
            self.logger.debug("The partition mode chosen was 'value', so "
                              "let's just extract the partition value "
                              "according to the 'date_partition_idx' given "
                              "by user.")
            # Taking the partition value
            partition_value_raw = prefix_uri.split("/")[date_partition_idx]

        self.logger.debug("Casting the partition value to integer")
        try:
            partition_value = int(partition_value_raw)
        except ValueError as ve:
            self.logger.error("Error on casting the partition value "
                              f"({partition_value_raw}) to integer. In many "
                              "cases, this error is related on trying to cast "
                              "a non integer partition value that was "
                              "incorretly gotten using information passed by "
                              "the user on method's call. Check if all method "
                              "arguments are correct.")
            raise ve

        return partition_value

    def get_last_date_partition(
        self,
        bucket_name: str,
        table_prefix: str,
        partition_mode: str = "name=value",
        date_partition_name: str = "anomesdia",
        date_partition_idx: int = -2
    ) -> int:
        """
        Retrieves the last date partition from a table in a S3 bucket.

        In big data scenarios, tables are stored in S3 in URIs that, at most,
        uses the following structure:
        s3://bucket-name/table-name/partition-name=value/data.parquet. So,
        applications that needs to consume partitioned tables applies filters
        and other optimization techniques to retrieve only data they need.

        In ETL proccess that stores new data frequently in daily, monthly,
        weekly or any other basis, new partitions are added everytime. So,
        consumers (other ETL proccesses or applications) that need to retrieve
        only the last data from a parent proccess may need to know in advance
        if the parent proccess had already stored their data.

        One way to do that is by looking at the date partitions of a given
        table as S3 prefixes and retrieving the value of the last
        partition. And that's what this method does.

        Tip: How is it possible?
            As a rule of construction, to get the last date partition from a
            table, the following steps are done:

            1. Retrieval of a pandas DataFrame with all objects information
            from the given bucket (using the table name/prefix as a filter)
            2. Extraction of all objects keys
            3. Collection of all partition values from the object keys
            4. Sorting of all partition values and collection of the last one

            As an additional information, this method puts together other
            methods from S3Client class as following:

            - `bucket_objects_report()` to get all objects from the bucket
            - `get_date_partition_value_from_prefix()` to get partition value

        Args:
            bucket_name (str):
                The name of the S3 bucket.

            table_prefix (str):
                The table name used as a prefix filter

            partition_mode (str, optional):
                The mode for extracting the partition value.
                Options are "name=value" (default) or "value".

            date_partition_name (str, optional):
                The name of the date partition in the URI.

            date_partition_idx (int, optional):
                The index of the date partition in the URI when using "value"
                mode.

        Returns:
            int: The last date partition value.

        Raises:
            botocore.exceptions.ClientError: If there's an error while making\
                the request.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.s3 import S3Client

            # Setting up a class instance
            s3 = S3Client()

            # Getting the last date partition value from a given table
            bucket_name = "my-bucket"
            table_name = "my-table-name"
            last_partition = s3.get_last_date_partition(
                bucket_name=bucket_name,
                table_name=table_name
            )
            ```
        """

        self.logger.debug("Retrieving a pandas DataFrame with bucket objects")
        df_objects = self.bucket_objects_report(
            bucket_name=bucket_name,
            prefix=table_prefix
        )

        self.logger.debug("Retrieving a list of object keys")
        objs_list = list(df_objects["Key"].values)

        self.logger.debug("Looping over all object keys and getting the "
                          "partition value from each prefix")
        partition_values = []
        for obj_prefix in objs_list:
            partition_value = self.get_date_partition_value_from_prefix(
                prefix_uri=obj_prefix,
                partition_mode=partition_mode,
                date_partition_name=date_partition_name,
                date_partition_idx=date_partition_idx
            )

            # Appending the value in a list
            partition_values.append(partition_value)

        self.logger.debug("Sorting the partition values list and getting the "
                          "last one")
        return sorted(partition_values)[-1]
