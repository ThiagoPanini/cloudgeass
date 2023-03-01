# A História da Criação da Biblioteca

## Uma Jornada Típica na AWS

Desenvolver soluções utilizando serviços da AWS é, em geral, uma tarefa desafiadora. Até que se tenha uma noção clara sobre as diversas possibilidades existentes, é preciso muito estudo, pesquisa e exploração.

Após o primeiro contato com o [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), percebi o quão imenso foi o leque de opções aberto. A partir deste ponto, mergulhei em jornadas de desenvolvimento de aplicações, sejam elas utilizando Lambda, EC2, Glue ou qualquer outro serviço que envolvia uma camada computacional onde o *boto3* pudesse brilhar.

Ao longo do tempo, notei que algumas operações codificadas com o citado SDK Python tinham características similares ou até mesmo idênticas. Por exemplo, a cada necessidade de listar objetos em um bucket S3 em uma nova aplicação, o mesmo código era simplesmente "copiado e colado". 

???+ quote "E assim surgiu o quesionamento:"

    *"Seria possível construir um conjunto de funcionalidades comuns do boto3 capazes de serem encapsuladas em uma nova biblioteca Python?"*

## O Início do Projeto

Buscando uma resposta para o questionamento acima, decidi mapear algumas ações comumente realizadas via *boto3* na AWS com uma boa margem de encapsulamento.

Como já citado anteriormente, imagine uma aplicação construída que, em um determinado momento, necessite obter uma relação de objetos presentes em um bucket S3. Um código para este processo poderia ser dado por:

```python
# Importando bibliotecas
import boto3

# Criando client s3
s3_client = boto3.client("s3")

# Realizando chamada de API para listagem
r = client.list_objects_v2(
    Bucket=bucket_name,
    Prefix=prefix
)

# Obtendo conteúdo do bucket
bucket_content = r["Contents"]
```

??? example "O código poderia ainda conter elementos adicionais"
    Algumas práticas como o tratamento de exceções e a escrita de mensagens claras de log poderiam fazer parte do *snippet* acima e sua versão final poderia ser dada por:

    ```python
    # Importando bibliotecas
    import boto3

    # Criando client s3
    s3_client = boto3.client("s3")

    # Realizando chamada de API para listagem de objetos de bucket
    try:
        r = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )

    except Exception as e:
        logger.error("Erro ao realizar chamada client.list_objects_v2() "
                     f"com Bucket={bucket_name} e Prefix={prefix}. "
                     f"Exception: {e}")
        raise e

    # Retornando conteúdo do bucket
    try:
        bucket_content = r["Contents"]

    except KeyError:
        logger.warning(f"Erro ao extrair conteúdo do bucket {bucket_name}. "
                       f"Provavelmente o bucket encontra-se sem objetos.")
        return None
    ```

Imagine repetir este bloco de código sempre que uma necessidade do tipo se fizer presente em cada nova aplicação construída na AWS. Um dos grandes objetivos do *cloudgeass*, como biblioteca, foi justamente endereçar a consolidação de tais operações comuns para que um processo simples como esse pudesse ser acionado por usuários a partir da chamada de uma única função.

```python
# Importando função
from cloudgeass.aws.s3 import bucket_objects_report

# Obtendo report de objetos de um bucket s3
bucket_objects = bucket_objects_report(bucket_name=bucket_name)
```

O resultado é dado como um DataFrame do pandas com detalhes ricos sobre os objetos armazenados em um determinado bucket. Além disso, todas as boas práticas de código, como o tratamento de exceção e as mensagens de logs, estariam prontamente codificadas e disponíveis para uso.

[![bucket_objects_report](https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/assets/imgs/readme-s3-example-bucket_objects_report.png?raw=true)](https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/assets/imgs/readme-s3-example-bucket_objects_report.png?raw=true)

## Ao Inifinito e Além

E assim, novas funcionalidades estão sendo pensadas, mapeadas, descobertas e implementadas de modo a suprir grande parte das necessidades mais comuns envolvendo operações na AWS.