# Cloudgeass library structure

Before your first experience with *cloudgeass*, it's important to know how the package is organized with its modules and classes.


## Modules

Getting straight to the point, each *cloudgeass* module represents an AWS service that contains at least one class and a bunch of methods built from both boto's source client and resource for that service.

In other words, some modules that you can find here are:

- `cloudgeass.aws.s3` for working with S3 service
- `cloudgeass.aws.ec2` for working with EC2 service
- `cloudgeass.aws.secrets` for working with Secrets Manager service
- *and some others*

## Classes

Each one of the aforementioned modules have at least one class that can be imported on user's application in order to provide access to all features for that given AWS service. So, we have:

- `cloudgeass.aws.s3.S3Client` class with methods to operate with S3 service
- `cloudgeass.aws.ec2.EC2Client` class with methods to operate with EC2 service
- `cloudgeass.aws.secrets.SecretsManagerClient` class with methods to operate with Secrets Manager service
- *and some others*

## Attributes

All *cloudgeass'* service classes are initialized with a set of predefined attributes to make the work easier. Those basic attributes are:

| **Service class attribute** | **Description** |
| :-- | :-- |
| `self.logger` | A preconfigured logger object to build and stream informative log messages |
| `self.client` | A boto3 client for the given service |
| `self.resource` | A boto3 resource for the given service |

The attributes can be externally accessed for all class instances created on an application. This means users can build an application using both *cloudgeass* and source boto3 code.

## Methods

Finally, each service class has its own set of methods that, in fact, enables the power of using *cloudgeass* to do simple tasks in an AWS environment. To mention some of them, we have:

- [S3Client.get_last_date_partition()](./mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.get_last_date_partition) to get the last date partition from a table stored in S3
- [EC2Client.get_default_vpc_id()](./mkdocstrings/ec2.md/#cloudgeass.aws.ec2.EC2Client.get_default_vpc_id) to get the default VPC ID of an AWS account
- [SecretsManagerClient.get_secret_string()](./mkdocstrings/secrets.md/#cloudgeass.aws.secrets.SecretsManagerClient.get_secret_string) to get a secret string given a secret ID