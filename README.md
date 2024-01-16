# IGC

Cálculo do índice geral de cursos (IGC), calculado pelo INEP, mas adaptado para calcular de cursos, departamentos, 
docentes...

## Sumário

* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Instruções de uso](#instruções-de-uso)
* [Contato](#contato)
* [Bibliografia](#bibliografia)

## Pré-requisitos

Esta seção detalha os pré-requisitos que outro usuário precisa atingir para poder executar o código-fonte. Por exemplo,
o parágrafo abaixo descreve um requisito do Python Anaconda:

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

Descreva aqui as instruções para instalar as ferramentas, bibliotecas e plugins para executar o código do projeto:

```bash
conda create --name igc python==3.11.* pip --yes
conda activate igc
pip install ibm_db  # use ibm_db==3.1.4 para o Windows
pip install "git+https://github.com/COPLIN-UFSM/db2.git"
conda install --file requirements.txt --yes
pip install --requirement pip_requirements.txt
```

**NOTA:** caso encontre problemas com o ibm_db no Windows, utilize a versão 3.1.4:

```bash
pip install ibm_db==3.1.4
```

## Instruções de Uso

Descreva aqui o passo-a-passo que outros usuários precisam realizar para conseguir executar com sucesso o código-fonte
deste projeto:

```bash
python from_open_data.py
```

## Contato

O repositório foi originalmente desenvolvido por Fulano: [fulano@ufsm.br]()

## Bibliografia

Adicione aqui entradas numa lista com a documentação pertinente:

* [Documentação ibm_db](https://www.ibm.com/docs/en/db2/11.5?topic=framework-application-development-db)