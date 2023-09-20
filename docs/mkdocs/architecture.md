# The library in visual terms

As said before, *cloudgeass* is nothing more than a python package that uses boto3's clients and resources to put together some useful functions that may help users in their day to day tasks in AWS.

![Library drawio diagram](../../assets/diagrams/cloudgeass-diagram.drawio)

???+ tip "But where's the magic?"
    At the end of the day, the "little magic" behind *cloudgeass* is that the package provides modules and classes for each AWS service in a way that enables users to get boto's features in a higher level of abstraction.
    
    With this approach, it is possible to get many boto's client and resource methods for a given AWS service in just one *cloudgeass* method.

    :material-alert-decagram:{ .mdx-pulse .warning } Don't forget to check the [library structure](./library-structure.md) page to know more about it.