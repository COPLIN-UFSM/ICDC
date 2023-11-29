# Título do repositório

Descrição curta do repositório.

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
conda create --name myenv python==3.* pip --yes
conda activate myenv
conda install --file requirements.txt --yes
```

## Instruções de Uso

Descreva aqui o passo-a-passo que outros usuários precisam realizar para conseguir executar com sucesso o código-fonte
deste projeto:

```bash
python main.py
```

## Contato

O repositório foi originalmente desenvolvido por Fulano: [fulano@ufsm.br]()

## Bibliografia

Adicione aqui entradas numa lista com a documentação pertinente:

* [Documentação ibm_db](https://www.ibm.com/docs/en/db2/11.5?topic=framework-application-development-db)