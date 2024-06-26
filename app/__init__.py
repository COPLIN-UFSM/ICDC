import csv
import locale
import os

import pandas as pd
from db2 import DB2Connection
from tqdm import tqdm


def load_dataframe(database_credentials, views_path):
    df_views = get_views(database_credentials, views_path)

    # turmas.loc[pd.isna(turmas['NOTA_DOCENTE_PELO_DISCENTE']), 'NOTA_DOCENTE_PELO_DISCENTE'] = 0.6

    # liga docentes com turmas
    first = pd.merge(df_views['PAINEL_IGC_DOCENTES'], df_views['PAINEL_IGC_TURMAS'])
    # liga o curso do discente com cursos
    cursos_discente = df_views['PAINEL_IGC_CURSOS'].copy(deep=True)
    cursos_discente = cursos_discente.rename(
        columns={x: x + '_CURSO_DISCENTE' if x != 'ID_CURSO' else 'ID_CURSO' for x in cursos_discente.columns}
    )
    cursos_solicitacao_turma = df_views['PAINEL_IGC_CURSOS'].copy(deep=True)
    cursos_solicitacao_turma = cursos_solicitacao_turma.rename(
        columns={
            x: x + '_CURSO_SOLICITACAO_TURMA' if x != 'ID_CURSO'
            else 'ID_CURSO'
            for x in cursos_solicitacao_turma.columns
        }
    )

    second = pd.merge(
        first, cursos_discente,
        left_on='ID_CURSO_DISCENTE', right_on='ID_CURSO', suffixes=('', '_CURSO_DISCENTE')
    )
    # liga o curso de solicitação da turma com cursos
    third = pd.merge(
        second, cursos_solicitacao_turma,
        left_on='ID_CURSO_SOLICITACAO_TURMA', right_on='ID_CURSO', suffixes=('', '_CURSO_SOLICITACAO_TURMA')
    )

    # remove coluna ID_CURSO, que foi usada apenas para o merge
    third = third.drop(columns=['ID_CURSO'])

    return third


def get_views(database_credentials, views_path):
    views = ['PAINEL_IGC_DOCENTES', 'PAINEL_IGC_CURSOS', 'PAINEL_IGC_TURMAS']

    df_views = dict()

    for view in tqdm(views, desc='Baixando views'):
        if not os.path.exists(os.path.join(views_path, view + '.csv')):
            with DB2Connection(database_credentials) as db2_conn:
                table = pd.DataFrame(db2_conn.query(f'''SELECT * FROM {view}''', as_dict=True))
                table = strip_all(table)

                table.to_csv(
                    os.path.join(views_path, view + '.csv'),
                    index=False, encoding='utf-8', sep=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC
                )

                df_views[view] = table
        else:
            df_views[view] = pd.read_csv(os.path.join(views_path, view + '.csv'))

    return df_views


def strip_all(df):
    """
    Função que remove espaços em branco de um DataFrame.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            df.loc[:, column] = df[column].apply(lambda x: x.strip() if not pd.isna(x) and isinstance(x, str) else x)
    return df


def calcular_igc(professor):
    # pega apenas os cursos de graduação
    gb_niveis = professor.groupby(by='NOME_NIVEL_CURSO_SOLICITACAO_TURMA').groups

    total_alunos = 0
    n_alunos_niveis = []
    media_niveis = []

    for nivel, indices in gb_niveis.items():
        alunos = professor.loc[indices]
        n_alunos_nivel = 0

        alunos = alunos.loc[
            alunos['CODIGO_CURSO_UNIFICADO_CURSO_DISCENTE'] == alunos['CODIGO_CURSO_UNIFICADO_CURSO_SOLICITACAO_TURMA']
        ]

        gb_turmas = alunos.groupby(by='ID_TURMA').groups

        denominador = 0
        numerador = 0
        for id_turma, turma_indices in gb_turmas.items():
            turma = alunos.loc[turma_indices]

            den_dt = turma.apply(lambda x: x['PESO_ALUNO'] * x['ENCARGO_DIDATICO_TURMA_DOCENTE'], axis='columns')
            num_dt = den_dt * turma['CPC_CONTINUO']

            numerador += num_dt.sum()
            denominador += den_dt.sum()
            n_alunos_nivel += turma['PESO_ALUNO'].sum()

        media_nivel = numerador/denominador

        media_niveis += [media_nivel]
        n_alunos_niveis += [n_alunos_nivel]
        total_alunos += n_alunos_nivel

    igc = 0
    for i in range(len(media_niveis)):
        igc += (n_alunos_niveis[i]/total_alunos) * media_niveis[i]

    return igc
