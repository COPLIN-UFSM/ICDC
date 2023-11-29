import argparse
import locale

import pandas as pd
from datetime import datetime as dt
from db2 import DB2Connection


def strip_all(df):
    """
    Função que remove espaços em branco de um DataFrame.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            df.loc[:, column] = df[column].apply(lambda x: x.strip() if not pd.isna(x) and isinstance(x, str) else x)
    return df


def get_cpc_by_course():
    df = pd.read_csv('data/cpc_2021.csv')
    rename = dict([(x, x.strip()) for x in df.columns])
    df.rename(columns=rename, inplace=True)

    ufsm = df.loc[df['Sigla da IES*'] == 'UFSM']
    return ufsm


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


def ncpc_graduacao(df):
    n_cursos = len(df)

    n_alunos = df['Nº de Concluintes Inscritos'].sum()

    _store = []

    g_ies = 0.
    for i, row in df.iterrows():
        ncpc_curso = locale.atof(row['CPC (Contínuo)'])
        razao = row['Nº de Concluintes Inscritos'] / n_alunos

        _store += [[row['Área de Avaliação'], ncpc_curso + razao, row['Nota Bruta - FG']]]

        g_ies += ncpc_curso + razao

    adf = pd.DataFrame(_store, columns=['CURSO', 'CALCULADO', 'REAL'])
    print(adf)
    exit(0)

    return g_ies


def main(database_credentials):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    cpc = get_cpc_by_course()
    g_ies = ncpc_graduacao(cpc)
    print('G_IES:', g_ies)
    print(cpc[['Área de Avaliação', 'CPC (Contínuo)']])
    # courses = get_graduate_data(database_credentials)
    # print(courses)


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
