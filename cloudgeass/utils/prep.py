"""
Módulo criado para consolidar funções úteis e genéricas que não estão
especificamente relacionadas a um dos módulos da biblioteca, mas que podem
ser utilizadas por qualquer um dos mesmos.

___
"""


# Definindo função para categorização de volume do objeto
def categorize_file_size(size_in_bytes: int or float) -> str:
    """
    Recebe uma informação em bytes e retorna o valor formatado em string.

    Esta função pode ser utilizada em processos onde se deseja obter uma
    informação de volume de determinados arquivos em um formato visualmente
    apresentável e em escala. A função valida a magnitude do valor em bytes do
    passado como argumento e categoriza o mesmo em B, KB, MB, GB e TB.

    Examples:
        ```python
        # Importando função
        from cloudgeass.utils.prep import categorize_file_size

        size_formatted = categorize_file_size(size_in_bytes=1024)

        # Resultado: "1 MB"
        ```

    Args:
        size_in_bytes (int or float): Valor em bytes a ser formatado.

    Returns:
        Valor em string já formatado e arredondado com a magnitude adequada.
    """

    # Aplicando validações de magnitude e formatando valor
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
