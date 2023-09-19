"""Test cases for features defined on cloudgeass.aws.ec2.EC2Client module class

This file handles the definition of all test cases for testing EC2Client class
and its features.

___
"""

# Importing libraries
import pytest
from moto import mock_ec2
import responses

from cloudgeass.aws.ec2 import LOCAL_IP_URL

from tests.helpers.user_inputs import (
    MOCKED_SG_NAME,
    LOCAL_IP_MOCKED_RESPONSE
)


@pytest.mark.ec2
@pytest.mark.get_default_vpc_id
@mock_ec2
def test_get_default_vpc_id_method_returns_vpc_id_when_there_is_a_default_vpc(
    ec2
):
    """
    G: Given that users want to get the default VPC ID from an AWS account
    W: When the method get_default_vpc_id() is called from EC2Client and,
       in fact there is a default VPC
    T: Then the return must be a string with the VPC ID
    """

    # Getting the mocked default VPC ID
    response = ec2.client.describe_vpcs()
    expected_default_vpc = [
        vpc["VpcId"] for vpc in response["Vpcs"] if vpc["IsDefault"]
    ][0]

    assert ec2.get_default_vpc_id() == expected_default_vpc


@pytest.mark.ec2
@pytest.mark.create_security_group_for_local_ssh_access
@mock_ec2
def test_create_security_group_for_local_ssh_access_method_creates_a_sec_group(
    ec2, mocked_sg_name: str = MOCKED_SG_NAME
):
    """
    G: Given that users want to create a preconfigured Security Group with an
       ingress rule that allows SSH access from the caller machine IP address
    W: When the method create_security_group_for_local_ssh_access() is called
    T: Then the new Security Group must exists in the account (check by
       Security Group ID)
    """

    # Mocking a request response to get a mocked local IP address
    responses.add(
        method=responses.GET,
        url=LOCAL_IP_URL,
        body=LOCAL_IP_MOCKED_RESPONSE
    )

    # Creating a mocked security group
    r = ec2.create_security_group_for_local_ssh_access(
        sg_name=mocked_sg_name,
        delete_if_exists=True
    )

    # Collecting the SG ID for further evaluation
    sg_id = r["GroupId"]

    # Retrieving a list of SGs in the account to see if the new SG exists
    sgs = ec2.client.describe_security_groups()
    sgs_ids = [sg["GroupId"] for sg in sgs["SecurityGroups"]]

    assert sg_id in sgs_ids


@pytest.mark.ec2
@pytest.mark.create_security_group_for_local_ssh_access
@mock_ec2
def test_security_group_created_has_a_ssh_inbound_rule_for_a_local_ip_address(
    ec2, mocked_sg_name: str = MOCKED_SG_NAME
):
    """
    G: Given that users want to create a preconfigured Security Group with an
       ingress rule that allows SSH access from the caller machine IP address
    W: When the method create_security_group_for_local_ssh_access() is called
    T: Then the new Security Group must have a inbound rule that allows SSH
       traffic for a given (mocked) IP address
    """

    # Mocking a request response to get a mocked local IP address
    responses.add(
        method=responses.GET,
        url=LOCAL_IP_URL,
        body=LOCAL_IP_MOCKED_RESPONSE
    )

    # Creating a mocked security group
    r = ec2.create_security_group_for_local_ssh_access(
        sg_name=mocked_sg_name,
        delete_if_exists=True
    )

    # Collecting the SG ID for further evaluation
    sg_id = r["GroupId"]

    # Retrieving the inbound rules for the recently created Security Grouyp
    sgs = ec2.client.describe_security_groups()
    sg_inbound_rules = [
        sg["IpPermissions"] for sg in sgs["SecurityGroups"]
        if sg["GroupId"] == sg_id
    ][0]

    # Check if there is only one inbound rule
    assert len(sg_inbound_rules) == 1

    # Check if the traffic is allowed from and to port 22
    assert sg_inbound_rules[0]["FromPort"] == 22
    assert sg_inbound_rules[0]["ToPort"] == 22

    # Check if traffic is allowed for the given (mocked) IP address
    allowed_ip_address = sg_inbound_rules[0]["IpRanges"][0]["CidrIp"]
    assert allowed_ip_address == LOCAL_IP_MOCKED_RESPONSE + "/32"
