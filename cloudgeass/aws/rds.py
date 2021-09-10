"""
---------------------------------------------------
------------------- MÓDULO: rds -------------------
---------------------------------------------------
Módulo responsável por consolidar códigos relevantes
relacionados à operações de bancos de dados relacionais
na AWS a partir do serviço RDS (Relation Database
Service). Com as funcionalidades aqui encapsuladas,
o usuário poderá utilizar funções e métodos para
manusear, gerenciar e executar operações em
bancos de dados a partir de endpoints já estabelecidos.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Banco de Dados PostgreSQL
    2.1 Classe estruturada utilizando psycopg2
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 18/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Biblioteca psycopg2
import psycopg2
import psycopg2.extras as extras

# Importando bibliotecas
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv

# Logging
import logging
from cloudgeass.utils.log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)


"""
---------------------------------------------------
---------- 2. BANCO DE DADOS POSTGRESQL -----------
    2.1 Classe estruturada utilizando psycopg2
---------------------------------------------------
"""

# Construção de classe para conexão ao banco PostgreSQL
class PostgreSQLConnection:
    """
    Classe responsável por propor uma conexão com um banco
    de dados PostgreSQL, permitindo também a execução de 
    métodos específicos para o manuseio de dados e o
    gerenciamento de alguns parâmetros intrínsecos do banco.
    
    Com essa classe, o usuário poderá utilizar métodos já
    preparados para a ingestão de dados em tabelas já
    existentes no banco de dados, além de aplicar queries
    de seleção, obtendo resultados diretos em um formato
    DataFrame do pandas.
    
    Atributos da classe
    -------------------
    :attr host:
        Host utilizado para conexão ao banco de dados. Caso
        o banco esteja hospedado localmente, é possível 
        passar o ip local da máquina ou a string 'localhost'
        [type: string]
        
    :attr database:
        Informação do banco de dados a ser utilizado na
        conexão.
        [type: string]
        
    :attr user:
        Usuário do banco de dados utilizado para formalizar
        a conexão.
        [type: string]
        
    :attr password:
        Senha do usuário de acesso ao banco de dados.
        [type: string]
        
    :attr verbose:
        Atributo de gerenciamento de loggers durante a
        execução de algumas operações da classe.
        [type: bool, default=True]
    """
    
    def __init__(self, host, database, user, password, verbose=True):
        self.verbose = verbose
        try:
            # Realizando conexão
            self.conn = psycopg2.connect(host=host, 
                                         user=user, 
                                         password=password,
                                         database=database)          
            # Comunicando sucesso na conexão
            if self.verbose:
                with self.conn.cursor() as cur:
                    cur.execute('SELECT version()')
                    logger.info(f'Conexão realizada com sucesso em {cur.fetchone()[0]}')
                    self.conn.commit()
                    
        except Exception as e:
            logger.error(f'Erro ao conectar ao banco de dados. Exception: {e}')
            exit()
            
    # Mostrando tabelas existentes no banco de dados
    def show_tables(self):
        """
        Método responsável por listar todas as tabelas presentes
        no banco de dados a partir do comando
        SELECT tablename FROM pg_catalog.pg_tables

        O resultado é fornecido em um formato DataFrame ao 
        usuário final.

        Retorno
        -------
        :return tables:
            DataFrame contendo uma única coluna com todas as
            referências de tabelas encontradas no banco.
            [type: pd.DataFrame]
        """

        # Criando e executando query a partir de uma conexão existente
        query = 'SELECT tablename FROM pg_catalog.pg_tables'
        with self.conn.cursor() as cur:
            cur.execute(query)
            tables = pd.DataFrame(cur.fetchall())
            tables.columns = ['tablename']
            logger.info(f'Foram encontradas {len(tables)} tabelas no banco de dados')

        return tables
    
    # Executando queries através de uma conexão
    def execute_query(self, query):
        """
        Método responsável por aplicar uma query em uma
        na conexão com o banco de dados estabelecida.

        Parâmetros
        ----------
        :param query:
            String responsável por alocar a query de consulta a ser
            executada na conexão existente com o banco de dados.
            [type: string]
        """
        
        try:
            with self.conn.cursor() as cur:
                # Aplicando consulta e transformando em DataFrame
                cur.execute(query)
                self.conn.commit()
                
                # Comunicando resultado e retornando objeto
                if self.verbose:
                    query_type = query.split(' ')[0]
                    query_type = query_type.replace('\n', '') if '\n' in query_type else query_type
                    logger.info(f'Query {query_type} executada com sucesso')
            
        except Exception as e:
            logger.error(f'Erro ao executar consulta. Exception: {e}')
            self.conn.rollback()
    
    # Construindo e executando comando de criação de tabela via df
    def create_table_from_df(self, df, table, constraints=''):
        """
        Método responsável por gerar uma string de criação de 
        tabela por meio de um objeto DataFrame fornecido como
        argumento da função. Visando propor uma abordagem
        básica e simples de utilização, foi desenvolvida uma
        função auxiliar para conversão dos tipos primitivos 
        originais do objeto DataFrame para versões aplicáveis
        em um banco de dados padrão.

        Parâmetros
        ----------
        :param df: 
            Objeto DataFrame do pandas contendo as referências
            colunares a serem utilizadas como base para a 
            construção da query de criação de tabela.
            [type: pd.DataFrame]

        :param table:
            Nome da tabela a ser utilizada no comando de criação.
            [type: string]

        :param constraints:
            Restrições adicionais a serem estabelecidas na query
            de criação de tabela.
            [type: string, default='']
        """

        # Inicializando strings e parâmetros
        ct_string = 'CREATE TABLE IF NOT EXISTS <table_name> (<col_string>)'
        col_string = ''
        constraints = ''

        # Iterando sobre colunas e tipos primitivos do DataFrame
        for col, dtype in df.dtypes.items():

            # Convertendo tipos primitivos mais básicos
            if dtype in ('int64', 'int32'):
                psql_dtype = 'INT'
            elif dtype == 'object':
                psql_dtype = 'VARCHAR(255)'
            elif dtype in ('float64', 'float32'):
                psql_dtype = 'NUMERIC'

            # Incrementando query string
            splitter = ', '
            col_string += col + ' ' + str(psql_dtype) + splitter

        # Eliminando última vírgula
        col_string = col_string[:-len(splitter)]
        col_string += ' ' + constraints
        col_string = col_string.strip()

        # Substituindo valores na query principal
        ct_string = ct_string.replace('<table_name>', table)
        ct_string = ct_string.replace('<col_string>', col_string)
        
        try:
            # Executando query
            with self.conn.cursor() as cur:
                cur.execute(ct_string)
                self.conn.commit()

                # Comunicando resultado e retornando objeto
                if self.verbose:
                    logger.info(f'Comando CREATE TABLE {table} executado com sucesso')
        
        except Exception as e:
            logger.warning(f'Erro ao criar tabela a partir do DataFrame. Exception: {e}')
            self.conn.rollback()
    
    # Ingestão via psycopg2 utilizando o método execute_values()
    def insert_execute_values(self, df, table):
        """
        Método responsável por propor a ingestão de dados a partir
        de um objeto DataFrame do pandas utilizando o método
        execute_values() da biblioteca psycopg2. A lógica de
        implementação construída considera a substituição
        automática das tuplas de dados diretamente no método
        execute_values(), não sendo assim necessária a definição
        dos espaços alocados para cada registro no template
        de query.

        Parâmetros
        ----------
        :param df:
            Objeto DataFrame do pandas contendo os registros a serem
            inseridos na tabela de referência no banco de dados.
            [type: pd.DataFrame]

        :param table:
            Referência de tabela alvo da ingestão de dados no banco.
            [type: string]
        """

        # Prepara valores e colunas da query de ingestão
        rows = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))

        # Cria template de query já substituindo alguns valores
        query = f'INSERT INTO {table} ({cols}) VALUES %s'

        # Criando cursor e executando inserção
        with self.conn.cursor() as cur:
            try:
                extras.execute_values(cur, query, rows)
                self.conn.commit()
                if self.verbose:
                    logger.info(f'{len(df)} registros inseridos na tabela {table}')
            except (Exception, psycopg2.DatabaseError) as e:
                logger.warning(f'Erro ao realizar ingestão. Exception: {e}')
                self.conn.rollback()
    
    # Retornando valores de uma tabela
    def select_values(self, query, columns=None):
        """
        Método responsável por aplicar uma query de seleção
        na conexão com o banco de dados estabelecida, retornando
        assim o resultado em um objeto do tipo DataFrame.
        
        Opcionalmente, é possível passar uma lista com as colunas
        utilizadas na query de seleção para que esta possa servir
        de referência para o DataFrame resultante.

        Parâmetros
        ----------
        :param query:
            String responsável por alocar a query de consulta a ser
            executada na conexão existente com o banco de dados.
            [type: string]

        :param columns:
            Lista opcional de colunas a ser utilizada para atualizar
            as colunas do DataFrame resultante. Em seu valor padrão,
            o DataFrame gerado possuirá apenas os índices em
            suas colunas.
            [type: list, default=None]
        """
        
        try:
            with self.conn.cursor() as cur:
                # Aplicando consulta e transformando em DataFrame
                cur.execute(query)
                df_rs = pd.DataFrame(cur.fetchall())
                self.conn.commit()
                
                # Adicionando colunas ao DataFrame
                if columns is not None:
                    df_rs.columns = columns
                
                # Comunicando resultado e retornando objeto
                if self.verbose:
                    logger.info(f'Consulta realizada com sucesso com {len(df_rs)} linha(s) retornada(s)')
                
                return df_rs
            
        except Exception as e:
            logger.warning(f'Erro ao consultar dados. Exception: {e}')
            self.conn.rollback()
    