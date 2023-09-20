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
import logging

from cloudgeass.utils.log import log_config


# Defining a variable with a website URL used to get the local IP address
LOCAL_IP_URL = "https://checkip.amazonaws.com"


class EC2Client():
    """Handles operations using ec2 client and resource from boto3.

    This class provides attributes and methods that can improve the way on how
    users operate with EC2 in AWS. In essence, it wraps some boto3 methods to
    build some useful features that makes it easy to operate with EC2 instances
    using python code.

    Examples:
        ```python
        # Importing the class
        from cloudgeass.aws.ec2 import EC2Client

        # Setting up an object and launching an EC2 instance
        ec2 = EC2Client()
        ec2.create_ec2_instance(
            image_id="some-image-id",
            instance_type="some-instance-type",
            key_name="some-key-pair-name",
            security_group_ids=["some-sg-id"]
        )
        ```

    Args:
        logger_level (int, optional):
            The logger level to be configured on the class logger object

    Attributes:
        logger (logging.Logger):
            A logger object to log steps according to a predefined logger level

        client (botocore.client.Ec2):
            An EC2 boto3 client to execute operations

        resource (botocore.client.Ec2):
            An EC2 boto3 resource to execute operations

    Methods:
        get_default_vpc_id() -> str:
            Retrieves the default VPC ID within an account

        create_security_group_for_local_ssh_access() -> dict:
            Creates a custom security group that allows SSH acces from local IP

        create_key_pair() -> dict:
            Creates and optionally saves a Key Pair for EC2 connection

        create_ec2_instance() -> dict:
            Creates an EC2 instance with basic configuration

    Tip: About the key word argument **client_kwargs:
        Users can get customized client and resource attributes for the given
        service passing additional keyword arguments. Under the hood, both
        client and resource class attributes are initialized as following:

        ```python
        # Setting up a boto3 client and resource
        self.client = boto3.client("ec2", **client_kwargs)
        self.resource = boto3.resource("ec2", **client_kwargs)
        ```
    """

    def __init__(self, logger_level=logging.INFO, **client_kwargs):
        # Setting up a logger object
        self.logger_level = logger_level
        self.logger = log_config(logger_level=self.logger_level)

        # Setting up a boto3 client and resource
        self.client = boto3.client("ec2", **client_kwargs)
        self.resource = boto3.resource("ec2", **client_kwargs)

    def get_default_vpc_id(self) -> str:
        """
        Retrieves the default VPC ID from the AWS account.

        Returns:
            str: The ID of the default VPC.

        Raises:
            botocore.exceptions.ClientError: If there's an error while\
                making the request.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.ec2 import EC2Client

            # Creating an instance
            ec2 = EC2Client()

            # Getting the default VPC ID from an AWS account
            default_vpc_id = ec2.get_default_vpc_id()
            ```
        """

        # Describing all VPCs and searching for the default one
        response = self.client.describe_vpcs()

        for vpc in response["Vpcs"]:
            if vpc["IsDefault"]:
                return vpc["VpcId"]

    def create_security_group_for_local_ssh_access(
        self,
        sg_name: str = "ssh-local-connection-sg",
        delete_if_exists: bool = True,
        tags: list = []
    ) -> dict:
        """
        Creates a preconfigured security group allowing local SSH access.

        Args:
            sg_name (str, optional):
                Name for the security group.

            delete_if_exists (bool, optional):
                Whether to delete existing security group if found with the
                same name.

            tags (list, optional):
                Additional tags for the security group.

        Returns:
            dict: Response from the create_security_group call.

        Raises:
            botocore.exceptions.ClientError: If there's an error while\
                making the request.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.ec2 import EC2Client

            # Creating an instance
            ec2 = EC2Client()

            # Creating a custom SG that allows SSH traffic from local machine
            response = ec2.create_security_group_for_local_ssh_access()
            ```
        """

        # Setting up tags
        resource_tags = tags + [
            {
                "Key": "Name",
                "Value": sg_name
            }
        ]

        self.logger.debug("Checking if the given SG already exists")
        response = self.client.describe_security_groups()
        for sg in response["SecurityGroups"]:
            if sg["GroupName"] == sg_name:
                # Security group exists. Checking the chosen delete behavior
                if delete_if_exists:
                    self.logger.debug(f"Security group {sg_name} already "
                                      "exists and the deletion flag is set "
                                      "as True. Proceeding to delete the "
                                      "security group.")
                    try:
                        self.client.delete_security_group(GroupName=sg_name)
                        self.logger.debug(f"Successfuly deleted the {sg_name}")
                    except Exception as e:
                        self.logger.error("Error on trying to delete the SG "
                                          f"{sg_name}. Exception: {e}")
                        raise e

                else:
                    self.logger.debug(f"Security group {sg_name} already "
                                      "and the deletion flag is set as False. "
                                      "Adding a random suffix at the name of "
                                      "the security group to be created in "
                                      "order to avoid errors.")

                    random_suffix = "-" + "".join(
                        random.choices(string.ascii_letters, k=7)
                    )
                    sg_name += random_suffix

        # Creating the security group after the validation
        self.logger.debug(f"Creating security group {sg_name}")
        try:
            sg_response = self.client.create_security_group(
                GroupName=sg_name,
                Description="Enables port 22 from a local IP address",
                VpcId=self.get_default_vpc_id(),
                TagSpecifications=[
                    {
                        "ResourceType": "security-group",
                        "Tags": resource_tags
                    }
                ]
            )
            self.logger.debug(f"Successfuly created security group {sg_name}")
        except Exception as e:
            self.logger.error(f"Error on trying to create security group "
                              f"{sg_name}. Exception: {e}")
            raise e

        # Setting up igress rules
        try:
            # Getting the IP address of the runner machine in CIDR format
            local_machine_ip = requests.get(LOCAL_IP_URL).text.strip()

            # Creating a ingress rule to allow SSH traffic from local IP
            _ = self.client.authorize_security_group_ingress(
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
            self.logger.debug("Successfully created an inbound rule that "
                              "allows SSH traffic for the caller machine IP "
                              "address")
        except Exception as e:
            self.logger.error("Error on trying to get the caller machine IP "
                              "address and setting up an inbound rule that "
                              f"allows SSH traffic from it. Exception: {e}")

        # Returning the response of security group creation call
        return sg_response

    def create_key_pair(
        self,
        key_name: str = "local-connection-kp",
        key_type: str = "rsa",
        key_format: str = "ppk",
        delete_if_exists: bool = True,
        save_file: bool = True,
        path_to_save_file: str = ".",
        tags: list = []
    ) -> dict:
        """
        Creates a key pair and optionally saves it to a file.

        Args:
            key_name (str, optional):
                A key pair name

            key_type (str, optional):
                Key pair type

            key_format (str, optional):
                Key pair format. Choose between "pem" and "ppk"

            delete_if_exists (bool, optional):
                Whether to delete existing key pair if found with the same name

            save_file (bool, optional):
                Whether to save the key material to a file.

            path_to_save_file (str, optional):
                Path to save the file.

            tags (list, optional):
                Additional tags for the key pair.

        Returns:
            dict: Response from the create_key_pair call.

        Raises:
            botocore.exceptions.ClientError: If there's an error while\
                making the request.
            OSError: If there's an error while saving the key to a file.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.ec2 import EC2Client

            # Creating an instance
            ec2 = EC2Client()

            # Creating and saving a Key Pair for an EC2 connection
            response = ec2.create_key_pair(
                key_type="rsa",
                key_format="ppk",
                save_file=True,
                path_to_save_file="../some-folder/"
            )
            ```
        """

        # Setting up tags
        resource_tags = tags + [
            {
                "Key": "Name",
                "Value": key_name
            }
        ]

        self.logger.debug("Checking if the given key pair already exists")
        response = self.client.describe_key_pairs()
        for kp in response["KeyPairs"]:
            if kp["KeyName"] == key_name:
                # Key pair already exists. Checking the chosen delete behavior
                if delete_if_exists:
                    self.logger.debug(f"Key pair {key_name} already exists "
                                      "and the deletion flag is set as True. "
                                      "Proceeding to delete the key pair.")
                    try:
                        self.client.delete_key_pair(KeyName=key_name)
                        self.logger.debug("Successfuly deleted the key pair "
                                          f"{key_name}")
                    except Exception as e:
                        self.logger.error("Error on trying to delete the key "
                                          f"pair {key_name}. Exception: {e}")
                        raise e

                else:
                    self.logger.debug(f"Key pair {key_name} already exists "
                                      "and the deletion flag is set as False. "
                                      "Adding a random suffix at the name of "
                                      "the key pair to be create to avoid "
                                      "errors.")

                    # Creating a random suffix
                    random_suffix = "-" + "".join(
                        random.choices(string.ascii_letters, k=7)
                    )

                    # Adding the random sufix to the key pair name
                    key_name += random_suffix

        # Creating a new key pair
        self.logger.debug(f"Creating key pair {key_name}")
        try:
            kp_response = self.client.create_key_pair(
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
            self.logger.debug(f"Successfuly created key pair {key_name}")

        except Exception as e:
            self.logger.error(f"Error on trying to create key pair "
                              f"{key_name}. Exception: {e}")
            raise e

        # Saving the key material (if applicable)
        if save_file:
            file_name = f"{key_name}.{key_format}"
            with open(os.path.join(path_to_save_file, file_name), "w") as f:
                f.write(kp_response["KeyMaterial"])

        # Returning the response of key pai creation call
        return kp_response

    def create_ec2_instance(
        self,
        image_id: str = "ami-04cb4ca688797756f",
        instance_type: str = "t2.micro",
        key_name: str = "",
        security_group_ids: list = list(),
        min_count: int = 1,
        max_count: int = 1,
        status_check_sleep_time: int = 5
    ) -> dict:
        """
        Creates a preconfigured EC2 instance.

        Args:
            key_name (str):
                Name of the key pair to associate with the instance.

            security_group_ids (list):
                List of security group IDs to associate with the instance.

            image_id (str, optional):
                AMI ID for the instance.

            instance_type (str, optional):
                Type of the instance.

            min_count (int, optional):
                Minimum number of instances to launch.

            max_count (int, optional):
                Maximum number of instances to launch.

            status_check_sleep_time (int, optional):
                Time to wait between status checks that aims to verify if
                the created instance is already running.

        Returns:
            dict: Response from the create_instances call.

        Raises:
            botocore.exceptions.ClientError: If there's an error while\
                making the request.

        Examples:
            ```python
            # Importing the class
            from cloudgeass.aws.ec2 import EC2Client

            # Creating an instance
            ec2 = EC2Client()

            # Creating and saving a Key Pair for an EC2 connection
            response = ec2.create_ec2_instance(
                image_id="some-image-id",
                instance_type="some-instance-type",
                key_name="some-key-pair-name",
                security_group_ids=["some-sg-id"]
            )
            ```
        """

        self.logger.debug("Creating a new EC2 instance")
        try:
            ec2_response = self.resource.create_instances(
                ImageId=image_id,
                InstanceType=instance_type,
                SecurityGroupIds=security_group_ids,
                KeyName=key_name,
                MinCount=min_count,
                MaxCount=max_count
            )

            # Getting the instance if for further status check
            instance_id = ec2_response[0].id
            self.logger.debug("Successfully created a new EC2 instance "
                              f"{instance_id}")
        except Exception as e:
            self.logger.error(f"Error on creating a new EC2 instance. "
                              f"Exception: {e}")

        # Checking the status and wait until instance is running
        self.logger.debug(f"Checking the instance {instance_id} status and "
                          "waiting until it's running")

        status_response = self.client.describe_instance_status()
        for instance in status_response["InstanceStatuses"]:
            if instance["InstanceId"] == instance_id:
                # Getting the status of the new instance
                status = instance["InstanceState"]["Name"]
                while status.strip().lower() != "running":
                    # Wait some time until next status check
                    self.logger.debug(f"The instance is still {status}")
                    time.sleep(status_check_sleep_time)
                    status = instance["InstanceState"]["Name"]

                self.logger.debug(f"The instance {instance_id} is now running "
                                  "and ready to connect ")
                break

        return ec2_response
