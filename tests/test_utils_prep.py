"""Test cases for features defined on cloudgeass.utils.prep
 module.

___
"""


# Importing libraries
import pytest

from cloudgeass.utils.prep import categorize_file_size


@pytest.mark.utils_prep
@pytest.mark.categorize_file_size
def test_categorize_file_size_function_categorizes_bytes_scale():
    """
    G: Given that users want to apply some categorization in file sizes to
       get more friendly representation of sizes in different formats
    W: When the function categorize_file_size() is called to categorize
       a file size in bytes scale (i.e 1000)
    T: Then it must return an expected string in bytes format
       (i.e. "1000 B")
    """

    # Preparing variables to test
    test_size = 1000
    expected_output = "1000 B"

    assert categorize_file_size(size_in_bytes=test_size) == expected_output


@pytest.mark.utils_prep
@pytest.mark.categorize_file_size
def test_categorize_file_size_function_categorizes_kilobytes_scale():
    """
    G: Given that users want to apply some categorization in file sizes to
       get more friendly representation of sizes in different formats
    W: When the function categorize_file_size() is called to categorize
       a file size in kilobytes scale (i.e. 2048)
    T: Then it must return an expected string in kilobytes format
       (i.e. "2.00 KB")
    """

    # Preparing variables to test
    test_size = 2048
    expected_output = "2.00 KB"

    assert categorize_file_size(size_in_bytes=test_size) == expected_output


@pytest.mark.utils_prep
@pytest.mark.categorize_file_size
def test_categorize_file_size_function_categorizes_megabytes_scale():
    """
    G: Given that users want to apply some categorization in file sizes to
       get more friendly representation of sizes in different formats
    W: When the function categorize_file_size() is called to categorize
       a file size in megabytes scale (i.e. 1048576)
    T: Then it must return an expected string in megabytes format
       (i.e. "1.00 MB")
    """

    # Preparing variables to test
    test_size = 1048576
    expected_output = "1.00 MB"

    assert categorize_file_size(size_in_bytes=test_size) == expected_output


@pytest.mark.utils_prep
@pytest.mark.categorize_file_size
def test_categorize_file_size_function_categorizes_gibabytes_scale():
    """
    G: Given that users want to apply some categorization in file sizes to
       get more friendly representation of sizes in different formats
    W: When the function categorize_file_size() is called to categorize
       a file size in gibabytes scale (i.e. 1073741824)
    T: Then it must return an expected string in gibabytes format
       (i.e. "1.00 GB")
    """

    # Preparing variables to test
    test_size = 1073741824
    expected_output = "1.00 GB"

    assert categorize_file_size(size_in_bytes=test_size) == expected_output


@pytest.mark.utils_prep
@pytest.mark.categorize_file_size
def test_categorize_file_size_function_categorizes_terabytes_scale():
    """
    G: Given that users want to apply some categorization in file sizes to
       get more friendly representation of sizes in different formats
    W: When the function categorize_file_size() is called to categorize
       a file size in terabytes scale (i.e. 1099511627776)
    T: Then it must return an expected string in terabytes format
       (i.e. "1.00 TB")
    """

    # Preparing variables to test
    test_size = 1099511627776
    expected_output = "1.00 TB"

    assert categorize_file_size(size_in_bytes=test_size) == expected_output
