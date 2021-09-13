<h1 align="center">
  <img src="https://i.imgur.com/lycaE7u.png", alt="cloudgeass logo">
</h1>

<div align="center">  
  
  ![Release](https://img.shields.io/badge/release-ok-brightgreen)
  [![PyPI](https://img.shields.io/pypi/v/cloudgeass?color=blue)](https://pypi.org/project/cloudgeass/)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudgeass?color=lightblue)
  ![PyPI - Status](https://img.shields.io/pypi/status/cloudgeass)

</div>

## Table of content

- [Sobre cloudgeass](#sobre-cloudgeass)
- [Instalação do Pacote](#instalação-do-pacote)
- [Funcionalidades Disponíveis](#funcionalidades-disponíveis)
  - [Módulo s3](#módulo-s3)
  - [Módulo rds](#módulo-rds)
  - [Módulo serverless](#módulo-serverless)
- [Utilização Prática](#utilização-prática)
- [Contatos](#contatos)

___

## Sobre cloudgeass

Em um cenário tecnológico onde soluções baseadas em cloud são cada vez mais comuns, imaginem o quão vantajoso seria se tivéssemos alguns componentes prontos para facilitar o desenvolvimento de sistemas, arquiteturas ou até mesmo auxiliar em operações simples do dia a dia. Imerso na ideia de tornar algumas etapas de construção simples, surge o _cloudgeass_: um pacote Python contendo elementos previamente desenvolvidos visando facilitar o intermédio entre scripts e ferramentas cloud. 

Mesmo que exemplos práticos sejam fornecidos ao longo desta documentação, é preciso entender o pacote _cloudgeass_ como um simples centralizador e fornecedor de classes, módulos ou funções prontas para que os usuários possam se servir em meio a operações envolvendo serviços da cloud. Com as funcionalidades aqui desenvolvidas é possível, por exemplo, criar um [bucket s3](https://aws.amazon.com/pt/s3/) de forma automática, ou mesmo realizar o upload, em um dado bucket, de todos os objetos contidos em um diretório local. Em uma outra gama de serviços cloud, também é possível criar [layers lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) a partir de uma única execução de função no módulo serverless.py. Ao longo do tempo, uma gama maior de operações poderão ser encapsuladas e fornecidas aos usuários do pacote, sempre com a premissa de simplificar e automatizar as operações.

___

## Instalação do Pacote

Com o [ambiente virtual python](https://realpython.com/python-virtual-environments-a-primer/) ativo, para a instalação do pacote _cloudgeass_ via pip, basta executar o comando abaixo:

```bash
pip install cloudgeass
```

Com isso, todo o ferramental disponível na última versão do pacote poderá ser usufruído. Vale citar que o pacote _cloudeass_ possui, como principal dependência, o SDK Python [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) com um vasto ferramental de operações na AWS utilizando python. Assim, as dependências do pacote são:
* `boto3`: SDK python para operações na AWS
* `pandas`: poderosa ferramenta para a manipulação de dados em python
___

## Funcionalidades Disponíveis

Como mencionado anteriormente, o pacote conta com alguns módulos essenciais para a realização de operações em serviços cloud a partir da linguagem Python. Focado, em um primeiro momento, em soluções AWS, _cloudgeass_ entrega dois principais módulos de componentes úteis: `s3.py` e `serverless.py`.

### Módulo s3

De forma intuitiva, o módulo s3 contempla funcionalidades focadas no serviço _Simple Storage Service_ da AWS. Como principal componente, encontra-se a classe [JimmyBuckets]() com uma série de métodos capazes de realizar as operações mais comuns em buckets do s3, desde a instância de um recurso e um client a partir do boto3 até operações de criação de buckets, upload e download de objetos ou mesmo diretórios completos. Como grande vantagem de utilização, as funcionalidades contidas na classe JimmyBuckets contam com uma vasta documentação e um acompanhamento de logs ao longo das operações, permitindo assim com que o usuário realize uma série de ações na AWS executando apenas uma única linhas de código.

Detalhando um pouco mais as _features_ disponíveis dentro da classe JimmyBuckets, a tabela abaixo pode servir de referência para consultas e validação de operações. Para visualizar um exemplo prático de utilização, basta acessar a seção de [utilização](#utilização-prática) ou então os [scripts de testes](https://github.com/ThiagoPanini/cloudgeass/blob/main/tests/s3_jbuckets.py) desenvolvidos para validar e testar, de forma bem detalhada, algumas das operações presentes na classe.

| Método                            | Descrição                                                                                             |
| :-------------------------------: | :---------------------------------------------------------------------------------------------------: |         
| `jbuckets.list_buckets()`         | Lista todos os buckets presentes na conta de utilização da AWS |
| `jbuckets.list_bucket_objects()`  | Lista todos os objetos (chaves) presentes em um determinado bucket |
| `jbuckets.delete_bucket()`        | Deleta um bucket já existente com a opção de esvaziá-lo antes |
| `jbuckets.create_bucket()`        | Cria um novo bucket com possibilidade de configurar opções de privacidade e ACL |
| `jbuckets.upload_object()`        | Realiza o upload de um objeto salvo localmente ou lido em memória |
| `jbuckets.upload_directory()`     | Realiza o upload de todos os arquivos presentes em um diretório alvo, mantendo a mesma estrutura de pastas locais através de prefixos no s3 |
| `jbuckets.download_all_objects()` | Realiza o download de todos os objetos presentes em um bucket, mantendo a mesma estrutura de prefixos no s3 através de pastas locais |
| `jbuckets.read_object()`          | Realiza a leitura de um objeto presente no s3, retornando um conteúdo binário que pode ser trabalhado posteriormente pelo código |
| `jbuckets.object_to_df()`         | Mirando dados em formato tabular (arquivos csv ou txt), realiza a leitura de um objeto no s3 direto em um formato de DataFrame do pandas |


## Módulo rds

De maneira geral, pode-se definir o módulo rds como um frente facilidadora para operações em bancos de dados relacionais, sejam estes presentes na nuvem ou não. Sabe-se que a linguagem python proporciona uma série de funcionalidades capazes de integrar serviços de leitura e escrita de dados utilizando os mais variados _engines_. Bibliotecas como [`pymysql`](https://pypi.org/project/PyMySQL/), [`psycopg2`](https://pypi.org/project/psycopg2/), entre outras são exemplos de pacotes que fornecem tais benefícios. Assim, visando encapsular as principais operações em termos de conexões a bancos de dados, o módulo rds, concebido com inspiração o serviço de bancos de dados relacionais da AWS (_Relational Database Service_) traz, como principal característica, classes responsáveis por inicializar objetos de conexão através de parâmetros essenciais fornecidos pelo usuário como, por exemplo, um endpoint, credenciais do usuário do banco, nome do banco de dados a ser utilizado, entre outros. Um exemplo prático deste módulo pode ser encontrado na classe [PostgreSQLConnection](https://github.com/ThiagoPanini/cloudgeass/blob/main/cloudgeass/aws/rds.py) que, construída sob os elementos de um banco de dados PostgreSQL a partir da biblioteca `psycopg2`, pode ser instanciada a partir dos seguintes parâmetros:

* _host:_ endpoint do servidor do banco de dados a ser utilizado na conexão
* _user:_ usuário do banco de dados
* _password:_ senha do usuário do banco de dados
* _database:_ referência do banco de dados utilizado na conexão

Com isso, tem-se em mãos um objeto de conexão que pode ser utilizado das mais variadas formas, seja para executar queries, criar tabelas, selecionar dados ou receber dados de forma dinâmica através de métodos que transformam resultados de consultas em objetos DataFrame do pandas. Abaixo, uma relação dos métodos presentes na classe `PostgreSQLConnection` utilizada como exemplo:

| Método                            | Descrição                                                                                             |
| :-------------------------------: | :---------------------------------------------------------------------------------------------------: |         
| `conn.show_tables()`              | Lista todas as tabelas presentes no banco de dados conectado |
| `jbuckets.execute_query()`        | Utiliza o objeto de conexão instanciado da classe para executar uma query no banco de dados |
| `jbuckets.crate_table_from_df()`  | Recebe um objeto DataFrame como entrada para verificar as colunas e os tipos primitivos de modo a construir uma query `CREATE TABLE` de acordo com o conteúdo dos dados |
| `jbuckets.insert_execute_values()`| Utiliza um método de alta performance para inserção de dados em uma tabela do banco de dados a partir de um objeto DataFrame |
| `jbuckets.select_values()`        | Executa uma query `SELECT` para retornar os dados em um formato DataFrame para o usuário solicitante |

### Módulo serverless

Neste módulo criado recentemente, são alocados recursos e encapsulados códigos capazes de atuar com o serviço [lambda](https://aws.amazon.com/pt/lambda/) presente na AWS. Baseado em funções e não em classes, aqui será possível encontrar elementos capazes de criar layers a serem utilizados em funções lambda de forma automática e sustentável, permitindo assim com que o usuário realize toda a preparação local das dependências a partir de um arquivo `requirements.txt` gerado manualmente ou automaticamente a partir de um ambiente virtual de trabalho. Para ilustrar algumas possibilidades, a tabela abaixo pode servir de referência inicial de consulta. Para maiores detalhes, é possível consumir o contéudo da seção de [utilização](#utilização-prática) ou então o [scripts de testes](https://github.com/ThiagoPanini/cloudgeass/blob/main/tests/serverless_layers.py) específico do módulo serverless.

| Método                            | Descrição                                                                                             |
| :-------------------------------: | :---------------------------------------------------------------------------------------------------: |         
| `create_layer_path()`             | Cria um diretório reconhecível pelo runtime do lambda para leitura das dependências python |
| `get_packages()`                  | Coleta as dependências via `requirements.txt` fornecido ou via `venv` e realiza a instalação direcionada das mesmas no diretório do layer |
| `upload_layer_to_bucket()`        | Transforma o diretório do layer em um arquivo .zip e realiza o upload do conteúdo em um bucket s3 para posterior associação a funções lambda|
| `build_lambda_layer()`            | Encapsula todas as operações acima citadas em um bloco único, partindo do início e resultando em um layer zipado presente no s3 |

___

## Utilização Prática

O snippet abaixo ilustra algumas operações detalhadas nas tabelas de cada módulo, permitindo assim uma visão prática sobre como utilizar os recursos do pacote _cloudgeass_. Para uma maior riqueza de detalhes, recomenda-se visualizar scripts mais detalhados presentes no diretório de [testes](https://github.com/ThiagoPanini/cloudgeass/tree/main/tests) deste repositório.

```python
# Importando bibliotecas
from cloudgeass.aws.s3 import JimmyBuckets
import os

# Instanciando classe e criando bucket, caso inexistente
jbuckets = JimmyBuckets(region=REGION)

# Coletando buckets existentes e aplicando drop + create
account_buckets = jbuckets.list_buckets()
if BUCKET_NAME not in account_buckets:
    jbuckets.create_bucket(bucket_name=BUCKET_NAME)
    
# Realizando o upload de objeto no bucket
jbuckets.upload_object(
    file=os.path.join(os.getcwd(), 'requirements.txt'),
    bucket_name='bucket_teste',
    key='test_folder/requirements.txt'
)

# Realizando o upload de todos os arquivos em um diretório
jbuckets.upload_directory(
    directory=os.getcwd(),
    bucket_name='bucket_teste'
)

# Baixando todos os objetos presentes em um bucket
jbuckets.download_all_objects(
    bucket_name='bucket_teste',
    prefix='',
    local_dir=os.path.join(os.getcwd(), 'tmp'),
    verbose=True
)
```

Em um exemplo básico de conexão a um banco de dados relacional (por exemplo, RDS com engine PostgreSQL), o código abaixo utiliza o módulo `cloudgeass.aws.rds` para gerenciar todas as operações de leitura e escrita no banco alvo:

```python
# Importando bibliotecas
from cloudgeass.aws.rds import PostgreSQLConnection

# Instância de conexão ao banco de dados
db = PostgreSQLConnection(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=os.getenv('DB_PWD')
)

# Dropando tabela alvo, caso existente
db.execute_query(f'DROP TABLE IF EXISTS {TABLE_NAME}')

# Retornando tabelas já existentes no banco
db_tables = db.show_tables()

# Criando tabela a partir de schema do DataFrame
db.create_table_from_df(df=df, table=TABLE_NAME)

# Inserindo dados a partir de DataFrame
db.insert_execute_values(df=df, table=TABLE_NAME)

# Realizando consulta para validar quantidade de registros
rows = db.select_values(
    query=f'SELECT count(1) AS qtd_linhas FROM {TABLE_NAME}',
    columns=['qtd_linhas']
)
```

Já em um exemplo básico de criação de layers lambda, o snippet abaixo traz a execução de uma única função capaz de encapsular todo o procedimento:

```python
# Importando bibliotecas
from clougeass.aws.serverless import build_lambda_layer

# Criando layer
build_lambda_layer(
    layer_path=os.path.join(os.getcwd(), 'lambda_layer/python'),
    bucket_name='layes_lambda',
    prefix='layer_teste/'
)
```

> Ao longo do tempo, novas funcionalidades poderão ser implementadas conforme novos conhecimentos forem sendo agregados.

## Contatos

* LinkedIn: https://www.linkedin.com/in/thiago-panini/
* Outros pacotes desenvolvidos: https://github.com/ThiagoPanini
