## Sumário

* [Documentação](#documentação)
* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Instruções de uso](#instruções-de-uso)

## Documentação

* Views do banco de dados utilizadas neste repositório: [VIEWS](VIEWS.md)
* Lógica do cálculo do ICDC: [GESTORES](GESTORES.md)

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

1. Clone este repositório na sua máquina (ou então baixe o zip e descompacte em algum local):

   ```bash
   git clone https://github.com/COPLIN-UFSM/IGC.git
   ```

2. Crie um ambiente virtual do Anaconda executando pela linha de comando 

   ```bash
   conda env create -f environment.yml
   ```
   
3. Dentro da pasta ICDC, crie uma pasta `instance`. Dentro dela, crie outra pasta, `data`, e dentro desta última uma 
   pasta `views`, de maneira que a estrutura de pastas fique da seguinte forma:

   * ICDC
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

Para executar o dashboard, entre na pasta ICDC pela linha de comando, e execute da seguinte forma:

```bash
cd icdc  # entra no repositório clonado localmente 
conda activate icdc  # ativa o ambiente virtual 
python run.py --database-credentials instance/database_credentials.json --views-path instance/data/views
```
