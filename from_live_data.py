import argparse

from app import load_dataframe


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
            alunos = alunos.loc[
                alunos['ID_PROGRAMA_SUCUPIRA_DISCENTE'] == alunos['ID_PROGRAMA_SUCUPIRA_CURSO_SOLICITACAO_TURMA']
                ]
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


def main(database_credentials, views_path):
    df = load_dataframe(database_credentials, views_path)

    professor = df.loc[df['NOME_DOCENTE'] == 'HENRY EMANUEL LEAL CAGNINI']

    igc = calcular_igc(professor)
    print('IGC docente:', igc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Roda um script que calcula o IGC de docentes.'
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
