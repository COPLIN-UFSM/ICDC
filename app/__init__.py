import csv
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
        columns={x: x + '_DISCENTE' if x != 'ID_CURSO' else 'ID_CURSO' for x in cursos_discente.columns}
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
    third['CPC_CONTINUO'] = third['CPC_CONTINUO'].astype(float)

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
