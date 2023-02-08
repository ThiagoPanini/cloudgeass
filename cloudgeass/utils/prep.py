"""
MÓDULO: cloudgeass.utils.prep.py

OBJETIVO:
---------
Módulo auxiliar criado para consolidar funções e blocos de
código utilizados em etapas relevantes da biblioteca e de suas
funcionalidades codificadas.
--------------------------------------------------------------
"""


# Definindo função para categorização de volume do objeto
def categorize_file_size(size_in_bytes: int or float):
    """
    Recebe uma informação em bytes e retorna valor formatado.

    Parâmetros
    ----------
    :param size_in_bytes:
        Valor em bytes a ser utilizado no processo de categorização
        [type: int|float]

    Retorno
    -------
    :return size_formatted:
        String formatada do tamanho em bytes inserido com base
        nas categorias B, KB, MB, GB e TB.
        [type: str]
    """

    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        size_in_kb = size_in_bytes / 1024
        return f"{size_in_kb:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        size_in_mb = size_in_bytes / (1024 ** 2)
        return f"{size_in_mb:.2f} MB"
    elif size_in_bytes < 1024 ** 4:
        size_in_gb = size_in_bytes / (1024 ** 3)
        return f"{size_in_gb:.2f} GB"
    else:
        size_in_tb = size_in_bytes / (1024 ** 4)
        return f"{size_in_tb:.2f} TB"
