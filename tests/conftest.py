"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
from moto import mock_s3

from cloudgeass.aws.s3 import S3Client

from tests.helpers.user_inputs import (
    MOCKED_REGION,
    MOCKED_BUCKET_CONTENT
)


""" -------------------------------------------------
    FIXTURES: S3Client class
    Bulding fixtures for cloudgeass.aws.s3.S3Client
------------------------------------------------- """


# A S3Client class object
@pytest.fixture
@mock_s3
def s3(region_name: str = MOCKED_REGION):
    return S3Client(region_name=region_name)


# Building a function as a fixture to create a mocked bucket with objects
@pytest.fixture()
@mock_s3
def prepare_mocked_bucket(s3: S3Client):
    def create_elements():
        # Lopping over a dictionary with all definition of mock content for s3
        for bucket_name, content_definition in MOCKED_BUCKET_CONTENT.items():
            # Creating a mocked bucket
            s3.resource.create_bucket(Bucket=bucket_name)

            # Putting mocked objects in this mocked bucket
            for _, content in content_definition.items():
                s3.client.put_object(
                    Bucket=bucket_name,
                    Body=content["Body"],
                    Key=content["Key"]
                )

    return create_elements
