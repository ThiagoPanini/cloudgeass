<div align="center">
    <br><img src="https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/imgs/01-header-readme.png?raw=true" alt="cloudgeass-logo">
</div>

<div align="center">  
  <br>
  
  [![PyPI](https://img.shields.io/pypi/v/cloudgeass?color=purple)](https://pypi.org/project/cloudgeass/)
  ![PyPI - Downloads](https://img.shields.io/pypi/dm/cloudgeass?color=purple)
  ![PyPI - Status](https://img.shields.io/pypi/status/cloudgeass?color=purple)
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ThiagoPanini/cloudgeass?color=purple)
  ![GitHub Last Commit](https://img.shields.io/github/last-commit/ThiagoPanini/cloudgeass?color=purple)
  <br>

  ![CI workflow](https://img.shields.io/github/actions/workflow/status/ThiagoPanini/cloudgeass/ci-cloudgeass-main.yml?label=ci)
  [![codecov](https://codecov.io/github/ThiagoPanini/cloudgeass/branch/main/graph/badge.svg?token=7HI1YGS4AA)](https://codecov.io/github/ThiagoPanini/cloudgeass)

</div>

## Table of content

- [Table of content](#table-of-content)
- [O que é o cloudgeass?](#o-que-é-o-cloudgeass)
- [Funcionalidades presentes](#funcionalidades-presentes)
  - [O módulo s3](#o-módulo-s3)
- [Contatos](#contatos)
- [Referências](#referências)

___

## O que é o cloudgeass?

Cloudgeass é uma biblioteca Python criada para centralizar uma série de módulos, classes, métodos e funções prontas para serem utilizadas nos mais variados serviços da AWS. Inspirado em um [renomado anime japonês](https://en.wikipedia.org/wiki/Code_Geass), o **cloudgeass** visa proporcionar um maior **controle** sobre atividades e operações comumente realizadas em aplicações criadas na nuvem.

> **Note**
> A construção desta biblioteca foi retomada após quase 2 anos em hiato. Suas funcionalidades estão sendo refatoradas e uma nova versão será construída e lançada aos poucos.

___

## Funcionalidades presentes

Em linhas gerais, a biblioteca **cloudgeass** é divida em diferentes módulos, cada um encapsulando e consolidando funcionalidades para fins específicos. Os módulos existentes até o momento são:

- 🪣 `cloudgeass.aws.s3` - funcionalidades para facilitar operações no S3 através do SDK `boto3`.
- 🧼 `cloudgeass.aws.glue` - em ideação


### O módulo s3

A ideia por trás do módulo `cloudgeass.aws.s3` gira em torno do fornecimento de funções e blocos de código contendo operações comumente realizadas no S3. Para navegar por todas as funcionalidades presentes, consulte o arquivo [s3.py](https://github.com/ThiagoPanini/cloudgeass/blob/main/cloudgeass/aws/s3.py) ou, se preferir, clique no _dropdown_ abaixo para assistir os vídeos de demonstrações.

> **Note**
> Vídeos marcados com ⭐ indicam _features_ provavelmente relevantes para o contexto de Analytics e são as preferidas dos usuários!

<details>
    <summary>📽️ Listando buckets de uma conta com <code>list_buckets()</code></summary>
    <br>
  
https://user-images.githubusercontent.com/38161178/218567983-cc852ca5-f5df-4cf7-9b59-7408e0f309fa.mp4

**Código utilizado:**

```python
from cloudgeass.aws.s3 import list_buckets

buckets = list_buckets()
buckets
```
</details>

<details>
    <summary>📽️ Obtendo um report de objetos de um bucket com <code>bucket_objects_report()</code></summary>
    <br>

https://user-images.githubusercontent.com/38161178/218573417-2d705b06-2ab0-4441-b845-f6afe43b8f17.mp4  
        
**Código utilizado:**

```python
from cloudgeass.aws.s3 import bucket_objects_report

bucket_name = "nome-de-bucket-aws"
df_objs_report = bucket_objects_report(bucket_name=bucket_name)

df_objs_report.head(3)
```
</details>


<details>
    <summary>📽️ Obtendo um report de objetos apenas de um determinado prefixo (ou tabela no S3)</code></summary>
    <br>

https://user-images.githubusercontent.com/38161178/218575065-ef22a25a-4ead-4983-bf5f-fe2a5502608c.mp4
        
**Código utilizado:**

```python
from cloudgeass.aws.s3 import bucket_objects_report

# Definindo nome de bucket e prefixo alvo da extração
bucket_name = "nome-de-bucket-aws"
prefix = "a-sample-prefix"

df_objs_report = bucket_objects_report(bucket_name=bucket_name, prefix=prefix)

df_objs_report.head(3)
```
</details>

<details>
    <summary>📽️ Obtendo um report de objetos de todos os buckets com <code>all_buckets_objects_report()</code></summary>
    <br>

https://user-images.githubusercontent.com/38161178/218576685-2215a62e-8b1f-4fb6-85b4-edf02d6706be.mp4
        
**Código utilizado:**

```python
from cloudgeass.aws.s3 import all_buckets_objects_report

df_report = all_buckets_objects_report()
df_report.head()
```
</details>

<details>
    <summary>📽️ Obtendo um report de objetos de todos os buckets ignorando alguns buckets</code></summary>
    <br>

https://user-images.githubusercontent.com/38161178/218577709-006b5d1c-51dc-4735-9230-cfb694126e4d.mp4
        
**Código utilizado:**

```python
from cloudgeass.aws.s3 import all_buckets_objects_report

# Definindo lista de buckets a serem ignorados no report de objetos
ignore_buckets = [
    "terraglue-athena-query-results-569781470788-us-east-1",
    "terraglue-glue-assets-569781470788-us-east-1",
    "terraglue-sor-data-569781470788-us-east-1",
    "terraglue-spec-data-569781470788-us-east-1"
]

# Obtendo report
df_report = all_buckets_objects_report(exclude_buckets=ignore_buckets)
df_report.head()
```
</details>

<details>
    <summary>📽️⭐ Lendo um objeto CSV, JSON ou PARQUET em um DataFrame do pandas com <code>read_s3_object()</code></summary>
    <br>

https://user-images.githubusercontent.com/38161178/218580090-385e4170-a76c-4b03-b00e-865b9e4ec05e.mp4
        
**Código utilizado:**

```python
from cloudgeass.aws.s3 import read_s3_object

# Definindo variáveis para leitura de objeto no S3
bucket_name = "nome-de-bucket"
obj_prefix = "tbsot_ecommerce_br/anomesdia=20230213/run-1676319522273-part-block-0-0-r-00004-snappy.parquet"

# Criando URI
s3_uri_parquet = f"s3://{bucket_name}/{obj_prefix}"

# Lendo objeto parquet
df_parquet = read_s3_object(s3_uri_parquet)
df_parquet.head()
```
</details>

<details>
    <summary>📽️⭐ Coletando última partição de tabela no S3 com <code>get_last_partition()</code></summary>
    <br>
         

https://user-images.githubusercontent.com/38161178/218581540-82a4836b-9224-4646-a9ff-6dc6966b0132.mp4


**Código utilizado:**

```python
from cloudgeass.aws.s3 import get_last_partition

# Definindo variáveis para leitura de objeto no S3
bucket_name = "terraglue-sot-data-569781470788-us-east-1"
table_prefix = "tbsot_ecommerce_br"

last_partition = get_last_partition(bucket_name, table_prefix)
```
</details>

___

## Contatos

- [Thiago Panini - LinkedIn](https://www.linkedin.com/in/thiago-panini/)
- [paninitechlab @ hashnode](https://panini.hashnode.dev/)

___

## Referências

**Python**

- [Python - Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Stack Overflow - Reading Pandas DataFrame from S3](https://stackoverflow.com/questions/37703634/how-to-import-a-text-file-on-aws-s3-into-pandas-without-writing-to-disk)

**Github**

- [GitHub Actions - pypa/gh-action-pypi-publish](https://github.com/marketplace/actions/pypi-publish)
- [Medium - Major, Minor and Patch](https://medium.com/fiverr-engineering/major-minor-patch-a5298e2e1798)
- [Medium - Automate PyPI Releases with GitHub Actions](https://medium.com/@VersuS_/automate-pypi-releases-with-github-actions-4c5a9cfe947d)

**Tests**
- [Codecov - Setting Threshold](https://github.com/codecov/codecov-action/issues/554#issuecomment-1261250304)
- [Codecov - About the Codecov YAML](https://docs.codecov.com/docs/codecov-yaml)
- [Codecov - Status Checks](https://docs.codecov.com/docs/commit-status)
- [Codecov - codecov.yml Reference](https://docs.codecov.com/docs/codecovyml-reference)
- [Codecov - Ignore Paths](https://docs.codecov.com/docs/ignoring-paths)
