# Getting the ID from the default VPC

## Feature overview

| | |
| :-- | :-- |
| 🚀 **Method** | [get_default_vpc_id()](../../mkdocstrings/ec2.md/#cloudgeass.aws.ec2.EC2Client.get_default_vpc_id) |
| 📄 **Description** | A method that enables users to get the ID of the account's default VPC |
| 📦 **Acessible from** | `cloudgeass.aws.ec2.EC2Client` |

## Feature demo

The EC2Client `get_default_vpc_id()` method is built from a [boto3 ec2 client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html) method called [describe_vpcs()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpcs.html). It takes the method's response and gets the VPC ID if the response key 'IsDefault' is true. Let's see this in practice.


```python
# Importing the client class
from cloudgeass.aws.ec2 import EC2Client

# Creating a class instance
ec2 = EC2Client()

# Getting the ID from the default VPC
vpc_id = ec2.get_default_vpc_id()
```

???+ example "📽️ Getting the ID from the default VPC in an AWS account"
    ![A video gif showing the get_default_vpc_id() method](https://github.com/ThiagoPanini/cloudgeass/blob/v2.0.x/docs/assets/gifs/ec2-get_default_vpc_id.gif?raw=true)
