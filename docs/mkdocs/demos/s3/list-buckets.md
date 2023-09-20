# Listing all buckets of an AWS account

## Feature overview

| | |
| :-- | :-- |
| 🚀 **Method** | [list_buckets()](../../mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.list_buckets) |
| 📄 **Description** | A method that enables users to get a list with all available buckets in an AWS account |
| 📦 **Acessible from** | `cloudgeass.aws.s3.S3Client` |

## Feature demo

To get a list of all buckets of an AWS account, users can use the following block of code:

```python
# Importing the client class
from cloudgeass.aws.s3 import S3Client

# Creating a class instance
s3 = S3Client()

# Getting a list of buckets
buckets = s3.list_buckets()
```

???+ example "📽️ Getting the list of buckets"
    