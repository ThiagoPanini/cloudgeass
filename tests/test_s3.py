"""Test cases for features defined on cloudgeass.aws.s3.S3Client module class

This file handles the definition of all test cases for testing S3Client class
and its features.

___
"""

# Importing libraries
import pytest
from moto import mock_s3


@pytest.mark.s3
@pytest.mark.list_buckets
@mock_s3
def test_return_of_list_buckets_method_is_a_list(s3, prepare_mocked_bucket):
    """
    G: Given that users want to get a list of all S3 buckets within an account
    W: When the method list_buckets() from S3Client class are called
    T: Then the return must be a Python list
    """

    # Preparing a mocked s3 environment with buckets and files
    prepare_mocked_bucket()

    # Checking if list_buckets() method returns a list
    assert isinstance(s3.list_buckets(), list)
