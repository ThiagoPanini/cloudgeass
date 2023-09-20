"""Test cases for features defined on cloudgeass.utils.log module.

___
"""

# Importing libraries
import pytest
import logging

from cloudgeass.utils.log import log_config


@pytest.mark.utils_log
@pytest.mark.log_config
def test_log_config_function_returns_a_logger_object():
    """
    G: Given that users want to obtain a preconfigured logger object
    W: When the function function log_config() is called
    T: Then it must return a logging.Logger object
    """

    logger = log_config()
    assert isinstance(logger, logging.Logger)
