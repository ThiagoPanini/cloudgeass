# Frequently Access Questions

## Usabilidade

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } Quais os conhecimentos necessários para poder utilizar a biblioteca cloudgeass?

Como recomendação, é **desejável** (mas não obrigatório) que usuários que queiram iniciar sua jornada de uso no *cloudgeass* tenham conhecimentos **básicos** em:

- Python
- AWS

De fato, o *cloudgeass* é uma biblioteca Python que consolida operações comuns utilizadas na AWS. Ter uma noção básica sobre estes dois universos é importante para usá-la da melhor forma possível!

___

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } É possível utilizar o cloudgeass localmente?

Sim! A principal canalização de uso do *cloudgeass* envolve a criação automática (e invisível pro usuário) de *clients* dos serviços AWS através do `boto3`. Toda a autenticação necessário para execução das funções (chamadas de APIs) segue o formato do próprio `boto3` e que pode ser encontrado em detalhe [neste link](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

Dessa forma, qualquer usuário que instalar a biblioteca *cloudgeass* e que tenha as credenciais AWS configuradas em seu ambiente local poderá usufruir de suas funcionalidades.

___


## Funcionalidades

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } Como funciona a lógica de obtenção da partição mais recente de uma tabela no S3 com base em seu prefixo?

De forma resumida, o processo consolidado na função `get_last_partition()` do [módulo s3](../features/exemplos-s3.md) considera a execução de três operações básicas:

??? info "1. Listagem de todas as chaves de objetos"
    Em casa de ferreiro, o espeto não pode ser de pau. Na funcionalidade de coleta de última partição de uma tabela, a listagem de todos objetos é feita através da função `bucket_objects_report()`, também do módulo s3 (verifique um vídeo de usabilidade no [link](../features/exemplos-s3.md#exemplos-práticos)). A única "exigência" para a obtenção desta listagem é que a função `bucket_objects_report()` seja configurada para extrair objetos apenas de um determinado prefixo, simulando uma espécie de listagem de todos os arquivos (incluindo partições) de uma determinada tabela.

    ```python
    # Coletando DataFrame de objetos do buckets
    df_objects = bucket_objects_report(
        bucket_name=bucket_name,
        prefix=table_prefix,
        client=client
    )
    ```

    Onde *bucket_name* representa o bucket onde a tabela alvo está armazenada e *table_prefix* indica o nome da tabela (prefixo no bucket s3)

    O resultado da função é dado através de um DataFrame pandas que possui uma série de atributos que caracterizam os objetos existentes. Entre eles, o atributo "Key" indica as chaves dos objetos e é justamente utilizado como base para a obtenção definitiva da listagem de chaves/arquivos existentes em uma tabela no S3.

    ```python
    # Extraindo lista de prefixos de objetos
    objs_list = list(df_objects["Key"].values)
    ```

    Com isso, as próximas etapas podem ter sequência.

??? info "2. Extração do valor da partição das chaves de objetos"
    Tendo em mãos a listagem de chaves de objetos, o próximo passo do processo envolve a entrada em um laço de repetição para iteração em cada um dos elementos desta lista de modo a extrair apenas os valores referentes às partições.

    Isto é feito através da função `get_partition_value_from_prefix()` também do [módulo s3](https://cloudgeass.readthedocs.io/pt/latest/features/s3/). Tal função possui uma série de parâmetros configuráveis que foram criados e pensados para os mais variados cenários envolvendo o particionamento de tabelas no S3. Para visualizar a documentação completa da função, acesse seu [código fonte](https://github.com/ThiagoPanini/cloudgeass/blob/main/cloudgeass/aws/s3.py#L243) direto no GitHub. Para uma descrição resumida sobre as configurações possíveis, o bloco abaixo poderá fornecer um entendimento mais claro.

    ??? abstract "Parâmetros da função `get_partition_value_from_prefix()`"

        | **Parâmetro** | **Descrição** |
        | :-- | :-- |
        | Modo da partição | Indica a forma como a partição de data está configurada no prefixo. Para uma partição do tipo `"anomesdia=20230101"`, este parâmetro deve ser indicado como `"name=value"`. Para partições contendo apenas valores (`20230101`), o parâmetro deve ser passado como apenas `"value"`. Sua referência na função é o parâmetro `partition_mode`. |
        | Nome da partição | Nome da partição. Este parâmetro é utilizado apenas quando `partition_mode="name=value"`. É aqui onde o usuário informa a referência da partição de data utilizada para extração dos valores. Exemplos como "anomes" ou "anomesdia" são cabíveis neste parâmetro. Sua referência na função é `date_partition_name`. |
        | Índice da partição | Para partições que não possuem nome no prefixo (`partition_mode="value"`), é preciso fornecer algum tipo de referência para que a coleta do valor possa ser realizada através da listagem de chaves de objeto. Este parâmetro é utilizado para indicar exatamente a posição do elemento que contém o valor da partição **após** a aplicação de um *split* por barra ("/"). Em outras palavras, um prefixo de objeto `table_name/20230101/arquivo.parquet` possui o valor da partição no índice -2 (`date_partition_idx=-2`), dado que a operação `prefix.split("/")[-2]` retorna o valor esperado. Sua referência na função é `date_partition_idx`. |

    Assim, considerando cada chave de objeto contida na listagem de `objs_list` obtida na etapa anterior, a função `get_partition_value_from_prefix()` é aplicada de modo a gerar uma nova listagem contendo apenas os **valores de partição** das chaves de objetos.

    ```python
    # Iterando sobre cada um dos prefixos de objetos
    partition_values = []
    for obj_prefix in objs_list:
        # Extraindo valor de partição
        partition_value = get_partition_value_from_prefix(
            prefix_uri=obj_prefix,
            partition_mode=partition_mode,
            date_partition_name=date_partition_name,
            date_partition_idx=date_partition_idx
        )

        # Incrementando lista
        partition_values.append(partition_value)
    ```

??? info "3. Ordenação e coleta da última partição da tabela"
    O último passo do processo é simples e direto: com a lista de valores de partições dada por `partition_values`, a partição mais recente é obtida através de uma ordenação e subsequente indexação do último elemento da lista:

    ```python
    return sorted(partition_values)[-1]
    ```

    Com isso, o usuário terá em mãos sempre o **valor da partição mais recente** de uma tabela contendo múltiplas partições **de data**.


Se o processo detalhado ainda esteja abstrato, imagine uma tabela qualquer armazenada no S3 e que esteja particionada por uma coluna chamada `anomesdia` cujos valores representam datas no formato `%Y%m%d` (ou `yyyMMdd`). Para cada etapa acima listada, o processo sequencial de obtenção da partição mais recente pode ser visualizado na prática por:

| **Etapa** | **Resultado** |
| :-- | :-- |
| 1. Listagem de objetos | `["anomesdia=20230101/arquivo01.parquet", "anomesdia=20230102/arquivo01.parquet"]` |
| 2. Extração de valor das partições | `[20230101, 20230102]` |
| 3. Ordenação e coleta do mais recente | `20230102` |


Por fim, é importante citar algumas premissas relacionadas ao uso da funcionalidade de extração da última partição.

???+ warning "Premissas para o uso da funcionalidade"
    1. Por natureza, a função só deve ser aplicada em tabelas particionadas e armazenadas no S3
    2. Atualmente, apenas tabelas contendo uma única partição podem ser alvos da funcionalidade
    3. Os valores das partições precisam ser "transformáveis" para inteiro visando o sucesso da ordenação
    4. As partições da tabela necessitam ter uma ordem lógica de grandeza baseada em datas para que o "elemento mais recente" possa ser devidamente coletado

Dito isso, é igualmente importante reforçar algumas das principais possibilidades de uso da funcionalidade.

???+ tip "Principais cenários de aplicação da funcionalidade"

    - É possível utilizar a função para tabelas particionadas nos formatos "name=value" (nome e valor) ou "value" (apenas valor)
    - O prefixo da tabela é indiferente para o sucesso da função, ou seja, não importa se o prefixo de uma tabela possui, por exemplo, o banco de dados antes do seu nome.
    - É possível consultar a última partição de uma tabela para utilizar como filtro em outros processos ou tomar decisões específicas acerca da aplicação.
