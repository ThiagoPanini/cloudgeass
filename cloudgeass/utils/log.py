"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando logs
---------------------------------------------------
"""

# Importando bibliotecas
import logging


# Função para configuração de log
def log_config(logger_name: str = __file__,
               logger_level: int = logging.INFO,
               logger_date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
    """
    Configuração de logs.

    Função criada para facilitar a criação de configuração
    de uma instância de Logger do Python utilizada no
    decorrer da aplicação Spark para registros de logs
    das atividades e das funcionalidades desenvolvidas.

    Parâmetros
    ----------
    :param logger_name:
        Nome da instância de logger.
        [type: str, default="glue_logger"]

    :param logger_level:
        Nível dos registros de log configurado.
        [type: int, default=logging.INFO]

    :param logger_date_format:
        Formato de data configurado para representação
        nas mensagens de logs.
        [type: str, default="%Y-%m-%d %H:%M:%S"]
    """
    print(logger_name)

    # Instanciando objeto de logging
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    # Configurando formato das mensagens no objeto
    log_format = "%(levelname)s;%(asctime)s;%(filename)s;"
    log_format += "%(lineno)d;%(message)s"
    formatter = logging.Formatter(log_format,
                                  datefmt=logger_date_format)

    # Configurando stream handler do objeto de log
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
