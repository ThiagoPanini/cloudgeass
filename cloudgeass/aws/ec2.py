"""Building features using boto3's EC2 client and resource.

This module provides utility functions for working with Amazon Web Services
(AWS) using the Boto3 library. It includes functions to retrieve the default
VPC ID, create a preconfigured security group for local SSH access,
create a key pair, and create a preconfigured EC2 instance.

Functions:
    - get_default_vpc_id:
        Retrieves the default VPC ID from the AWS account.

    - create_security_group_for_local_ssh_access:
        Creates a preconfigured security group allowing local SSH access.

    - create_key_pair:
        Creates a key pair and optionally saves it to a file.

    - create_ec2_instance:
        Creates a preconfigured EC2 instance.

Usage:
    # Importing the module
    from cloudgeass.aws import ec2

    # Retrieve the default VPC ID
    default_vpc_id = ec2.get_default_vpc_id()

    # Create a security group for local SSH access
    sg_response = ec2.create_security_group_for_local_ssh_access()

    # Create a key pair and save it to a file
    kp_response = ec2.create_key_pair()

    # Create a preconfigured EC2 instance
    instance_response = ec2.create_ec2_instance(
        key_name=kp_response["KeyName"],
        security_group_ids=[sg_response["GroupId"]]
    )

Note:
    This module requires proper AWS credentials to be configured on the system.
    Make sure to have Boto3 library installed.

___
"""

# Importing libraries
import boto3
import string
import random
import requests
import os
import time

from cloudgeass.utils.log import log_config


# Setting up a logger object
logger = log_config(__file__)

# Getting EC2 client and resource
ec2_client = boto3.client("ec2")
ec2_resource = boto3.resource("ec2")


# Getting the default VPC ID from an AWS account
def get_default_vpc_id(ec2_client=ec2_client) -> str:
    """
    Retrieves the default VPC ID from the AWS account.

    Args:
        ec2_client (boto3.client, optional): EC2 client.

    Returns:
        str: The ID of the default VPC.

    Raises:
        botocore.exceptions.ClientError: If there's an error while making the\
            request.
    """

    # Describing all VPCs and searching for the default one
    response = ec2_client.describe_vpcs()

    for vpc in response["Vpcs"]:
        if vpc["IsDefault"]:
            return vpc["VpcId"]


# Creating a preconfigured security group for local SSH access
def create_security_group_for_local_ssh_access(
    ec2_client=ec2_client,
    sg_name: str = "ssh-local-connection-sg",
    delete_if_exists: bool = True,
    tags: list = []
):
    """
    Creates a preconfigured security group allowing local SSH access.

    Args:
        ec2_client (boto3.client, optional):
            EC2 client.

        sg_name (str, optional):
            Name for the security group.

        delete_if_exists (bool, optional):
            Whether to delete existing security group if found with the same
            name.

        tags (list, optional):
            Additional tags for the security group.

    Returns:
        dict: Response from the create_security_group call.

    Raises:
        botocore.exceptions.ClientError: If there's an error while making the\
            request.
    """

    # Setting up tags
    resource_tags = tags + [
        {
            "Key": "Name",
            "Value": sg_name
        }
    ]

    logger.info("Checking if the given security group already exists")
    response = ec2_client.describe_security_groups()
    for sg in response["SecurityGroups"]:
        if sg["GroupName"] == sg_name:
            # Security group exists. Checking the chosen delete behavior
            if delete_if_exists:
                logger.info(f"Security group {sg_name} already exists and the "
                            "deletion flag is set as True. Proceeding to "
                            "delete the security group.")
                try:
                    ec2_client.delete_security_group(GroupName=sg_name)
                    logger.info(f"Successfuly deleted the SG {sg_name}")
                except Exception as e:
                    logger.error(f"Error on trying to delete the SG {sg_name}."
                                 f" Exception: {e}")
                    raise e

            else:
                logger.info(f"Security group {sg_name} already exists and the "
                            "deletion flag is set as False. Adding a random "
                            "suffix at the name of the security group to be "
                            "created in order to avoid errors.")

                random_suffix = "-" + "".join(
                    random.choices(string.ascii_letters, k=7)
                )
                sg_name += random_suffix

    # Creating the security group after the validation
    logger.info(f"Creating security group {sg_name}")
    try:
        sg_response = ec2_client.create_security_group(
            GroupName=sg_name,
            Description="Enables port 22 from a local IP address",
            VpcId=get_default_vpc_id(),
            TagSpecifications=[
                {
                    "ResourceType": "security-group",
                    "Tags": resource_tags
                }
            ]
        )
        logger.info(f"Successfuly created security group {sg_name}")
    except Exception as e:
        logger.error(f"Error on trying to create security group {sg_name}. "
                     f"Exception: {e}")
        raise e

    # Setting up igress rules
    try:
        local_machine_ip = requests.get('https://checkip.amazonaws.com')\
            .text.strip()
        _ = ec2_client.authorize_security_group_ingress(
            GroupName=sg_name,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [
                        {
                            "CidrIp": f"{local_machine_ip}/32"
                        }
                    ]
                }
            ]
        )
        logger.info("Successfully created an inbound rule that allows SSH "
                    "traffic for the caller machine IP address")
    except Exception as e:
        logger.error("Error on trying to get the called machine IP address "
                     "and setting up an inbound rule that allows SSH traffic "
                     f"from it. Exception: {e}")

    # Returning the response of security group creation call
    return sg_response


# Creating a key pair
def create_key_pair(
    ec2_client=ec2_client,
    key_name: str = "local-connection-kp",
    key_type: str = "rsa",
    key_format: str = "ppk",
    delete_if_exists: bool = True,
    save_file: bool = True,
    path_to_save_file: str = ".",
    tags: list = []
):
    """
    Creates a key pair and optionally saves it to a file.

    Args:
        ec2_client (boto3.client, optional): EC2 client.
        key_name (str, optional): Name for the key pair.
        key_type (str, optional): Type of the key.
        key_format (str, optional): Format of the key.
        delete_if_exists (bool, optional): Whether to delete existing key pair
            if found with the same name.
        save_file (bool, optional): Whether to save the key material to a file.
        path_to_save_file (str, optional): Path to save the file.
        tags (list, optional): Additional tags for the key pair.

    Returns:
        dict: Response from the create_key_pair call.

    Raises:
        botocore.exceptions.ClientError: If there's an error while making the\
            request.
        OSError: If there's an error while saving the key to a file.
    """

    # Setting up tags
    resource_tags = tags + [
        {
            "Key": "Name",
            "Value": key_name
        }
    ]

    logger.info("Checking if the given security group already exists")
    response = ec2_client.describe_key_pairs()
    for kp in response["KeyPairs"]:
        if kp["KeyName"] == key_name:
            # Key pair already exists. Checking the chosen delete behavior
            if delete_if_exists:
                logger.info(f"Key pair {key_name} already exists and the "
                            "deletion flag is set as True. Proceeding to "
                            "delete the key pair.")
                try:
                    ec2_client.delete_key_pair(KeyName=key_name)
                    logger.info(f"Successfuly deleted the key pair {key_name}")
                except Exception as e:
                    logger.error("Error on trying to delete the key pair "
                                 f"{key_name}. Exception: {e}")
                    raise e

            else:
                logger.info(f"Key pair {key_name} already exists and the "
                            "deletion flag is set as False. Adding a random "
                            "suffix at the name of the key pair to be create "
                            "to avoid errors.")

                random_suffix = "-" + "".join(
                    random.choices(string.ascii_letters, k=7)
                )
                key_name += random_suffix

    # Creating a new key pair
    try:
        logger.info(f"Creating key pair {key_name}")
        kp_response = ec2_client.create_key_pair(
            KeyName=key_name,
            KeyType=key_type,
            KeyFormat=key_format,
            TagSpecifications=[
                {
                    "ResourceType": "key-pair",
                    "Tags": resource_tags
                }
            ]
        )
        logger.info(f"Successfuly created key pair {key_name}")

    except Exception as e:
        logger.error(f"Error on trying to create key pair {key_name}. "
                     f"Exception: {e}")
        raise e

    # Saving the key material (if applicable)
    if save_file:
        file_name = f"{key_name}.{key_format}"
        with open(os.path.join(path_to_save_file, file_name), "w") as f:
            f.write(kp_response["KeyMaterial"])

    # Returning the response of key pai creation call
    return kp_response


# Creating an simple and preconfigured EC2 instance
def create_ec2_instance(
    key_name: str,
    security_group_ids: list,
    ec2_resource=ec2_resource,
    ec2_client=ec2_client,
    image_id: str = "ami-04cb4ca688797756f",
    instance_type: str = "t2.micro",
    min_count: int = 1,
    max_count: int = 1,
    status_check_sleep_time: int = 5
):
    """
    Creates a preconfigured EC2 instance.

    Args:
        key_name (str): Name of the key pair to associate with the instance.
        security_group_ids (list): List of security group IDs to associate
            with the instance.
        ec2_resource (boto3.resource, optional): EC2 resource.
        ec2_client (boto3.client, optional): EC2 client.
        image_id (str, optional): AMI ID for the instance.
        instance_type (str, optional): Type of the instance.
        min_count (int, optional): Minimum number of instances to launch.
        max_count (int, optional): Maximum number of instances to launch.
        status_check_sleep_time (int, optional): Time to wait between status
            checks.

    Returns:
        dict: Response from the create_instances call.

    Raises:
        botocore.exceptions.ClientError: If there's an error while making the\
            request.
    """

    # Calling the method to create a new EC2 instance
    try:
        logger.info("Creating a new EC2 instance")
        ec2_response = ec2_resource.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            SecurityGroupIds=security_group_ids,
            KeyName=key_name,
            MinCount=min_count,
            MaxCount=max_count
        )

        # Getting the instance if for further status check
        instance_id = ec2_response[0].id
        logger.info(f"Successfully created a new EC2 instance {instance_id}")
    except Exception as e:
        logger.error(f"Error on creating a new EC2 instance. Exception: {e}")

    # Checking the status and wait until instance is running
    logger.info(f"Checking the instance {instance_id} status "
                "and waiting until it's running")
    status_response = ec2_client.describe_instance_status()
    for instance in status_response["InstanceStatuses"]:
        if instance["InstanceId"] == instance_id:
            # Get the status of the new instance
            status = instance["InstanceState"]["Name"]
            while status.strip().lower() != "running":
                # Wait some time until next status check
                logger.info(f"The instance is still in {status} status")
                time.sleep(status_check_sleep_time)
                status = instance["InstanceState"]["Name"]

            logger.info(f"The instance {instance_id} is now running "
                        "and ready to connect ")
            break

    return ec2_response
