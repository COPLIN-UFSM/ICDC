# Fonte dos dados

## Insumos

Para calcular o IGC, são necessários os seguintes dados:

* Do triênio para o qual o IGC está sendo calculado...
  * [Censo da Educação Superior](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior), a nível de IES e Cursos
  * [Valor do CPC](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior) para cada curso 
* Do ano para o qual o IGC está sendo calculado...
  * [Dados abertos da CAPES](https://dadosabertos.capes.gov.br/dataset?organization=diretoria-de-avaliacao), com a 
    lista de discentes de cada **curso** (não programa) de pós-graduação

## Cálculo

A [Nota técnica](../nota_técnica_igc.pdf) descreve como calcular o IGC. 

1. Deve-se pegar o CPC mais atualizado (dentro do triênio de dados disponíveis) para cada curso;
2. Se um curso não tiver CPC, não deve-se utilizá-lo;
3. Cursos de pós-graduação em avaliação não devem ser computados.