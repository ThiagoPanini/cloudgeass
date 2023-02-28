# Cloudgeass

## Visão Geral

Cloudgeass é uma biblioteca Python criada para centralizar uma série de módulos, classes, métodos e funções prontas para serem utilizadas nos mais variados serviços da AWS. Inspirado em um [renomado anime japonês](https://en.wikipedia.org/wiki/Code_Geass), o cloudgeass visa proporcionar um maior controle sobre atividades e operações comumente realizadas em aplicações criadas na nuvem.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/cloudgeass/blob/feature/create-docs-page-with-mkdocs/docs/assets/imgs/cloudgeass-logo.png?raw=true" alt="cloudgeass-logo" width=200 height=200>
</div>

<div align="center">
    <i>cloudgeass<br>
    Python Library</i>
</div>

<div align="center">  
  <br>
  <a href="https://pypi.org/project/cloudgeass/">
    <img src="https://img.shields.io/pypi/v/cloudgeass?color=purple" alt="Shield cloudgeass PyPI version">
  </a>

  <a href="https://pypi.org/project/cloudgeass/">
    <img src="https://img.shields.io/pypi/dm/cloudgeass?color=purple" alt="Shield cloudgeass PyPI downloads">
  </a>

  <a href="https://pypi.org/project/cloudgeass/">
    <img src="https://img.shields.io/pypi/status/cloudgeass?color=purple" alt="Shield cloudgeass PyPI status">
  </a>
  
  <img src="https://img.shields.io/github/commit-activity/m/ThiagoPanini/cloudgeass?color=purple" alt="Shield github commit activity">
  
  <img src="https://img.shields.io/github/last-commit/ThiagoPanini/cloudgeass?color=purple" alt="Shield github last commit">

  <br>
  
  <img src="https://img.shields.io/github/actions/workflow/status/ThiagoPanini/cloudgeass/ci-cloudgeass-main.yml?label=ci" alt="Shield github CI workflow">

  <a href='https://cloudgeass.readthedocs.io/pt/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/cloudgeass/badge/?version=latest' alt='Documentation Status' />
  </a>
  
  <a href="https://codecov.io/github/ThiagoPanini/cloudgeass">
    <img src="https://codecov.io/github/ThiagoPanini/cloudgeass/branch/main/graph/badge.svg?token=7HI1YGS4AA" alt="Shield cloudgeass CodeCov">
  </a>

</div>

___

## Instalação

A última versão da biblioteca *cloudgeass* já está publicada no [PyPI](https://pypi.org/project/cloudgeass/) e disponível para uso totalmente gratuito por qualquer um interessado em aprimorar a construção de suas aplicações em um ambiente de nuvem. Para iniciar sua jornada de uso, basta realizar sua instalação através do seguinte comando:

```bash
pip install cloudgeass
```

??? tip "Dica: sobre ambientes virtuais Python"
    Em geral, uma boa prática relacionada a criação de novos projetos Python diz respeito à criação e uso de [ambientes virtuais](https://docs.python.org/3/library/venv.html) (ou *virtual environments*, no inglês). Criar um *venv* para cada projeto Python iniciado permite, entre outras vantagens, ter em mãos um ambiente isolado com um controle mais refinado sobre as dependências utilizadas.

    ??? example "Criando ambientes virtuais"
        Para criar um ambiente virtual Python, basta navegar até um diretório escolhido para organizar todos os *virtual envs* criados e executar o seguinte comando:

        ```bash
        python -m venv <nome_venv>
        ```

        Onde `<nome_venv>` deve ser substituído pelo nome escolhido para o ambiente virtual a ser criado. É comum ter nomes de ambientes virtuais associados à projetos (ex: `cloudgeass_venv`).

    ??? example "Acessando ambientes virtuais"
        Criar um *virtual env* é apenas a primeira etapa do processo. Após criado, o ambiente precisa ser explicitamente acessado pelo usuário para garantir que todas as ações subsequentes relacionadas à instalação de bibliotecas sejam realizadas, de fato, no ambiente isolado criado.
        
        Se o sistema operacional utilizado é Windows, então use o comando abaixo para acessar o ambiente virtual Python:

        ```bash
        # Acessando ambiente virtual no Windows
        <caminho_venv>/Scripts/activate
        ```

        Em caso de uso de um sistema operacional Linux (ou Git Bash no Windows), o comando possui pequenas alterações e é dado por:

        ```bash
        # Acessando ambiente virtual no Linux
        source <caminho_venv>/Scripts/activate
        ```

        Onde `<caminho_venv>` é a referência da localização do ambiente virtual recém criado. Por exemplo, se você criou o ambiente virtual de nome *test_venv* no seu diretório de usuário, então `<caminho_venv>` pode ser substituído por `C:\Users\usuario\test_venv` no Windows ou simplesmente `~/test_venv` no Linux.
    
    Para mais informações, o [excelente artigo do blog Real Python](https://realpython.com/python-virtual-environments-a-primer/) poderá esclarecer uma série de dúvidas envolvendo a criação e o uso de ambientes virtuais Python.

## O Poder do cloudgeass

Agora que o *cloudgeass* foi instalado com sucesso, todo o seu leque de funcionalidades se encontra disponível para utilização e suas funções e métodos poderão ser importadas em aplicações Python.

:material-alert-decagram:{ .mdx-pulse .warning } Não deixe de assistir as [demonstrações práticas](https://cloudgeass.readthedocs.io/pt/latest/features/organizacao/) de grande parte daquilo que o *cloudgeass* pode oferecer! Imagino que você possa se surpreender com as vantagens envolvidas em seu uso!

## Contatos

- :fontawesome-brands-github: [@ThiagoPanini](https://github.com/ThiagoPanini)
- :fontawesome-brands-linkedin: [Thiago Panini](https://www.linkedin.com/in/thiago-panini/)
- :fontawesome-brands-hashnode: [panini-tech-lab](https://panini.hashnode.dev/)

