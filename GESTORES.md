# Gestores

Este documento detalha a lógica de cálculo do **Índice de Contribuição Docente na Qualidade do Curso**, ou **ICDC.**

## Sumário 

  * [Proposta](#proposta)
  * [Cálculo](#cálculo)
    * [Nota média por modalidade](#nota-média-por-modalidade)
      * [Relação de peso de alunos](#relação-de-peso-de-alunos)
        * [Equivalência de alunos de mestrado](#equivalência-de-alunos-de-mestrado)
        * [Equivalência de alunos de doutorado](#equivalência-de-alunos-de-doutorado)
    * [Proporção de alunos](#proporção-de-alunos)
      * [Graduação](#graduação-)
      * [Mestrado](#mestrado)
      * [Doutorado](#doutorado)
    * [Cálculo do ICDC](#cálculo-do-icdc)
  * [Exemplos](#exemplos)

## Proposta

A proposta do ICDC é compor um índice em que seja possível mensurar a contribuição do docente na nota do 
[Conceito Preliminar de Curso (CPC)](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/indicadores-de-qualidade-da-educacao-superior/conceito-preliminar-de-curso-cpc),
que por sua vez é utilizado no [Índice Geral de Curso (IGC)](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/indicadores-de-qualidade-da-educacao-superior/indice-geral-de-cursos-igc).

A propriedade distributiva do ICDC é seu aspecto mais importante. Com base na nota do CPC contínuo (graduação) ou 
[Conceito CAPES](https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/avaliacao/sobre-a-avaliacao/avaliacao-o-que-e/sobre-a-avaliacao-conceitos-processos-e-normas/conceito-avaliacao) 
(pós-graduação) de cada curso, distribui-se esta nota para todos os docentes que lecionaram para turmas deste curso, 
ponderando-se pelo encargo didático (tempo lecionando) de cada docente, pelo número de alunos na turma do curso que 
solicitou a disciplina, e também pelo peso de cada aluno em sala de aula. 

A lógica do ICDC segue uma linha de raciocínio semelhante ao cálculo do Índice Geral de Cursos, porém com a ponderação
por encargo didático. A nota técnica do IGC do ano de 2022 está [aqui](data/nota_técnica_igc.pdf).
O cálculo do IGC por docente segue a mesma linha de raciocínio, porém utilizando dados de turmas e encargos.

## Cálculo

O cálculo do ICDC, à semelhança do IGC, segue diversas etapas. Primeiro calcula-se a 
[nota média por modalidade](#nota-média-por-modalidade) de ensino (graduação, mestrado, doutorado) - ou seja, o quão 
bom o docente é para cada modalidade de ensino que esse leciona.

A nota por modalidade se encontra no intervalo entre 0 e 5, sendo zero a pior qualidade e cinco a melhor qualidade. 
Docentes que não lecionam em uma modalidade terão nota zero.

A nota média por modalidade é ponderada pela [proporção de alunos](#proporção-de-alunos) daquela modalidade.

O [Cálculo do ICDC](#cálculo-do-icdc) é simplesmente o somatório das notas médias por modalidade ponderadas pela 
proporção de alunos por modalidade.

### Nota média por modalidade

A nota média por modalidade (graduação, mestrado, doutorado) é dada por

$$
\text{Média}\_{m} = \frac{\sum\_{t}^{T \in m} (N\_{c}^{(t)} * P\_{m,c} * \text{encargo}^{(t)} * \text{CC}\_c^{(t)})}{\sum\_{t}^{T \in m} (N_{c}^{(t)} * P\_{m,c} * \text{encargo}^{(t)})}
$$

Onde:

* $\text{Média}\_{m}$ é a nota média do docente na modalidade $m$ (graduação, mestrado ou doutorado);
* $T$ é o conjunto de todas as turmas do docente para a modalidade $m$, para o ano calculado, sendo $t$ uma turma em 
  particular;
* $P\_{m,c}$ é o [peso do discente](#relação-de-peso-de-alunos) para aquela modalidade, para aquele curso;
* $N\_{c}^{(t)}$ é o número de alunos aprovados com nota, reprovados com nota, ou matriculados na disciplina, no ano do 
  cálculo;
* $\text{encargo}^{(t)}$ é o encargo didático da turma;
* $\text{CC}\_c^{(t)}$ é o conceito do curso: CPC contínuo mais recente para cursos de graduação, e Conceito CAPES mais
  recente para cursos de pós-graduação

#### Relação de peso de alunos

Segundo a [lógica do IGC](data/nota_técnica_igc.pdf), deve-se estabelecer uma relação de peso entre alunos de graduação
e pós-graduação, nas modalidades de mestrado e doutorado, a depender do Conceito CAPES do programa de pós-graduação.

Alunos de graduação sempre possuem peso $P\_{\text{graduação},c} = 1$, independente do CPC Contínuo do curso.

##### Equivalência de alunos de mestrado

| Conceito do mestrado CAPES | $P\_{\text{mestrado},c}$ |
|:---------------------------|:-------------------------|
| 3                          | 1                        |
| 4                          | 2                        |
| 5                          | 3                        |
| 6                          | 3                        |
| 7                          | 3                        |

##### Equivalência de alunos de doutorado

| Conceito do doutorado CAPES | $P\_{\text{doutorado},c}$ |
|:----------------------------|:--------------------------|
| 3                           | 1                         |
| 4                           | 2                         |
| 5                           | 3                         |
| 6                           | 4                         |
| 7                           | 5                         |

### Proporção de alunos

A proporção de alunos $\alpha$, $\beta$ e $\gamma$ são simplesmente o somatório do número de alunos, cujo curso é o 
mesmo do curso de solicitação da vaga na turma, **para aquela modalidade,** dividido pelo número de alunos, cujo curso 
é o mesmo do curso de solicitação da vaga na turma, **para todas as modalidades:**

#### Graduação 

$$
\alpha = \frac{\sum\_{t}^{T\_{\text{graduação}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

#### Mestrado

$$
\beta = \frac{\sum\_{t}^{T\_{\text{mestrado}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

#### Doutorado

$$
\gamma = \frac{\sum\_{t}^{T\_{\text{doutorado}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

Onde:

* $T\_{\text{graduação}}$, $T\_{\text{mestrado}}$ e $T\_{\text{doutorado}}$ são respectivamente o número de alunos de 
  graduação, mestrado e doutorado, cujo curso é o mesmo curso de solicitação de vaga na turma, para os quais o professor
  deu aula no ano do cálculo;
* $\sum\_{t}^{T} N\_{c}^{(t)}$ são todos os alunos cujo curso é o mesmo curso de solicitação de vaga na turma, para os 
  quais o professor deu aula no ano analisado.

### Cálculo do ICDC

O cálculo do ICDC é dado por

$$
ICDC = \alpha * \text{Média}\_{\text{graduação}} + \beta * \text{Média}\_{\text{mestrado}} + \gamma * \text{Média}\_{\text{doutorado}}
$$

## Exemplos

### Exemplo 1: um professor 

| Turma | Disciplina | Modalidade | Docentes          | Encargo didático | Curso de solicitação da turma |       Conceito de Curso (CC) |                                       Alunos |
|:------|:-----------|:-----------|:------------------|-----------------:|:------------------------------|-----------------------------:|---------------------------------------------:|
| 10    | Cálculo A  | Graduação  | 1 (João da Silva) |              90h | Engenharia Química            |                        3.366 | 20 (Eng. Química); 7 (Ciência da Computação) |
| 11    | Cálculo B  | Graduação  | 1 (João da Silva) |              90h | Engenharia Civil              |                        3.570 |            15 (Eng. Civil); 5 (Eng. Química) |
 

Como o docente João da Silva não leciona nenhuma disciplina no mestrado ou doutorado, 
$\text{Média}\_{\text{mestrado}} = 0$ e $\text{Média}\_{\text{doutorado}} = 0$.

Considerando que o peso de alunos de graduação P\_{\text{graduação},c} é sempre 1, independente da qualidade do curso 
$c$, a nota média da graduação deste docente é 

$$
\begin{eqnarray}
\text{Média}\_{\text{graduação}} =& \frac{\sum\_{t}^{T \in \text{graduação}} (N\_{c}^{(t)} * P\_{\text{graduação},c} * \text{encargo}^{(t)} * \text{CC}\_c^{(t)})}{\sum\_{t}^{T \in \text{graduação}} (N_{c}^{(t)} * P\_{\text{graduação},c} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{graduação}} =& \frac{(20 * 1 * 90 * 3.366) + (15 * 1 * 90 * 3.570)}{(20 * 1 * 90) + (15 * 1 * 90)} \\
& \\
\text{Média}\_{\text{graduação}} =& \frac{10878.3}{3150} \\
& \\
\text{Média}\_{\text{graduação}} =& \frac{10878.3}{3150} \\
& \\
\text{Média}\_{\text{graduação}} =& 3.453428571 = 3.45
\end{eqnarray}
$$