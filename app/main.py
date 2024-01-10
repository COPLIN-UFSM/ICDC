import argparse
import csv
import os
from tqdm import tqdm

import pandas as pd
from db2 import DB2Connection


def strip_all(df):
    """
    Função que remove espaços em branco de um DataFrame.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            df.loc[:, column] = df[column].apply(lambda x: x.strip() if not pd.isna(x) and isinstance(x, str) else x)
    return df


def download_views(database_credentials, views_path):
    with DB2Connection(database_credentials) as db2_conn:
        views = ['PAINEL_IGC_DOCENTES', 'PAINEL_IGC_CURSOS', 'PAINEL_IGC_TURMAS']

        for view in tqdm(views, desc='Baixando views'):
            table = pd.DataFrame(db2_conn.query(f'''SELECT * FROM {view}''', as_dict=True))
            table = strip_all(table)

            table.to_csv(
                os.path.join(views_path, view + '.csv'),
                index=False, encoding='utf-8', sep=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC
            )


def calcular_igc(crop):
    z = 0


def main(database_credentials, views_path):
    docentes = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_DOCENTES.csv'))
    cursos = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_CURSOS.csv'))
    turmas = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_TURMAS.csv'))

    turmas.loc[pd.isna(turmas['NOTA_DOCENTE_PELO_DISCENTE']), 'NOTA_DOCENTE_PELO_DISCENTE'] = 0.6

    first = pd.merge(docentes, turmas)
    second = pd.merge(first, cursos, left_on='ID_CURSO_DISCENTE', right_on='ID_CURSO', suffixes=('', '_CURSO_DISCENTE'))
    third = pd.merge(second, cursos, left_on='ID_CURSO_SOLICITACAO_TURMA', right_on='ID_CURSO', suffixes=('', '_SOLICITACAO_TURMA'))

    henry = third.loc[third['NOME_DOCENTE'] == 'HENRY EMANUEL LEAL CAGNINI']

    igc = calcular_igc(henry)
    print(igc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Elabora um dashboard com dados do IGC para docentes.'
    )

    parser.add_argument(
        '--database-credentials', action='store', required=True,
        help='Caminho para um arquivo json com as credenciais do banco de dados.'
    )

    parser.add_argument(
        '--views-path', action='store', required=True,
        help='Onde escrever as views lidas do banco de dados'
    )

    args = parser.parse_args()
    main(args.database_credentials, args.views_path)
