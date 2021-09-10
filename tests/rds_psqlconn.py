"""
---------------------------------------------------
--------------- TESTS: rds_psqlconn ---------------
---------------------------------------------------
Testes relacionados às funcionalidades da classe
PostgreSQLConnection presente no módulo rds.py do
pacote cloudgeass. Entre as features a serem testadas,
encontram-se a criação e eliminação de tabelas
relacionais no bancos de dados, upload de dados,
execuções de queries variadas e seleções de dados
em formatos de DataFrame.

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Gerenciando tabelas em bancos de dados
    2.1 Preparando e instanciando objetos
    2.2 Criando tabelas a partir de DataFrames
    2.3 Realizando ingestão em tabelas via DataFrame
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 01/09/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Módulos internos cloudgeass
from cloudgeass.aws.rds import PostgreSQLConnection
from cloudgeass.aws.s3 import JimmyBuckets

# Bibliotecas padrão
import os
from dotenv import find_dotenv, load_dotenv

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

# Variáveis de configuração AWS - RDS
load_dotenv(find_dotenv())
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = 'tbl_nbaflow_gamelog'

# Variáveis de configuração AWS - S3
REGION = 'sa-east-1'
BUCKET_NAME = 'nbaflow-files'
S3_OBJ_KEY = 'all_players_gamelog.csv'

# Variáveis de diretório
PROJECT_PATH = os.getcwd()
TMP_PATH = os.path.join(PROJECT_PATH, 'tmp')


"""
---------------------------------------------------
---- 2. GERENCIANDO TABELAS EM BANCOS DE DADOS ----
       2.1 Preparando e instanciando objetos
---------------------------------------------------
"""

# Instância de conexão ao banco de dados
db = PostgreSQLConnection(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=os.getenv('DB_PWD')
)

# Retorando arquivo de dados do s3 via JimmyBuckets
jbuckets = JimmyBuckets(region=REGION)
df = jbuckets.object_to_df(bucket_name=BUCKET_NAME, key=S3_OBJ_KEY)

# Dropando tabela alvo, caso existente
db.execute_query(f'DROP TABLE IF EXISTS {TABLE_NAME}')


"""
---------------------------------------------------
---- 2. GERENCIANDO TABELAS EM BANCOS DE DADOS ----
     2.2 Criando tabelas a partir de DataFrames
---------------------------------------------------
"""

# Retornando tabelas já existentes no banco
db_tables = db.show_tables()

# Criando tabela a partir de schema do DataFrame
db.create_table_from_df(df=df, table=TABLE_NAME)

# Retornando nova lista de tabelas
db_tables2 = db.show_tables()

# Validando funcionalidade
assert TABLE_NAME not in db_tables['tablename'].values, f'Tabela {TABLE_NAME} já existente no banco de dados antes da execução do método db.create_table_from_df()'
assert TABLE_NAME in db_tables2['tablename'].values, f'Tabela {TABLE_NAME} não existente na nova lista de tabelas do banco após a execução do método db.create_table_from_df()'
assert len(db_tables2) == len(db_tables) + 1, f'Quantidade de tabelas após o método ({len(db_tables2)}) diferente da quantidade de tabelas antes o método ({len(db_tables)}) + 1'


"""
---------------------------------------------------
---- 2. GERENCIANDO TABELAS EM BANCOS DE DADOS ----
 2.3 Realizando ingestão em tabelas via DataFrame
---------------------------------------------------
"""

# Inserindo dados a partir de DataFrame
db.insert_execute_values(df=df, table=TABLE_NAME)

# Realizando consulta para validar quantidade de registros
rows = db.select_values(
    query=f'SELECT count(1) AS qtd_linhas FROM {TABLE_NAME}',
    columns=['qtd_linhas']
)
qtd_rows = rows['qtd_linhas'][0]

# Validando funcionalidade
assert len(df) == qtd_rows, f'Quantidade de registros presentes na tabela após inserção ({qtd_rows}) difere da quantidade de linhas do DataFrame ({len(df)})'