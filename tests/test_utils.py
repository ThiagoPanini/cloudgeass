"""
SCRIPT: test_utils.py

OBJETIVO:
---------
Consolidar uma suíte de testes capaz de testar e validar
funcionalidades presentes no módulo utils do cloudgeass.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
import pytest

from cloudgeass.utils.prep import categorize_file_size


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@pytest.mark.categorize_file_size
def test_funcao_de_categorizacao_de_volume_retorna_bytes():
    """
    G: dado que o usuário deseja categorizar o volume de arquivos com
       base em um valor numérico representando seus respectivos tamanhos
    W: quando o método categorize_file_size() de cloudgeass.utils.prep
       for executado com um argumento numérico igual a 1000
    T: então o retorno deve ser uma string representando o tamanho do
       próprio arquivo em bytes e sem alteração de escala (1000 B)
    """

    # Preparando parâmetros
    test_size = 1000
    expected_output = "1000 B"

    assert categorize_file_size(test_size) == expected_output


@pytest.mark.categorize_file_size
def test_funcao_de_categorizacao_de_volume_retorna_kilobytes():
    """
    G: dado que o usuário deseja categorizar o volume de arquivos com
       base em um valor numérico representando seus respectivos tamanhos
    W: quando o método categorize_file_size() de cloudgeass.utils.prep
       for executado com um argumento numérico igual a 2048
    T: então o retorno deve ser uma string representando o tamanho do
       arquivo formatado na escala de kilobytes (2.00 KB)
    """

    # Preparando parâmetros
    test_size = 2048
    expected_output = "2.00 KB"

    assert categorize_file_size(test_size) == expected_output


@pytest.mark.categorize_file_size
def test_funcao_de_categorizacao_de_volume_retorna_megabytes():
    """
    G: dado que o usuário deseja categorizar o volume de arquivos com
       base em um valor numérico representando seus respectivos tamanhos
    W: quando o método categorize_file_size() de cloudgeass.utils.prep
       for executado com um argumento numérico igual a 1048576
    T: então o retorno deve ser uma string representando o tamanho do
       arquivo formatado na escala de megabytes (1.00 MB)
    """

    # Preparando parâmetros
    test_size = 1048576
    expected_output = "1.00 MB"

    assert categorize_file_size(test_size) == expected_output


@pytest.mark.categorize_file_size
def test_funcao_de_categorizacao_de_volume_retorna_gigabytes():
    """
    G: dado que o usuário deseja categorizar o volume de arquivos com
       base em um valor numérico representando seus respectivos tamanhos
    W: quando o método categorize_file_size() de cloudgeass.utils.prep
       for executado com um argumento numérico igual a 1073741824
    T: então o retorno deve ser uma string representando o tamanho do
       arquivo formatado na escala de gigabytes (1.00 GB)
    """

    # Preparando parâmetros
    test_size = 1073741824
    expected_output = "1.00 GB"

    assert categorize_file_size(test_size) == expected_output


@pytest.mark.categorize_file_size
def test_funcao_de_categorizacao_de_volume_retorna_terabytes():
    """
    G: dado que o usuário deseja categorizar o volume de arquivos com
       base em um valor numérico representando seus respectivos tamanhos
    W: quando o método categorize_file_size() de cloudgeass.utils.prep
       for executado com um argumento numérico igual a 1099511627776
    T: então o retorno deve ser uma string representando o tamanho do
       arquivo formatado na escala de terabytes (1.00 TB)
    """

    # Preparando parâmetros
    test_size = 1099511627776
    expected_output = "1.00 TB"

    assert categorize_file_size(test_size) == expected_output
