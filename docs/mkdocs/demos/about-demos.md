# The place where you see some things in practice

This section brings some examples of using *cloudgeass* methods in practical scenarios. By the way, there would be virtually impossible to record a demo for every method that are currently available on the library, so here you will see just some of them in practice.

???+ tip "So what do we have by now?"
    The demos are divided by modules and by now we have the following scenarios:

    - **S3 module**
        - [Getting a list of all buckets within an account](./s3/list_buckets.md)
        - [Getting a pandas DataFrame with a report of all objects within a bucket](./s3/bucket_objects_report.md)
        - :material-alert-decagram:{ .mdx-pulse .warning } [Getting the last date partition of a partitioned table stored in S3](./s3/get_last_date_partition.md)

    ___

    - **EC2 module**
        - [Getting the ID of the account's default VPC](./ec2/get_default_vpc_id.md)

    ___

    - **Secrets module**
        - [Getting a secret value from a given secret name](./secrets/get_secret_string.md)


## Official docs

Even though there aren't demos for all available methods, you can always use the [official documentation page](../mkdocstrings/s3.md) where all classes and methods were thoroughly documented in order to delivery the best experience for all users.