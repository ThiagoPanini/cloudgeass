# Getting a secret value from Secrets Manager

## Feature overview

| | |
| :-- | :-- |
| 🚀 **Method** | [get_secret_string()](../../mkdocstrings/secrets.md/#cloudgeass.aws.secrets.SecretsManagerClient.get_secret_string) |
| 📄 **Description** | A method that can be used to retrieve a secret string from a secret ID stored in Secrets Manager|
| 📦 **Acessible from** | `cloudgeass.aws.secrets.SecretsManagerClient` |

## Feature demo

The SecretsManagerClient `get_secret_string()` method is built from a [boto3 secretsmanager client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html) method called [get_secret_value()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html).


```python
# Importing the client class
from cloudgeass.aws.secrets import SecretsManagerClient

# Creating a class instance
sm = SecretsManagerClient()

# Getting a secret value from Secrets Manager
my_secret_value = sm.get_secret_string(
    secret_id="my-secret-name"
)
```

???+ example "📽️ Getting a secret value from a given secret ID"
    ![A video gif showing the get_secret_string() method](https://github.com/ThiagoPanini/cloudgeass/blob/v2.0.x/docs/assets/gifs/secrets-get_secret_string.gif?raw=true)
