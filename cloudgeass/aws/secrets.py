"""
Módulo responsável por alocar funcionalidades relacionadas ao client do
Secrets Manager no boto3. O grande objetivo deste módulo é fornecer ao usuário
um conjunto de funções que visam facilitar operações envolvendo o gerenciamento
de segredos na AWS.

___
"""

# Importando bibliotecas
import boto3

from cloudgeass.utils.log import log_config


# Configurando objeto de logger
logger = log_config(logger_name=__file__)

# Instanciando client e recurso do Secrets Manager para uso nas funções
client = boto3.client("secretsmanager")


# Coletando o valor de um segredo através de seu ID
def get_secret_string(secret_id: str, client=client) -> str:
    """Coleta de string de segredo existente no Secrets Manager.

    Com esta funcionalidade, os usuários podem passar um ID de segredo e obter,
    como resposta, a string referente ao valor do segredo armazenado.

    Examples:
        ```python
        from cloudgeass.aws.secrets import get_secret_string

        secret = get_secret_string(secret_id="some-secret-id")
        ```

    Args:
        secret_id (str):
            ID do segredo existente no Secrets Manager

        client (botocore.client.SecretsManager):
            Client do Secrets Manager instanciado via boto3

    Returns:
        Valor do segredo identificado pelo ID em formato de string

    Raises:
        Exception: Exceção ao obter falha na tentativa de ralizar a chamada\
        client.get_secret_value()
    """

    # Realizando chamada de obtendo string do segredo
    logger.info(f"Coletando segredo {secret_id} do Secrets Manager")
    try:
        response = client.get_secret_value(SecretId=secret_id)
        return response["SecretString"]

    except Exception as e:
        logger.error(f"Erro ao obter resposta do segredo {secret_id}. "
                     f"Exception: {e}")
        raise e
