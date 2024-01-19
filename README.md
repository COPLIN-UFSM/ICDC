# IGC

Cálculo do índice geral de cursos (IGC), calculado pelo INEP, mas adaptado para calcular de cursos, departamentos, 
docentes...

## Sumário

* [Documentação](#documentação)
* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Instruções de uso](#instruções-de-uso)
* [Contato](#contato)
* [Bibliografia](#bibliografia)

## Documentação

* Views do banco de dados utilizadas neste repositório: [PAINÉIS](PAINEIS.md)
* Lógica do cálculo do IGC Docente: [IGC_DOCENTE](IGC_DOCENTE.md)
* [Nota técnica IGC 2022](data/nota_técnica_igc.pdf)

## Pré-requisitos

Este repositório requer a última versão do [Python Anaconda](https://www.anaconda.com/download) para ser executado, 
visto que usa o gerenciador de pacotes conda. O código executará em qualquer Sistema Operacional, mas foi desenvolvido
originalmente para Windows 10 Pro (64 bits).

As configurações da máquina que o repositório foi desenvolvido encontram-se na tabela abaixo:

| Configuração        | Valor                    |
|---------------------|--------------------------|
| Sistema operacional | Windows 10 Pro (64 bits) |
| Processador         | Intel core i7 9700       |
| Memória RAM         | 16GB                     |
| Necessita rede?     | Sim                      |


## Instalação

1. Crie um ambiente virtual do Anaconda com as seguintes configurações:

   ```bash
   conda create --name igc python==3.11.* pip --yes
   conda activate igc
   pip install ibm_db  # use ibm_db==3.1.4 para o Windows
   pip install "git+https://github.com/COPLIN-UFSM/db2.git"
   conda install --file requirements.txt --yes
   pip install --requirement pip_requirements.txt
   ```

2. Clone este repositório na sua máquina (ou então baixe o zip e descompacte em algum local):

   ```bash
   git clone https://github.com/COPLIN-UFSM/IGC.git
   ```
   
3. Dentro da pasta IGC, crie uma pasta `instance`. Dentro dela, crie outra pasta, `data`, e dentro desta última uma pasta `views`,
   de maneira que a estrutura de pastas fique da seguinte forma:

   * IGC
     * instance
       * database_credentials.json
       * data
         * views

4. Crie um arquivo `database_credentials.json` dentro da pasta `instance`, com as seguintes informações:

   ```json
   {
     "user": "bee",
     "password": null,
     "host": "bi.proj.ufsm.br",
     "port": 50000,
     "database": "bee"
   }
   ```
   Substitua `null` pela senha de acesso ao banco de dados.

## Instruções de Uso

Para executar o dashboard, entre na pasta IGC pela linha de comando, e execute da seguinte forma:

```bash
cd IGC  # entra na pasta clonada - pode ser outro diretório que não este
conda activate igc  # ativa o ambiente virtual 
python run.py --database-credentials instance/database_credentials.json --views-path instance/data/views
```

## Contato

O repositório foi originalmente desenvolvido por Henry: [henry.cagnini@ufsm.br]()

## Bibliografia

* [Documentação ibm_db](https://www.ibm.com/docs/en/db2/11.5?topic=framework-application-development-db)
