# Getting the last date partition from a table in S3

## Feature overview

| | |
| :-- | :-- |
| 🚀 **Method** | [get_last_date_partition()](../../mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.get_last_date_partition) |
| 📄 **Description** | A method that enables users to get the last date partition (integer descending sorting) from a partitioned table stored in S3 |
| 📦 **Acessible from** | `cloudgeass.aws.s3.S3Client` |

## Feature demo

First of all, suppose we have a table in the [Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) that receives new data every day from an Glue job Spark ETL script. All the data are stored in S3. So, we want to build another ETL proccess that reads data from this daily table but only the last updated records.

The `get_last_date_partition()` method provides an easy way to look at a date partitioned table location on S3 and get the last available partition (i.e. the last date partition prefix that exists for the given table). Let's see how it works:


```python
# Importing the client class
from cloudgeass.aws.s3 import S3Client

# Creating a class instance
s3 = S3Client()

# Getting the last date partition from a table in S3
last_partition = s3.get_last_date_partition(
    bucket_name="datadelivery-sot-data-245034457829-us-east-1",
    table_prefix="tbsot_ecommerce_data/",
    date_partition_name="anomesdia",
    partition_mode="name=value"
)

# Checking the result
last_partition
```

???+ example "📽️ Getting the last date partition from a table stored in S3"
    ![A video gif showing the get_last_date_partition() method](https://github.com/ThiagoPanini/cloudgeass/blob/v2.0.x/docs/assets/gifs/s3-get_last_date_partition.gif?raw=true)


## Additional comments

???+ question "A little bit more about how the method really works"
    Well, in simple terms, that's what happens when users call the `get_last_date_partition()` method:

    1. First, the method [bucket_objects_report()](../../mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.bucket_objects_report) is called to return a pandas DataFrame with information about all objects within a given bucket **and a prefix** (in this case, a table prefix where the given table is stored)
    2. Then, a list of all object keys is obtained from the pandas DataFrame gotten in the previous step
    3. For all object keys from the previous step list, the method [get_date_partition_value_from_prefix()](../../mkdocstrings/s3.md/#cloudgeass.aws.s3.S3Client.get_date_partition_value_from_prefix) is called in order to get the value of all date partition prefix. The result of this loop is a list with all date partition values
    4. The list are sorted in descending order and the last value is obtained (i.e. the last available date partition)