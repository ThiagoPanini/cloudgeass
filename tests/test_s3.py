"""Test cases for features defined on cloudgeass.aws.s3.S3Client module class

This file handles the definition of all test cases for testing S3Client class
and its features.

___
"""

# Importing libraries
import pytest
from moto import mock_s3
import pandas as pd

from tests.helpers.user_inputs import (
    MOCKED_BUCKET_CONTENT,
    NON_EMPTY_BUCKET_NAME,
    EMPTY_BUCKET_NAME,
    EXPECTED_OBJECTS_REPORT_COLS,
    PARTITIONED_S3_TABLES
)


@pytest.mark.s3
@pytest.mark.list_buckets
@mock_s3
def test_list_buckets_method_returns_a_list(s3, prepare_mocked_bucket):
    """
    G: Given that users want to get a list of all S3 buckets within an account
    W: When the method list_buckets() from S3Client class is called
    T: Then the return must be a Python list
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Checking if list_buckets() method returns a list
    assert isinstance(s3.list_buckets(), list)


@pytest.mark.s3
@pytest.mark.list_buckets
@mock_s3
def test_list_buckets_method_returns_all_expected_buckets_within_an_account(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get a list of all S3 buckets within an account
    W: When the method list_buckets() from S3Client class is called
    T: Then the returned list must contain all expected bucket names
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Extracting all expected bucket names from user inputs
    expected_buckets = list(MOCKED_BUCKET_CONTENT.keys())

    assert s3.list_buckets() == expected_buckets


@pytest.mark.s3
@pytest.mark.bucket_objects_report
@mock_s3
def test_bucket_objects_report_method_returns_a_pandas_dataframe(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve information about objects in a bucket
    W: When the method buckets_objects_report() from S3Client class is called
    T: Then the return must be a pandas DataFrame
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Getting the objects report
    df_objects_report = s3.bucket_objects_report(
        bucket_name=NON_EMPTY_BUCKET_NAME,
        prefix=""
    )

    assert isinstance(df_objects_report, pd.DataFrame)


@pytest.mark.s3
@pytest.mark.bucket_objects_report
@mock_s3
def test_bucket_objects_report_dataframe_has_expected_columns(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve information about objects in a bucket
    W: When the method buckets_objects_report() from S3Client class is called
    T: Then the DataFrame return must have a list of expected columns
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Getting the objects report
    df_objects_report = s3.bucket_objects_report(
        bucket_name=NON_EMPTY_BUCKET_NAME,
        prefix=""
    )

    assert list(df_objects_report.columns) == EXPECTED_OBJECTS_REPORT_COLS


@pytest.mark.s3
@pytest.mark.bucket_objects_report
@mock_s3
def test_error_on_trying_to_retrieve_objects_report_from_a_invalid_bucket(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve information about objects in a bucket
    W: When the method buckets_objects_report() from S3Client class is called
       with an invalid bucket name (i.e. a bucket name that doesn't exists)
    T: Then an Exception must be thrown
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    with pytest.raises(Exception):
        _ = s3.bucket_objects_report(
            bucket_name="invalid-bucket-name"
        )


@pytest.mark.s3
@pytest.mark.bucket_objects_report
@mock_s3
def test_bucket_objects_report_method_returns_none_when_called_on_empty_bucket(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve information about objects in a bucket
    W: When the method buckets_objects_report() from S3Client class is called
       on an empty bucket
    T: Then the return must be None
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    assert s3.bucket_objects_report(EMPTY_BUCKET_NAME) is None


@pytest.mark.s3
@pytest.mark.all_buckets_objects_report
@mock_s3
def test_all_buckets_objects_report_returns_a_pandas_dataframe(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve a DataFrame with info of all objects
       from all S3 buckets within an account
    W: When the method all_buckets_objects_report() is called
    T: Then the return must be a pandas DataFrame
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    assert isinstance(s3.all_buckets_objects_report(), pd.DataFrame)


@pytest.mark.s3
@pytest.mark.all_buckets_objects_report
@mock_s3
def test_all_buckets_objects_report_has_more_rows_than_single_bucket_report(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve a DataFrame with info of all objects
       from all S3 buckets within an account
    W: When the method all_buckets_objects_report() is called
    T: Then the number of rows of the returned DataFrame must be higher than
       the number of rows of a DataFrame retrieve from bucket_objects_report()
       method (since we are talking about a complete report from all buckets
       versus a report from a single bucket)
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Getting all buckets report and a single bucket report
    df_all_buckets_report = s3.all_buckets_objects_report()
    df_bucket_report = s3.bucket_objects_report(NON_EMPTY_BUCKET_NAME)

    assert len(df_all_buckets_report) > len(df_bucket_report)


@pytest.mark.s3
@pytest.mark.get_date_partition_value_from_prefix
@mock_s3
def test_get_partition_value_from_prefix_uri_with_name_and_value_format(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get the partition value from a partition S3 URI
    W: When the method get_date_partition_value_from_prefix() is called from
       S3Client class with partition_mode equals to "name=value"
    T: Then the return integer must be the expected partition value
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Defining variables to build a target URI
    partition_name = "ano_mes_dia"
    expected_partition_value = 20230101

    # Building a target URI to extract the partition
    target_uri = "s3://my-bucket/my-table/"\
        f"{partition_name}={str(expected_partition_value)}/sub/file.csv"

    # Extracting the partition value
    partition_value = s3.get_date_partition_value_from_prefix(
        prefix_uri=target_uri,
        partition_mode="name=value",
        date_partition_name="ano_mes_dia"
    )

    assert partition_value == expected_partition_value


@pytest.mark.s3
@pytest.mark.get_date_partition_value_from_prefix
@mock_s3
def test_get_partition_value_from_prefix_uri_with_only_value_format(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get the partition value from a partition S3 URI
    W: When the method get_date_partition_value_from_prefix() is called from
       S3Client class with partition_mode equals to "value"
    T: Then the return integer must be the expected partition value
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Defining variables to build a target URI
    expected_partition_value = 20230101
    date_partition_idx = -3

    # Building a target URI to extract the partition
    target_uri = "s3://my-bucket/my-table/"\
        f"{str(expected_partition_value)}/sub/file.csv"

    # Extracting the partition value
    partition_value = s3.get_date_partition_value_from_prefix(
        prefix_uri=target_uri,
        partition_mode="value",
        date_partition_idx=date_partition_idx
    )

    assert partition_value == expected_partition_value


@pytest.mark.s3
@pytest.mark.get_date_partition_value_from_prefix
@mock_s3
def test_error_when_passing_an_invalid_mode_for_get_partition_value_method(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get the partition value from a partition S3 URI
    W: When the method get_date_partition_value_from_prefix() is called from
       S3Client class with an invalid partition_mode (i.e something different
       than 'name=value' and 'value')
    T: Then a ValueError exception must be thrown
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Defining variables to build a target URI
    partition_name = "ano_mes_dia"
    expected_partition_value = 20230101

    # Building a target URI to extract the partition
    target_uri = "s3://my-bucket/my-table/"\
        f"{partition_name}={str(expected_partition_value)}/sub/file.csv"

    # Extracting the partition value
    with pytest.raises(ValueError):
        _ = s3.get_date_partition_value_from_prefix(
            prefix_uri=target_uri,
            partition_mode="dummy",
            date_partition_name=partition_name
        )


@pytest.mark.s3
@pytest.mark.get_date_partition_value_from_prefix
@mock_s3
def test_error_when_passing_a_date_partition_name_that_doesnt_exists(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get the partition value from a partition S3 URI
    W: When the method get_date_partition_value_from_prefix() is called from
       S3Client class with an date_partition_name argument that doesn't exists
       in the partition_uri
    T: Then a ValueError exception must be thrown
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Defining variables to build a target URI
    partition_name = "ano_mes_dia"
    expected_partition_value = 20230101

    # Building a target URI to extract the partition
    target_uri = "s3://my-bucket/my-table/"\
        f"{partition_name}={str(expected_partition_value)}/sub/file.csv"

    # Extracting the partition value
    with pytest.raises(ValueError):
        _ = s3.get_date_partition_value_from_prefix(
            prefix_uri=target_uri,
            partition_mode="name=value",
            date_partition_name="anomesdia"  # This name doesn't exists
        )


@pytest.mark.s3
@pytest.mark.get_date_partition_value_from_prefix
@mock_s3
def test_error_when_passing_a_partition_mode_that_doesnt_match_with_the_uri(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to get the partition value from a partition S3 URI
    W: When the method get_date_partition_value_from_prefix() is called from
       S3Client class with an partition_mode that doesn't match with the URI
       format (i.e. passing "name=value" to extract the partition value from
       an URI that has only the partition value and not the name)
    T: Then a ValueError exception must be thrown
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Defining variables to build a target URI
    partition_name = "ano_mes_dia"
    expected_partition_value = 20230101

    # Building a target URI to extract the partition
    target_uri = "s3://my-bucket/my-table/"\
        f"{partition_name}={str(expected_partition_value)}/sub/file.csv"

    # Extracting the partition value
    with pytest.raises(ValueError):
        _ = s3.get_date_partition_value_from_prefix(
            prefix_uri=target_uri,
            partition_mode="value",
            date_partition_name="anomesdia"  # This name doesn't exists
        )


@pytest.mark.s3
@pytest.mark.get_last_date_partition
@mock_s3
def test_get_last_date_partition_method_returns_last_partition_in_daily_basis(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve the last date partition from a table
       that is partitioned in a daily basis in the format %Y%m%d
    W: When the method get_last_date_partition()
    T: Then the expected partition must be retrieved
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Retrieving the last partition
    last_partition = s3.get_last_date_partition(
        bucket_name=PARTITIONED_S3_TABLES["daily"]["bucket_name"],
        table_prefix=PARTITIONED_S3_TABLES["daily"]["table_name"],
        partition_mode=PARTITIONED_S3_TABLES["daily"]["partition_mode"],
        date_partition_name=PARTITIONED_S3_TABLES["daily"]["partition_name"]
    )

    # Getting the expected last partition
    expected_partition = PARTITIONED_S3_TABLES["daily"]["expected_partition"]

    assert last_partition == expected_partition


@pytest.mark.s3
@pytest.mark.get_last_date_partition
@mock_s3
def test_get_last_date_partition_method_returns_last_partition_in_monthlybasis(
    s3, prepare_mocked_bucket
):
    """
    G: Given that users want to retrieve the last date partition from a table
       that is partitioned in a monthly basis in the format %Y%m
    W: When the method get_last_date_partition()
    T: Then the expected partition must be retrieved
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Retrieving the last partition
    last_partition = s3.get_last_date_partition(
        bucket_name=PARTITIONED_S3_TABLES["monthly"]["bucket_name"],
        table_prefix=PARTITIONED_S3_TABLES["monthly"]["table_name"],
        partition_mode=PARTITIONED_S3_TABLES["monthly"]["partition_mode"],
        date_partition_name=PARTITIONED_S3_TABLES["monthly"]["partition_name"]
    )

    # Getting the expected last partition
    expected_partition = PARTITIONED_S3_TABLES[
        "monthly"
    ]["expected_partition"]

    assert last_partition == expected_partition
