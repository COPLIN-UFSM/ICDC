# IGC Docente

## Nota média por modalidade

$$
\text{Media}\_{m} = \frac{\sum\_{t}^{T \in m} (N\_{c}^{(t)} * P\_{m,c} * \text{encargo}^{(t)} * \text{CPC}\_c^{(t)})}{\sum\_{t}^{T \in m} (N_{c}^{(t)} * P\_{m,c} * \text{encargo}^{(t)})}
$$

Onde:

* $\text{Media}\_{m}$ é a nota média do docente na modalidade $m$ (graduação, mestrado ou doutorado);
* $T$ são todas as turmas do docente para a modalidade $m$, para o ano calculado, sendo $t$ uma turma em particular;
* $P\_{m,c}$ é o peso do discente para aquela modalidade, para aquele curso (veja Tabela 1);
* $N\_{c}^{(t)}$ são o número de alunos aprovados com nota, reprovados com nota, ou matriculados na disciplina, no ano de cálculo;
* $\text{encargo}^{(t)}$ é o encargo didático da turma;
* $\text{CPC}\_c^{(t)}$ é o CPC contínuo mais recente para o curso de solicitação da vaga na turma.

## Relação de peso de alunos 

Alunos de graduação possuem peso $P\_{\text{graduação},c} = 1$, enquanto alunos de pós-graduação são multiplicados por um peso, de acordo com uma tabela de conversão do INEP:

### Mestrado

| Conceito do mestrado Capes | $P\_{\text{mestrado},c}$ |
|:---------------------------|:-------------------------|
| 3                          | 1                        |
| 4                          | 2                        |
| 5                          | 3                        |
| 6                          | 3                        |
| 7                          | 3                        |

### Doutorado

| Conceito do doutorado Capes | $P\_{\text{doutorado},c}$ |
|:----------------------------|:--------------------------|
| 3                          | 1                          |
| 4                          | 2                          |
| 5                          | 3                          |
| 6                          | 4                          |
| 7                          | 5                          |

## Proporção de alunos

A proporção de alunos $\alpha$, $\beta$ e $\gamma$ são simplesmente o somatório do número de alunos, cujo curso é o mesmo do curso de solicitação da vaga na turma, **para aquela modalidade,**
dividido pelo número de alunos, cujo curso é o mesmo do curso de solicitação da vaga na turma, **para todas as modalidades:**

$$
\alpha = \frac{\sum\_{t}^{T\_{\text{graduação}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

$$
\beta = \frac{\sum\_{t}^{T\_{\text{mestrado}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

$$
\gamma = \frac{\sum\_{t}^{T\_{\text{doutorado}}} N\_{c}^{(t)}}{\sum\_{t}^{T} N\_{c}^{(t)}}
$$

Onde:

* $T\_{\text{graduação}}$, $T\_{\text{mestrado}}$ e $T\_{\text{doutorado}}$ são respectivamente o número de alunos de graduação, mestrado e doutorado, cujo curso é o mesmo curso de
  solicitação de vaga na turma, para os quais o professor deu aula no ano analisado;
* $\sum\_{t}^{T} N\_{c}^{(t)}$ são todos os alunos cujo curso é o mesmo curso de solicitação de vaga na turma, para os quais o professor deu aula no ano analisado.

## Cálculo do IGC

O cálculo do IGC do docente é simplesmente

$$
IGC\_{\text{docente}} = \alpha * \text{Media}\_{\text{graduação}} + \beta * \text{Media}\_{\text{mestrado}} + \gamma * \text{Media}\_{\text{doutorado}}
$$
