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


def calcular_igc(professor):
    # pega apenas os cursos de graduação
    # crop = crop.loc[crop['NOME_NIVEL_CURSO_SOLICITACAO_TURMA'] == 'Graduação']
    total_alunos = 0

    gb_niveis = professor.groupby(by='NOME_NIVEL_CURSO_SOLICITACAO_TURMA').groups

    n_alunos_niveis = []
    media_niveis = []

    for nivel, indices in gb_niveis.items():
        alunos = professor.loc[indices]
        n_alunos_nivel = 0

        if nivel == 'Graduação':
            # pega apenas alunos cujo curso é o mesmo do curso de solicitação da vaga
            alunos = alunos.loc[alunos['ID_CURSO_DISCENTE'] == alunos['ID_CURSO_SOLICITACAO_TURMA']]
        elif nivel == 'Pós-Graduação':
            # pega apenas alunos cujo programa de pós é o mesmo programa do curso de solicitação da vaga
            alunos = alunos.loc[alunos['ID_PROGRAMA_DISCENTE'] == alunos['ID_PROGRAMA_SOLICITACAO_TURMA']]
            # TODO conta errada para pós-graduação!

        gb_turmas = alunos.groupby(by='ID_TURMA').groups

        denominador = 0
        numerador = 0
        for id_turma, turma_indices in gb_turmas.items():
            turma = alunos.loc[turma_indices]

            den_dt = turma.apply(lambda x: x['PESO_ALUNO'] * x['ENCARGO_DIDATICO_TURMA_DOCENTE'], axis='columns')
            num_dt = den_dt * turma['CPC_CONTINUO']

            numerador += num_dt.sum()
            denominador += den_dt.sum()
            n_alunos_nivel = turma['PESO_ALUNO'].sum()

        media_nivel = numerador/denominador

        media_niveis += [media_nivel]
        n_alunos_niveis += [n_alunos_nivel]
        total_alunos += n_alunos_nivel

    igc = 0
    for i in range(len(media_niveis)):
        igc += (n_alunos_niveis[i]/total_alunos) * media_niveis[i]

    return igc


def main(database_credentials, views_path):
    docentes = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_DOCENTES.csv'))
    cursos = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_CURSOS.csv'))
    turmas = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_TURMAS.csv'))

    turmas.loc[pd.isna(turmas['NOTA_DOCENTE_PELO_DISCENTE']), 'NOTA_DOCENTE_PELO_DISCENTE'] = 0.6

    first = pd.merge(docentes, turmas)
    second = pd.merge(first, cursos, left_on='ID_CURSO_DISCENTE', right_on='ID_CURSO', suffixes=('', '_CURSO_DISCENTE'))
    third = pd.merge(second, cursos, left_on='ID_CURSO_SOLICITACAO_TURMA', right_on='ID_CURSO', suffixes=('', '_CURSO_SOLICITACAO_TURMA'))

    # TODO retirar depois - apenas para teste!
    professor = third.loc[third['NOME_DOCENTE'] == 'MARTHA BOHRER ADAIME']
    # professor = third.loc[third['NOME_DOCENTE'] == 'HENRY EMANUEL LEAL CAGNINI']

    igc = calcular_igc(professor)
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
