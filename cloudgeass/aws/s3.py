"""
---------------------------------------------------
------------------- MÓDULO: s3 --------------------
---------------------------------------------------
Módulo responsável por alocar desenvolvimentos
relacionados à utilização do SDK Python boto3 para
o gerencimento do serviço s3 (Simple Storage Service)
da AWS. O objetivo deste arquivo é providenciar
funções, classes e métodos encapsulados capazes de
facilitar o desenvolvimento de aplicações que 
necessitem utilizar o serviço de s3 de armazenamento
de objetos na nuvem.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Simple Storage Service
    2.1 Classe estruturada para operações no s3
    2.2 Funções de utilidade geral
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 27/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# SDK Python
import boto3
from botocore.exceptions import ClientError

# Bibliotecas padrão
import os
import pandas as pd
from io import BytesIO

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


# Definindo parâmetro de região para uso nas funções
REGION = 'sa-east-1'


"""
---------------------------------------------------
------------ 2. SIMPLE STORAGE SERVICE ------------
     2.1 Classe estruturada para operações no s3
---------------------------------------------------
"""

class JimmyBuckets():
    """
    Classe construída para facilitar a aplicação de operações
    básicas no s3 utilizando SDK Python boto3. Com ela, é 
    possível utilizar métodos encapsulados para operações de
    criação, exclusão, upload e leitura de objetos em buckets
    no s3. Cada instância de objeto desta classe recebe um 
    único argumento referente à região de atuação para que, 
    em seu método construtor, seja possível instanciar um
    recurso e um client s3 via boto3.

    Atributos da classe
    -------------------
    :attr region:
        Região de utilização dos recursos s3 da AWS. Por 
        padrão, o módulo contém uma variável atribuída
        no início do código que define uma região em
        específico que, ao mesmo tempo, pode ser modificada
        no ato de instância desta classe.
        [type: string, default='sa-east-1']
    """

    def __init__(self, region=REGION):
        # Instanciando recurso e client s3 via boto3
        self.region = region
        self.s3_resource = boto3.resource('s3', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)

    # Listando buckets existentes
    def list_buckets(self):
        return [b.name for b in self.s3_resource.buckets.all()]
    
    # Listando todos os objetos em um bucket
    def list_bucket_objects(self, bucket_name, prefix=''):
        bucket = self.s3_resource.Bucket(bucket_name)
        return [obj.key for obj in bucket.objects.filter(Prefix=prefix)]

    # Criando novos buckets na AWS
    def create_bucket(self, bucket_name, acl='private', **kwargs):
        """
        Método criado para consolidar os principais elementos de
        criação de buckets s3 através do SDK boto3. O código aqui
        encapsulado visa propor um detalhamento mais claro sobre
        as etapas mais comuns de criação de bucket, providenciando
        ao usuário uma maior abstração nas configurações mais
        básicas dentro deste universo. De maneira geral, esta
        função instancia um recurso s3 via boto3 e utiliza o método
        create_bucket() para consolidar as operações de criação
        de buckets.
        
        Para detalhes adicionais ou operações mais avançadas
        relacionadas à criação de buckets, verificar a documentação
        oficial do boto3 na AWS.
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]
            
        :param acl:
            Parâmetro que define o controle de acesso definido
            para o bucket (Access Control List). Neste contexto
            o argumento acl propõe a utilização de um bloco
            consolidado de controle predefinido dentro das 
            diretrizes da AWS. Através da documentação de 
            referência do SDK, é possível visualizar as opções 
            possíveis enblocadas para a definição de controle 
            de acesso.
            [type: string, default='private']
            
        Argumentos Adicionais
        ---------------------
        :kwarg block_public:
            Flag que define a modificação da política de acesso
            ao bucket criado. Ao ser configurado como True, é
            instanciado um client s3 via boto3 e executado o
            método put_public_access_block() para bloqueio de
            todo acesso público proveniente ACLs ou configurações
            adicionais do bucket. A definição exata do bloqueio
            de acesso público é definida a partir do argumento
            adicional block_public_config.
            [type: bool, default=True]
        
        :kwarg block_public_config:
            Dicionário de configuração com chaves específicas 
            de definição das restrições a serem aplicadas no
            método put_public_acess_block() do client s3
            instanciado.
            [type: dict, default={
                            'BlockPublicAcls': True,
                            'IgnorePublicAcls': True,
                            'BlockPublicPolicy': True,
                            'RestrictPublicBuckets': True
                        }]
        """

        # Criando um novo bucket
        try:
            location = kwargs['location'] if 'location' in kwargs else {'LocationConstraint': self.region}
            self.s3_resource.create_bucket(
                Bucket=bucket_name, 
                ACL=acl,
                CreateBucketConfiguration=location
            )
            logger.info(f'Bucket {bucket_name} criado com sucesso')

        except (self.s3_client.exceptions.BucketAlreadyExists, self.s3_client.exceptions.BucketAlreadyOwnedByYou) as e:
            logger.warning(f'Bucket {bucket_name} já existente. A criação de um novo bucket não será realizada. Exception: {e}')
            return None

        except ClientError as ce:
            logger.error(f'Erro durante a criação do bucket. Exception: {ce}')
                
        # Validando bloqueio de acesso público ao bucket
        block_public = kwargs['block_public'] if 'block_public' in kwargs else True
        if block_public:
            config = {
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
            block_public_config = kwargs['block_public_config'] if 'block_public_config' in kwargs else config
            
            # Instanciando sessão e configurando bloqueio de acesso público
            try:
                self.s3_client.put_public_access_block(Bucket=bucket_name,
                                                PublicAccessBlockConfiguration=block_public_config)
            except Exception as e:
                logger.warning(f'Erro ao instanciar client e bloquear acesso público ao bucket {bucket_name}. Exception: {e}')
                
    # Eliminando buckets já existentes na AWS
    def delete_bucket(self, bucket_name, empty_bucket=False):
        """
        Método criado para encapsular as ações relacionadas à 
        exclusão de buckets s3 através do SDK boto3. De maneira 
        geral, o método utiliza um recurso do s3 instanciado via 
        boto3 para a criação de um objeto "bucket" gerado através 
        do método resource.Bucket(), permitindo a posterior execução
        do método bucket.delete(). Em linha com as funcionalidades 
        deste módulo, este método comporta as principais tratativas 
        de erros encontradas no processo de exclusão de buckets, 
        permitindo assim um detalhamento claro e direto ao usuário. 
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]

        :param empty_bucket:
            Flag que define o esvaziamento do bucket, ou seja,
            a exclusão de todos os objetos existentes no mesmo.
            O gerenciamento incorreto deste argumento pode
            causar danos irreversíveis ao conteúdo do bucket
            selecionado e, portanto, sua atribuição deve ser
            realizada com cautela. No código, ao tentar eliminar 
            um bucket através do método bucket.delete(), a
            exceção ClientError é invocada e, por ela, a 
            verificação de esvaziamento de bucket é verificada
            para que todos os objetos sejam eliminados antes de
            uma nova tentativa de delete do bucket. Caso o código
            caia nesta exceção e o parâmetro empty_bucket esteja
            configurado como "False", a exclusão do bucket não
            é realizada.
            [type: bool, default=False]
        """

        # Deletando bucket 
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            bucket.delete()
            logger.info(f'Bucket {bucket_name} deletado com sucesso')
        
        except self.s3_client.exceptions.NoSuchBucket as nsbe:
            logger.warning(f'Bucket {bucket_name} inexistente. Nenhuma ação de delete realizada. Exception: {nsbe}')
            return None

        except ClientError as ce:
            # Coletando objetos do bucket e verificando flag de esvaziamento
            bucket_objects = [obj for obj in bucket.objects.all()]
            if len(bucket_objects) > 0 and empty_bucket:            
                # Esvaziando e deletando bucket
                logger.warning(f'O bucket {bucket_name} possui {len(bucket_objects)} objetos. Esvaziando bucket e tentando delete novamente')
                try:
                    bucket.objects.all().delete()
                    bucket.delete()
                    logger.info(f'Bucket {bucket_name} deletado com sucesso')
                except Exception as e:
                    logger.error(f'Erro ao esvaziar e deletar bucket {bucket_name}. Exception: {e}')
            else:
                # Bucket não está vazio e flag de esvaziamento não configurado
                logger.error(f'Erro ao deletar bucket {bucket_name}. O bucket possui {len(bucket_objects)} e o parâmetro "empty_bucket" é igual a False. Exception: {ce}')
            
    # Realizando upload de arquivos para buckets s3
    def upload_object(self, file, bucket_name, key,
                      method='put_object', verbose=True):
        
        """
        Método criado para encapsular as ações relacionadas ao 
        upload de objetos em um bucket s3 utilizando o SDK boto3.
        Entre as possibilidades existentes, o usuário pode escolher,
        através do argumento "method" da função, realizar o upload 
        por dois diferentes métodos de um client: put_object() ou 
        upload_file().

        Com o method igual a put_object(), o usuário pode fornecer, para
        o argumento "file" deste método, um caminho de armazenamento
        local do objeto ou então o conteúdo binário do mesmo lido
        previamente no código. Já com o método upload_file(), o
        usuário deve passar obrigatoriamente apenas um caminho
        de armazenamento local do objeto.
        
        Parâmetros
        ----------
        :param file:
            Buffer binário do objeto alvo ou então string de
            referência de armazenamento local do arquivo (caso
            o método seja definido como upload_object()).
            [type: string or buffer]

        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]
            
        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param method:
            Método de upload do objeto no bucket de referência.
            O usuário deve selecionar entre "put_object" ou
            "upload_file" para que, internamente, o método possa
            realizar a execução de um dos dois métodos do client
            instanciado. Como precaução, o usuário deve apenas
            atentar-se ao fato de que, caso o método escolhido
            seja "upload_file", o parâmetro "file" da função
            deve, obrigatoriamente, referenciar um caminho
            local de armazenamento do arquivo a ser ingerido.
            Adicionalmente, o método trata qualquer outro caso
            de possível equívoco caso o usuário selecione um
            método diferente dessas duas possibilidades, retornando
            uma mensagem e cancelando o processo de upload.
            [type: string, default="put_object"]

        :param verbose:
            Flag de verbosidade para logs aplicados durante
            as tratativas de upload de objetos no método.
            [type: bool, default=True]
        """

        # Verificando método de upload
        if method == 'put_object':
            # Realizando upload de stream binária já em buffer
            try:
                with open(file, 'rb') as f:
                    self.s3_client.put_object(Bucket=bucket_name, Body=f, Key=key)
            except Exception as e:
                logger.error(f'Erro ao realizar upload via client.put_object(). Exception: {e}')
                return None
        
        elif method == 'upload_file':
            # Realizando upload a partir de arquivo local
            try:
                self.s3_client.upload_file(Bucket=bucket_name, Filename=file, Key=key)
            except ValueError as ve:
                logger.error(f'Erro ao realizar upload via client.upload_file(). Exception: {ve}')
                return None
        
        else:
            logger.error(f'Método de upload "{method}" inválido. Selecione entre "put_object" ou "upload_file"')
            return None

        # Comunicando resultado
        if verbose:
            logger.info(f'Upload do objeto {key} realizado com sucesso no bucket {bucket_name}')

    # Realizando upload de todos os arquivos em um diretório local
    def upload_directory(self, directory, bucket_name, ignore_folders=[], ignore_files=[],
                         folder_prefix='', method='put_object', inner_verbose=False, outer_verbose=True):
        """
        Método criado para com o objetivo de encapsular múltiplas
        execuções de upload de objetos no s3 presentes em um
        diretório local de referência. Em outras palavras, o
        argumento principal deste método é uma referência de 
        diretório que, por sua vez, será utilizada para verificar
        todos os subdiretórios e arquivos presentes, propondo assim
        múltiplas execuções da função upload_object() presente
        neste módulo.

        Visando propor uma melhor organização dos objetos a serem
        ingeridos no bucket, o método conta com uma lógica que
        coleta os subdiretórios encontrados e os transforma em
        prefixos (ou pastas) no s3, fazendo assim com que a mesma
        estrutura organizacional dos arquivos no dirtório raíz
        seja mantida também no s3.
        
        Parâmetros
        ----------
        :param directory:
            Referência local de diretório a ser utilizado como
            alvo de navegação para extração de todos os arquivos
            presentes. Na prática, a função utiliza o método
            os.walk() para coletar todos os subdiretórios e 
            arquivos do diretório em um laço de repetição que,
            ao final, chama a função de upload individual de
            objeto para cada referência de arquivo encontrada.
            [type: string]

        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]

        :param folder_prefix:
            Propondo uma maior liberdade em definições de
            organização da estrutura a ser espelhada no bucket
            este argumento permite com que o usuário defina um
            prefixo (ou diretório) raíz a ser inserido no s3.
            Por padrão, o argumento contempla uma string vazia
            para que a mesma estrutura do diretório raíz seja
            espelhada no s3.
            [type: string, default='']
    
        :param method:
            Método de upload do objeto no bucket de referência.
            O usuário deve selecionar entre "put_object" ou
            "upload_file" para que, internamente, o método possa
            realizar a execução de um dos dois métodos do client
            instanciado. Como precaução, o usuário deve apenas
            atentar-se ao fato de que, caso o método escolhido
            seja "upload_file", o parâmetro "file" da função
            deve, obrigatoriamente, referenciar um caminho
            local de armazenamento do arquivo a ser ingerido.
            Adicionalmente, o método trata qualquer outro caso
            de possível equívoco caso o usuário selecione um
            método diferente dessas duas possibilidades, retornando
            uma mensagem e cancelando o processo de upload.
            [type: string, default="put_object"]

        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param inner_verbose:
            Flag de verbosidade para as mensagens de logs 
            aplicadas no método individual de upload de objetos. 
            Este parâmetro é passado para o parâmetro "verbose" 
            do método upload_object().
            [type: bool, default=False]

        :param outer_verbose:
            Flag de verbosidade para as mensagens de logs 
            aplicadas em laços externos neste método.
            [type: bool, default=True]
        """

        # Levantando parâmetros
        """if outer_verbose:
            total_objects = len([name for _, _, files in os.walk(directory) for name in files])
            logger.debug(f'Iniciando upload dos {total_objects} objetos encontrados no diretório alvo')"""

        # Navegando por todos os arquivos em um diretório
        i = 0
        for path, dirs, files in os.walk(directory):
            # Criando novas listas eliminando pastas e arquivos ignorados
            dirs[:] = [d for d in dirs if d not in ignore_folders]
            files[:] = [f for f in files if f not in ignore_files]

            # Iterando sobre cada arquivo e realizando upload
            for name in files:
                i += 1
                filepath = os.path.join(path, name)
                key = filepath.replace(directory, folder_prefix).replace(os.path.sep, '/')[1:]
                # Realizando ingestão de cada objeto encontrado
                self.upload_object(
                    file=filepath,
                    bucket_name=bucket_name,
                    key=key,
                    method=method,
                    verbose=inner_verbose
                )

        if outer_verbose:
            logger.info(f'Fim do processo de upload dos {i} objetos listados no diretório')
    
    # Lendo objeto direto do s3
    def read_object(self, bucket_name, key, verbose=True):
        """
        Método criado para a coleta de um objeto no s3 em um
        stream binário de bytes. Na prática, este método atua
        como um facilitador dentro da aplicação do método
        client.get_object de um client s3 instanciado. De
        forma adicional, outros métodos da classe JimmyBuckets
        podem utilizar deste método para implementações 
        específicas de leitura de objetos como, por exemplo, a
        leitura de um objeto em um bucket direto em um formato
        DataFrame.

        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]
            
        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param verbose:
            Flag de verbosidade para logs aplicados durante
            as tratativas de upload de objetos no método.
            [type: bool, default=True]

        Retorno
        -------
        :return data:
            Stream de dados referente ao objeto lido do bucket.
            Na prática, o método entrega o conteúdo da chave
            ['Body'] do elemento resultante do método 
            client.get_object() do boto3. O resultado é entregue
            em um formato de bytes através da leitura do conteúdo
            originalmente entregue em um formato identificado por
            botocore.response.StreamingBody.
            Eventualmente, o conteúdo em bytes pode ser transformado
            em um streaming de dados a partir da utilização de um
            buffer (StringIO ou BytesIO).
            [type: bytes]
        """

        try:
            obj = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            data = obj['Body'].read()
            if verbose:
                logger.info(f'Objeto {key} lido com sucesso e transformado em bytes')
            return data
        
        except self.s3_client.exceptions.NoSuchKey as nske:
            logger.error(f'Erro ao coletar objeto {key} por erro de chave inválida. Exception: {nske}')
            return None

        except ClientError as ce:
            logger.error(f'Erro de client ao coletar objeto. Exception: {ce}')
            return None

    # Lendo objetos no s3 e transformando em DataFrame
    def object_to_df(self, bucket_name, key, encoding='utf-8', verbose=True):
        """
        Método criado para a coleta de um objeto no s3 seguida
        da transformação em um DataFrame do pandas. Com esse
        método, o usuário pode fornecer uma chave específica
        de um objeto armazenado em um bucket e obter o resultado
        direto em um DataFrame, facilitando tratativas e análises
        posteriores. A transferência ocorre a partir da resposta
        obtida através da execução do método client.get_object(),
        onde é feita um armazenamento em buffer de bytes para a
        devida leitura via pd.read_csv(). Neste cenário, é 
        importante citar que este método funciona bem para objetos
        do tipo .csv ou .txt legíveis pela função de leitura
        do pandas. Outros objetos que eventualmente diferem 
        destes formatos podem gerar falhas de execução.
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]
            
        :param key:
            Chave de armazenamento do objeto no s3.
            [type: string]

        :param encoding:
            Tipo de encoding utilizado na leitura do buffer
            do stream de dados armazenado.
            [type: string, default="utf-8"]

        :param verbose:
            Flag de verbosidade para logs aplicados durante
            as tratativas de upload de objetos no método.
            [type: bool, default=True]
        
        Retorno
        -------
        :return df:
            DataFrame do pandas gerado a partir da utilização
            de um buffer BytesIO para armazenamento dos dados
            em bytes lidos a partir da execução do método
            self.read_object() desta classe.
            [type: pd.DataFrame]
        """
        
        logger.debug(f'Coletando objeto {key} do bucket {bucket_name} e transformando em DataFrame')
        try:
            data = self.read_object(bucket_name=bucket_name, key=key, verbose=verbose)
            df = pd.read_csv(BytesIO(data), encoding=encoding)
            if verbose:
                logger.info(f'Objeto {key} coletado com sucesso. Dimensões do DataFrame resultante: {df.shape}')
            return df
        
        except self.s3_client.exceptions.NoSuchKey as nske:
            logger.error(f'Erro ao coletar objeto {key} por erro de chave inválida. Exception: {nske}')
            return None

        except UnicodeDecodeError as ude:
            logger.error(f'Erro de codificação do objeto {key}. Verifique se o objeto é um arquivo em formato csv ou txt válido. Exception: {ude}')
            return None

        except ClientError as ce:
            logger.error(f'Erro de client ao coletar objeto. Exception: {ce}')
            return None

    # Baixando todos os objetos de um bucket mantendo a estrutura local
    def download_all_objects(self, bucket_name, prefix='', verbose=True, **kwargs):
        """
        Método criado para o download de todos os objetos
        listados em um determinado bucket com a opção de 
        filtrar um prefixo específico. Como feature adicional,
        toda a estrutura de prefixos (diretórios) do bucket
        selecionado é mantida localmente a partir do retorno
        dos prefixos e criação de diretórios locais a partir
        de um caminho inicial fornecido pelo parâmetro
        "local_dir" deste método.

        Em outras palavras, ao apontar pra um determinado
        bucket e selecionar um determinado prefixo, toda
        sua estrutura é espelhada localmente a partir da
        criação de novos diretórios capazes de receber
        todos os objetos/arquivos baixados do bucket.
        
        Parâmetros
        ----------
        :param bucket_name:
            Referência do bucket a ser utilizada dentro da 
            proposta de execução do método.
            [type: string]
            
        :param prefix:
            Prefixo ou "subdiretório" a ser utilizado como
            filtro na busca dos arquivos a serem baixados
            dentro de um determinado bucket. Por padrão,
            este argumento é configurado como uma string
            vazia para que, dessa forma, a varredura de 
            objetos seja feita utilizando o próprio bucket
            como raíz.
            [type: string, default='']

        :param verbose:
            Flag de verbosidade para logs aplicados durante
            as tratativas de upload de objetos no método.
            [type: bool, default=True]

        Argumentos Adicionais
        ---------------------
        :kwarg local_dir:
            Diretório local de destino de toda a estrutura
            do bucket, incluindo subdiretórios e arquivos.
            Caso o usuário não passe explicitamente este
            argumento, o diretório raíz de download da 
            estrutura do bucket é definido como sendo o 
            diretório atual de trabalho contando com uma
            pasta com o nome do bucket alvo.
            [type: string, 
             default=os.path.join(os.getcwd(), bucket_name)]
        """

        # Estrutura do bucket
        logger.debug(f'Coletando estrutura completa do bucket {bucket_name} incluindo chaves e prefixos')
        bucket = self.s3_resource.Bucket(bucket_name)
        keys = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
        prefixes = sorted(list(dict.fromkeys([os.path.dirname(k) for k in keys if '/' in k])))
        local_dir = kwargs['local_dir'] if 'local_dir' in kwargs else os.path.join(os.getcwd(), bucket_name)

        # Estrutura local
        logger.debug(f'Preparando estrutura local com os prefixos obtidos')
        for dirname in prefixes:
            try:
                local_path = os.path.join(local_dir, dirname)
                if not os.path.isdir(local_path):
                    os.makedirs(local_path)
            except Exception as e:
                logger.warning(f'Erro ao criar diretório {dirname}. Exception: {e}')
        
        # Download dos objetos
        logger.debug(f'Realizando download dos objetos listados na estrutura local criada')
        i = 0
        for k in keys:
            try:
                self.s3_client.download_file(bucket_name, k, os.path.join(local_dir, k))
                i += 1
            except Exception as e:
                if verbose:
                    logger.error(f'Erro ao realizar o donwload do objeto {k}. Exception: {e}')

        logger.info(f'Download de {i} dos {len(keys)} objetos listados em {local_dir}. Efetividade de {100*round(i/len(keys), 0)}%')

