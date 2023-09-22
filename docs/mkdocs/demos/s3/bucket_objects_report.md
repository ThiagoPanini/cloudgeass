# Getting a report of all objects within a bucket

## Feature overview

| | |
| :-- | :-- |
| 🚀 **Method** | [bucket_objects_report()](../../mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.bucket_objects_report) |
| 📄 **Description** | A method that enables users to get a pandas DataFrame with a friendly report of all objects within a bucket (and optionally within a bucket prefix) |
| 📦 **Acessible from** | `cloudgeass.aws.s3.S3Client` |

## Feature demo

In this demo, we will get a pandas DataFrame with useful details about all objects within a bucket called `datadelivery-sor-data-282495905450-us-east-1` (adding a filter prefix to get only objects inside `br_ecommerce/`).

```python
# Importing the client class
from cloudgeass.aws.s3 import S3Client

# Creating a class instance
s3 = S3Client()

# Getting a report of objects within a bucket
df_objects_report = s3.bucket_objects_report(
    bucket_name="datadelivery-sor-data-282495905450-us-east-1",
    prefix="br_ecommerce"
)

# Checking the result
df_objects_report.head()
```

???+ example "📽️ Getting a report of all objects within a S3 bucket"
    ![A video gif showing the bucket_objects_report() method](https://github.com/ThiagoPanini/cloudgeass/blob/v2.0.x/docs/assets/gifs/s3-bucket_objects_report.gif?raw=true)


## Additional comments

This method uses a source boto3 s3 client [list_objects_v2()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html) with a bucket name and a prefix parameteres to filter the data analyzed.

By using the `bucket_objects_report()` method, *cloudgeass* users can have in hands a pandas DataFrame in a friendly format that enables the extraction of many insights, such as:

- The size of the largest objects in the bucket
- The name and the file format of all objects stored in the given bucket
- The storage class of all objects (optimization opportunities)
- *and many others*