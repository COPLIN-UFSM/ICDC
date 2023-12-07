import argparse
import locale
import os
import sys
from functools import reduce

import pandas as pd
from datetime import datetime as dt
from db2 import DB2Connection
import numpy as np
import re
import math


def strip_all(df):
    """
    Função que remove espaços em branco de um DataFrame.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            df.loc[:, column] = df[column].apply(lambda x: x.strip() if not pd.isna(x) and isinstance(x, str) else x)
    return df


def get_something(database_credentials, query_str, index_col=None):
    """
    Coleta algo do banco de dados, dada uma string de consulta SQL.
    """
    with DB2Connection(database_credentials) as db2_conn:
        courses = pd.DataFrame(db2_conn.query(query_str, as_dict=True))
        if index_col is not None:
            courses = courses.set_index(index_col)
        return courses


def get_undergraduate_data(database_credentials, ano_indice=None):
    if ano_indice is None:
        ano_indice = dt.now().year

    query_str = f'''
    select ac.id_curso, NOME_CURSO, temp.QUANTIDADE_ALUNOS
    from ACAD_CURSOS ac
    inner join (
        select ac.ID_CURSO, count(*) QUANTIDADE_ALUNOS
        from ACAD_CURSOS ac
        inner join CURSOS_ALUNOS_ATZ caa on ac.ID_CURSO = caa.ID_CURSO
        WHERE ID_PROGRAMA_SUCUPIRA IS NULL
        -- AND DT_SAIDA IS NULL
        AND (ANO_INGRESSO >= {ano_indice - 3}) AND (ANO_INGRESSO <= {ano_indice}) 
        group by ac.ID_CURSO
    ) AS TEMP on ac.ID_CURSO = TEMP.ID_CURSO;
    '''
    df = get_something(database_credentials, query_str)


def get_graduate_data(database_credentials, ano_indice=None):
    if ano_indice is None:
        ano_indice = dt.now().year

    query_str = f'''
        select ac.id_curso, NOME_CURSO, NOME_PROGRAMA_SUCUPIRA,
            spi.CONCEITO_MESTRADO_ACADEMICO, spi.CONCEITO_MESTRADO_PROFISSIONAL,
            spi.CONCEITO_DOUTORADO_ACADEMICO, 
            --spi.CONCEITO_DOUTORADO_PROFISSIONAL, -- não usa nota de doutorado profissional
            TEMP.QUANTIDADE_ALUNOS
        from ACAD_CURSOS ac
        inner join SUCUPIRA_PROGRAMAS SP on ac.ID_PROGRAMA_SUCUPIRA = sp.ID_PROGRAMA_SUCUPIRA
        inner join SUCUPIRA_PROGRAMAS_INDICES spi on sp.ID_PROGRAMA_SUCUPIRA = spi.ID_PROGRAMA_SUCUPIRA
        inner join (
            select ac.ID_CURSO, count(*) QUANTIDADE_ALUNOS
            from ACAD_CURSOS ac
            inner join CURSOS_ALUNOS_ATZ caa on ac.ID_CURSO = caa.ID_CURSO
            WHERE ID_PROGRAMA_SUCUPIRA IS NOT NULL
            AND (ANO_INGRESSO >= {ano_indice - 3}) AND (ANO_INGRESSO <= {ano_indice})
            group by ac.ID_CURSO
        ) AS TEMP on ac.ID_CURSO = TEMP.ID_CURSO;
    '''

    df = get_something(database_credentials, query_str)
    return df


def get_ufsm_census(ano_calculo, path, anos_calculo=None, nome_instituicao='UNIVERSIDADE FEDERAL DE SANTA MARIA'):
    censo_cursos = [x for x in os.listdir(path) if f'censo_cursos' in x]
    if anos_calculo is None:
        anos_calculo = (anos_calculo, ano_calculo - 1, ano_calculo - 2)
    censo_cursos = [x for x in censo_cursos if any([str(y) in x for y in anos_calculo])]

    censo_ies = [x for x in os.listdir(path) if f'censo_ies_{ano_calculo}' in x]

    # tanto faz o dataframe, é só para pegar o código da ufsm
    ies = pd.read_csv(os.path.join(path, censo_ies[0]), encoding='ISO-8859-1', sep=';')
    loced = ies.loc[ies['NO_IES'].apply(lambda x: x.upper()) == nome_instituicao]
    COD_IES = loced['CO_IES'].iloc[0]

    s_cursos = [pd.read_csv(os.path.join(path, x), encoding='ISO-8859-1', sep=';') for x in censo_cursos]
    s_cursos = [df.loc[df['CO_IES'] == COD_IES] for df in s_cursos]

    all_cursos = reduce(lambda x, y: pd.concat((x, y), ignore_index=True), s_cursos)
    return all_cursos


def get_ufsm_cpc(ano_calculo, path, anos_calculo=None, sigla_instituicao='UFSM'):
    files = [x for x in os.listdir(path) if 'cpc_' in x]
    if anos_calculo is None:
        anos_calculo = (anos_calculo, ano_calculo - 1, ano_calculo - 2)
    files = [x for x in files if any([str(y) in x for y in anos_calculo])]

    cpcs = [pd.read_csv(os.path.join(path, x), sep=',', encoding='utf-8') for x in files]
    s_cpcs = []
    for cpc in cpcs:
        rename = dict([(x, x.strip()) for x in cpc.columns])
        cpc.rename(columns=rename, inplace=True)
        cpc = cpc.loc[cpc['Sigla da IES'] == sigla_instituicao]
        s_cpcs += [cpc]

    all_cpcs = reduce(lambda x, y: pd.concat((x, y), ignore_index=True), s_cpcs)
    all_cpcs['Ano'] = all_cpcs['Ano'].astype(int)

    count_cods = all_cpcs['Código do Curso'].value_counts()
    more_than_one = count_cods[count_cods > 1].index.tolist()

    # descarta cursos duplicados, pegando o mais recente
    for course in more_than_one:
        loced = all_cpcs.loc[all_cpcs['Código do Curso'] == course]
        to_drop = loced.loc[loced['Ano'] != loced['Ano'].max()]
        all_cpcs = all_cpcs.drop(to_drop.index, axis='index')

    all_cpcs.loc[:, 'CPC (Contínuo)'] = all_cpcs['CPC (Contínuo)'].apply(locale.atof)

    return all_cpcs


def nota_graduacao(ano_calculo: int, path: str, anos_calculo: tuple = None) -> tuple:
    """
    Calcula a nota da graduação do IGC.

    :param ano_calculo: Ano do cálculo do IGC.
    :param path: Caminho de onde ler os arquivos
    :param anos_calculo: Opcional - caso os anos do triênio sejam um caso especial.
    :return: A nota da graduação como float e o número de matriculados como um int.
    """
    census = get_ufsm_census(ano_calculo, path, anos_calculo)
    cpc = get_ufsm_cpc(ano_calculo, path, anos_calculo)

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

    # df = pd.DataFrame(
    #     _store, index=_index, columns=[
    #         'Nome curso (CPC)', 'Nome curso (Censo)', 'CPC Contínuo (CPC)', 'Ingressantes curso triênio (Censo)',
    #         'Total matriculados Triênio (Censo)', 'Razão ingressantes curso/total (Censo)', 'G_ies curso (Calculado)'
    #     ]
    # )
    # df.to_csv('ncpc_calculado_test.csv', index_label='CO_CURSO', decimal=',', float_format=lambda x: round(x, 4))
    # print(f'O conceito médio de graduação da instituição é {tg}')

    return tg, total_matriculados_trienio


def trunc(value, places=3):
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


def nota_doutorado(df, ano_calculo, conv_conceito_pos, conv_matricula):
    loced = df.loc[
        (df['AN_BASE'] == ano_calculo) &
        (df['SG_ENTIDADE_ENSINO'] == 'UFSM') &
        (df['NM_GRAU_PROGRAMA'].apply(lambda x: ('DOUTORADO' in x) and 'PROFISSIONAL' not in x)) &
        (df['CD_CONCEITO_CURSO'] != 'A') &
        (df['NM_SITUACAO_DISCENTE'].apply(lambda x: (x == 'MATRICULADO') or (x == 'TITULADO'))) &
        df['DS_GRAU_ACADEMICO_DISCENTE'].apply(lambda x: 'DOUTORADO' in x)
    ]
    return calcula_indice_e_matriculas_pos(loced, conv_conceito_pos, conv_matricula)


def nota_mestrado(df, ano_calculo, conv_conceito_pos, conv_matricula):
    loced = df.loc[
        (df['AN_BASE'] == ano_calculo) &
        (df['SG_ENTIDADE_ENSINO'] == 'UFSM') &
        (df['NM_GRAU_PROGRAMA'].apply(lambda x: 'MESTRADO' in x)) &
        (df['CD_CONCEITO_CURSO'] != 'A') &
        (df['NM_SITUACAO_DISCENTE'].apply(lambda x: (x == 'MATRICULADO') or (x == 'TITULADO'))) &
        df['DS_GRAU_ACADEMICO_DISCENTE'].apply(lambda x: 'MESTRADO' in x)
    ]
    return calcula_indice_e_matriculas_pos(loced, conv_conceito_pos, conv_matricula)


def letras_gregas(mat_grd, mat_mst, mat_doc):
    soma = sum((mat_grd, mat_mst, mat_doc))
    return mat_grd/soma, mat_mst/soma, mat_doc/soma


def main(database_credentials):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # grad_courses = get_graduate_data(database_credentials, 2021)
    # undergrad_courses = get_undergraduate_data(database_credentials, 2021)

    conv_conceito_pos = {
        3: 4,
        4: 4.5,
        5: 5,
        6: 5,
        7: 5
    }

    conv_matricula_mestrado = {
        3: 1,
        4: 2,
        5: 3,
        6: 3,
        7: 3,
    }

    conv_matricula_doutorado = {
        3: 1,
        4: 2,
        5: 3,
        6: 4,
        7: 5,
    }

    df_pos = pd.read_csv(
        os.path.join('data', 'br-capes-colsucup-discentes-2021-2022-11-30.csv'),
        sep=',', encoding='utf-8', quotechar='"'
    )

    tg, mat_grd = nota_graduacao(2021, 'data', anos_calculo=(2021, 2019, 2018))
    tm, mat_mst = nota_mestrado(df_pos, 2021, conv_conceito_pos, conv_matricula_mestrado)
    td, mat_doc = nota_doutorado(df_pos, 2021, conv_conceito_pos, conv_matricula_doutorado)
    alpha, beta, gamma = letras_gregas(mat_grd, mat_mst, mat_doc)
    print(f'O conceito médio da graduação da instituição é {trunc(tg, 3)}. O valor correto é 3.440')
    print(f'O conceito médio do mestrado da instituição é {trunc(tm, 3)}. O valor correto é 4.532')
    print(f'O conceito médio do doutorado da instituição é {trunc(td, 3)}. O valor correto é 4.738')
    print(f'Alfa, Beta e Gama são {trunc(alpha, 3)}, {trunc(beta, 3)}, {trunc(gamma, 3)}. Os valores corretos são 0.591, 0.204, 0.203')
    print(f'O IGC da instituição é {trunc(tg * alpha + tm * beta + td * gamma, 3)}. O valor correto é 3.928')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Coleta dados do banco de dados para treinamento do algoritmo. Realiza pré-processamento.'
    )

    parser.add_argument(
        '--database-credentials', action='store', required=True,
        help='Caminho para um arquivo json com as credenciais do banco de dados .'
    )

    args = parser.parse_args()
    main(args.database_credentials)
