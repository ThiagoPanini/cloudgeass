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
    EXPECTED_OBJECTS_REPORT_COLS
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
