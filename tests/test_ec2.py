"""Test cases for features defined on cloudgeass.aws.ec2.EC2Client module class

This file handles the definition of all test cases for testing EC2Client class
and its features.

___
"""

# Importing libraries
import pytest
from moto import mock_ec2
import responses

import os

from cloudgeass.aws.ec2 import LOCAL_IP_URL

from tests.helpers.user_inputs import (
    MOCKED_SG_NAME,
    LOCAL_IP_MOCKED_RESPONSE,
    MOCKED_KP_CONFIG,
    MOCKED_EC2_CONFIG
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
def test_sg_creation_with_a_name_that_already_exists_and_with_deletion_flag(
    ec2, mocked_sg_name: str = MOCKED_SG_NAME
):
    """
    G: Given that users want to create a preconfigured Security Group with an
       ingress rule that allows SSH access from the caller machine IP address
    W: When the method create_security_group_for_local_ssh_access() is called
       to create a Security Group with a name that already exists and the
       deletion flag set as True (delete_if_exists=True)
    T: Then the SG that already exists must be deleted and a new SG with the
       same name must be created
    """

    # Mocking a request response to get a mocked local IP address
    responses.add(
        method=responses.GET,
        url=LOCAL_IP_URL,
        body=LOCAL_IP_MOCKED_RESPONSE
    )

    # Creating a mocked SG just to simulate a SG that already exists
    r = ec2.create_security_group_for_local_ssh_access(
        sg_name=mocked_sg_name
    )

    # Trying to create a new SG with the same name
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
def test_sg_creation_with_a_name_that_already_exists_and_without_deletion_flag(
    ec2, mocked_sg_name: str = MOCKED_SG_NAME
):
    """
    G: Given that users want to create a preconfigured Security Group with an
       ingress rule that allows SSH access from the caller machine IP address
    W: When the method create_security_group_for_local_ssh_access() is called
       to create a Security Group with a name that already exists and the
       deletion flag set as False (delete_if_exists=False)
    T: Then the SG that already exists must be deleted and a new SG with the
       same name must be created
    """

    # Mocking a request response to get a mocked local IP address
    responses.add(
        method=responses.GET,
        url=LOCAL_IP_URL,
        body=LOCAL_IP_MOCKED_RESPONSE
    )

    # Creating a mocked SG just to simulate a SG that already exists
    r = ec2.create_security_group_for_local_ssh_access(
        sg_name=mocked_sg_name
    )

    # Trying to create a new SG with the same name
    r = ec2.create_security_group_for_local_ssh_access(
        sg_name=mocked_sg_name,
        delete_if_exists=False
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


@pytest.mark.ec2
@pytest.mark.create_key_pair
@mock_ec2
def test_create_key_pair_method_creates_a_key_pair(
    ec2, mocked_kp_config: dict = MOCKED_KP_CONFIG
):
    """
    G: Given that users want to create a new key pair to connect to their EC2
    W: When the method create_key_pair() is called
    T: Then the new key pair must exists in the account (checked by key pair
       ID)
    """

    # Creating a mocked key pair
    r = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        delete_if_exists=True,
        save_file=False
    )

    # Collecting key pair information for further evaluation
    kp_id = r["KeyPairId"]

    # Retrieving a list of KPs in the account to see if the new KP exists
    key_pairs = ec2.client.describe_key_pairs()
    key_pairs_ids = [kp["KeyPairId"] for kp in key_pairs["KeyPairs"]]

    assert kp_id in key_pairs_ids


@pytest.mark.ec2
@pytest.mark.create_key_pair
@mock_ec2
def test_kp_creation_with_a_name_that_already_exists_and_with_deletion_flag(
    ec2, mocked_kp_config: dict = MOCKED_KP_CONFIG
):
    """
    G: Given that users want to create a new key pair to connect to their EC2
    W: When the method create_key_pair() is called to create a key pair with a
       name that already exists and the deletion flag set as True
       (delete_if_exists=True)
    T: Then the KP that already exists must be deleted and a new KP with the
       same name must be created
    """

    # Creating a mocked KP just to simulate a SG that already exists
    r = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        save_file=False
    )

    # Trying to create a new KP with the same name
    r = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        delete_if_exists=True,
        save_file=False
    )

    # Collecting key pair information for further evaluation
    kp_id = r["KeyPairId"]

    # Retrieving a list of KPs in the account to see if the new KP exists
    key_pairs = ec2.client.describe_key_pairs()
    key_pairs_ids = [kp["KeyPairId"] for kp in key_pairs["KeyPairs"]]

    assert kp_id in key_pairs_ids


@pytest.mark.ec2
@pytest.mark.create_key_pair
@mock_ec2
def test_kp_creation_with_a_name_that_already_exists_and_without_deletion_flag(
    ec2, mocked_kp_config: dict = MOCKED_KP_CONFIG
):
    """
    G: Given that users want to create a new key pair to connect to their EC2
    W: When the method create_key_pair() is called to create a key pair with a
       name that already exists and the deletion flag set as False
       (delete_if_exists=False)
    T: Then the KP that already exists must be deleted and a new KP with the
       same name must be created
    """

    # Creating a mocked KP just to simulate a SG that already exists
    r = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        save_file=False
    )

    # Trying to create a new KP with the same name
    r = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        delete_if_exists=False,
        save_file=False
    )

    # Collecting key pair information for further evaluation
    kp_id = r["KeyPairId"]

    # Retrieving a list of KPs in the account to see if the new KP exists
    key_pairs = ec2.client.describe_key_pairs()
    key_pairs_ids = [kp["KeyPairId"] for kp in key_pairs["KeyPairs"]]

    assert kp_id in key_pairs_ids


@pytest.mark.ec2
@pytest.mark.create_key_pair
@mock_ec2
def test_create_key_pair_method_creates_and_saves_a_key_pair_file(
    ec2, mocked_kp_config: dict = MOCKED_KP_CONFIG
):
    """
    G: Given that users want to create a new key pair to connect to their EC2
    W: When the method create_key_pair() is called
    T: Then the new key pair must exists in the account (checked by key pair
       ID)
    """

    # Creating a mocked key pair
    _ = ec2.create_key_pair(
        key_name=mocked_kp_config["key_name"],
        key_type=mocked_kp_config["key_type"],
        key_format=mocked_kp_config["key_format"],
        delete_if_exists=True,
        save_file=True,
        path_to_save_file=mocked_kp_config["path_to_save_file"]
    )

    # Checking if there is a new key pair file saved on disk
    key_name = mocked_kp_config["key_name"]
    key_format = mocked_kp_config["key_format"]
    kp_filename = key_name + '.' + key_format

    assert kp_filename in os.listdir(mocked_kp_config["path_to_save_file"])

    # Tear down: deleting the kp file
    kp_path = os.path.join(
        mocked_kp_config["path_to_save_file"],
        kp_filename
    )
    os.remove(kp_path)


@pytest.mark.ec2
@pytest.mark.create_ec2_instance
@mock_ec2
def test_create_ec2_instance_method_creates_an_ec2_instance(
    ec2, mocked_ec2_config: dict = MOCKED_EC2_CONFIG
):
    """
    G: Given that users want to create a new EC2 instance
    W: When the method create_ec2_instance() is called
    T: Then there must be a new EC2 instance in the account (checked by
       instance ID)
    """

    # Creating a mocked EC2 instance
    r = ec2.create_ec2_instance(
        image_id=mocked_ec2_config["image_id"],
        instance_type=mocked_ec2_config["instance_type"]
    )

    # Retrieving the instance ID for further evaluation
    instance_id = r[0].id

    # Retrieving a list of KPs in the account to see if the new KP exists
    instances = ec2.client.describe_instances()
    instances_ids = [
        i["InstanceId"] for i in [
            instance["Instances"] for instance in instances["Reservations"]
        ][0]
    ]

    assert instance_id in instances_ids
