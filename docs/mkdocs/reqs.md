# Pré Requisitos de Uso

## Visão do Usuário

A biblioteca *cloudgeass* foi imaginada como uma forma rápida e eficiente de facilitar o trabalho do usuário no desenvolvimento de novas aplicações que envolvam operações na AWS. Para iniciar sua jornada de uso, basta ter em mãos:

- :snake: **Python 3 instalado**
- :key: **Acesso programático na AWS**

??? info "Configurando chaves de acesso programático na AWS"
    Para que as operações encapsuladas pelo *cloudgeass* tenham o efeito desejado, é preciso utilizá-lo a partir de uma entidade (usuário ou serviço) com acessos à provedora *cloud* já configurados.

    Em caso de utilização da biblioteca em um serviço AWS, como por exemplo, funções Lambda, as [roles IAM](https://docs.aws.amazon.com/pt_br/IAM/latest/UserGuide/id_roles.html) possuem o papel de fornecer os acessos temporários necessários para que as operações na nuvem possam ser executadas entre os serviços.

    Supondo agora o uso local da biblioteca para validação e construção de aplicações antes da fase de implantação na nuvem, é preciso realizar a configuração das credenciais através das chaves de acesso de um usuário que tenham as permissões atreladas à operação que se deseja fazer via *cloudgeass*. As chaves de acesso são dadas pela `access_key_id` e pela `secret_access_key` e seu processo de configuração é dado através do seguinte comando:
    
    ```bash
    aws configure
    ```

    Para maiores informações a cerca deste processo, a [seguinte documentação da AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) poderá auxiliar.

## Dependências da Biblioteca

No final do dia, o *cloudgeass* é um pacote Python que funciona como uma espécie de [*wrapper*](https://www.ionos.com/digitalguide/websites/web-development/what-is-a-wrapper/) do [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), famoso SDK Python para desenvolvimento na AWS. Neste contexo, uma série de outras bibliotecas fazem parte da orquestra e possuem papéis específicos.

Diante disso, além do *boto3* já citado, fazem parte das dependências do *cloudgeass*:

| **Biblioteca** | **Descrição e uso** |
| :-- | :-- |
| [pandas](https://pandas.pydata.org/) | Poderosa ferramenta de manipulação e análise de dados. Grande parte das funcionalidades do *cloudgeass* envolve a obtenção de respostas como DataFrames do pandas. |
| [s3fs](https://s3fs.readthedocs.io/en/latest/) | Funciona como uma interface para operações de arquivos no S3 via Python. No projeto, essa biblioteca é utilizada principalmente para habilitar a leitura de objetos no S3 via pandas através da URI dos mesmos. |
| [pyarrow](https://arrow.apache.org/docs/python/index.html) | Proporciona uma interface com o pandas para a leitura otimizada de arquivos com extensões específicas, como por exemplo, o formato parquet. |


???+ question "Preciso instalar cada uma das dependências?"
    A resposta é **não**. No [arquivo de setup](https://github.com/ThiagoPanini/cloudgeass/blob/main/setup.py) da biblioteca, todas as dependências listadas já estão endereçadas e serão automaticamente instaladas no ambiente virtual do usuário assim que o comando `pip install cloudgeass` for executado.
