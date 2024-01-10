"""
Lógica usando dados abertos de censo.
"""

import argparse
import locale
import os

import pandas as pd

from scripts.inep_routines import get_census_data, get_cpc_data


def trunc(value: float, places: int = 3) -> float:
    """
    Trunca um valor numérico em places casas decimais.
    :param value: O valor, em ponto flutuante.
    :param places: O número de casas decimais para truncar o valor.
    :return: Um valor float truncado em places casas decimais.
    """
    power = 10**places
    return int(value * power) / power


def calcula_indice_e_matriculas_pos(df, conv_conceito_pos, conv_matricula):
    df = df.copy(deep=True)

    df.loc[:, 'CD_CONCEITO_CURSO'] = df['CD_CONCEITO_CURSO'].astype(int)

    gb_values = df.groupby(by='CD_PROGRAMA_IES')['CD_CONCEITO_CURSO'].agg(['mean', 'count'])

    total_matriculados_ano = gb_values['count'].sum()

    matriculas_ponderadas = 0

    t = 0.
    for i, row in gb_values.iterrows():
        conceito_capes = int(row['mean'])
        multiplicador_matricula = conv_matricula[conceito_capes]
        conceito_curso_transf = conv_conceito_pos[int(row['mean'])]
        matriculados_curso = row['count']
        matriculas_ponderadas += matriculados_curso * multiplicador_matricula
        razao = matriculados_curso / total_matriculados_ano

        calc = conceito_curso_transf * razao

        t += calc

    return t, matriculas_ponderadas


def nota_doutorado(df, ano_calculo, conv_conceito_pos):
    conv_matricula = {
        3: 1,
        4: 2,
        5: 3,
        6: 4,
        7: 5,
    }

    loced = df.loc[
        (df['AN_BASE'] == ano_calculo) &
        (df['SG_ENTIDADE_ENSINO'] == 'UFSM') &
        (df['NM_GRAU_PROGRAMA'].apply(lambda x: ('DOUTORADO' in x) and 'PROFISSIONAL' not in x)) &
        (df['CD_CONCEITO_CURSO'] != 'A') &
        (df['NM_SITUACAO_DISCENTE'].apply(lambda x: (x == 'MATRICULADO') or (x == 'TITULADO'))) &
        df['DS_GRAU_ACADEMICO_DISCENTE'].apply(lambda x: 'DOUTORADO' in x)
    ]
    return calcula_indice_e_matriculas_pos(loced, conv_conceito_pos, conv_matricula)


def nota_mestrado(df, ano_calculo, conv_conceito_pos):
    conv_matricula = {
        3: 1,
        4: 2,
        5: 3,
        6: 3,
        7: 3,
    }

    loced = df.loc[
        (df['AN_BASE'] == ano_calculo) &
        (df['SG_ENTIDADE_ENSINO'] == 'UFSM') &
        (df['NM_GRAU_PROGRAMA'].apply(lambda x: 'MESTRADO' in x)) &
        (df['CD_CONCEITO_CURSO'] != 'A') &
        (df['NM_SITUACAO_DISCENTE'].apply(lambda x: (x == 'MATRICULADO') or (x == 'TITULADO'))) &
        df['DS_GRAU_ACADEMICO_DISCENTE'].apply(lambda x: 'MESTRADO' in x)
    ]
    return calcula_indice_e_matriculas_pos(loced, conv_conceito_pos, conv_matricula)


def nota_graduacao(ano_calculo: int, path: str, anos_calculo: tuple = None) -> tuple:
    """
    Calcula a nota da graduação do IGC.

    :param ano_calculo: Ano do cálculo do IGC.
    :param path: Caminho de onde ler os arquivos
    :param anos_calculo: Opcional - caso os anos do triênio sejam um caso especial.
    :return: A nota da graduação como float e o número de matriculados como um int.
    """
    census = get_census_data(ano_calculo, path, anos_calculo)
    cpc = get_cpc_data(ano_calculo, path, anos_calculo)

    censo_matriculas_somadas = census.groupby(by=['CO_CURSO', 'NU_ANO_CENSO'])['QT_MAT'].agg(['sum']).reset_index()
    censo_matriculas_somadas = censo_matriculas_somadas.rename(columns={'sum': 'QT_MAT'})

    census_and_cpc = pd.merge(
        cpc, censo_matriculas_somadas, left_on=('Código do Curso', 'Ano'), right_on=('CO_CURSO', 'NU_ANO_CENSO'),
        how='inner', validate='one_to_one'
    )
    gb = census_and_cpc.groupby(by='CO_CURSO')
    gb_vals = gb.agg(['mean', 'sum'])

    _index = []
    _store = []

    total_matriculados_trienio = gb_vals[('QT_MAT', 'sum')].sum()

    tg = 0.
    for i, row in gb_vals.iterrows():
        ncpc_curso = row.loc[('CPC (Contínuo)', 'mean')]
        matriculados_curso = row.loc[('QT_MAT', 'sum')]
        razao = matriculados_curso / total_matriculados_trienio

        calc = ncpc_curso * razao

        _index += [row.name]
        _store += [[
            cpc.loc[cpc['Código do Curso'] == row.name, 'Área de Avaliação'].values.tolist()[0],
            census.loc[census['CO_CURSO'] == row.name, 'NO_CURSO'].values.tolist()[0],
            ncpc_curso,
            matriculados_curso,
            total_matriculados_trienio,
            razao,
            calc,
        ]]

        tg += calc

    return tg, total_matriculados_trienio


def letras_gregas(mat_grd, mat_mst, mat_doc):
    soma = sum((mat_grd, mat_mst, mat_doc))
    return mat_grd/soma, mat_mst/soma, mat_doc/soma


def main():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    conv_conceito_pos = {
        3: 4,
        4: 4.5,
        5: 5,
        6: 5,
        7: 5
    }

    df_pos = pd.read_csv(
        os.path.join('data', 'br-capes-colsucup-discentes-2021-2022-11-30.csv'),
        sep=',', encoding='utf-8', quotechar='"'
    )

    tg, mat_grd = nota_graduacao(2021, 'data', anos_calculo=(2021, 2019, 2018))
    tm, mat_mst = nota_mestrado(df_pos, 2021, conv_conceito_pos)
    td, mat_doc = nota_doutorado(df_pos, 2021, conv_conceito_pos)
    alpha, beta, gamma = letras_gregas(mat_grd, mat_mst, mat_doc)
    print(f'O conceito médio da graduação da instituição é {trunc(tg, 3)}. O valor correto é 3.440')
    print(f'O conceito médio do mestrado da instituição é {trunc(tm, 3)}. O valor correto é 4.532')
    print(f'O conceito médio do doutorado da instituição é {trunc(td, 3)}. O valor correto é 4.738')
    print(f'Alfa, Beta e Gama são {trunc(alpha, 3)}, {trunc(beta, 3)}, {trunc(gamma, 3)}. '
          f'Os valores corretos são 0.591, 0.204, 0.203')
    print(f'O IGC da instituição é {trunc(tg * alpha + tm * beta + td * gamma, 3)}. O valor correto é 3.928')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calcula o IGC a partir de dados abertos.'
    )

    args = parser.parse_args()
    main()
