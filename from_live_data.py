import argparse

from app import load_dataframe, calcular_igc


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
