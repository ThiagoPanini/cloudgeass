# Organização da Biblioteca

## Módulos Disponíveis

Antes de navegar pelas diferentes possibilidades da biblioteca *cloudgeass*, é importante entender um pouco mais sobre sua estrutura. Em linhas gerais, sua organização se dá através de **funções** presentes em diferentes **módulos** que encapsulam funcionalidaes de acordo com uma temática ou serviço AWS.

Atualmente, os módulos disponíveis na biblioteca são:

- :bucket: `cloudgeass.aws.s3`: funcionalidades para operações no S3
- :key: `cloudgeass.aws.secrets`: funcionalidades para operações no Secrets Manager
- :soap: `cloudgeass.aws.glue`: :warning: *em ideação*

???+ note "Sobre a ideia de futuro da biblioteca"
    
    A medida que novas necessidades se façam presentes, módulos adicionais poderão ser codificados e entregues aos usuários sempre com a mesma proposta: facilitar a construção de aplicações na AWS a partir do encapsulamento de blocos de código contendo operações comuns.

___

## Exemplos Práticos

Visando alcançar o maior número de usuários possível, uma série de demonstrações práticas foram gravadas para exemplificar algumas das principais funcionalidades do *cloudgeass*. Não deixe de assistir!

:material-alert-decagram:{ .mdx-pulse .warning } [Funcionalidades envolvendo o S3](./exemplos-s3.md)