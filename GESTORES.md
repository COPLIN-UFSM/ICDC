[![LiaScript](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)](https://liascript.github.io/course/?https://raw.githubusercontent.com/COPLIN-UFSM/ICDC/main/GESTORES.md)

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
    * [Graduação](#graduação)
    * [Mestrado](#mestrado)
    * [Doutorado](#doutorado)
  * [Cálculo do ICDC](#cálculo-do-icdc)
* [Casos especiais](#casos-especiais)
  * [Cursos ABI (Área Básica de Ingresso)](#cursos-abi-área-básica-de-ingresso)
  * [Cursos técnicos, ensino médio, e educação básica](#cursos-técnicos-ensino-médio-e-educação-básica)
  * [Período de tempo de cálculo](#período-de-tempo-de-cálculo)
* [Exemplos](#exemplos)
  * [Exemplo 1: um professor por disciplina](#exemplo-1-um-professor-por-disciplina)
  * [Exemplo 2: dois professores em uma disciplina](#exemplo-2-dois-professores-em-uma-disciplina)
  * [Exemplo 3: cursos de pós-graduação](#exemplo-3-cursos-de-pós-graduação)


## Proposta

A proposta do ICDC é compor um índice em que seja possível mensurar a contribuição **indireta** do docente na nota do 
[Conceito Preliminar de Curso (CPC)](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/indicadores-de-qualidade-da-educacao-superior/conceito-preliminar-de-curso-cpc)
(graduação) e no [Conceito CAPES](https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/avaliacao/sobre-a-avaliacao/avaliacao-o-que-e/sobre-a-avaliacao-conceitos-processos-e-normas/conceito-avaliacao) (pós-graduação).

A propriedade distributiva do ICDC é seu aspecto mais importante. Com base na nota do Conceito de Curso (CC), que é 
o CPC contínuo (graduação) ou Conceito CAPES (pós-graduação) de cada curso, distribui-se esta nota para todos os 
docentes que lecionaram para turmas deste curso, ponderando-se pelo encargo didático (tempo lecionando) de cada docente, 
pelo número de alunos na turma do curso que solicitou a disciplina, e também pelo peso de cada aluno em sala de aula. 

A lógica do ICDC segue uma linha de raciocínio semelhante ao cálculo do [Índice Geral de Cursos](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/indicadores-de-qualidade-da-educacao-superior/indice-geral-de-cursos-igc),
porém ponderando-se pelo encargo didático. Para maiores detalhes do cálculo do IGC, consulte a 
[nota técnica do ano 2022](data/nota_técnica_igc.pdf), utilizada como base para o ICDC. 

## Cálculo

O ICDC possui diversas etapas de cálculo. Primeiro calcula-se a 
[nota média por modalidade](#nota-média-por-modalidade) de ensino (graduação, mestrado, doutorado) - ou seja, o quanto o docente contribui
na qualidade do curso, por modalidade lecionada.

A nota por modalidade encontra-se no intervalo entre 0 e 5, sendo zero a pior qualidade e cinco a melhor qualidade. 
Docentes que não lecionam em uma modalidade terão nota zero.

A nota média por modalidade é ponderada pela [proporção de alunos](#proporção-de-alunos) daquela modalidade.

O [Cálculo do ICDC](#cálculo-do-icdc) é simplesmente o somatório das notas médias por modalidade ponderadas pela 
proporção de alunos por modalidade. O ICDC também encontra-se no intervalo entre 0 e 5.

### Nota média por modalidade

A nota média por modalidade (graduação, mestrado, doutorado) é dada por

$$
\text{Média}\_{m} = \frac{\sum\_{t}^{T \in m} (N\^{(t)} * P\_{m}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in m} (N^{(t)} * P\_{m}^{(t)} * \text{encargo}^{(t)})}
$$

Onde:

* $\text{Média}\_{m}$ é a nota média do docente na modalidade $m$ (graduação, mestrado ou doutorado);
* $T$ é o conjunto de todas as turmas do docente para a modalidade $m$, para o ano calculado, sendo $t$ uma turma em 
  particular;
* $P\_{m}^{(t)}$ é o [peso do discente](#relação-de-peso-de-alunos) para aquela modalidade, para o curso que solicitou a turma;
* $N\^{(t)}$ é o número de alunos aprovados com nota, reprovados com nota, ou matriculados na disciplina, no ano do 
  cálculo;
* $\text{encargo}^{(t)}$ é o encargo didático da turma;
* $\text{CC}^{(t)}$ é o conceito do curso da turma: CPC contínuo mais recente para cursos de graduação, e Conceito CAPES
  **convertido** mais recente para cursos de pós-graduação.

O conceito CAPES convertido segue tabela proporcionada pelo INEP:

| Conceito CAPES | Nota para fins de cálculo do ICDC |
|---------------:|----------------------------------:|
|              3 |                                 4 |
|              4 |                               4.5 |
|              5 |                                 5 |
|              6 |                                 5 |
|              7 |                                 5 |

> [!NOTE]
> **Por que apenas alunos do mesmo curso do curso que solicitou a turma são contabilizados?**
> 
> O cálculo é feito desta maneira pois o docente não pode controlar quais alunos de outros cursos estão matriculados nas
> suas turmas. Estes alunos matriculam-se à revelia do curso que solicitou a turma, e do departamento que disponibilizou
> o(s) docente(s).
> 
> Por exemplo: uma disciplina de Cálculo A, solicitada pelo curso de Engenharia Química, pode ter alunos de Engenharia 
> Civil, Ciência da Computação, Sistemas de Informação, etc. Seria injusto que estes alunos fossem contabilizados no
> cálculo do ICDC, pois o docente, no momento que concordou em lecionar a turma para Engenharia Química, não 
> necessariamente concordou em lecionar para alunos de outros cursos - que podem ter valores de CPC bem distintos do
> curso que solicitou a turma.
> 
> A maneira como o docente prepara sua aula para um curso também pode não ser adequada para alunos de outros cursos.


#### Relação de peso de alunos

Segundo a [lógica do IGC](data/nota_técnica_igc.pdf), deve-se estabelecer uma relação de peso entre alunos de graduação
e pós-graduação, nas modalidades de mestrado e doutorado, a depender do Conceito CAPES do programa de pós-graduação.

Alunos de graduação sempre possuem peso $P\_{\text{graduação}}^{(t)} = 1$, independente do CPC Contínuo do curso.

##### Equivalência de alunos de mestrado

| Conceito do mestrado CAPES | $P\_{\text{mestrado}}$ |
|:---------------------------|:-----------------------|
| 3                          | 1                      |
| 4                          | 2                      |
| 5                          | 3                      |
| 6                          | 3                      |
| 7                          | 3                      |

##### Equivalência de alunos de doutorado

| Conceito do doutorado CAPES | $P\_{\text{doutorado}}$ |
|:----------------------------|:------------------------|
| 3                           | 1                       |
| 4                           | 2                       |
| 5                           | 3                       |
| 6                           | 4                       |
| 7                           | 5                       |

### Proporção de alunos

A proporção de alunos $\alpha$, $\beta$ e $\gamma$ são simplesmente o somatório do número de alunos **vezes** o peso dos
alunos (conforme tabelas da [Seção Relação de peso de alunos](#relação-de-peso-de-alunos), cujo curso é o 
mesmo do curso de solicitação da vaga na turma, **para aquela modalidade,** dividido pelo número de alunos, cujo curso 
é o mesmo do curso de solicitação da vaga na turma, **para todas as modalidades:**

#### Graduação

$$
\alpha = \frac{
  \sum\_{t}^{T\_{\text{graduação}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
}
$$

#### Mestrado

$$
\beta = \frac{
  \sum\_{t}^{T\_{\text{mestrado}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
}
$$

#### Doutorado

$$
\gamma = \frac{
  \sum\_{t}^{T\_{\text{doutorado}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
}
$$

Onde:

* $N\^{(t)}$ é o número de alunos em uma turma $t$;
* $P\_{m}\^{(t)}$ é peso dos alunos da turma $t$ que pertencem à modalidade $m$, conforme 
  [Seção Relação de peso de alunos](#relação-de-peso-de-alunos);
* $T\_{\text{graduação}}$, $T\_{\text{mestrado}}$ e $T\_{\text{doutorado}}$ são respectivamente o número de alunos de 
  graduação, mestrado e doutorado, cujo curso é o mesmo curso de solicitação de vaga na turma, para os quais o professor
  deu aula no ano do cálculo;
* $\sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}$ são todos os alunos, de todas as turmas $T$ e todas as 
  modalidades $M$, cujo curso é o mesmo curso de solicitação de vaga na turma, para os quais o professor deu aula no ano
  do cálculo.

### Cálculo do ICDC

O ICDC é dado por

$$
ICDC = \alpha * \text{Média}\_{\text{graduação}} + 
       \beta * \text{Média}\_{\text{mestrado}} + 
       \gamma * \text{Média}\_{\text{doutorado}}
$$

## Casos especiais

### Cursos ABI (Área Básica de Ingresso)

Para cursos ABI (Área Básica de Ingresso), em que o aluno ingressa em um curso básico e depois faz a opção por um curso
específico (por exemplo, Ciências Biológicas), o núcleo comum não possui um CPC Contínuo pois nenhum aluno se forma neste
curso. Portanto, para calcular o CPC Contínuo do núcleo comum, tira-se simplesmente a média do CPC dos cursos 
que derivam do núcleo comum.

### Cursos técnicos, ensino médio, e educação básica

Como estes cursos não possuem nem CPC Contínuo, nem Conceito CAPES, eles não contribuem para o ICDC. Um professor que 
leciona exclusivamente em cursos técnicos, por exemplo, terá ICDC = 0. 

### Período do cálculo

O ICDC pode ser apenas calculado a partir do ano de 2019, pois as informações de encargos didáticos anteriores a 2019
não estão disponíveis.

## Exemplos

### Exemplo 1: um professor por disciplina

| Turma | Disciplina | Modalidade |    Encargo didático | Curso de solicitação da turma |       Conceito de Curso (CC) |                                       Alunos |
|:------|:-----------|:-----------|--------------------:|:------------------------------|-----------------------------:|---------------------------------------------:|
| 10    | Cálculo A  | Graduação  | 90h (João da Silva) | Engenharia Química            |                        3.366 | 20 (Eng. Química); 7 (Ciência da Computação) |
| 11    | Cálculo B  | Graduação  | 90h (João da Silva) | Engenharia Civil              |                        3.570 |            15 (Eng. Civil); 5 (Eng. Química) |
 

Como o docente João da Silva não leciona nenhuma disciplina no mestrado ou doutorado, 
$\text{Média}\_{\text{mestrado}} = 0$ e $\text{Média}\_{\text{doutorado}} = 0$. Da mesma maneira, as proporções $\beta$ 
e $\gamma$ do docente também serão zero.

Considerando que o peso de alunos de graduação $P\_{\text{graduação}}^{(t)}$ é sempre 1, independente da qualidade do 
curso, a nota média da graduação deste docente é 

$$
\begin{aligned}
\text{Média}\_{\text{graduação}} &= \frac{\sum\_{t}^{T \in \text{graduação}} (N\^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{graduação}} (N^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{(20 * 1 * 90 * 3.366) + (15 * 1 * 90 * 3.570)}{(20 * 1 * 90) + (15 * 1 * 90)} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{10878.3}{3150} \\
& \\
\text{Média}\_{\text{graduação}} &= 3.453428571 \approx 3.45
\end{aligned}
$$

O docente João da Silva possui 47 alunos no total, mas apenas 35 são do curso que solicitou as turmas nas 
quais eles estudaram. Então $\sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)} = (20 * 1 + 15 * 1) = 35$.

Como o docente leciona apenas na graduação, $\alpha = \frac{35}{35} = 1$. 

O ICDC do docente João da Silva é

$$
\begin{aligned}
ICDC &= \alpha * \text{Média}\_{\text{graduação}} + \beta * \text{Média}\_{\text{mestrado}} + \gamma * \text{Média}\_{\text{doutorado}} \\
& \\
ICDC &= (1 * 3.45) + (0 * 0) + (0 * 0) \\
& \\
ICDC &= 3.45
\end{aligned}
$$

### Exemplo 2: dois professores em uma disciplina

Algumas disciplinas são lecionadas por mais de um docente. Para estes casos, considera-se apenas o encargo didático 
respectivo a cada docente, para cada disciplina.

| Turma | Disciplina | Modalidade |                       Encargo didático | Curso de solicitação da turma |       Conceito de Curso (CC) |                                       Alunos |
|:------|:-----------|:-----------|---------------------------------------:|:------------------------------|-----------------------------:|---------------------------------------------:|
| 10    | Cálculo A  | Graduação  | 30h (João da Silva); 60h (Pedro Paulo) | Engenharia Química            |                        3.366 | 20 (Eng. Química); 7 (Ciência da Computação) |
| 11    | Cálculo B  | Graduação  |                    90h (João da Silva) | Engenharia Civil              |                        3.570 |            15 (Eng. Civil); 5 (Eng. Química) |

A nota média da graduação do docente **João da Silva** é

$$
\begin{aligned}
\text{Média}\_{\text{graduação}} &= \frac{\sum\_{t}^{T \in \text{graduação}} (N\^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{graduação}} (N^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{(20 * 1 * 30 * 3.366) + (15 * 1 * 90 * 3.570)}{(20 * 1 * 30) + (15 * 1 * 90)} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{6839.1}{1950} \\
& \\
\text{Média}\_{\text{graduação}} &= 3.507230769 \approx 3.51
\end{aligned}
$$

A nota média da graduação do docente **Pedro Paulo** é

$$
\begin{aligned}
\text{Média}\_{\text{graduação}} &= \frac{\sum\_{t}^{T \in \text{graduação}} (N\^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{graduação}} (N^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{(20 * 1 * 60 * 3.366)}{(20 * 1 * 60)} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{4039.2}{1200} \\
& \\
\text{Média}\_{\text{graduação}} &= 3.366
\end{aligned}
$$

### Exemplo 3: cursos de pós-graduação

Cursos de pós-graduação frequentemente possuem turmas mistas, onde uma mesma disciplina é lecionada para alunos de 
mestrado e doutorado do mesmo Programa de Pós-Graduação. Nesse caso, considera-se o **programa** de solicitação da 
turma, ao invés do **curso**.

Alunos de graduação que cursam disciplinas de pós-graduação, bem como alunos especiais (e.g. servidores), **não são** 
contabilizados no cálculo do ICDC.

| Turma | Disciplina                | Modalidade    |    Encargo didático | Curso de solicitação da turma           |     Conceito de Curso (CC) |                                                                Alunos |
|:------|:--------------------------|:--------------|--------------------:|:----------------------------------------|---------------------------:|----------------------------------------------------------------------:|
| 10    | Cálculo A                 | Graduação     | 90h (João da Silva) | Engenharia Química (Curso de Graduação) |                      3.366 |                          20 (Eng. Química); 7 (Ciência da Computação) |
| 11    | Método Científico e Ética | Pós-Graduação | 60h (João da Silva) | Química (Programa de Pós-Graduação)     | 7 (Conceito CAPES); 5 (CC) | 5 (Química - Mestrado); 3 (Química - Doutorado); 2 (alunos especiais) |


#### Nota média da graduação

$$
\begin{aligned}
\text{Média}\_{\text{graduação}} &= \frac{\sum\_{t}^{T \in \text{graduação}} (N\^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{graduação}} (N^{(t)} * P\_{\text{graduação}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{(20 * 1 * 90 * 3.366)}{(20 * 1 * 90)} \\
& \\
\text{Média}\_{\text{graduação}} &= \frac{6058.8}{1800} \\
& \\
\text{Média}\_{\text{graduação}} &= 3.366
\end{aligned}
$$

#### Nota média do mestrado

Segue-se a tabela de equivalência da [Seção Equivalência de Alunos de Mestrado](#equivalência-de-alunos-de-mestrado).
Como o Programa de Pós-Graduação em Química possui conceito CAPES 7, cada aluno de mestrado deste programa equivale a 
3 alunos de graduação: 

$$
\begin{aligned}
\text{Média}\_{\text{mestrado}} &= \frac{\sum\_{t}^{T \in \text{mestrado}} (N\^{(t)} * P\_{\text{mestrado}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{mestrado}} (N^{(t)} * P\_{\text{mestrado}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{mestrado}} &= \frac{(5 * 3 * 60 * 5)}{(5 * 3 * 60)} \\
& \\
\text{Média}\_{\text{mestrado}} &= \frac{4500}{900} \\
& \\
\text{Média}\_{\text{mestrado}} &= 5
\end{aligned}
$$

#### Nota média do doutorado

Segue-se a tabela de equivalência da [Seção Equivalência de Alunos de Doutorado](#equivalência-de-alunos-de-doutorado).
Como o Programa de Pós-Graduação em Química possui conceito CAPES 7, cada aluno de doutorado deste programa equivale a 
5 alunos de graduação: 

$$
\begin{aligned}
\text{Média}\_{\text{doutorado}} &= \frac{\sum\_{t}^{T \in \text{doutorado}} (N\^{(t)} * P\_{\text{doutorado}}^{(t)} * \text{encargo}^{(t)} * \text{CC}^{(t)})}{\sum\_{t}^{T \in \text{doutorado}} (N^{(t)} * P\_{\text{doutorado}}^{(t)} * \text{encargo}^{(t)})} \\
& \\
\text{Média}\_{\text{doutorado}} &= \frac{(3 * 5 * 60 * 5)}{(3 * 5 * 60)} \\
& \\
\text{Média}\_{\text{doutorado}} &= \frac{4500}{900} \\
& \\
\text{Média}\_{\text{doutorado}} &= 5
\end{aligned}
$$

#### Proporções de alunos

O docente leciona para 37 alunos no total, mas apenas 28 são de cursos ou programas que solicitaram as turmas. Portanto,
seu número de alunos é $\sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)} = (20 * 1) + (5 * 3) + (3 * 5) = 50$.

$$
\begin{aligned}
\alpha &= \frac{
  \sum\_{t}^{T\_{\text{graduação}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
} = \frac{20}{50} = 0.4 \\
& \\
\beta &= \frac{
  \sum\_{t}^{T\_{\text{mestrado}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
} = \frac{15}{50} = 0.3 \\
& \\
\gamma &= \frac{
  \sum\_{t}^{T\_{\text{doutorado}}} N\^{(t)}
}{
  \sum\_{t}^{T} \sum_{m}^{M} N\^{(t)} * P\_{m}\^{(t)}
} = \frac{15}{50} = 0.3
\end{aligned}
$$

#### ICDC

Para este exemplo, o ICDC do docente João da Silva é

$$
\begin{aligned}
ICDC &= \alpha * \text{Média}\_{\text{graduação}} + \beta * \text{Média}\_{\text{mestrado}} + \gamma * \text{Média}\_{\text{doutorado}} \\
& \\
ICDC &= (0.4 * 3.366) + (0.3 * 5) + (0.3 * 5) \\
& \\
ICDC &= 4.3464
\end{aligned}
$$
