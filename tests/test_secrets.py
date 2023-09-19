"""Test cases for features defined on cloudgeass.aws.secrets module classes

This file handles the definition of all test cases for testing
SecretsManagerClient class and its features.

___
"""

# Importing libraries
import pytest
from moto import mock_secretsmanager

from tests.helpers.user_inputs import (
    MOCKED_SECRET_NAME,
    MOCKED_SECRET_VALUE
)


@pytest.mark.secrets
@pytest.mark.get_secret_string
@mock_secretsmanager
def test_get_secret_string_method_retrieves_the_expected_secret_string(
    sm, prepare_mocked_secrets
):
    """
    G: Given that users want to retrieve a secret string from a secret ID
    W: When the method get_secret_string() is called from SecretsManagerClient
    T: Then the expected secret string must be retrieved
    """

    # Preparing a mocked Secrets Manager environment with mocked secrets
    prepare_mocked_secrets()

    # Retrieving a secret string
    secret_string = sm.get_secret_string(secret_id=MOCKED_SECRET_NAME)

    assert secret_string == MOCKED_SECRET_VALUE


@pytest.mark.secrets
@pytest.mark.get_secret_string
@mock_secretsmanager
def test_error_on_trying_to_retrieve_a_secret_string_with_an_invalid_secret_id(
    sm, prepare_mocked_secrets
):
    """
    G: Given that users want to retrieve a secret string from a secret ID
    W: When the method get_secret_string() is called from SecretsManagerClient
       with an invalid secret id (i.e. a secret ID that doesn't exists)
    T: Then a exception must be thrown
    """

    # Preparing a mocked Secrets Manager environment with mocked secrets
    prepare_mocked_secrets()

    with pytest.raises(Exception):
        _ = sm.get_secret_string(secret_id="some-invalid-secret-id")
