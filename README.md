<div align="center">
    <br><img src="https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/imgs/01-header-readme.png?raw=true" alt="cloudgeass-logo">
</div>

<div align="center">  
  <br>
  
  [![PyPI](https://img.shields.io/pypi/v/cloudgeass?color=purple)](https://pypi.org/project/cloudgeass/)
    ![PyPI - Status](https://img.shields.io/pypi/status/cloudgeass?color=red)
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ThiagoPanini/cloudgeass?color=blue)
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

> **Note**
> Futuramente, novos módulos serão inclusos na biblioteca, expandindo o leque de funcionalidades e permitindo aos usuários uma forma fácil e rápida de codificar suas operações na nuvem.


### O módulo s3

A ideia por trás do módulo `cloudgeass.aws.s3` gira em torno do fornecimento de funções e blocos de código contendo operações comumente realizadas no S3.

Para navegar por todas as funcionalidades presentes, consulte o arquivo [s3.py](https://github.com/ThiagoPanini/cloudgeass/blob/main/cloudgeass/aws/s3.py). Abaixo, um exemplo prático de utilização de uma funcionalidade capaz de retornar detalhes relevantes de todos os objetos de um *bucket* s3.

```python
# Importando módulo
from cloudgeass.aws.s3 import bucket_objects_report

# Obtendo DataFrame com report de objetos de um bucket
df_objects_report = bucket_objects_report(
  bucket_name="terraglue-sor-data-sa-east-1"
)

# Visualizando resultado
df_objects_report.head()
```

O resultado é dado como um DataFrame do pandas capaz de ser utilizado de acordo com os propósitos do usuário:

<div align="center">
    <img src="https://github.com/ThiagoPanini/cloudgeass/blob/main/docs/imgs/readme-s3-example-bucket_objects_report.png?raw=true" alt="bucket_objects_report">
</div>


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