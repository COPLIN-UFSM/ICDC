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
    gb_niveis = professor.groupby(by='NOME_NIVEL_CURSO_SOLICITACAO_TURMA').groups

    total_alunos = 0
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
            alunos = alunos.loc[alunos['ID_PROGRAMA_SUCUPIRA_DISCENTE'] == alunos['ID_PROGRAMA_SOLICITACAO_TURMA']]
        else:
            raise TypeError(f'Nível desconhecido: {nivel}')

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


def novo_calculo(crop):
    pass


def main(database_credentials, views_path):
    docentes = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_DOCENTES.csv'))
    cursos = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_CURSOS.csv'))
    turmas = pd.read_csv(os.path.join(views_path, 'PAINEL_IGC_TURMAS.csv'))

    turmas.loc[pd.isna(turmas['NOTA_DOCENTE_PELO_DISCENTE']), 'NOTA_DOCENTE_PELO_DISCENTE'] = 0.6

    # liga docentes com turmas
    first = pd.merge(docentes, turmas)
    # liga o curso do discente com cursos
    cursos_discente = cursos.copy(deep=True)
    cursos_discente = cursos_discente.rename(
        columns={x: x + '_DISCENTE' if x != 'ID_CURSO' else 'ID_CURSO' for x in cursos_discente.columns}
    )
    cursos_solicitacao_turma = cursos.copy(deep=True)
    cursos_solicitacao_turma = cursos_solicitacao_turma.rename(
        columns={
            x: x + '_CURSO_SOLICITACAO_TURMA' if x != 'ID_CURSO'
            else 'ID_CURSO'
            for x in cursos_solicitacao_turma.columns
        }
    )

    second = pd.merge(
        first, cursos_discente,
        left_on='ID_CURSO_DISCENTE', right_on='ID_CURSO',  suffixes=('', '_CURSO_DISCENTE')
    )
    # liga o curso de solicitação da turma com cursos
    third = pd.merge(
        second, cursos_solicitacao_turma,
        left_on='ID_CURSO_SOLICITACAO_TURMA', right_on='ID_CURSO',  suffixes=('', '_CURSO_SOLICITACAO_TURMA')
    )

    # remove coluna ID_CURSO, que foi usada apenas para o merge
    third = third.drop(columns=['ID_CURSO'])
    third['CPC_CONTINUO'] = third['CPC_CONTINUO'].astype(float)

    # TODO retirar depois - apenas para teste!
    # professor = third.loc[third['NOME_DOCENTE'] == 'MARTHA BOHRER ADAIME']
    # professor = third.loc[third['NOME_DOCENTE'] == 'HENRY EMANUEL LEAL CAGNINI']
    professor = third.loc[third['NOME_DOCENTE'] == 'LEONARDO RAMOS EMMENDORFER']

    # professor.to_csv(
    #     'abuble.csv', index=False, encoding='ISO-8859-1', sep=';', quotechar='"',
    #     decimal=',', float_format='%.4f', quoting=csv.QUOTE_NONNUMERIC
    # )

    igc = calcular_igc(professor)
    # igc_novo = novo_calculo(professor)
    print('IGC antigo:', igc)
    # print('IGC novo:', igc_novo)


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
